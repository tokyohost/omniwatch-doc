# Linux 一键安装

本文提供 Pico Monitor 在常见 Linux 发行版上的一键安装命令。安装脚本来自 GitHub `master` 分支的 Raw URL，会自动识别当前系统使用的包管理器、安装运行依赖，并注册 `pico-monitor.service`。

> 安装过程需要写入 `/opt`、`/usr/local/bin` 和 `/etc`，请使用具有 `sudo` 权限的账号执行。生产环境建议先查看 [`install-linux.sh`](install-linux.sh) 内容，再运行远程脚本。

## Debian、Ubuntu、Linux Mint、Raspberry Pi OS

```sh
sudo apt-get update && sudo apt-get install -y curl && curl -fsSL https://raw.githubusercontent.com/tokyohost/pico-vision/master/monitor/install-linux.sh | sudo sh
```

## Fedora

```sh
sudo dnf install -y curl && curl -fsSL https://raw.githubusercontent.com/tokyohost/pico-vision/master/monitor/install-linux.sh | sudo sh
```

## RHEL、Rocky Linux、AlmaLinux

```sh
sudo dnf install -y curl && curl -fsSL https://raw.githubusercontent.com/tokyohost/pico-vision/master/monitor/install-linux.sh | sudo sh
```

## openSUSE Leap、Tumbleweed

```sh
sudo zypper --non-interactive install curl && curl -fsSL https://raw.githubusercontent.com/tokyohost/pico-vision/master/monitor/install-linux.sh | sudo sh
```

## Arch Linux、Manjaro

```sh
sudo pacman -Syu --needed --noconfirm curl && curl -fsSL https://raw.githubusercontent.com/tokyohost/pico-vision/master/monitor/install-linux.sh | sudo sh
```

## 使用 wget 安装

系统未安装 `curl`、但已安装 `wget` 时，可以执行：

```sh
wget -qO- https://raw.githubusercontent.com/tokyohost/pico-vision/master/monitor/install-linux.sh | sudo sh
```

## 安装验证

安装完成后执行：

```sh
pico-monitor --version
sudo systemctl status pico-monitor
```

实时查看运行日志：

```sh
sudo journalctl -u pico-monitor -f
```

配置文件位于 `/etc/pico-monitor.conf`。修改配置后执行以下命令使配置生效：

```sh
sudo systemctl restart pico-monitor
```

如果当前系统不使用 systemd，安装脚本只部署程序文件，不会注册开机服务。此时可以手动启动：

```sh
sudo pico-monitor --config /etc/pico-monitor.conf
```
