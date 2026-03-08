import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MESSAGES_DB_PATH = os.getenv('MESSAGES_DB_PATH')
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN environment variable is required")
        if not cls.MESSAGES_DB_PATH:
            raise ValueError("MESSAGES_DB_PATH environment variable is required")