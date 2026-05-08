def remove_duplicate_jobs(jobs):

    seen = set()

    unique_jobs = []

    for job in jobs:

        # ==============================
        # SAFE FIELD EXTRACTION
        # ==============================

        title = (
            job.get("title", "")
            .strip()
            .lower()
        )

        company = (
            job.get("company", "")
            .strip()
            .lower()
        )

        source = (
            job.get("source", "")
            .strip()
            .lower()
        )

        # ==============================
        # UNIQUE KEY
        # ==============================

        unique_key = (
            title,
            company,
            source
        )

        # ==============================
        # REMOVE DUPLICATES
        # ==============================

        if unique_key not in seen:

            seen.add(unique_key)

            unique_jobs.append(job)

    return unique_jobs