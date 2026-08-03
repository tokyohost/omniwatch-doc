"""提供无需自定义数据插件的纯界面时钟样式。"""

from config import BLACK, BLUE, DARK, GRAY, HEIGHT, WHITE, WIDTH
from styles.style_plugins import register_style


class StyleOnlyClock:
    """绘制主机时间、日期和基础运行状态。"""

    name = "only_clock"
    zh_name = "纯样式时钟"
    type = "custom"
    width = WIDTH
    height = HEIGHT
    landscape = False
    font_name = "native"

    @staticmethod
    def create_dirty_regions():
        """声明时钟主体的动态刷新区域。"""
        return [("clock", 8, 72, 224, 210)]

    @classmethod
    def select_dirty_regions(cls, previous, current):
        """当主机时间或基础状态变化时选择时钟区域。"""
        previous = previous or {}
        current = current or {}
        watched_fields = ("timestamp", "cpu", "memory")
        changed = any(previous.get(key) != current.get(key) for key in watched_fields)
        return cls.create_dirty_regions() if changed else []

    @staticmethod
    def _text(snapshot, key, default="--"):
        """安全读取快照中的文本字段。"""
        value = (snapshot or {}).get(key, default)
        return str(value if value not in (None, "") else default)

    @staticmethod
    def _percent(snapshot, section):
        """把快照分组中的 percent 转换为零到一百之间的整数。"""
        try:
            values = (snapshot or {}).get(section, {}) or {}
            return max(0, min(100, int(float(values.get("percent", 0)))))
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _draw_header(canvas):
        """绘制固定标题和顶部分隔线。"""
        canvas.text(8, 16, "OMNI CLOCK", BLUE, 2)
        canvas.line(8, 50, 232, 50, DARK)

    def _draw_clock(self, canvas, snapshot):
        """绘制时间、日期、CPU 和内存摘要。"""
        timestamp = self._text(snapshot, "timestamp", "")
        current_time = timestamp[11:19] if len(timestamp) >= 19 else "--:--:--"
        current_date = timestamp[:10] if len(timestamp) >= 10 else "----/--/--"
        cpu = self._percent(snapshot, "cpu")
        memory = self._percent(snapshot, "memory")
        canvas.text(8, 82, current_time, WHITE, 4)
        canvas.text(8, 132, current_date, GRAY)
        canvas.fill_rect(8, 174, 224, 2, DARK)
        canvas.text(8, 202, "CPU {:3d}%".format(cpu), BLUE, 2)
        canvas.text(8, 242, "RAM {:3d}%".format(memory), WHITE, 2)

    def draw_visible(self, canvas, snapshot):
        """绘制当前可见区域的完整时钟界面。"""
        canvas.clear(BLACK)
        self._draw_header(canvas)
        self._draw_clock(canvas, snapshot)

    def draw_dirty(self, canvas, key, snapshot):
        """根据区域键重绘时钟主体。"""
        if key != "clock":
            return
        canvas.fill_rect(8, 72, 224, 210, BLACK)
        self._draw_clock(canvas, snapshot)


def create_style_only_clock():
    """创建纯样式时钟实例。"""
    return StyleOnlyClock()


register_style(StyleOnlyClock.name, create_style_only_clock)
