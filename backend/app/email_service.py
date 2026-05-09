import os
import requests

from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


# =========================
# SEND JOB EMAIL
# =========================

def send_job_email(
    receiver_email,
    jobs
):

    try:

        # =========================
        # VALIDATION
        # =========================

        if not RESEND_API_KEY:

            print(
                "RESEND_API_KEY missing"
            )

            return False

        if not receiver_email:

            print(
                "Receiver email missing"
            )

            return False

        if not jobs or len(jobs) == 0:

            print(
                f"No jobs found for "
                f"{receiver_email}"
            )

            return False

        # =========================
        # BUILD JOB HTML
        # =========================

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

        # =========================
        # FULL EMAIL HTML
        # =========================

        html = f"""
        <html>

        <body style="
            background:#020617;
            color:white;
            font-family:Arial;
            padding:30px;
        ">

            <h1 style="
                color:#38bdf8;
            ">
                JobPulse AI
            </h1>

            <p>
                Latest curated opportunities
                curated specifically for you.
            </p>

            {html_jobs}

        </body>

        </html>
        """

        # =========================
        # RESEND PAYLOAD
        # =========================

        payload = {

            "from": (
                "JobPulse AI "
                "<onboarding@resend.dev>"
            ),

            "to": [receiver_email],

            "subject": (
                "JobPulse AI - "
                "Fresh Opportunities"
            ),

            "html": html
        }

        headers = {

            "Authorization": (
                f"Bearer {RESEND_API_KEY}"
            ),

            "Content-Type": (
                "application/json"
            )
        }

        # =========================
        # SEND EMAIL
        # =========================

        response = requests.post(

            "https://api.resend.com/emails",

            json=payload,

            headers=headers,

            timeout=30
        )

        # =========================
        # LOGGING
        # =========================

        print(
            "RESEND STATUS:",
            response.status_code
        )

        print(
            "RESEND RESPONSE:",
            response.text
        )

        # =========================
        # SUCCESS CHECK
        # =========================

        if response.status_code in [200, 201]:

            print(
                f"Email successfully sent "
                f"to {receiver_email}"
            )

            return True

        else:

            print(
                f"Resend failed for "
                f"{receiver_email}"
            )

            return False

    except requests.exceptions.Timeout:

        print(
            f"Timeout sending email "
            f"to {receiver_email}"
        )

        return False

    except requests.exceptions.ConnectionError:

        print(
            f"Connection error sending "
            f"email to {receiver_email}"
        )

        return False

    except Exception as e:

        print(
            "EMAIL ERROR:",
            str(e)
        )

        return False