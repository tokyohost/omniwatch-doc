# Linux HTTP 管理页面

Pico Monitor 在 Linux 上默认启用无桌面的 HTTP 管理页面，适合服务器、迷你主机和 NAS 使用。默认监听地址为 `0.0.0.0:9876`，初始 Auth 为 `omni-watch-123456789`。

> 初始 Auth 是公开的默认值。首次登录后请立即在 `/etc/pico-monitor.conf` 中替换为高强度随机密钥，并重启服务。

## 当前支持范围

当前 Linux HTTP 后端支持：

- 查看应用名称、Monitor 版本和基础配置；
- 查看设备是否连接、当前端口和传输类型；
- 通过健康检查接口确认 HTTP 服务是否正常。

当前 Linux HTTP 后端暂不支持修改配置、扫描或连接 Wi-Fi、管理 WebSocket 客户端、上传样式和选择服务器本地文件。页面调用未开放的功能时，会返回“Linux HTTP 管理页面暂不支持此操作”。设备 Wi-Fi 配置请参阅 [`linux-wifi-config.md`](linux-wifi-config.md)。

## 默认配置

编辑 Linux 服务配置：

```sh
sudo nano /etc/pico-monitor.conf
```

默认安装生成的 `http` 配置如下：

```yaml
http:
  enabled: true
  host: 0.0.0.0
  port: 9876
  auth: "omni-watch-123456789"
```

各配置项含义：

| 配置项 | 说明 |
|---|---|
| `enabled` | 是否启用 HTTP 管理页面。 |
| `host` | 监听地址；`0.0.0.0` 允许局域网访问，`127.0.0.1` 仅允许本机访问。 |
| `port` | 首选监听端口，默认为 `9876`。 |
| `auth` | 浏览器和接口请求使用的鉴权密钥；初始值为 `omni-watch-123456789`。 |

可以使用 OpenSSL 生成随机 Auth：

```sh
openssl rand -base64 32
```

首次登录后，将输出内容复制到 `auth`，并保留 YAML 双引号，然后重启服务。不要把真实 Auth 提交到 Git 仓库、截图或公开日志中。

## 重启并检查服务

应用配置：

```sh
sudo systemctl restart pico-monitor
sudo systemctl status pico-monitor
```

查看启动日志：

```sh
sudo journalctl -u pico-monitor -n 50 --no-pager
```

正常情况下会看到类似日志：

```text
HTTP 管理页面已启动：http://0.0.0.0:9876，Auth=******
```

如果配置的端口已被占用，程序会从该端口开始自动寻找可用端口。请以启动日志中记录的实际端口为准。

当配置中的 `auth` 为空时，程序会在每次启动时生成新的随机 Auth，并将明文 Auth 写入启动日志。为保证地址稳定且减少密钥暴露，长期运行时建议显式配置 Auth。

## 浏览器访问

仅在 Linux 主机本机访问：

```text
http://127.0.0.1:9876/
```

从同一局域网的其他电脑访问：

```text
http://Linux主机IP:9876/
```

页面首次建立连接时会提示输入 Auth。首次安装可输入 `omni-watch-123456789`，登录后应立即更换该默认值。验证成功后，Auth 会保存在当前浏览器的本地存储中；修改 Auth 后，可清除该站点的浏览器存储并重新输入。

## 健康检查

健康检查接口不要求 Auth：

```sh
curl -fsS http://127.0.0.1:9876/api/health
```

正常响应：

```json
{"ok": true, "service": "omniwatch-http"}
```

查看页面运行参数：

```sh
curl -fsS http://127.0.0.1:9876/api/runtime
```

## HTTP 接口调用示例

管理页面主要通过 WebSocket 调用后端，同时也提供 `POST /api/invoke`。以下示例读取设备连接状态：

```sh
read -rsp "HTTP Auth: " OMNIWATCH_HTTP_AUTH; printf '\n'
curl -fsS \
  -H "Authorization: Bearer ${OMNIWATCH_HTTP_AUTH}" \
  -H "Content-Type: application/json" \
  -d '{"action":"device.status","payload":{}}' \
  http://127.0.0.1:9876/api/invoke
unset OMNIWATCH_HTTP_AUTH
```

读取应用首屏信息：

```sh
read -rsp "HTTP Auth: " OMNIWATCH_HTTP_AUTH; printf '\n'
curl -fsS \
  -H "Authorization: Bearer ${OMNIWATCH_HTTP_AUTH}" \
  -H "Content-Type: application/json" \
  -d '{"action":"app.bootstrap","payload":{}}' \
  http://127.0.0.1:9876/api/invoke
unset OMNIWATCH_HTTP_AUTH
```

使用 `read -s` 可以避免 Auth 显示在终端和 Shell 历史中。

## 配置防火墙

仅在确实需要局域网访问时开放端口，并尽量限制可信网段。

使用 UFW 的系统可以执行：

```sh
sudo ufw allow from 192.168.1.0/24 to any port 9876 proto tcp
```

使用 firewalld 的系统可以执行：

```sh
sudo firewall-cmd --permanent --zone=public --add-port=9876/tcp
sudo firewall-cmd --reload
```

firewalld 的端口规则会允许该区域内的来源访问。如果需要限制来源，请改用符合本机网络策略的 rich rule。

## 安全建议

- 只在本机管理时，将 `host` 设置为 `127.0.0.1`。
- 不要长期使用默认 Auth `omni-watch-123456789`。
- 局域网访问时使用高强度随机 Auth，并通过防火墙限制来源。
- HTTP 本身不加密，不要直接暴露到公网。
- 需要跨互联网管理时，应通过 VPN 或带 HTTPS 的反向代理访问。
- 不要在命令参数、Shell 历史、截图或工单中泄露 Auth。

## 常见问题

### 浏览器无法访问

检查监听地址和实际端口：

```sh
sudo journalctl -u pico-monitor -n 100 --no-pager
sudo ss -lntp | grep pico-monitor
```

如果 `host` 为 `127.0.0.1`，其他电脑无法直接访问，这是预期行为。

### 页面提示鉴权失败

确认输入的是 `/etc/pico-monitor.conf` 中的 `http.auth`；首次安装的默认值是 `omni-watch-123456789`。如果该值为空，请从本次服务启动日志中获取随机 Auth。修改配置后必须重启服务。

### 页面为空或静态资源返回 404

确认使用正式 DEB 或通用 Linux 发布包安装。源码运行时必须先构建 `monitor/win/ui-web/dist`，否则 HTTP 服务无法提供 Vue 页面。

### 端口不是 9876

端口被占用时，Pico Monitor 会自动选择后续可用端口。通过服务日志确认实际地址；若防火墙只开放了 `9876`，应先释放该端口再重启服务。
