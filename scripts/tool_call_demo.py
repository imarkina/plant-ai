from urllib import response

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


def get_plant_info(plant_id: int) -> dict:
    """Возвращает информацию о растении по его id: вид, горшок, расположение."""
    print(f">>> Вызвана get_plant_info(plant_id={plant_id})")

    if plant_id != 42:
        raise ValueError(f'Растение с plant_id={plant_id} не найдено')

    return {"species": "Hoya carnosa", "pot": "пластик без дренажа", "location": "северное окно"}


TOOLS = {
    'get_watering_history': get_watering_history,
    'get_plant_info': get_plant_info
}

MAX_STEPS = 5


async def run_agent(question: str):
    config = types.GenerateContentConfig(
        tools=[get_watering_history, get_plant_info],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=question)])]

    for step in range(MAX_STEPS):
        print('шаг', step)
        response = await client.aio.models.generate_content(
            model=api_model, contents=contents, config=config,
        )

        if not response.function_calls:
            print('результат', response.text)
            return response.text

        contents.append(response.candidates[0].content)

        parts = []

        for call in response.function_calls:
            print('кол', call.name, call.args)
            try:
                result = TOOLS[call.name](**call.args)
                print(f'результат вызова {call.name}: {result}')
                parts.append(types.Part.from_function_response(  # ←
                    name=call.name, response={"result": result},
                ))
            except Exception as e:
                parts.append(types.Part.from_function_response(  # ←
                    name=call.name, response={"error":  str(e)},
                ))
                print(e)

        contents.append(types.Content(role="user", parts=parts))

    return "Агент не смог ответить за отведённое число шагов"


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
    asyncio.run(run_agent("Я поливаю растение с id 999 каждые 3 дня. Ему ок с его горшком и местом?"))
