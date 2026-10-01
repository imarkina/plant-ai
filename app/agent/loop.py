from app.config import GEMINI_MODEL, client, MAX_AGENT_LOOP_STEPS
from google.genai import types

async def run_agent(question: str, tools: dict):
    config = types.GenerateContentConfig(
        tools=list(tools.values()),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        system_instruction="Если для инструмента не хватает данных (например, города), не придумывай их, а спроси пользователя",
    )

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=question)])]

    for step in range(MAX_AGENT_LOOP_STEPS):
        print('шаг', step)
        response = await client.aio.models.generate_content(
            model=GEMINI_MODEL, contents=contents, config=config,
        )

        if not response.function_calls:
            print('результат', response.text)
            return response.text

        contents.append(response.candidates[0].content)

        parts = []

        for call in response.function_calls:

            try:
                if call.name not in tools:
                    raise KeyError(f'Инструмента {call.name} нет. Доступны: {", ".join(tools)}')
                print('кол', call.name, call.args)
                result = await tools[call.name](**call.args)
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
