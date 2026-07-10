#!/usr/bin/env python3
"""OmniWatch 自定义数据插件示例。"""

import datetime as dt
import random


def collect():
    """返回可以写入 snapshot.ext.demo_sensor 的 JSON 对象。"""
    return {
        "time": dt.datetime.now().isoformat(timespec="seconds"),
        "temperature_c": round(25 + random.random() * 5, 1),
        "status": "ok",
    }
