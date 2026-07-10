"""提供显示自定义天气数据的 OmniWatch 屏幕样式。"""

from config import BLACK, BLUE, DARK, GRAY, GREEN, HEIGHT, WHITE, WIDTH, YELLOW
from styles.style_plugins import register_style


class WeatherPanelStyle:
    """绘制城市、温度、天气描述、湿度、风速和更新时间。"""

    name = "weather_panel"
    zh_name = "天气面板"
    type = "custom"
    width = WIDTH
    height = HEIGHT
    landscape = False
    font_name = "native"

    @staticmethod
    def create_dirty_regions():
        """声明天气内容和页脚时钟两个动态刷新区域。"""
        return [
            ("weather", 8, 52, 224, 180),
            ("footer", 8, 282, 224, 28),
        ]

    @classmethod
    def select_dirty_regions(cls, previous, current):
        """当天气数据或系统时间变化时选择需要重绘的区域。"""
        previous = previous or {}
        current = current or {}
        regions = {item[0]: item for item in cls.create_dirty_regions()}
        selected = []
        previous_weather = previous.get("ext", {}).get("weather", {})
        current_weather = current.get("ext", {}).get("weather", {})
        if previous_weather != current_weather:
            selected.append(regions["weather"])
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

    @staticmethod
    def _short_text(value, limit):
        """把任意值转换为适合小屏显示的短文本。"""
        text = str(value or "--")
        return text[:limit]

    @staticmethod
    def _read_weather(snapshot):
        """从 snapshot.ext.weather 中读取天气对象。"""
        return (snapshot or {}).get("ext", {}).get("weather", {}) or {}

    def _draw_header(self, canvas):
        """绘制固定标题和分隔线。"""
        canvas.text(8, 12, "WEATHER", BLUE, 2)
        canvas.line(8, 42, 232, 42, DARK)

    def _draw_weather(self, canvas, snapshot):
        """绘制天气主体内容。"""
        weather = self._read_weather(snapshot)
        status = weather.get("status")
        if status != "ok":
            canvas.text(8, 72, "Waiting weather", YELLOW)
            canvas.text(8, 96, "Check plugin data", GRAY)
            return

        city = self._short_text(weather.get("city"), 18)
        text = self._short_text(weather.get("text"), 18)
        temperature = self._number(weather.get("temperature_c"))
        humidity = self._number(weather.get("humidity"))
        wind = self._number(weather.get("wind_kmh"))
        updated_at = self._short_text(weather.get("updated_at"), 8)

        canvas.text(8, 60, city, WHITE)
        canvas.text(8, 92, "{:4.1f} C".format(temperature), GREEN, 3)
        canvas.text(8, 136, text, WHITE, 2)
        canvas.fill_rect(8, 176, 224, 2, DARK)
        canvas.text(8, 194, "HUM {:3.0f}%".format(humidity), GRAY)
        canvas.text(120, 194, "WIND {:4.1f}".format(wind), GRAY)
        canvas.text(8, 218, "UPDATED " + updated_at, BLUE)

    @staticmethod
    def _draw_footer(canvas, snapshot):
        """绘制系统当前时间，方便判断屏幕仍在刷新。"""
        timestamp = str((snapshot or {}).get("timestamp", ""))
        clock = timestamp[11:19] if len(timestamp) >= 19 else "--:--:--"
        canvas.line(8, 280, 232, 280, DARK)
        canvas.text(8, 292, "LOCAL " + clock, GRAY)

    def draw_visible(self, canvas, snapshot):
        """绘制当前条带中可见的完整天气屏幕。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        self._draw_header(canvas)
        self._draw_weather(canvas, snapshot)
        self._draw_footer(canvas, snapshot)

    def draw_dirty(self, canvas, key, snapshot):
        """根据区域键重绘天气主体或页脚时钟。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        if key == "weather":
            self._draw_weather(canvas, snapshot)
        elif key == "footer":
            self._draw_footer(canvas, snapshot)


def create_weather_panel_style():
    """创建天气面板样式实例。"""
    return WeatherPanelStyle()


register_style(WeatherPanelStyle.name, create_weather_panel_style)
