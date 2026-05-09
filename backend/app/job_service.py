from datetime import datetime

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User

from .pipeline import get_jobs_for_categories
from .email_service import send_job_email


# =========================
# PROCESS SCHEDULED EMAILS
# =========================

def process_scheduled_jobs():

    db: Session = SessionLocal()

    try:

        users = db.query(User).all()

        current_time = datetime.now().strftime("%I:%M %p")

        current_date = datetime.now().strftime("%Y-%m-%d")

        print(f"\nChecking schedules for: {current_time}")

        for user in users:

            print(
                f"User: {user.email} | "
                f"Saved Time: {user.delivery_time}"
            )

            already_sent_today = (
                user.last_email_sent_date
                == current_date
            )

            if (
                user.delivery_time == current_time
                and not already_sent_today
            ):

                print(
                    f"Sending scheduled email "
                    f"to {user.email}"
                )

                categories = [
                    c.strip()
                    for c in user.categories.split(",")
                ]

                jobs = get_jobs_for_categories(categories)

                print(f"Jobs fetched: {len(jobs)}")

                if jobs and len(jobs) > 0:

                    send_job_email(
                        user.email,
                        jobs
                    )

                    user.last_email_sent_date = current_date

                    db.commit()

                    print(
                        f"Scheduled email sent to "
                        f"{user.email}"
                    )

    except Exception as e:

        print(f"Job processing error: {str(e)}")

    finally:

        db.close()