import asyncio

from google import genai
from google.genai import types, errors
from app.config import api_model, api_key, GEMINI_TIMEOUT_SECONDS
from app.prompts import prompt
from app.schemas import PlantReport

client = genai.Client(api_key=api_key)


class GeminiError(Exception):
    """Базовая ошибка работы с Gemini"""

class GeminiQuotaError(GeminiError):
    """Исчерпан лимит запросов"""

class GeminiUnavailableError(GeminiError):
    """Gemini недоступен или вернул некорректный ответ"""

class GeminiTimeoutError(GeminiError):
    """Превышено время ожидания ответа"""

class GeminiConfigError(GeminiError):
    """Невалидный ключ или неверная локация"""

async def analyze_photo_image(image_bytes, content_type):
    try:
        result = await asyncio.wait_for(
             client.aio.models.generate_content(
                model=api_model,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                    response_schema=PlantReport,
                ),
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_bytes, mime_type=content_type),
                ],
            ),
            timeout=GEMINI_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError as e:
        raise GeminiTimeoutError("Gemini не ответил вовремя") from e

    except errors.ClientError as e:  # 4xx от Gemini
        if e.code == 429:
            raise GeminiQuotaError("Исчерпан лимит запросов") from e
        raise GeminiConfigError(f"Ошибка запроса к Gemini: {e.code}") from e
    except errors.ServerError as e:  # 5xx от Gemini
        raise GeminiUnavailableError("Gemini недоступен") from e

    if result.parsed is None:
        raise ("Ответ не соответствует схеме")

    return result.parsed