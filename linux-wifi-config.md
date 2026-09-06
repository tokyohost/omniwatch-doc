# Linux 命令行配置设备 Wi-Fi

本文说明如何在没有桌面环境的 Linux 主机上，通过 Pico Monitor 命令行控制通道为设备配置 Wi-Fi。

## Linux HTTP 管理页面说明

Linux 版本确实内置了 HTTP 管理页面，并在默认安装配置中启用。默认监听端口为 `9876`，初始 Auth 为 `omni-watch-123456789`。`/etc/pico-monitor.conf` 中的默认配置如下：

```yaml
http:
  enabled: true
  host: 0.0.0.0
  port: 9876
  auth: "omni-watch-123456789"
```

修改后重启服务：

```sh
sudo systemctl restart pico-monitor
sudo journalctl -u pico-monitor -n 50 --no-pager
```

然后使用浏览器访问 `http://Linux主机IP:9876/`，首次访问时输入 `omni-watch-123456789`。该初始 Auth 是公开默认值，首次登录后应立即替换为高强度随机密钥；如果 `auth` 留空，程序会在每次启动时随机生成 Auth，并将它写入启动日志。

当前版本的 Linux HTTP 后端只支持读取应用信息和设备连接状态，尚未开放 `wifi.list`、`wifi.connect` 和 `wifi.forget`。因此页面虽然包含 Wi-Fi 界面，但点击扫描、连接或忘记网络时会返回“Linux HTTP 管理页面暂不支持此操作”。设备配网仍需使用本文后续的命令行控制方式。

> 将 `host` 配置为 `0.0.0.0` 会向局域网开放管理页面。请设置高强度 Auth，并通过主机防火墙限制访问来源；仅在本机使用时建议配置为 `127.0.0.1`。

## 使用条件

- 设备固件必须支持 Wi-Fi，例如启用了 Wi-Fi 的 ESP32-S3 固件。
- 首次配网必须通过 USB CDC 连接设备。
- Linux 主机已经安装 Pico Monitor，并能执行 `pico-monitor --version`。
- 当前账号具有 `sudo` 权限。

RP2040 本身不具备 Wi-Fi 功能。设备未在握手信息中声明支持 Wi-Fi 时，配网命令会失败。

## 1. 确认 USB 设备

连接设备后查看串口：

```sh
ls -l /dev/serial/by-id/ 2>/dev/null
ls -l /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
```

通常无需固定串口，Pico Monitor 会通过 PV1 握手自动识别正确的 USB CDC 数据接口。如果自动识别失败，可在后续命令中添加 `--port /dev/ttyACM1`，并替换为实际设备路径。

## 2. 停止后台服务

systemd 服务可能正在占用串口。进入交互配网前先停止服务：

```sh
sudo systemctl stop pico-monitor
```

## 3. 启动命令行配网会话

执行：

```sh
sudo pico-monitor --config /etc/pico-monitor.conf --worker --force-usb-cdc
```

需要固定串口时执行：

```sh
sudo pico-monitor --config /etc/pico-monitor.conf --worker --force-usb-cdc --port /dev/ttyACM1
```

等待终端显示 `Pico LCD 已连接` 后，在同一终端中输入下面的控制命令。每条命令输入完成后按 Enter。

## 4. 扫描附近 Wi-Fi

输入：

```text
WIFI_LIST
```

成功时会输出一行以 `WIFI_RESULT:` 开头的 JSON，例如：

```text
WIFI_RESULT:{"status":"ok","action":"list","data":{"networks":[{"ssid":"Home-WiFi","rssi":-45,"security":"WPA2"}]}}
```

设备扫描无线网络可能需要数秒，请等待结果返回后再输入下一条命令。

## 5. 连接 Wi-Fi

输入以下命令，并替换 Wi-Fi 名称和密码：

```text
WIFI_CONNECT:{"ssid":"Home-WiFi","password":"your-password"}
```

连接开放网络时，密码使用空字符串：

```text
WIFI_CONNECT:{"ssid":"Guest-WiFi","password":""}
```

成功结果中的 `data` 会包含设备当前 Wi-Fi 状态和 IP 地址，例如：

```text
WIFI_RESULT:{"status":"ok","action":"connect","data":{"wifi":{"ssid":"Home-WiFi","ip":"192.168.1.50"}}}
```

请记录返回的 IP 地址。Wi-Fi 名称或密码包含双引号、反斜杠等特殊字符时，必须按照 JSON 字符串规则转义。

> 密码会显示在当前终端输入区域，但不会出现在 Shell 命令历史中，Monitor 的结果和日志也不会回显密码。请避免在录屏、共享终端或不可信会话中操作。

## 6. 忘记已保存的 Wi-Fi

需要删除设备中保存的网络时，在 USB 配网会话中输入：

```text
WIFI_FORGET:{"ssid":"Home-WiFi"}
```

成功时会输出：

```text
WIFI_RESULT:{"status":"ok","action":"forget","data":{"forgotten":"Home-WiFi"}}
```

## 7. 退出配网并启用 Wi-Fi 连接

配网成功后按 `Ctrl+C` 结束交互进程，然后编辑配置：

```sh
sudo nano /etc/pico-monitor.conf
```

如果希望固定连接刚才返回的设备 IP，在 `network` 节点中增加或修改：

```yaml
network:
  websocket_url: ws://192.168.1.50:8765/pv1
  force_usb_cdc: false
```

如果设备使用 DHCP，IP 地址可能变化。此时可将 `websocket_url` 留空，使用默认的 UDP 公告和局域网扫描自动发现：

```yaml
network:
  websocket_url: ""
  force_usb_cdc: false
  discovery_strategy: announcement
```

重新启动服务：

```sh
sudo systemctl start pico-monitor
sudo systemctl status pico-monitor
```

查看连接日志：

```sh
sudo journalctl -u pico-monitor -f
```

日志中出现 `WebSocket 连接` 和设备地址，表示 Wi-Fi 通信已经建立。设备仍通过同一根 USB 线连接主机时，USB 通信具有更高优先级；需要验证纯 Wi-Fi 模式时，应断开 USB 数据连接，并通过其他方式为设备供电。

## 常见问题

### 没有发现串口

确认设备和 USB 线支持数据传输，并检查内核日志：

```sh
sudo dmesg --follow
```

重新插入设备后，观察是否出现 `ttyACM` 或 `ttyUSB`。

### 返回 `Wi-Fi 名称不能为空` 或 JSON 错误

确认 `WIFI_CONNECT:` 或 `WIFI_FORGET:` 后面紧跟合法 JSON，属性名和字符串必须使用英文双引号。

### Wi-Fi 连接超时

确认 SSID、密码和信号强度正确。设备支持的频段取决于硬件；常见 ESP32-S3 设备只能连接 2.4 GHz Wi-Fi。

### 配网后服务仍使用 USB

USB 是优先传输方式。确认配置中的 `force_usb_cdc` 为 `false`，结束配网进程后断开 USB 数据连接，再启动 systemd 服务。
