import os
import smtplib

from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# =========================
# SEND JOB EMAIL
# =========================

def send_job_email(receiver_email, jobs):

    try:

        # Prevent empty emails
        if not jobs or len(jobs) == 0:

            print("No jobs found. Email skipped.")

            return

        html_jobs = ""

        for job in jobs[:15]:

            html_jobs += f"""
            <div style="
                padding:20px;
                margin-bottom:20px;
                border-radius:12px;
                background:#0f172a;
                border:1px solid #1e293b;
            ">

                <h2 style="
                    color:#38bdf8;
                    margin-bottom:10px;
                ">
                    {job.get('title', 'Unknown Title')}
                </h2>

                <p style="color:white;">
                    <strong>Company:</strong>
                    {job.get('company', 'Unknown')}
                </p>

                <p style="color:white;">
                    <strong>Category:</strong>
                    {job.get('category', 'General')}
                </p>

                <a
                    href="{job.get('link', '#')}"
                    style="
                        color:#22c55e;
                        text-decoration:none;
                        font-weight:bold;
                    "
                >
                    Apply Here →
                </a>

            </div>
            """

        html = f"""
        <html>

        <body style="
            background:#020617;
            color:white;
            font-family:Arial, sans-serif;
            padding:30px;
        ">

            <div style="
                max-width:700px;
                margin:auto;
            ">

                <h1 style="
                    color:#38bdf8;
                    margin-bottom:10px;
                ">
                    JobPulse AI
                </h1>

                <p style="
                    color:#cbd5e1;
                    margin-bottom:30px;
                ">
                    Latest curated opportunities for you.
                </p>

                {html_jobs}

            </div>

        </body>

        </html>
        """

        message = MIMEMultipart("alternative")

        message["Subject"] = "JobPulse AI - Fresh Opportunities"

        message["From"] = EMAIL_ADDRESS

        message["To"] = receiver_email

        message.attach(
            MIMEText(html, "html")
        )

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

        print(f"Email sent successfully to {receiver_email}")

    except Exception as e:

        print(f"Email sending failed: {str(e)}")