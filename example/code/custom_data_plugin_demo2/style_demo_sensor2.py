"""提供演示传感器2的绑定屏幕样式。"""

from config import BLACK, BLUE, DARK, GRAY, GREEN, HEIGHT, WHITE, WIDTH, YELLOW
from styles.style_plugins import register_style


class DemoSensor2Style:
    """绘制演示传感器2的温度、湿度、状态和更新时间。"""

    name = "demo_sensor2"
    zh_name = "演示传感器2"
    type = "custom"
    width = WIDTH
    height = HEIGHT
    landscape = False
    font_name = "native"

    @staticmethod
    def create_dirty_regions():
        """声明传感器主体的动态刷新区域。"""
        return [("sensor", 8, 56, 224, 240)]

    @classmethod
    def select_dirty_regions(cls, previous, current):
        """当演示传感器2数据发生变化时选择主体区域。"""
        previous_data = (previous or {}).get("ext", {}).get("demo_sensor2", {})
        current_data = (current or {}).get("ext", {}).get("demo_sensor2", {})
        return cls.create_dirty_regions() if previous_data != current_data else []

    @staticmethod
    def _number(value, default=0):
        """把未知输入安全转换为浮点数。"""
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    @staticmethod
    def _read_sensor(snapshot):
        """从 snapshot.ext.demo_sensor2 中读取传感器对象。"""
        return (snapshot or {}).get("ext", {}).get("demo_sensor2", {}) or {}

    @staticmethod
    def _draw_header(canvas):
        """绘制固定标题和分隔线。"""
        canvas.text(8, 14, "SENSOR 2", BLUE, 2)
        canvas.line(8, 44, 232, 44, DARK)

    def _draw_sensor(self, canvas, snapshot):
        """绘制温湿度、状态和更新时间。"""
        sensor = self._read_sensor(snapshot)
        if not sensor:
            canvas.text(8, 76, "WAITING DATA", YELLOW)
            canvas.text(8, 102, "Enable plugin", GRAY)
            return

        temperature = self._number(sensor.get("temperature_c"))
        humidity = max(0, min(100, self._number(sensor.get("humidity"))))
        status = str(sensor.get("status", "unknown")).upper()[:12]
        updated_at = str(sensor.get("updated_at", "--:--:--"))[:8]
        status_color = GREEN if status == "OK" else YELLOW

        canvas.text(8, 68, "TEMPERATURE", GRAY)
        canvas.text(8, 94, "{:4.1f} C".format(temperature), WHITE, 3)
        canvas.text(8, 146, "HUMIDITY {:3.0f}%".format(humidity), GRAY)
        canvas.fill_rect(8, 170, 224, 14, DARK)
        canvas.fill_rect(8, 170, int(224 * humidity / 100), 14, BLUE)
        canvas.text(8, 212, "STATUS " + status, status_color)
        canvas.text(8, 250, "UPDATED " + updated_at, GRAY)

    def draw_visible(self, canvas, snapshot):
        """绘制当前条带中可见的完整传感器屏幕。"""
        canvas.clear(BLACK)
        self._draw_header(canvas)
        self._draw_sensor(canvas, snapshot)

    def draw_dirty(self, canvas, key, snapshot):
        """根据区域键重绘传感器主体。"""
        canvas.clear(BLACK)
        if key == "sensor":
            self._draw_sensor(canvas, snapshot)


def create_demo_sensor2_style():
    """创建演示传感器2样式实例。"""
    return DemoSensor2Style()


register_style(DemoSensor2Style.name, create_demo_sensor2_style)
