from datetime import datetime


def generate_email_html(
    jobs,
    source_results
):

    # ======================================
    # LIMIT EMAIL SIZE
    # ======================================

    jobs = jobs[:50]

    # ======================================
    # SOURCE SUMMARY
    # ======================================

    source_html = ""

    for source, count in source_results.items():

        source_html += f"""
        <span
            style="
                display:inline-block;
                background:#1E293B;
                color:white;
                padding:8px 14px;
                border-radius:20px;
                margin:5px;
                font-size:14px;
            "
        >
            {source}: {count}
        </span>
        """

    # ======================================
    # EMAIL START
    # ======================================

    html = f"""
    <html>
    <body
        style="
            font-family:Arial,sans-serif;
            background:#F4F7FA;
            padding:20px;
        "
    >

    <div
        style="
            max-width:900px;
            margin:auto;
            background:white;
            padding:30px;
            border-radius:12px;
            box-shadow:0px 0px 10px rgba(0,0,0,0.1);
        "
    >

    <h1
        style="
            color:#16A34A;
            margin-bottom:5px;
        "
    >
        Daily Job Alerts
    </h1>

    <p style="color:#555;">
        Fresh opportunities collected from
        multiple platforms.
    </p>

    <div style="margin-top:20px; margin-bottom:25px;">
        {source_html}
    </div>
    """

    # ======================================
    # CATEGORY GROUPING
    # ======================================

    fresher_jobs = []

    internships = []

    research_jobs = []

    for job in jobs:

        title = (
            job.get("title", "")
            .lower()
        )

        if (
            "research" in title
            or "assistant" in title
            or "fellow" in title
        ):

            research_jobs.append(job)

        elif (
            "intern" in title
            or "internship" in title
        ):

            internships.append(job)

        else:

            fresher_jobs.append(job)

    # ======================================
    # SECTION RENDER FUNCTION
    # ======================================

    def render_section(
        section_title,
        section_jobs
    ):

        nonlocal html

        if not section_jobs:
            return

        html += f"""
        <h2
            style="
                margin-top:35px;
                color:#0F172A;
                border-bottom:2px solid #E2E8F0;
                padding-bottom:10px;
            "
        >
            {section_title}
        </h2>
        """

        for index, job in enumerate(
            section_jobs,
            start=1
        ):

            title = job.get(
                "title",
                "N/A"
            )

            company = job.get(
                "company",
                "N/A"
            )

            location = job.get(
                "location",
                "Remote"
            )

            apply_link = job.get(
                "apply_link",
                "#"
            )

            source = job.get(
                "source",
                "Unknown"
            )

            remote_tag = ""

            if "remote" in location.lower():

                remote_tag = """
                <span
                    style="
                        background:#DCFCE7;
                        color:#166534;
                        padding:4px 10px;
                        border-radius:15px;
                        font-size:12px;
                        margin-left:10px;
                    "
                >
                    Remote
                </span>
                """

            html += f"""

            <div
                style="
                    background:#F8FAFC;
                    border:1px solid #E2E8F0;
                    border-radius:12px;
                    padding:20px;
                    margin-top:18px;
                "
            >

            <h3 style="margin:0; color:#111827;">
                #{index} {title}
            </h3>

            <p
                style="
                    margin-top:10px;
                    color:#475569;
                "
            >
                <strong>Company:</strong> {company}
                <br>
                <strong>Location:</strong> {location}
                {remote_tag}
                <br>
                <strong>Source:</strong> {source}
            </p>

            <a
                href="{apply_link}"
                target="_blank"
                style="
                    display:inline-block;
                    margin-top:12px;
                    background:#16A34A;
                    color:white;
                    padding:10px 18px;
                    text-decoration:none;
                    border-radius:8px;
                    font-weight:bold;
                "
            >
                Apply Now
            </a>

            </div>
            """

    # ======================================
    # RENDER SECTIONS
    # ======================================

    render_section(
        "Fresher Jobs",
        fresher_jobs
    )

    render_section(
        "Internships",
        internships
    )

    render_section(
        "Research Opportunities",
        research_jobs
    )

    # ======================================
    # FOOTER
    # ======================================

    html += f"""

    <hr style="margin-top:40px;">

    <p
        style="
            color:#64748B;
            font-size:13px;
            margin-top:20px;
        "
    >
        Generated automatically by the
        AI-Powered Job Aggregation Platform.
        <br><br>
        Generated at:
        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </p>

    </div>
    </body>
    </html>
    """

    return html