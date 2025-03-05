import os
from dotenv import load_dotenv


load_dotenv()

DISCORD_SDK = os.getenv("DISCORD_API_TOKEN")
GEMINI_SDK=os.getenv("GEMINI_API")
