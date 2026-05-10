from datetime import datetime

import pytz

from sqlalchemy.orm import Session

from .models import User
from .pipeline import get_jobs_for_categories
from .email_service import (
    send_job_email,
    create_email_log
)


IST = pytz.timezone(
    "Asia/Kolkata"
)


def send_instant_email(
    db: Session,
    user: User
):

    try:

        categories = [
            c.strip()
            for c in user.categories.split(",")
            if c.strip()
        ]

        jobs = get_jobs_for_categories(
            categories
        )

        print(
            f"ONBOARDING JOBS: {len(jobs)}"
        )

        if not jobs:

            create_email_log(
                db=db,
                user_email=user.email,
                email_type="onboarding",
                status="failed",
                message="No jobs found"
            )

            return False

        email_sent = send_job_email(
            receiver_email=user.email,
            jobs=jobs,
            email_type="onboarding"
        )

        if email_sent:

            user.onboarding_email_sent_at = (
                datetime.now(IST)
            )

            db.commit()

            create_email_log(
                db=db,
                user_email=user.email,
                email_type="onboarding",
                status="success",
                message="Onboarding email sent"
            )

            print(
                f"ONBOARDING EMAIL SENT: "
                f"{user.email}"
            )

            return True

        create_email_log(
            db=db,
            user_email=user.email,
            email_type="onboarding",
            status="failed",
            message="Email sending failed"
        )

        return False

    except Exception as e:

        print(
            f"INSTANT EMAIL ERROR: "
            f"{str(e)}"
        )

        create_email_log(
            db=db,
            user_email=user.email,
            email_type="onboarding",
            status="failed",
            message=str(e)
        )

        db.rollback()

        return False