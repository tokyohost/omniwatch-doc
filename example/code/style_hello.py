"""提供适合第一次上传的 OmniWatch 欢迎样式。"""

from config import BLACK, BLUE, HEIGHT, WHITE, WIDTH
from styles.style_plugins import register_style


class HelloStyle:
    """绘制固定标题和欢迎文字。"""

    name = "hello"
    zh_name = "你好世界"
    type = "custom"
    width = WIDTH
    height = HEIGHT
    landscape = False
    font_name = "native"

    @staticmethod
    def create_dirty_regions():
        """声明本样式没有需要单独更新的动态区域。"""
        return []

    def draw_visible(self, canvas, snapshot):
        """绘制当前条带中可见的全部固定内容。"""
        canvas.clear(BLACK)
        canvas.fill_rect(8, 8, 224, 28, BLUE)
        canvas.text(16, 18, "OMNIWATCH", WHITE)
        canvas.text(16, 64, "HELLO!", WHITE, 2)
        canvas.text(16, 96, "MY FIRST STYLE", BLUE)

    def draw_dirty(self, canvas, key, snapshot):
        """处理动态区域重绘；本样式暂时没有动态区域。"""
        return None


def create_hello_style():
    """创建你好世界样式实例。"""
    return HelloStyle()


register_style(HelloStyle.name, create_hello_style)
