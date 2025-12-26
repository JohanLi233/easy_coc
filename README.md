# Easy COC DNS

将 `game.clashofclans.com` 映射到 `sqbwiki.com` 的简单 DNS 服务器，用于玩 COC 国际服。

## 使用方法

### 1. 启动服务器

```bash
sudo python3 dns_server.py
```

服务器会在 `0.0.0.0:53` 监听。

### 2. 手机配置 DNS

1. 查看本机 IP：
   ```bash
   ipconfig getifaddr en0
   ```
2. 手机连接同一 WiFi，修改网络设置：
   - DNS 服务器设置为你的电脑 IP（如 `192.168.1.13`）

### 3. 测试

访问 `game.clashofclans.com`，会被解析到 `124.223.85.31`（sqbwiki.com 的 IP）。

## IP 变更

如果 sqbwiki.com 的 IP 变化了，编辑 `dns_server.py` 第 17 行：

```python
TARGET_IP = "新IP"
```

## 获取 sqbwiki.com 当前 IP

```bash
nslookup sqbwiki.com
# 或
dig +short sqbwiki.com
```
