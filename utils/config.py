import os
from dotenv import load_dotenv

load_dotenv()

GMAIL = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_PASSWORD")

ALLOWED_DOMAINS = ["Hospital", "Academic", "HR"]

