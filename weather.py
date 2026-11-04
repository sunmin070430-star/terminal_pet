import requests

SEOUL_LAT = 37.57
SEOUL_LON = 126.98
API_URL = "https://api.open-meteo.com/v1/forecast"


def code_to_weather(code):
    """WMO 날씨 코드를 맑음/흐림/비/눈 중 하나로 바꾼다."""
    if code in (0, 1):
        return "맑음"
    if code in (2, 3, 45, 48):
        return "흐림"
    if 71 <= code <= 77 or code in (85, 86):
        return "눈"
    return "비"


def get_weather():
    """서울의 현재 날씨와 기온을 가져온다. 실패하면 None을 반환한다."""
    params = {
        "latitude": SEOUL_LAT,
        "longitude": SEOUL_LON,
        "current": "temperature_2m,weather_code",
    }
    try:
        response = requests.get(API_URL, params=params, timeout=5)
        response.raise_for_status()
        current = response.json()["current"]
        return {
            "weather": code_to_weather(current["weather_code"]),
            "temperature": current["temperature_2m"],
        }
    except (requests.RequestException, KeyError, ValueError):
        return None


if __name__ == "__main__":
    print(get_weather())