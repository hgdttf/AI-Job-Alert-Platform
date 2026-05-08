import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PythonProjectforJobs.old_streamlit_backup.config.settings import (
    EMAIL_SENDER,
    EMAIL_PASSWORD
)


def send_email(receiver_email, html_content):

    try:

        msg = MIMEMultipart(
            "alternative"
        )

        msg["Subject"] = (
            "Daily Fresher Job Alerts"
        )

        msg["From"] = EMAIL_SENDER

        msg["To"] = receiver_email

        msg.attach(
            MIMEText(
                html_content,
                "html"
            )
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL_SENDER,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_SENDER,
            receiver_email,
            msg.as_string()
        )

        server.quit()

    except Exception as e:

        print(
            f"Email error: {e}"
        )