import requests

from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_internshala_jobs(categories):

    print("Running Internshala scraper...")

    jobs = []

    try:

        for category in categories:

            query = (
                category
                .lower()
                .replace(" ", "-")
            )

            url = (
                "https://internshala.com/jobs/"
                f"{query}-jobs/"
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
                class_="individual_internship"
            )

            for card in cards[:10]:

                try:

                    title = card.find("h3")

                    company = card.find(
                        "p",
                        class_="company-name"
                    )

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
                        "link": (
                            "https://internshala.com"
                            + link["href"]
                        ),
                        "source": "Internshala"
                    })

                except Exception:
                    continue

    except Exception as e:

        print(
            "Internshala scraper error:",
            e
        )

    return jobs