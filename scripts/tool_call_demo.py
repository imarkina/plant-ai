from app.config import api_model, client
from google.genai import types
import asyncio  # это наверх, к остальным импортам

def get_watering_history(plant_id: int) -> list[str]:
    """Возвращает даты последних поливов растения по его id"""
    print(f">>> Вызвана get_watering_history(plant_id={plant_id})")
    return ["2026-09-20", "2026-09-23", "2026-09-27"]

def get_currency_rate(currency_id: int) -> list[str]:
    """Возвращает курс валют"""
    print(f">>> Вызвана get_currency_rate(currency_id={currency_id})")
    return ["100", "200"]
# test
async def analyze_text(question: str):
    response = await client.aio.models.generate_content(
        model=api_model,
        contents=question,
        config=types.GenerateContentConfig(
            tools=[get_watering_history, get_currency_rate]
        )
    )
    print(response.text)
    return response.text

if __name__ == "__main__":
    asyncio.run(analyze_text("Я поливаю хойю с id 42. Не слишком ли часто?"))