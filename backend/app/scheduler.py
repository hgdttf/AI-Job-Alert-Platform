from datetime import datetime
from datetime import date

import pytz

from .pipeline import get_jobs_for_categories
from .email_service import send_job_email
from .models import User


IST = pytz.timezone("Asia/Kolkata")


def run_scheduler(db):

    now_ist = datetime.now(IST)

    current_time = now_ist.strftime(
        "%I:%M %p"
    )

    today = date.today()

    print(
        f"Scheduler running for IST time: "
        f"{current_time}"
    )

    users = db.query(User).all()

    processed_users = 0

    for user in users:

        try:

            user_time = (
                user.delivery_time.strip()
            )

            print(
                f"Checking user {user.email} "
                f"scheduled for {user_time}"
            )

            # =====================================
            # TIME MATCH
            # =====================================

            if user_time != current_time:

                continue

            # =====================================
            # DUPLICATE PREVENTION
            # =====================================

            if (
                user.last_email_sent_date
                == today
            ):

                print(
                    f"Skipping duplicate email "
                    f"for {user.email}"
                )

                continue

            categories = [
                c.strip()
                for c in user.categories.split(",")
            ]

            jobs = get_jobs_for_categories(
                categories
            )

            if not jobs:

                print(
                    f"No jobs found for "
                    f"{user.email}"
                )

                continue

            email_sent = send_job_email(
                user.email,
                jobs
            )

            if email_sent:

                user.last_email_sent_date = (
                    today
                )

                db.commit()

                processed_users += 1

                print(
                    f"Scheduled email sent to "
                    f"{user.email}"
                )

        except Exception as e:

            print(
                f"Scheduler error for "
                f"{user.email}: {str(e)}"
            )

    return processed_users