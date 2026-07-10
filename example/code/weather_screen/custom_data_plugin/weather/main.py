#!/usr/bin/env python3
"""采集 Open-Meteo 天气数据并转换为 OmniWatch 易显示的字段。"""

import datetime as dt

import requests


LATITUDE = 31.2304
LONGITUDE = 121.4737
CITY_NAME = "Shanghai"
TIMEZONE = "Asia/Shanghai"
API_URL = "https://api.open-meteo.com/v1/forecast"
USE_SYSTEM_PROXY = False

WEATHER_TEXT = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Cloudy",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Rain shower",
    81: "Shower",
    82: "Heavy shower",
    95: "Thunderstorm",
}


def _weather_text(code):
    """把天气代码转换为适合点阵屏显示的英文短文本。"""
    return WEATHER_TEXT.get(code, "Unknown")


def _hour_minute(value):
    """从接口时间字符串中提取小时和分钟。"""
    try:
        parsed = dt.datetime.fromisoformat(str(value))
        return parsed.strftime("%H:%M")
    except ValueError:
        return "--:--"


def collect():
    """请求天气接口并返回可写入 snapshot.ext.weather 的 JSON 对象。"""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "timezone": TIMEZONE,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
    }
    try:
        session = requests.Session()
        session.trust_env = USE_SYSTEM_PROXY
        response = session.get(API_URL, params=params, timeout=(3, 6))
        response.raise_for_status()
        payload = response.json()
        current = payload.get("current") or {}
        weather_code = current.get("weather_code")

        return {
            "city": CITY_NAME,
            "temperature_c": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_kmh": current.get("wind_speed_10m"),
            "code": weather_code,
            "text": _weather_text(weather_code),
            "updated_at": _hour_minute(current.get("time")),
            "status": "ok",
        }
    except requests.RequestException as exc:
        return {
            "city": CITY_NAME,
            "text": "Network error",
            "updated_at": dt.datetime.now().strftime("%H:%M"),
            "status": "error",
            "message": str(exc)[:80],
        }
