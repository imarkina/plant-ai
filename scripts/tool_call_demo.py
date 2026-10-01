import httpx

from app.config import api_model, client
from google.genai import types
import asyncio


async def get_watering_history(plant_id: int) -> list[str]:
    """Возвращает даты последних поливов растения по его id"""
    print(f">>> Вызвана get_watering_history(plant_id={plant_id})")
    return ["2026-09-20", "2026-09-23", "2026-09-27"]


async def get_plant_info(plant_id: int) -> dict:
    """Возвращает информацию о растении по его id: вид, горшок, расположение."""
    print(f">>> Вызвана get_plant_info(plant_id={plant_id})")

    if plant_id != 42:
        raise ValueError(f'Растение с plant_id={plant_id} не найдено')

    return {"species": "Hoya carnosa", "pot": "пластик без дренажа", "location": "северное окно"}


async def get_weather(latitude: float, longitude: float) -> dict:
    """Возвращает информацию о температуре и влажности в городе по координатам"""
    async with httpx.AsyncClient() as http:
        resp = await http.get('https://api.open-meteo.com/v1/forecast?latitude',
                              params={"latitude": latitude, "longitude": longitude,
                                      "current": "temperature_2m,relative_humidity_2m"})
        resp.raise_for_status()
        data = resp.json()
        temperature = data["current"]["temperature_2m"]
        humidity = data["current"]["relative_humidity_2m"]
        print(temperature, humidity)
        return {'temperature': temperature, 'humidity': humidity}

async def get_user_location() -> str:
    """Возвращает город пользователя"""
    return 'Москва'

TOOLS = {
    'get_watering_history': get_watering_history,
    'get_plant_info': get_plant_info,
    'get_weather': get_weather,
    'get_user_location': get_user_location
}

MAX_STEPS = 5


async def run_agent(question: str):
    config = types.GenerateContentConfig(
        tools=list(TOOLS.values()),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        system_instruction="Если для инструмента не хватает данных (например, города), не придумывай их, а спроси пользователя",
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

            try:
                if call.name not in TOOLS:
                    raise KeyError(f'Инструмента {call.name} нет. Доступны: {", ".join(TOOLS)}')
                print('кол', call.name, call.args)
                result = await TOOLS[call.name](**call.args)
                print(f'результат вызова {call.name}: {result}')
                parts.append(types.Part.from_function_response(  # ←
                    name=call.name, response={"result": result},
                ))
            except Exception as e:
                parts.append(types.Part.from_function_response(  # ←
                    name=call.name, response={"error": str(e)},
                ))
                print(e)

        contents.append(types.Content(role="user", parts=parts))

    return "Агент не смог ответить за отведённое число шагов"


if __name__ == "__main__":
    # asyncio.run(run_agent("Какая сейчас погода в Москве? Можно ли выставить хойю с id 42 на балкон?"))
    asyncio.run(run_agent("Какая погода там, где стоит моя хойя с id 42?"))
