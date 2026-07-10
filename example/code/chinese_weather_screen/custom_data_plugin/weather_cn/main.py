#!/usr/bin/env python3
"""采集 Open-Meteo 天气数据并转换为中文天气字段。"""

import datetime as dt

import requests


LATITUDE = 31.2304
LONGITUDE = 121.4737
CITY_NAME = "上海"
TIMEZONE = "Asia/Shanghai"
API_URL = "https://api.open-meteo.com/v1/forecast"
USE_SYSTEM_PROXY = False

WEATHER_TEXT = {
    0: "晴",
    1: "晴",
    2: "多云",
    3: "阴",
    45: "雾",
    48: "雾",
    51: "小雨",
    53: "小雨",
    55: "中雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "雪",
    73: "雪",
    75: "雪",
    80: "小雨",
    81: "中雨",
    82: "大雨",
    95: "雷雨",
}


def _weather_text(code):
    """把天气代码转换为中文短文本。"""
    return WEATHER_TEXT.get(code, "异常")


def _hour_minute(value):
    """从接口时间字符串中提取小时和分钟。"""
    try:
        parsed = dt.datetime.fromisoformat(str(value))
        return parsed.strftime("%H:%M")
    except ValueError:
        return "--:--"


def collect():
    """请求天气接口并返回中文天气 JSON 对象。"""
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
            "text": "异常",
            "updated_at": dt.datetime.now().strftime("%H:%M"),
            "status": "error",
            "message": str(exc)[:80],
        }
