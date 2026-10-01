from app.agent.tools.care import make_care_tools
from app.agent.tools.plants import make_plant_tools
from app.agent.tools.weather import make_weather_tools


def make_tools(user_id: str) -> dict:
    return {
        **make_plant_tools(user_id),
        **make_weather_tools(),
        **make_care_tools(user_id)
    }