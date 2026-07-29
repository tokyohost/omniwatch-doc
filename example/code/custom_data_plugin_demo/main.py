#!/usr/bin/env python3
"""OmniWatch 自定义数据插件示例。"""

import datetime as dt
import json
import random


def collect(config_json):
    """解析面板配置并返回可以写入 snapshot.ext.demo_sensor 的 JSON 对象。"""
    config = json.loads(config_json)
    offset = float(config.get("offset", 0))
    return {
        "time": dt.datetime.now().isoformat(timespec="seconds"),
        "temperature_c": round(25 + random.random() * 5 + offset, 1),
        "status": "ok",
    }
