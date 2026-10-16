import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")

GROQ_KEY = os.getenv("GROQ_API_KEY")

POST_TIME = os.getenv("POST_TIME", "09:00")
