"""提供显示主机、CPU 和时间的 OmniWatch 入门样式。"""

from config import BLACK, BLUE, GRAY, HEIGHT, WHITE, WIDTH
from styles.style_plugins import register_style


class MyStatusStyle:
    """安全读取数据快照并绘制基础监控信息。"""

    name = "my_status"
    zh_name = "我的状态"
    type = "custom"
    width = WIDTH
    height = HEIGHT
    landscape = False
    font_name = "native"

    @staticmethod
    def create_dirty_regions():
        """声明主机名、CPU 数值和时钟的动态区域。"""
        return [
            ("host", 8, 8, 224, 24),
            ("cpu", 8, 56, 224, 24),
            ("clock", 8, 292, 224, 18),
        ]

    @classmethod
    def select_dirty_regions(cls, previous, current):
        """比较前后快照并选择真正变化的区域。"""
        previous = previous or {}
        current = current or {}
        regions = {item[0]: item for item in cls.create_dirty_regions()}
        selected = []
        if previous.get("host") != current.get("host"):
            selected.append(regions["host"])
        if previous.get("cpu", {}).get("percent") != current.get("cpu", {}).get("percent"):
            selected.append(regions["cpu"])
        if previous.get("timestamp") != current.get("timestamp"):
            selected.append(regions["clock"])
        return selected

    @staticmethod
    def _number(value, default=0):
        """把未知输入安全转换为浮点数。"""
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    def _draw_host(self, canvas, snapshot):
        """绘制经过长度限制的主机名称。"""
        host = str(snapshot.get("host", "WAITING"))[:18]
        canvas.text(8, 12, host, WHITE, 2)

    def _draw_cpu(self, canvas, snapshot):
        """绘制经过范围限制的 CPU 使用率。"""
        percent = self._number(snapshot.get("cpu", {}).get("percent"))
        percent = max(0, min(100, percent))
        canvas.text(8, 58, "CPU {:3.0f}%".format(percent), BLUE, 2)

    def _draw_clock(self, canvas, snapshot):
        """从标准时间字符串中截取时分秒。"""
        timestamp = str(snapshot.get("timestamp", ""))
        clock = timestamp[11:19] if len(timestamp) >= 19 else "--:--:--"
        canvas.text(8, 296, clock, GRAY)

    def draw_visible(self, canvas, snapshot):
        """绘制当前条带中可见的全部监控内容。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        self._draw_host(canvas, snapshot)
        self._draw_cpu(canvas, snapshot)
        self._draw_clock(canvas, snapshot)

    def draw_dirty(self, canvas, key, snapshot):
        """根据区域键重绘一项变化的监控内容。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        if key == "host":
            self._draw_host(canvas, snapshot)
        elif key == "cpu":
            self._draw_cpu(canvas, snapshot)
        elif key == "clock":
            self._draw_clock(canvas, snapshot)


def create_my_status_style():
    """创建我的状态样式实例。"""
    return MyStatusStyle()


register_style(MyStatusStyle.name, create_my_status_style)
