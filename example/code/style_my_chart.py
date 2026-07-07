"""提供带 CPU 历史面积图的 OmniWatch 自定义样式。"""

from config import BLACK, BLUE, GRAY, GREEN, HEIGHT, WHITE, WIDTH, YELLOW
from styles.style_plugins import register_style


class MyChartStyle:
    """绘制 CPU 当前值、历史图表和时间。"""

    name = "my_chart"
    zh_name = "我的图表"
    type = "custom"
    width = WIDTH
    height = HEIGHT
    landscape = False
    font_name = "native"

    @staticmethod
    def create_dirty_regions():
        """声明数值、图表上下半区和时钟的动态区域。"""
        return [
            ("cpu", 8, 48, 224, 32),
            ("history_top", 8, 112, 224, 38),
            ("history_bottom", 8, 150, 224, 38),
            ("clock", 8, 292, 224, 18),
        ]

    @classmethod
    def select_dirty_regions(cls, previous, current):
        """按 CPU 数值、历史数据和时间变化选择区域。"""
        previous = previous or {}
        current = current or {}
        regions = {item[0]: item for item in cls.create_dirty_regions()}
        selected = []
        previous_cpu = previous.get("cpu", {})
        current_cpu = current.get("cpu", {})
        if previous_cpu.get("percent") != current_cpu.get("percent"):
            selected.append(regions["cpu"])
        if previous_cpu.get("history") != current_cpu.get("history"):
            selected.append(regions["history_top"])
            selected.append(regions["history_bottom"])
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

    @staticmethod
    def _visible(canvas, top, bottom):
        """判断完整屏幕纵向区间是否与当前画布相交。"""
        return top < canvas.origin_y + canvas.height and bottom > canvas.origin_y

    def _draw_cpu(self, canvas, snapshot):
        """绘制当前 CPU 使用率。"""
        percent = self._number(snapshot.get("cpu", {}).get("percent"))
        percent = max(0, min(100, percent))
        canvas.text(8, 52, "CPU {:3.0f}%".format(percent), WHITE, 2)

    @staticmethod
    def _draw_history(canvas, values):
        """使用批量图表接口绘制 CPU 历史面积图。"""
        canvas.draw_line_chart({
            "x": 8,
            "y": 112,
            "width": 224,
            "height": 76,
            "maximum": 100,
            "color": BLUE,
            "filled": True,
            "regions": ((60, GREEN), (85, YELLOW), (101, BLUE)),
            "grid_step_x": 16,
            "grid_step_y": 12,
            "grid_color": GRAY,
        }, values or ())

    @staticmethod
    def _draw_clock(canvas, snapshot):
        """绘制从时间戳中提取的时分秒。"""
        timestamp = str(snapshot.get("timestamp", ""))
        clock = timestamp[11:19] if len(timestamp) >= 19 else "--:--:--"
        canvas.text(8, 296, clock, GRAY)

    def draw_visible(self, canvas, snapshot):
        """仅在当前条带相交时绘制对应内容。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        if self._visible(canvas, 0, 32):
            canvas.text(8, 12, "CPU HISTORY", BLUE, 2)
        if self._visible(canvas, 48, 80):
            self._draw_cpu(canvas, snapshot)
        if self._visible(canvas, 112, 188):
            self._draw_history(canvas, snapshot.get("cpu", {}).get("history", ()))
        if self._visible(canvas, 292, 310):
            self._draw_clock(canvas, snapshot)

    def draw_dirty(self, canvas, key, snapshot):
        """根据区域键重绘 CPU、图表或时钟。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        if key == "cpu":
            self._draw_cpu(canvas, snapshot)
        elif key in ("history_top", "history_bottom"):
            self._draw_history(canvas, snapshot.get("cpu", {}).get("history", ()))
        elif key == "clock":
            self._draw_clock(canvas, snapshot)


def create_my_chart_style():
    """创建我的图表样式实例。"""
    return MyChartStyle()


register_style(MyChartStyle.name, create_my_chart_style)
