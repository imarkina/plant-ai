import httpx

def make_weather_tools() -> dict:
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

    return {
        "get_weather": get_weather,
    }
