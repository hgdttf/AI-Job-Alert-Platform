from apscheduler.schedulers.background import BackgroundScheduler

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User

from .pipeline import get_jobs_for_categories

from .email_service import send_job_email

from datetime import datetime

scheduler = BackgroundScheduler()

already_sent_users = {}


def send_daily_jobs():

    db: Session = SessionLocal()

    users = db.query(User).all()

    current_time = datetime.now().strftime("%I:%M %p")

    print(f"\nChecking schedules for: {current_time}")

    for user in users:

        print(
            f"User: {user.email} | "
            f"Saved Time: {user.delivery_time}"
        )

        if user.email not in already_sent_users:

            print(f"Sending initial email to {user.email}")

            categories = user.categories.split(", ")

            jobs = get_jobs_for_categories(categories)

            print(f"Jobs fetched: {len(jobs)}")

            if len(jobs) > 0:

                send_job_email(
                    user.email,
                    jobs
                )

                print(
                    f"Initial email sent to "
                    f"{user.email}"
                )

            already_sent_users[user.email] = True

        elif user.delivery_time == current_time:

            print(f"Sending scheduled email to {user.email}")

            categories = user.categories.split(", ")

            jobs = get_jobs_for_categories(categories)

            print(f"Jobs fetched: {len(jobs)}")

            if len(jobs) > 0:

                send_job_email(
                    user.email,
                    jobs
                )

                print(
                    f"Scheduled email sent to "
                    f"{user.email}"
                )

    db.close()


def start_scheduler():

    scheduler.add_job(
        send_daily_jobs,
        "interval",
        minutes=1
    )

    scheduler.start()

    print("Scheduler started...")