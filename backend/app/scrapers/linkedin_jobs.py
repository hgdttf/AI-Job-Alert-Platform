import requests

from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_linkedin_jobs(categories):

    print("Running LinkedIn scraper...")

    jobs = []

    try:

        for category in categories:

            query = (
                category
                .replace(" ", "%20")
            )

            url = (
                "https://www.linkedin.com/jobs/search"
                f"?keywords={query}"
            )

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=15
            )

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            cards = soup.find_all(
                "div",
                class_="base-card"
            )

            for card in cards[:10]:

                try:

                    title = card.find("h3")

                    company = card.find("h4")

                    link = card.find(
                        "a",
                        href=True
                    )

                    if (
                        not title
                        or not company
                        or not link
                    ):
                        continue

                    jobs.append({
                        "title": title.text.strip(),
                        "company": company.text.strip(),
                        "link": link["href"],
                        "source": "LinkedIn"
                    })

                except Exception:
                    continue

    except Exception as e:

        print("LinkedIn scraper error:", e)

    return jobs