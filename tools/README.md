# tools/ - 原始日志工具

## 原始字节日志格式

文件：`logs/YYYY-MM-DD_raw.bin`

每条消息一行，格式：

```
[HH:MM:SS.mmm] >>> 客户端发送的原始字节\n
[HH:MM:SS.mmm] <<< 服务器返回的原始字节\n
```

- `>>>` 客户端→服务器（GBK 编码，含所有控制字符）
- `<<<` 服务器→客户端（GBK 编码，含 Telnet IAC、ANSI 转义、MXP 标签等）
- 时间戳精确到毫秒
- **完全未经任何处理**：未剥离 Telnet IAC、未解码、未去除 ANSI
- 原始数据本身可能含 `\n`，解析时需按时间戳行首 `[\\d{2}:\\d{2}:\\d{2}` 分割

与 `logs/YYYY-MM-DD_raw.log`（UTF-8 文本日志，经 GBK 解码和行分割处理）互补。

## read_raw_log.py

读取和解析 `.bin` 原始日志的工具。

### CLI 用法

```bash
# 查看全部（GBK 解码文本）
python tools/read_raw_log.py logs/2026-06-12_raw.bin

# 按时间范围过滤
python tools/read_raw_log.py --from 10:12:00 --to 10:13:00 logs/2026-06-12_raw.bin

# 只看服务器→客户端
python tools/read_raw_log.py --dir recv logs/2026-06-12_raw.bin

# 十六进制模式（查看 Telnet IAC 等二进制内容）
python tools/read_raw_log.py --mode hex logs/2026-06-12_raw.bin

# 混合模式（GBK 解码，不可解码部分显示为 \xHH）
python tools/read_raw_log.py --mode mixed logs/2026-06-12_raw.bin

# 限制条数
python tools/read_raw_log.py --limit 20 logs/2026-06-12_raw.bin
```

### 作为模块调用（供 AI / 脚本使用）

```python
from read_raw_log import parse_raw_log, format_entry

entries = parse_raw_log('logs/2026-06-12_raw.bin',
                        time_from='10:12:00',
                        time_to='10:13:00',
                        direction='recv',
                        limit=50)

for entry in entries:
    # entry.timestamp: "HH:MM:SS.mmm"
    # entry.direction: "send" 或 "recv"
    # entry.raw_bytes: bytes 原始负载
    print(format_entry(entry, mode='text'))
```

### 输出模式

| 模式 | 说明 |
|------|------|
| `text` | GBK 解码为可读文本（默认） |
| `hex` | 十六进制 dump，适合查看二进制协议（Telnet IAC 等） |
| `mixed` | GBK 解码，不可解码字节显示为 `\xHH` |
