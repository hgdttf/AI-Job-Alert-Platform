import html
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from sqlalchemy.orm import Session

from .config import settings
from .models import EmailLog


RESEND_API_URL = "https://api.resend.com/emails"


session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[
        429,
        500,
        502,
        503,
        504
    ],
    allowed_methods=["POST"]
)

adapter = HTTPAdapter(
    max_retries=retry_strategy
)

session.mount(
    "https://",
    adapter
)


def create_email_log(
    db: Session,
    user_email: str,
    email_type: str,
    status: str,
    message: str = None
):

    try:

        log = EmailLog(
            user_email=user_email,
            email_type=email_type,
            status=status,
            message=message
        )

        db.add(log)

        db.commit()

    except Exception as e:

        print("EMAIL LOG ERROR:", str(e))

        db.rollback()


def send_job_email(
    receiver_email,
    jobs,
    email_type="scheduler"
):

    if not jobs:

        print("No jobs found")

        return False

    html_jobs = ""

    for job in jobs[:15]:

        title = html.escape(
            str(job.get("title", "Unknown Role"))
        )

        company = html.escape(
            str(job.get("company", "Unknown Company"))
        )

        category = html.escape(
            str(job.get("category", "General"))
        )

        link = str(
            job.get("link", "#")
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
                <strong>Company:</strong> {company}
            </p>

            <p style="color:white;">
                <strong>Category:</strong> {category}
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

    title_prefix = (
        "Welcome to JobPulse AI"
        if email_type == "onboarding"
        else "JobPulse AI - Fresh Opportunities"
    )

    html_content = f"""
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

    payload = {
        "from": settings.FROM_EMAIL,
        "to": [receiver_email],
        "subject": title_prefix,
        "html": html_content
    }

    headers = {
        "Authorization": (
            f"Bearer {settings.RESEND_API_KEY}"
        ),
        "Content-Type": "application/json"
    }

    try:

        response = session.post(
            RESEND_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        print(
            "RESEND STATUS:",
            response.status_code
        )

        print(
            "RESEND RESPONSE:",
            response.text
        )

        response.raise_for_status()

        print(
            f"Email sent successfully to "
            f"{receiver_email}"
        )

        return True

    except Exception as e:

        print(
            f"EMAIL ERROR: {str(e)}"
        )

        return False