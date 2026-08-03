# 纯样式插件示例

这是一个只有屏幕样式、没有数据采集入口的 `type: "style"` 市场资源。

目录内容：

- `plugin.json`：声明市场类型、版本、样式文件和 HTML 详情。
- `style_only_clock.py`：实际上传到设备的屏幕样式。
- `style_only_clock_detail.html`：市场详情页，可按需删除并同步移除清单中的绑定字段。

发布时把这三个文件直接压缩到同一个 ZIP 根目录。纯样式包不应包含 `entry`、`main.py`、`interval` 或自定义数据配置。
