# Canvas 绘图接口速查表

[返回总目录](../README.md) · [上传与排错](06-上传与排错.md)

所有坐标都是完整屏幕坐标，颜色从 `config` 导入。

## 基础接口

| 调用 | 作用 | 示例 |
| --- | --- | --- |
| `clear(color)` | 清空当前条带或脏区域 | `canvas.clear(BLACK)` |
| `pixel(x, y, color)` | 画一个像素 | `canvas.pixel(10, 10, WHITE)` |
| `fill_rect(x, y, w, h, color)` | 实心矩形 | `canvas.fill_rect(8, 8, 80, 20, BLUE)` |
| `fill_round_rect(x, y, w, h, color, radius)` | 小圆角实心矩形 | `canvas.fill_round_rect(8, 8, 80, 20, DARK, 3)` |
| `line(x0, y0, x1, y1, color)` | 线段 | `canvas.line(8, 40, 232, 40, GRAY)` |
| `text(x, y, value, color, scale)` | 点阵文字 | `canvas.text(8, 8, "CPU", WHITE, 2)` |
| `text_width(value, scale)` | 计算文字像素宽度 | `width = canvas.text_width("CPU", 2)` |

## 居中文字

```python
text = "OMNIWATCH"
text_width = canvas.text_width(text)
x = (240 - text_width) // 2
canvas.text(x, 12, text, WHITE)
```

## 图形与批量接口

| 调用 | 用途 |
| --- | --- |
| `draw_rect(x, y, w, h, color, thickness=1)` | 一次调用画矩形边框 |
| `draw_grid(x, y, w, h, step_x, step_y, color)` | 规则点阵网格 |
| `draw_polyline(points, color)` | 绘制已经计算好的连续折线 |
| `fill_polygon(points, color)` | 填充同色多边形 |
| `draw_columns(columns, bottom=None)` | 批量画采样列或面积列 |
| `draw_line_chart(definition, values)` | 自动缩放和绘制历史图 |
| `draw_commands(commands)` | 一次提交多条矩形、边框或线段命令 |

## 批量命令格式

每条命令是 `(操作, x, y, 参数A, 参数B, 颜色)`：

```python
from canvas import DRAW_COMMAND_FILL_RECT, DRAW_COMMAND_LINE, DRAW_COMMAND_RECT

commands = (
    (DRAW_COMMAND_FILL_RECT, 8, 8, 80, 20, DARK),
    (DRAW_COMMAND_RECT, 8, 8, 80, 20, BLUE),
    (DRAW_COMMAND_LINE, 8, 40, 88, 40, GRAY),
)
canvas.draw_commands(commands)
```

对于矩形操作，参数 A/B 是宽和高；对于线段操作，它们是终点 `x1/y1`。

## 可见性判断模板

复杂图表可先判断是否与当前条带相交：

```python
@staticmethod
def _visible(canvas, top, bottom):
    """判断完整屏幕纵向区间是否与当前画布相交。"""
    return top < canvas.origin_y + canvas.height and bottom > canvas.origin_y
```

调用：

```python
if self._visible(canvas, 112, 188):
    self._draw_history(canvas, values)
```

## 选择接口的小原则

能用一个高级接口完成时，就不要在 Python 中循环数百次调用 `pixel()`。基础接口适合简单元素；图表、多边形和大量线条优先使用批量接口。
