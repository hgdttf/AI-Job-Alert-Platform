from datetime import datetime

import pytz

from .models import User

from .pipeline import get_jobs_for_categories

from .email_service import send_job_email


IST = pytz.timezone(
    "Asia/Kolkata"
)


def run_scheduler(db):

    now_ist = datetime.now(IST)

    current_hour = now_ist.hour

    current_minute = now_ist.minute

    print(
        f"Scheduler running at "
        f"{now_ist.strftime('%I:%M %p')}"
    )

    users = db.query(User).filter(
        User.is_active == True
    ).all()

    processed_users = 0

    for user in users:

        try:

            # =================================
            # NORMALIZE USER TIME
            # =================================

            user_time = datetime.strptime(
                user.delivery_time,
                "%I:%M %p"
            )

            user_hour = user_time.hour

            user_minute = user_time.minute

            # =================================
            # MATCH HOUR + MINUTE
            # =================================

            if (
                user_hour != current_hour
                or
                user_minute != current_minute
            ):

                continue

            # =================================
            # DUPLICATE PREVENTION
            # =================================

            if (
                user.last_scheduler_email_sent_at
            ):

                last_sent = (
                    user.last_scheduler_email_sent_at
                    .astimezone(IST)
                )

                if (
                    last_sent.date()
                    ==
                    now_ist.date()
                ):

                    print(
                        f"Skipping duplicate "
                        f"scheduler email for "
                        f"{user.email}"
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

                continue

            email_sent = send_job_email(
                user.email,
                jobs
            )

            if email_sent:

                user.last_scheduler_email_sent_at = (
                    now_ist
                )

                db.commit()

                processed_users += 1

                print(
                    f"Scheduler email sent "
                    f"to {user.email}"
                )

        except Exception as e:

            print(
                f"Scheduler error for "
                f"{user.email}: {str(e)}"
            )

    return processed_users