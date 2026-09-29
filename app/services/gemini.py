from google import genai
from google.genai import types
from app.config import api_model, api_key
from app.prompts import prompt
from app.schemas import PlantReport

client = genai.Client(api_key=api_key)


async def analyze_photo_image(image_bytes):
    result = await client.aio.models.generate_content(
        model=api_model,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=PlantReport,
        ),
        contents=[
            prompt,
            types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
        ],
    )
    return result.parsed
