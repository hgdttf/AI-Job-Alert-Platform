import requests
from bs4 import BeautifulSoup


def get_internshala_jobs():

    jobs = []

    try:

        response = requests.get(
            "https://internshala.com/internships/",
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        cards = soup.select(
            "div.individual_internship"
        )

        for card in cards[:25]:

            try:

                title_tag = card.select_one(
                    "h3.job-internship-name"
                )

                company_tag = card.select_one(
                    "p.company-name"
                )

                location_tag = card.select_one(
                    "a.location_link"
                )

                if not title_tag:
                    continue

                jobs.append({

                    "title":
                        title_tag.text.strip(),

                    "company":
                        company_tag.text.strip()
                        if company_tag
                        else "Unknown",

                    "location":
                        location_tag.text.strip()
                        if location_tag
                        else "India",

                    "link":
                        "https://internshala.com/internships/",

                    "source":
                        "Internshala"
                })

            except:
                continue

    except Exception as e:

        print(
            f"Internshala scraper error: {e}"
        )

    print(
        f"Internshala jobs found: {len(jobs)}"
    )

    return jobs