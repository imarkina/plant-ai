import os
from os.path import join, dirname

from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
api_key = os.environ.get("GEMINI_API_KEY")
api_model = os.environ.get("GEMINI_MODEL")

SUPPORTED_CONTENT_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
MAX_FILE_SIZE = 10_000_000
GEMINI_TIMEOUT_SECONDS = 60