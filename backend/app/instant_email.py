from datetime import date

from .pipeline import get_jobs_for_categories
from .email_service import send_job_email


def send_instant_email(user, db):

    try:

        categories = [
            c.strip()
            for c in user.categories.split(",")
        ]

        jobs = get_jobs_for_categories(
            categories
        )

        print(
            f"Fetched {len(jobs)} jobs "
            f"for immediate email"
        )

        if not jobs:

            print(
                "No jobs found for immediate email"
            )

            return False

        email_sent = send_job_email(
            user.email,
            jobs
        )

        print(
            f"Immediate email status: "
            f"{email_sent}"
        )

        if email_sent:

            user.first_email_sent = True

            user.last_email_sent_date = (
                date.today()
            )

            db.commit()

            return True

        return False

    except Exception as e:

        print(
            f"Instant email failed: "
            f"{str(e)}"
        )

        return False