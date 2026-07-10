#!/usr/bin/env python3
"""把中文文本转换为 OmniWatch 自定义样式可使用的点阵字模。"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _load_font(font_path, size):
    """按指定字号加载字体文件。"""
    return ImageFont.truetype(str(font_path), size=size)


def _measure_char(font, char):
    """计算单个字符的实际绘制区域。"""
    left, top, right, bottom = font.getbbox(char)
    width = max(1, right - left)
    height = max(1, bottom - top)
    return left, top, width, height


def _render_char(font, char, threshold):
    """把单个字符渲染为由 0 和 1 组成的点阵行。"""
    left, top, width, height = _measure_char(font, char)
    image = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(image)
    draw.text((-left, -top), char, fill=255, font=font)
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(1 if image.getpixel((x, y)) >= threshold else 0)
        rows.append(row)
    return {
        "width": width,
        "height": height,
        "rows": rows,
    }


def _render_char_hex(font, char, threshold, box_size):
    """把单个字符渲染为固定尺寸的十六进制点阵行。"""
    left, top, width, height = _measure_char(font, char)
    image = Image.new("L", (box_size, box_size), 0)
    draw = ImageDraw.Draw(image)
    x = (box_size - width) // 2 - left
    y = (box_size - height) // 2 - top
    draw.text((x, y), char, fill=255, font=font)
    rows = []
    for row_index in range(box_size):
        row_bits = 0
        for col_index in range(box_size):
            if image.getpixel((col_index, row_index)) >= threshold:
                row_bits |= 1 << (box_size - 1 - col_index)
        rows.append("{:0{}x}".format(row_bits, max(1, (box_size + 3) // 4)))
    return tuple(rows)


def _unique_chars(text):
    """按首次出现顺序提取文本中的唯一字符。"""
    chars = []
    for char in text:
        if char not in chars and char not in ("\r", "\n", "\t"):
            chars.append(char)
    return chars


def _to_python_dict(name, glyphs):
    """把字模数据格式化为 Python 常量。"""
    lines = [name + " = {"]
    for char, glyph in glyphs.items():
        lines.append("    " + repr(char) + ": {")
        lines.append('        "width": ' + str(glyph["width"]) + ",")
        lines.append('        "height": ' + str(glyph["height"]) + ",")
        lines.append('        "rows": (')
        for row in glyph["rows"]:
            lines.append("            " + repr(tuple(row)) + ",")
        lines.append("        ),")
        lines.append("    },")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _to_python_hex_dict(name, glyphs):
    """把紧凑十六进制字模数据格式化为 Python 常量。"""
    lines = [name + " = {"]
    for char, rows in glyphs.items():
        lines.append("    " + repr(char) + ": " + repr(tuple(rows)) + ",")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _to_json(glyphs):
    """把字模数据格式化为 JSON 文本。"""
    return json.dumps(glyphs, ensure_ascii=False, indent=2)


def _print_preview(glyphs):
    """在终端中打印点阵预览，便于检查字形是否清楚。"""
    for char, glyph in glyphs.items():
        if isinstance(glyph, tuple):
            width = max(1, len(glyph[0]) * 4)
            print("字符：" + char + "  尺寸：" + str(width) + "x" + str(len(glyph)))
            for row in glyph:
                row_bits = int(row, 16)
                print("".join("##" if row_bits & (1 << (width - 1 - index)) else "  " for index in range(width)))
        else:
            print("字符：" + char + "  尺寸：" + str(glyph["width"]) + "x" + str(glyph["height"]))
            for row in glyph["rows"]:
                print("".join("##" if item else "  " for item in row))
        print()


def build_arg_parser():
    """创建命令行参数解析器。"""
    parser = argparse.ArgumentParser(description="把中文文本转换为 OmniWatch 点阵字模")
    parser.add_argument("text", help="需要转换的中文文本，例如：上海多云湿度风速更新时间")
    parser.add_argument("--font", required=True, help="字体文件路径，例如 C:/Windows/Fonts/msyh.ttc")
    parser.add_argument("--size", type=int, default=16, help="字号，默认 16")
    parser.add_argument("--box-size", type=int, default=16, help="固定点阵盒尺寸，默认 16")
    parser.add_argument("--threshold", type=int, default=96, help="像素阈值，默认 96")
    parser.add_argument("--name", default="FONT_16", help="输出的 Python 常量名，默认 FONT_16")
    parser.add_argument("--format", choices=("python", "python-hex", "json"), default="python-hex", help="输出格式")
    parser.add_argument("--output", help="输出文件路径，不填则打印到终端")
    parser.add_argument("--preview", action="store_true", help="同时打印点阵预览")
    return parser


def main():
    """读取参数、生成字模并输出结果。"""
    parser = build_arg_parser()
    args = parser.parse_args()
    font = _load_font(Path(args.font), args.size)
    glyphs = {}
    for char in _unique_chars(args.text):
        if args.format == "python-hex":
            glyphs[char] = _render_char_hex(font, char, args.threshold, args.box_size)
        else:
            glyphs[char] = _render_char(font, char, args.threshold)

    if args.preview:
        _print_preview(glyphs)

    if args.format == "json":
        content = _to_json(glyphs) + "\n"
    elif args.format == "python-hex":
        content = _to_python_hex_dict(args.name, glyphs)
    else:
        content = _to_python_dict(args.name, glyphs)

    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
