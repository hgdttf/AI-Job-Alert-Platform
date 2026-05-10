from datetime import datetime

import pytz

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .pipeline import get_jobs_for_categories
from .email_service import (
    send_job_email,
    create_email_log
)


IST = pytz.timezone(
    "Asia/Kolkata"
)


def normalize_time_string(
    value: str
):

    return (
        value.strip()
        .upper()
        .replace(".", "")
    )


def run_scheduler():

    db: Session = SessionLocal()

    try:

        now_ist = datetime.now(IST)

        current_time_ist = (
            now_ist.strftime("%I:%M %p")
        )

        normalized_current_time = (
            normalize_time_string(
                current_time_ist
            )
        )

        print(
            f"SCHEDULER RUNNING AT: "
            f"{normalized_current_time}"
        )

        users = db.query(User).filter(
            User.is_active == True
        ).all()

        processed_users = 0

        for user in users:

            try:

                delivery_time = (
                    normalize_time_string(
                        user.delivery_time
                    )
                )

                if (
                    delivery_time
                    !=
                    normalized_current_time
                ):

                    continue

                # =====================================
                # DUPLICATE PREVENTION
                # =====================================

                if (
                    user.last_scheduler_email_sent_at
                ):

                    last_sent_ist = (
                        user
                        .last_scheduler_email_sent_at
                        .astimezone(IST)
                    )

                    if (
                        last_sent_ist.date()
                        ==
                        now_ist.date()
                    ):

                        print(
                            f"SKIPPING DUPLICATE: "
                            f"{user.email}"
                        )

                        continue

                categories = [
                    c.strip()
                    for c in user.categories.split(",")
                    if c.strip()
                ]

                jobs = get_jobs_for_categories(
                    categories
                )

                print(
                    f"SCHEDULER JOBS "
                    f"{user.email}: "
                    f"{len(jobs)}"
                )

                if not jobs:

                    create_email_log(
                        db=db,
                        user_email=user.email,
                        email_type="scheduler",
                        status="failed",
                        message="No jobs found"
                    )

                    continue

                email_sent = send_job_email(
                    receiver_email=user.email,
                    jobs=jobs,
                    email_type="scheduler"
                )

                if email_sent:

                    user.last_scheduler_email_sent_at = (
                        now_ist
                    )

                    db.commit()

                    processed_users += 1

                    create_email_log(
                        db=db,
                        user_email=user.email,
                        email_type="scheduler",
                        status="success",
                        message="Scheduler email sent"
                    )

                    print(
                        f"SCHEDULER EMAIL SENT: "
                        f"{user.email}"
                    )

                else:

                    create_email_log(
                        db=db,
                        user_email=user.email,
                        email_type="scheduler",
                        status="failed",
                        message="Email sending failed"
                    )

            except Exception as user_error:

                print(
                    f"SCHEDULER USER ERROR: "
                    f"{str(user_error)}"
                )

                create_email_log(
                    db=db,
                    user_email=user.email,
                    email_type="scheduler",
                    status="failed",
                    message=str(user_error)
                )

                db.rollback()

        print(
            f"SCHEDULER COMPLETED: "
            f"{processed_users}"
        )

        return {
            "message":
            "Scheduler completed",

            "processed_users":
            processed_users,

            "current_time_ist":
            current_time_ist
        }

    except Exception as e:

        print(
            f"SCHEDULER ERROR: {str(e)}"
        )

        db.rollback()

        return {
            "message":
            "Scheduler failed",

            "error":
            str(e)
        }

    finally:

        db.close()