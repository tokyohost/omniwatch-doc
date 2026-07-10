"""提供使用中文点阵字模显示天气数据的 OmniWatch 屏幕样式。"""

from config import BLACK, BLUE, DARK, GRAY, GREEN, HEIGHT, WHITE, WIDTH, YELLOW
from styles.style_plugins import register_style


FONT_16 = {
    '天': ('0000', '7ffe', '0180', '0180', '0180', '0180', 'ffff', '0180', '0380', '0340', '0660', '0c30', '1818', '700e', '4002', '0000'),
    '气': ('0000', '1800', '1ffe', '3000', '2000', '7ffc', '4000', 'c000', 'bff8', '0008', '0008', '0009', '000b', '000f', '0006', '0000'),
    '上': ('0000', '0300', '0300', '0300', '0300', '03fe', '0300', '0300', '0300', '0300', '0300', '0300', '0300', 'ffff', '0000', '0000'),
    '海': ('4300', '73ff', '1400', '0c00', 'cbfc', '6244', '2664', '0624', '0fff', '24c4', '2444', '2424', '67fe', '600c', '4078', '0000'),
    '多': ('0300', '0600', '0ffc', '181c', '3430', '66e0', '0780', '3cc0', '61fe', '0706', '1d18', '31f0', '01c0', '1f00', '7800', '0000'),
    '云': ('3ffc', '0000', '0000', '0000', '0000', 'ffff', '0300', '0600', '0c20', '0c30', '1818', '3018', '7ffc', '2006', '0006', '0000'),
    '阴': ('7dfe', '4d86', '4d86', '4986', '59fe', '5986', '4986', '4d06', '4dfe', '4506', '4d06', '7f06', '4206', '463e', '4400', '0000'),
    '小': ('0180', '0180', '0180', '0180', '1990', '1998', '1188', '318c', '2184', '6186', '4182', '4183', '0180', '0180', '0f80', '0000'),
    '雨': ('0000', 'ffff', '0180', '0180', '7ffe', '6186', '79e6', '6db6', '679e', '79e6', '6db6', '659e', '6186', '61bc', '0000', '0000'),
    '中': ('0000', '0180', '0180', '7ffe', '6186', '6186', '6186', '6186', '7ffe', '6186', '0180', '0180', '0180', '0180', '0180', '0000'),
    '大': ('0180', '0180', '0180', '0180', 'ffff', '0180', '0180', '0180', '03c0', '0240', '0660', '0c30', '1818', '700e', '4002', '0000'),
    '雷': ('0000', '3ffc', '0180', '7ffe', '4182', '5ffa', '0180', '1ff8', '0000', '3ffc', '2184', '3ffc', '2184', '3ffc', '2004', '0000'),
    '雪': ('0000', '3ffc', '0180', '7ffe', '4182', '5ffa', '0180', '1ff8', '0000', '3ffc', '0004', '3ffc', '0004', '7ffc', '0004', '0000'),
    '雾': ('3ffc', '0180', '7ffe', '4182', '1ff8', '0c00', '3ffc', '6c38', '07e0', 'fc7f', '0200', '3ffc', '0608', '78f8', '0000', '0000'),
    '湿': ('4000', '77fe', '1606', '07fe', 'c606', '67fe', '2606', '0492', '2492', '2496', '6694', '6294', '6090', '4fff', '4000', '0000'),
    '度': ('0000', '0080', '00c0', '3fff', '2000', '2218', '3fff', '2218', '23f8', '2000', '2ffc', '6218', '61f0', 'c7f8', '9c0e', '0000'),
    '风': ('3ff8', '2008', '2868', '2c48', '26c8', '2288', '2388', '2188', '2388', '66c8', '6c6b', '6c6f', '482f', 'c006', 'c000', '0000'),
    '速': ('4060', '6060', '37ff', '1060', '07fe', 'f666', '3666', '37fe', '36e6', '31f8', '376e', '7462', 'f800', 'cfff', '0000', '0000'),
    '更': ('7ffe', '0180', '3ffc', '2184', '2184', '3ffc', '2184', '2184', '3ffc', '1104', '1b00', '0e00', '0fc0', '38ff', 'e000', '0000'),
    '新': ('1800', '080e', '7f7e', '2240', '2640', 'ffc0', '087f', '084c', '7f4c', '084c', '6acc', 'cbcc', '098c', '390c', '0000', '0000'),
    '等': ('1820', '3060', '3fff', '68d0', 'cd98', '7ffe', '0180', '0180', 'ffff', '0030', '0030', '7ffe', '0c30', '0430', '01f0', '0000'),
    '待': ('1820', '1820', '33fe', '6020', 'c820', '1fff', '3000', '3000', '77ff', 'f008', 'b308', '3188', '3088', '3008', '3078', '3000'),
    '数': ('0830', '6920', '2b20', '087f', 'ff66', '1ee6', '6be4', 'c924', '102c', 'ff3c', '2318', '3618', '1e3c', '7be6', 'e083', '0000'),
    '据': ('3000', '33fe', '3202', 'fe02', '33fe', '3232', '3232', '3bff', '7e30', 'f630', '37fe', '3582', '3582', '3dfe', 'e982', '0000'),
    '插': ('201e', '23f8', '2020', 'f820', '37ff', '2020', '39a0', '3f3e', 'f622', 'a622', '27fe', '2622', '2622', '27fe', 'e602', '0602'),
    '件': ('0000', '1830', '1930', '1330', '33fe', '7230', '7630', 'f430', 'b030', '37ff', '3030', '3030', '3030', '3030', '3030', '0000'),
    '异': ('0000', '3ff8', '2008', '2008', '3ff8', '200a', '3002', '3ffe', '0000', '0000', 'ffff', '0830', '1810', '3010', '6010', '0000'),
    '常': ('118c', '0998', '7ffe', '4002', '5ffa', '1008', '1008', '1ff8', '1188', '0180', '3ffe', '2186', '2184', '21bc', '0180', '0000'),
    '网': ('0000', '7ffe', '6006', '700e', '7b9e', '6ad6', '6e76', '6466', '6e76', '6b76', '7bde', '708e', '7006', '603c', '0000', '0000'),
    '络': ('0000', '1080', '30fe', '6d84', '4fcc', 'fa78', '1078', '31ce', '6703', '79fe', '0106', '7d06', 'f106', '01fe', '0106', '0000'),
    '错': ('2088', '2088', '7ffe', '4088', 'c088', 'ffff', '3000', '33fe', 'ff06', '3306', '33fe', '3306', '3b06', '33fe', '2306', '0000'),
    '误': ('0000', '63fe', '3206', '1206', '03fe', 'e206', '2000', '27fe', '2060', '2060', '2fff', '28e0', '3998', '270e', '0e06', '0000'),
    '晴': ('0020', '7bff', '4820', '4bfe', '4820', '4fff', '7800', '49fe', '4902', '49fe', '4902', '49fe', '7902', '4906', '013e', '0000'),
}


class WeatherCnStyle:
    """绘制中文城市、天气描述、湿度、风速和更新时间。"""

    name = "weather_cn"
    zh_name = "中文天气"
    type = "custom"
    width = WIDTH
    height = HEIGHT
    landscape = False
    font_name = "native"

    @staticmethod
    def create_dirty_regions():
        """声明中文天气主体和页脚两个动态刷新区域。"""
        return [
            ("weather", 8, 52, 224, 180),
            ("footer", 8, 282, 224, 28),
        ]

    @classmethod
    def select_dirty_regions(cls, previous, current):
        """根据天气数据和系统时间变化选择需要重绘的区域。"""
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
    def _read_weather(snapshot):
        """从 snapshot.ext.weather 中读取天气对象。"""
        return (snapshot or {}).get("ext", {}).get("weather", {}) or {}

    @staticmethod
    def _draw_bitmap_char(canvas, x, y, char, color, scale=1):
        """按点阵数据绘制单个中文字符，并返回字符占用宽度。"""
        rows = FONT_16.get(char)
        if not rows:
            return 0
        width = 16
        for row_index, row_hex in enumerate(rows):
            row_bits = int(row_hex, 16)
            for col_index in range(width):
                if row_bits & (1 << (width - 1 - col_index)):
                    if scale == 1:
                        canvas.pixel(x + col_index, y + row_index, color)
                    else:
                        canvas.fill_rect(
                            x + col_index * scale,
                            y + row_index * scale,
                            scale,
                            scale,
                            color,
                        )
        return width * scale

    @classmethod
    def _draw_bitmap_text(cls, canvas, x, y, text, color, scale=1, spacing=1):
        """按点阵字模绘制中文文本，缺失字会被跳过。"""
        cursor_x = x
        for char in str(text or ""):
            width = cls._draw_bitmap_char(canvas, cursor_x, y, char, color, scale)
            if width > 0:
                cursor_x += width + spacing
            elif char == " ":
                cursor_x += 4 * scale
        return cursor_x - x

    def _draw_header(self, canvas):
        """绘制中文标题和分隔线。"""
        self._draw_bitmap_text(canvas, 8, 12, "天气", BLUE, 1, 2)
        canvas.line(8, 42, 232, 42, DARK)

    def _draw_weather(self, canvas, snapshot):
        """绘制中文天气主体内容。"""
        weather = self._read_weather(snapshot)
        if weather.get("status") != "ok":
            self._draw_bitmap_text(canvas, 8, 72, "等待数据", YELLOW)
            self._draw_bitmap_text(canvas, 8, 96, "插件异常", GRAY)
            return

        city = str(weather.get("city", "--"))
        text = str(weather.get("text", "--"))
        temperature = self._number(weather.get("temperature_c"))
        humidity = self._number(weather.get("humidity"))
        wind = self._number(weather.get("wind_kmh"))
        updated_at = str(weather.get("updated_at", "--:--"))

        self._draw_bitmap_text(canvas, 8, 60, city, WHITE)
        canvas.text(8, 92, "{:4.1f} C".format(temperature), GREEN, 3)
        self._draw_bitmap_text(canvas, 8, 140, text, WHITE, 1, 2)
        canvas.fill_rect(8, 176, 224, 2, DARK)
        self._draw_bitmap_text(canvas, 8, 194, "湿度", GRAY)
        canvas.text(48, 194, "{:3.0f}%".format(humidity), GRAY)
        self._draw_bitmap_text(canvas, 112, 194, "风速", GRAY)
        canvas.text(152, 194, "{:4.1f}".format(wind), GRAY)
        self._draw_bitmap_text(canvas, 8, 220, "更新", BLUE)
        canvas.text(48, 220, updated_at, BLUE)

    @staticmethod
    def _draw_footer(canvas, snapshot):
        """绘制系统当前时间，方便确认屏幕仍在刷新。"""
        timestamp = str((snapshot or {}).get("timestamp", ""))
        clock = timestamp[11:19] if len(timestamp) >= 19 else "--:--:--"
        canvas.line(8, 280, 232, 280, DARK)
        canvas.text(8, 292, clock, GRAY)

    def draw_visible(self, canvas, snapshot):
        """绘制当前条带中可见的完整中文天气屏幕。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        self._draw_header(canvas)
        self._draw_weather(canvas, snapshot)
        self._draw_footer(canvas, snapshot)

    def draw_dirty(self, canvas, key, snapshot):
        """按区域键重绘天气主体或页脚。"""
        snapshot = snapshot or {}
        canvas.clear(BLACK)
        if key == "weather":
            self._draw_weather(canvas, snapshot)
        elif key == "footer":
            self._draw_footer(canvas, snapshot)


def create_weather_cn_style():
    """创建中文天气样式实例。"""
    return WeatherCnStyle()


register_style(WeatherCnStyle.name, create_weather_cn_style)
