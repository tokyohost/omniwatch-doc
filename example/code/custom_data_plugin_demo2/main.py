#!/usr/bin/env python3
"""生成演示传感器2的模拟温湿度数据。"""

import datetime as dt
import json
import random


def _bounded_random(base, amplitude, minimum, maximum):
    """围绕基准值生成随机数，并把结果限制在指定范围内。"""
    value = float(base) + random.uniform(-amplitude, amplitude)
    return round(max(minimum, min(maximum, value)), 1)


def collect(config_json):
    """解析面板配置并返回可写入 snapshot.ext.demo_sensor2 的数据。"""
    config = json.loads(config_json)
    temperature = _bounded_random(config.get("temperature_base", 26), 1.5, -40, 100)
    humidity = _bounded_random(config.get("humidity_base", 55), 4, 0, 100)
    return {
        "temperature_c": temperature,
        "humidity": humidity,
        "status": "warning" if temperature >= 30 else "ok",
        "updated_at": dt.datetime.now().strftime("%H:%M:%S"),
    }
