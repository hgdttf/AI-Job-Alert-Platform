import os
import requests

from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

FROM_EMAIL = os.getenv(
    "FROM_EMAIL",
    "alerts@jobpulse.xyz"
)


def send_job_email(receiver_email, jobs):

    try:

        if not jobs:

            print("NO JOBS FOUND")

            return False

        html_jobs = ""

        for job in jobs[:15]:

            title = job.get(
                "title",
                "Unknown Role"
            )

            company = job.get(
                "company",
                "Unknown Company"
            )

            category = job.get(
                "category",
                "General"
            )

            link = job.get(
                "link",
                "#"
            )

            html_jobs += f"""
            <div
                style="
                    background:#0f172a;
                    padding:20px;
                    margin-bottom:20px;
                    border-radius:12px;
                    border:1px solid #1e293b;
                "
            >

                <h2 style="color:#38bdf8;">
                    {title}
                </h2>

                <p style="color:white;">
                    <strong>Company:</strong>
                    {company}
                </p>

                <p style="color:white;">
                    <strong>Category:</strong>
                    {category}
                </p>

                <a
                    href="{link}"
                    style="
                        display:inline-block;
                        margin-top:10px;
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

        <body
            style="
                background:#020617;
                color:white;
                font-family:Arial;
                padding:30px;
            "
        >

            <h1 style="color:#38bdf8;">
                JobPulse AI
            </h1>

            <p>
                Latest curated opportunities
                for you.
            </p>

            {html_jobs}

        </body>

        </html>
        """

        payload = {

            "from": f"JobPulse AI <{FROM_EMAIL}>",

            "to": [receiver_email],

            "subject": (
                "JobPulse AI - Fresh Opportunities"
            ),

            "html": html
        }

        headers = {

            "Authorization": (
                f"Bearer {RESEND_API_KEY}"
            ),

            "Content-Type": "application/json"
        }

        print("=================================")
        print("SENDING EMAIL")
        print("TO:", receiver_email)
        print("FROM:", FROM_EMAIL)
        print("=================================")

        response = requests.post(

            "https://api.resend.com/emails",

            json=payload,

            headers=headers,

            timeout=30
        )

        print("RESEND STATUS:",
            response.status_code)

        print("RESEND RESPONSE:",
            response.text)

        response.raise_for_status()

        return True

    except Exception as e:

        print("EMAIL ERROR:", str(e))

        return False
