from config.settings import (
    TECH_KEYWORDS,
    LIFE_SCIENCE_KEYWORDS,
    MS_RESEARCH_KEYWORDS
)


# ==========================================
# JOB SCORING ENGINE
# ==========================================

def calculate_job_score(job):

    score = 0

    title = (
        job.get("title", "")
        .lower()
    )

    location = (
        job.get("location", "")
        .lower()
    )

    # ======================================
    # PRIORITY 1
    # FRESHER / ENTRY LEVEL
    # ======================================

    fresher_keywords = [

        "fresher",
        "graduate",
        "associate",
        "junior",
        "entry level",
        "trainee"

    ]

    if any(
        keyword in title
        for keyword in fresher_keywords
    ):

        score += 60

    # ======================================
    # PRIORITY 2
    # FULL-TIME TECH JOBS
    # ======================================

    full_time_keywords = [

        "software engineer",
        "developer",
        "engineer",
        "analyst",
        "backend",
        "frontend",
        "full stack"

    ]

    if any(
        keyword in title
        for keyword in full_time_keywords
    ):

        score += 45

    # ======================================
    # PRIORITY 3
    # INTERNSHIPS
    # ======================================

    internship_keywords = [

        "intern",
        "internship"

    ]

    if any(
        keyword in title
        for keyword in internship_keywords
    ):

        score += 30

    # ======================================
    # PRIORITY 4
    # RESEARCH ROLES
    # ======================================

    research_keywords = [

        "research",
        "assistant",
        "fellow",
        "lab"

    ]

    if any(
        keyword in title
        for keyword in research_keywords
    ):

        score += 20

    # ======================================
    # REMOTE BONUS
    # ======================================

    if "remote" in location:

        score += 10

    # ======================================
    # AI / ML BONUS
    # ======================================

    ai_keywords = [

        "ai",
        "machine learning",
        "ml",
        "data science"

    ]

    if any(
        keyword in title
        for keyword in ai_keywords
    ):

        score += 15

    return score


# ==========================================
# FILTER + RANK JOBS
# ==========================================

def filter_jobs(
    jobs,
    btech,
    mtech,
    life_science,
    ms_research
):

    filtered = []

    for job in jobs:

        title = (
            job.get("title", "")
            .lower()
        )

        # ======================================
        # TECH JOBS
        # ======================================

        if btech or mtech:

            if any(
                keyword in title
                for keyword in TECH_KEYWORDS
            ):

                filtered.append(job)

                continue

        # ======================================
        # LIFE SCIENCE
        # ======================================

        if life_science:

            if any(
                keyword in title
                for keyword in LIFE_SCIENCE_KEYWORDS
            ):

                filtered.append(job)

                continue

        # ======================================
        # MS RESEARCH
        # ======================================

        if ms_research:

            if any(
                keyword in title
                for keyword in MS_RESEARCH_KEYWORDS
            ):

                filtered.append(job)

                continue

    # ==========================================
    # SORT BY INTELLIGENT SCORE
    # ==========================================

    filtered.sort(
        key=calculate_job_score,
        reverse=True
    )

    return filtered