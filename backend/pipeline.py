from datetime import datetime, timedelta

from database.db import cursor, conn

from backend.filters import filter_jobs

from services.email_service import send_email
from services.dedup_service import remove_duplicate_jobs
from services.html_generator import generate_email_html

from scrapers.linkedin_scraper import (
    get_linkedin_jobs
)

from scrapers.internshala_scraper import (
    get_internshala_jobs
)

from scrapers.github_repo_scraper import (
    get_github_internships
)


# ==========================================
# CHECK 24-HOUR RULE
# ==========================================

def should_send(last_sent):

    try:

        if not last_sent:
            return True

        last = datetime.strptime(
            last_sent,
            "%Y-%m-%d %H:%M:%S"
        )

        return (
            datetime.now() - last
        ) >= timedelta(hours=24)

    except Exception as e:

        print(
            f"Date parsing error: {e}"
        )

        return True


# ==========================================
# MAIN PIPELINE
# ==========================================

def run_pipeline():

    print("\n==============================")
    print("Running pipeline...")
    print("==============================\n")

    try:

        current_dt = datetime.now()

        cursor.execute(
            "SELECT * FROM users"
        )

        users = cursor.fetchall()

        if not users:

            print(
                "No registered users found."
            )

            return

        for user in users:

            try:

                # ==================================
                # USER DATA
                # ==================================

                user_id = user[0]

                email = user[1]

                send_time = user[2][:5]

                btech = bool(user[3])

                mtech = bool(user[4])

                life_science = bool(user[5])

                ms_research = bool(user[6])

                last_sent = user[7]

                print(
                    f"\nChecking user: {email}"
                )

                # ==================================
                # DELIVERY WINDOW CHECK
                # ==================================

                send_dt = datetime.strptime(
                    send_time,
                    "%H:%M"
                )

                current_minutes = (
                    current_dt.hour * 60
                    + current_dt.minute
                )

                send_minutes = (
                    send_dt.hour * 60
                    + send_dt.minute
                )

                time_difference = abs(
                    current_minutes
                    - send_minutes
                )

                # 5-minute delivery window

                if time_difference > 5:

                    print(
                        f"Skipping {email} "
                        f"(outside delivery window)"
                    )

                    continue

                # ==================================
                # 24-HOUR CHECK
                # ==================================

                if not should_send(last_sent):

                    print(
                        f"Skipping {email} "
                        f"(24-hour rule active)"
                    )

                    continue

                # ==================================
                # START SCRAPING
                # ==================================

                jobs = []

                source_results = {}

                print(
                    "Starting scraper execution..."
                )

                # ==================================
                # LINKEDIN
                # ==================================

                try:

                    linkedin_jobs = (
                        get_linkedin_jobs()
                    )

                    if linkedin_jobs:

                        jobs.extend(
                            linkedin_jobs
                        )

                        source_results[
                            "LinkedIn"
                        ] = len(
                            linkedin_jobs
                        )

                    print(
                        f"LinkedIn jobs: "
                        f"{len(linkedin_jobs)}"
                    )

                except Exception as e:

                    print(
                        f"LinkedIn error: {e}"
                    )

                # ==================================
                # INTERNSHALA
                # ==================================

                try:

                    internshala_jobs = (
                        get_internshala_jobs()
                    )

                    if internshala_jobs:

                        jobs.extend(
                            internshala_jobs
                        )

                        source_results[
                            "Internshala"
                        ] = len(
                            internshala_jobs
                        )

                    print(
                        f"Internshala jobs: "
                        f"{len(internshala_jobs)}"
                    )

                except Exception as e:

                    print(
                        f"Internshala error: {e}"
                    )

                # ==================================
                # GITHUB INTERNSHIPS
                # ==================================

                try:

                    github_jobs = (
                        get_github_internships()
                    )

                    if github_jobs:

                        jobs.extend(
                            github_jobs
                        )

                        source_results[
                            "GitHub"
                        ] = len(
                            github_jobs
                        )

                    print(
                        f"GitHub jobs: "
                        f"{len(github_jobs)}"
                    )

                except Exception as e:

                    print(
                        f"GitHub error: {e}"
                    )

                # ==================================
                # TOTAL JOBS
                # ==================================

                print(
                    f"Total jobs collected: "
                    f"{len(jobs)}"
                )

                if not jobs:

                    print(
                        "No jobs collected "
                        "from any source."
                    )

                    continue

                # ==================================
                # FILTER JOBS
                # ==================================

                filtered = filter_jobs(
                    jobs,
                    btech,
                    mtech,
                    life_science,
                    ms_research
                )

                print(
                    f"Filtered jobs: "
                    f"{len(filtered)}"
                )

                if not filtered:

                    print(
                        "No matching jobs "
                        "after filtering."
                    )

                    continue

                # ==================================
                # REMOVE DUPLICATES
                # ==================================

                unique = remove_duplicate_jobs(
                    filtered
                )

                print(
                    f"Unique jobs: "
                    f"{len(unique)}"
                )

                if not unique:

                    print(
                        "No unique jobs "
                        "remaining."
                    )

                    continue

                # ==================================
                # GENERATE EMAIL
                # ==================================

                try:

                    html = generate_email_html(
                        unique,
                        source_results
                    )

                except Exception as e:

                    print(
                        f"HTML generation error: {e}"
                    )

                    continue

                # ==================================
                # SEND EMAIL
                # ==================================

                try:

                    send_email(
                        email,
                        html
                    )

                    print(
                        f"Email sent to {email}"
                    )

                except Exception as e:

                    print(
                        f"Email sending error: {e}"
                    )

                    continue

                # ==================================
                # UPDATE DATABASE
                # ==================================

                try:

                    cursor.execute(
                        """
                        UPDATE users
                        SET last_sent=?
                        WHERE id=?
                        """,
                        (
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            user_id
                        )
                    )

                    conn.commit()

                    print(
                        f"Database updated for "
                        f"{email}"
                    )

                except Exception as e:

                    print(
                        f"Database update error: {e}"
                    )

            except Exception as e:

                print(
                    f"Pipeline user error: {e}"
                )

    except Exception as e:

        print(
            f"Fatal pipeline error: {e}"
        )

    finally:

        print(
            "\nPipeline execution finished.\n"
        )