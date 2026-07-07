"""提供带进度条和局部刷新的 OmniWatch 仪表盘样式。"""

from config import BLACK, BLUE, DARK, GRAY, GREEN, HEIGHT, WHITE, WIDTH, YELLOW
from styles.style_plugins import register_style


class MyDashboardStyle:
    """绘制主机标题、CPU 进度条、网络状态和时钟。"""

    name = "my_dashboard"
    zh_name = "我的仪表盘"
    type = "custom"
    width = WIDTH
    height = HEIGHT
    landscape = False
    font_name = "native"

    @staticmethod
    def create_dirty_regions():
        """声明全部可独立刷新的动态内容区域。"""
        return [
            ("header", 8, 8, 224, 28),
            ("cpu", 8, 48, 224, 40),
            ("network", 8, 136, 224, 32),
            ("footer", 8, 292, 224, 18),
        ]

    @classmethod
    def select_dirty_regions(cls, previous, current):
        """按字段变化选择需要更新的动态区域。"""
        previous = previous or {}
        current = current or {}
        regions = {item[0]: item for item in cls.create_dirty_regions()}
        selected = []
        if previous.get("host") != current.get("host"):
            selected.append(regions["header"])
        if previous.get("cpu", {}).get("percent") != current.get("cpu", {}).get("percent"):
            selected.append(regions["cpu"])
        if previous.get("network") != current.get("network"):
            selected.append(regions["network"])
        if previous.get("timestamp") != current.get("timestamp"):
            selected.append(regions["footer"])
        return selected

    @staticmethod
    def _number(value, default=0):
        """把未知输入安全转换为浮点数。"""
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    def _draw_header(self, canvas, snapshot):
        """绘制标题背景和主机名称。"""
        host = str(snapshot.get("host", "WAITING"))[:18]
        canvas.fill_rect(8, 8, 224, 28, BLUE)
        canvas.text(16, 18, host, WHITE)

    def _draw_cpu(self, canvas, snapshot):
        """绘制 CPU 数值和水平进度条。"""
        percent = self._number(snapshot.get("cpu", {}).get("percent"))
        percent = max(0, min(100, percent))
        color = YELLOW if percent >= 80 else BLUE
        canvas.text(8, 50, "CPU {:3.0f}%".format(percent), WHITE)
        canvas.fill_rect(8, 70, 224, 12, DARK)
        canvas.fill_rect(8, 70, int(224 * percent / 100), 12, color)

    def _draw_network(self, canvas, snapshot):
        """根据在线状态绘制不同颜色的网络文字。"""
        online = bool(snapshot.get("network", {}).get("online"))
        text = "NETWORK ONLINE" if online else "NETWORK OFFLINE"
        canvas.text(8, 148, text, GREEN if online else YELLOW)

    def _draw_footer(self, canvas, snapshot):
        """绘制页脚分隔线和当前时间。"""
        timestamp = str(snapshot.get("timestamp", ""))
        clock = timestamp[11:19] if len(timestamp) >= 19 else "--:--:--"
        canvas.line(8, 290, 232, 290, DARK)
        canvas.text(8, 296, clock, GRAY)

    def draw_visible(self, canvas, snapshot):
        """绘制当前条带中可见的全部仪表盘内容。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        self._draw_header(canvas, snapshot)
        self._draw_cpu(canvas, snapshot)
        self._draw_network(canvas, snapshot)
        self._draw_footer(canvas, snapshot)

    def draw_dirty(self, canvas, key, snapshot):
        """根据区域键重绘一块变化的仪表盘内容。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        if key == "header":
            self._draw_header(canvas, snapshot)
        elif key == "cpu":
            self._draw_cpu(canvas, snapshot)
        elif key == "network":
            self._draw_network(canvas, snapshot)
        elif key == "footer":
            self._draw_footer(canvas, snapshot)


def create_my_dashboard_style():
    """创建我的仪表盘样式实例。"""
    return MyDashboardStyle()


register_style(MyDashboardStyle.name, create_my_dashboard_style)
