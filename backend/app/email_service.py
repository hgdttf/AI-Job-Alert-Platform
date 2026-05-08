import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_job_email(receiver_email, jobs):

    if len(jobs) == 0:

        print("No jobs found. Email skipped.")

        return

    html_jobs = ""

    for job in jobs[:15]:

        html_jobs += f"""
        <div style="
            padding:15px;
            margin-bottom:15px;
            border-radius:10px;
            background:#0f172a;
        ">

            <h2 style="color:#38bdf8;">
                {job['title']}
            </h2>

            <p style="color:white;">
                <strong>Company:</strong>
                {job['company']}
            </p>

            <p style="color:white;">
                <strong>Category:</strong>
                {job['category']}
            </p>

            <a
                href="{job['link']}"
                style="
                    color:#22c55e;
                    text-decoration:none;
                "
            >
                Apply Here
            </a>

        </div>
        """

    html = f"""
    <html>

    <body style="
        background:#020617;
        color:white;
        font-family:Arial;
        padding:20px;
    ">

        <h1 style="color:#38bdf8;">
            JobPulse AI
        </h1>

        <p>
            Latest curated opportunities for you.
        </p>

        {html_jobs}

    </body>

    </html>
    """

    message = MIMEMultipart("alternative")

    message["Subject"] = "JobPulse AI - Daily Jobs"

    message["From"] = EMAIL_ADDRESS

    message["To"] = receiver_email

    message.attach(
        MIMEText(html, "html")
    )

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.sendmail(
                EMAIL_ADDRESS,
                receiver_email,
                message.as_string()
            )

        print(f"Email sent to {receiver_email}")

    except Exception as e:

        print("Email error:", e)