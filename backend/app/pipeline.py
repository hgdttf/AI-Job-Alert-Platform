from .scrapers.linkedin_jobs import (
    scrape_linkedin_jobs
)

from .scrapers.internshala import (
    scrape_internshala_jobs
)

from .filters import CATEGORY_KEYWORDS


def remove_duplicates(jobs):

    seen = set()

    unique_jobs = []

    for job in jobs:

        key = (
            job["title"],
            job["company"]
        )

        if key not in seen:

            seen.add(key)

            unique_jobs.append(job)

    return unique_jobs


def expand_keywords(categories):

    keywords = []

    for category in categories:

        if category in CATEGORY_KEYWORDS:

            keywords.extend(
                CATEGORY_KEYWORDS[category]
            )

    return list(set(keywords))


def get_jobs_for_categories(categories):

    jobs = []

    keywords = expand_keywords(categories)

    print(f"Expanded Keywords: {keywords}")

    try:

        linkedin_jobs = (
            scrape_linkedin_jobs(keywords)
        )

        print(
            f"LinkedIn Jobs: "
            f"{len(linkedin_jobs)}"
        )

        jobs.extend(linkedin_jobs)

    except Exception as e:

        print(
            "LinkedIn scraper failed:",
            e
        )

    try:

        internshala_jobs = (
            scrape_internshala_jobs(keywords)
        )

        print(
            f"Internshala Jobs: "
            f"{len(internshala_jobs)}"
        )

        jobs.extend(internshala_jobs)

    except Exception as e:

        print(
            "Internshala scraper failed:",
            e
        )

    jobs = remove_duplicates(jobs)

    print(
        f"Total Jobs After Deduplication: "
        f"{len(jobs)}"
    )

    return jobs