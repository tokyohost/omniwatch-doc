#!/usr/bin/env python3
"""OmniWatch 自定义数据采集示例。"""

import datetime as dt
import random


# ext 节点下的数据字段名，所有自定义数据脚本之间必须唯一。
CUSTOM_DATA_KEY = "demo_sensor"

# 采集任务英文标识，配置采集间隔时使用 custom_data.demo_sensor。
CUSTOM_DATA_NAME = "demo_sensor"

# Windows 配置页和日志中展示的中文名称。
CUSTOM_DATA_ZH_NAME = "演示传感器"

# 默认采集间隔，单位为秒；可在配置页或 pico-monitor.conf 中覆盖。
CUSTOM_DATA_INTERVAL = 5


def collect():
    """返回一个可以写入 snapshot.ext.demo_sensor 的 JSON 对象。"""
    return {
        "time": dt.datetime.now().isoformat(timespec="seconds"),
        "temperature_c": round(25 + random.random() * 5, 1),
        "status": "ok",
    }
