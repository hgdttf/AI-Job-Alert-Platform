import os
import requests

from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


# =========================
# SEND EMAIL
# =========================

def send_job_email(receiver_email, jobs):

    print("\n========== EMAIL SERVICE STARTED ==========")

    print("Receiver:", receiver_email)

    if not RESEND_API_KEY:

        print("ERROR: RESEND_API_KEY missing")

        return False

    if not jobs:

        print("No jobs found")

        return False

    print(f"Jobs count: {len(jobs)}")

    # =========================
    # BUILD HTML
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

    html = f"""
    <html>

    <body style="
        background:#020617;
        color:white;
        font-family:Arial;
        padding:30px;
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

    # =========================
    # RESEND PAYLOAD
    # =========================

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

    # =========================
    # SEND EMAIL
    # =========================

    try:

        print("Sending request to Resend API...")

        response = requests.post(
            "https://api.resend.com/emails",
            json=payload,
            headers=headers,
            timeout=30
        )

        print(
            f"Resend status code: "
            f"{response.status_code}"
        )

        print(
            f"Resend response: "
            f"{response.text}"
        )

        response.raise_for_status()

        print(
            f"SUCCESS: Email sent to "
            f"{receiver_email}"
        )

        return True

    except requests.exceptions.Timeout:

        print("ERROR: Request timeout")

        return False

    except requests.exceptions.ConnectionError:

        print("ERROR: Connection failed")

        return False

    except requests.exceptions.HTTPError as e:

        print(
            f"HTTP ERROR: {str(e)}"
        )

        print(
            f"Response Body: "
            f"{response.text}"
        )

        return False

    except Exception as e:

        print(
            f"UNKNOWN EMAIL ERROR: "
            f"{str(e)}"
        )

        return False