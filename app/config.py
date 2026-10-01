import os
from os.path import join, dirname

from dotenv import load_dotenv
from google import genai

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

SUPPORTED_CONTENT_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
MAX_FILE_SIZE = 10_000_000
GEMINI_TIMEOUT_SECONDS = 60
MAX_AGENT_LOOP_STEPS = 5