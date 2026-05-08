from jobspy import scrape_jobs
from PythonProjectforJobs.old_streamlit_backup.config.settings import SEARCH_TERMS


def get_linkedin_jobs():

    jobs_collected = []

    for term in SEARCH_TERMS:

        try:

            jobs = scrape_jobs(
                site_name=["linkedin"],
                search_term=term,
                location="India",
                results_wanted=20,
                hours_old=24,
                country_indeed="India"
            )

            for _, row in jobs.iterrows():

                jobs_collected.append({
                    "title": row.get("title", ""),
                    "company": row.get("company", ""),
                    "location": row.get("location", ""),
                    "link": row.get("job_url", ""),
                    "source": "LinkedIn"
                })

        except:
            continue

    return jobs_collected