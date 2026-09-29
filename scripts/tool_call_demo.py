from app.config import api_model, client
from google.genai import types
import asyncio

def get_watering_history(plant_id: int) -> list[str]:
    """Возвращает даты последних поливов растения по его id"""
    print(f">>> Вызвана get_watering_history(plant_id={plant_id})")
    return ["2026-09-20", "2026-09-23", "2026-09-27"]

def get_currency_rate(currency_id: int) -> list[str]:
    """Возвращает курс валют"""
    print(f">>> Вызвана get_currency_rate(currency_id={currency_id})")
    return ["100", "200"]

TOOLS = {
    'get_watering_history': get_watering_history
}

async def analyze_text(question: str):
    config = types.GenerateContentConfig(
        tools=[get_watering_history],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    user_message = types.Content(role="user", parts=[types.Part.from_text(text=question)])

    response = await client.aio.models.generate_content(
        model=api_model, contents=[user_message], config=config,
    )

    call = response.function_calls[0]
    result = TOOLS[call.name](**call.args)

    tool_message = types.Content(role="user", parts=[
        types.Part.from_function_response(name=call.name, response={"result": result}),
    ])

    print(response.function_calls)

    final = await client.aio.models.generate_content(
        model=api_model,
        contents=[user_message, response.candidates[0].content, tool_message],
        config=config,
    )

    print(final.text)
    return response.text

if __name__ == "__main__":
    asyncio.run(analyze_text("Я поливаю хойю с id 42. Не слишком ли часто?"))