import requests


def get_github_internships():

    jobs = []

    try:

        response = requests.get(
            "https://raw.githubusercontent.com/pittcsc/Summer2026-Internships/master/README.md",
            timeout=20
        )

        lines = response.text.splitlines()

        count = 0

        for line in lines:

            if "|" in line:

                count += 1

                jobs.append({

                    "title":
                        "Software Internship",

                    "company":
                        "GitHub Internship Repo",

                    "location":
                        "Various",

                    "link":
                        f"https://github.com/pittcsc/Summer2026-Internships#{count}",

                    "source":
                        "GitHub"
                })

    except Exception as e:

        print(
            f"GitHub scraper error: {e}"
        )

    print(
        f"GitHub jobs found: {len(jobs)}"
    )

    return jobs