import os
import requests

from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


def send_job_email(receiver_email, jobs):

    if not RESEND_API_KEY:

        print("RESEND_API_KEY missing")

        return False

    if len(jobs) == 0:

        print("No jobs found.")

        return False

    html_jobs = ""

    for job in jobs[:15]:

        html_jobs += f"""
        <div style="
            background:#0f172a;
            padding:20px;
            border-radius:12px;
            margin-bottom:20px;
            border:1px solid #1e293b;
        ">

            <h2 style="
                color:#38bdf8;
                margin-bottom:10px;
            ">
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
                    display:inline-block;
                    margin-top:12px;
                    padding:10px 18px;
                    background:#2563eb;
                    color:white;
                    text-decoration:none;
                    border-radius:8px;
                    font-weight:bold;
                "
            >
                Apply Now
            </a>

        </div>
        """

    html = f"""
    <html>

    <body style="
        background:#020617;
        color:white;
        font-family:Arial,sans-serif;
        padding:30px;
    ">

        <div style="
            max-width:700px;
            margin:auto;
        ">

            <h1 style="
                color:#38bdf8;
                font-size:32px;
            ">
                JobPulse AI
            </h1>

            <p style="
                color:#cbd5e1;
                font-size:16px;
                margin-bottom:30px;
            ">
                Fresh curated opportunities matching your interests.
            </p>

            {html_jobs}

            <hr style="
                border:none;
                border-top:1px solid #1e293b;
                margin:30px 0;
            ">

            <p style="
                color:#64748b;
                font-size:14px;
            ">
                Powered by JobPulse AI
            </p>

        </div>

    </body>

    </html>
    """

    payload = {
        "from": "JobPulse AI <onboarding@resend.dev>",
        "to": [receiver_email],
        "subject": "JobPulse AI - Fresh Opportunities",
        "html": html
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    try:

        response = requests.post(
            "https://api.resend.com/emails",
            json=payload,
            headers=headers,
            timeout=30
        )

        print("EMAIL STATUS:", response.status_code)

        print("EMAIL RESPONSE:", response.text)

        if response.status_code in [200, 201]:

            print(f"Email sent to {receiver_email}")

            return True

        else:

            print("Email sending failed")

            return False

    except Exception as e:

        print("Email service error:", e)

        return False