from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SEARCH_TERMS = [

    # Fresher Jobs
    "software engineer fresher",
    "graduate engineer trainee",
    "associate software engineer",
    "junior developer",
    "entry level software engineer",
    "fresher hiring",
    "graduate trainee",

    # Internships
    "software internship",
    "data science internship",
    "web development internship",
    "python internship",
    "backend internship",

    # Research Internships
    "research internship",
    "machine learning research intern",
    "summer research fellowship",
    "research assistant",

    # Life Science
    "bioinformatics internship",
    "clinical research internship",
    "biotech internship",
    "pharma internship",

    # General Tech
    "cloud engineer fresher",
    "data analyst fresher",
    "AI internship",
    "machine learning internship"
]
TECH_KEYWORDS = [

    "software",
    "developer",
    "engineer",
    "programmer",
    "analyst",
    "associate",
    "trainee",
    "graduate",
    "intern",
    "cloud",
    "backend",
    "frontend",
    "web",
    "python",
    "java",
    "full stack",
    "data",
    "ai",
    "machine learning"
]


LIFE_SCIENCE_KEYWORDS = [

    "clinical",
    "research",
    "biotech",
    "bioinformatics",
    "life science",
    "pharma",
    "lab"
]


MS_RESEARCH_KEYWORDS = [

    "research intern",
    "research assistant",
    "machine learning research",
    "ms internship",
    "phd internship",
    "summer research",
    "research fellow",
    "ai research",
    "lab intern"
]