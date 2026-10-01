from app.agent.loop import run_agent
import asyncio

from app.agent.tools import make_tools

async def main():
    tools = make_tools("3758ff46-f092-415f-a440-f526c067383a")
    answer = await run_agent("Что мне сегодня сделать по уходу за растениями?", tools)
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())