#!/usr/bin/env python3
"""读取 .bin 原始字节日志的工具。

日志格式：
    每条消息一行，以 \\n 结尾。
    [HH:MM:SS.mmm] >>> 原始字节\\n    (客户端→服务器)
    [HH:MM:SS.mmm] <<< 原始字节\\n    (服务器→客户端)

用法（CLI）：
    python tools/read_raw_log.py [选项] [日志文件]

    选项：
      --from TIME       起始时间 (HH:MM:SS)
      --to TIME         结束时间 (HH:MM:SS)
      --dir DIR         方向过滤: send / recv / all (默认 all)
      --mode MODE       输出模式: text / hex / mixed (默认 text)
      --limit N         最多输出 N 条 (默认无限制)

    示例：
      python tools/read_raw_log.py logs/2026-06-12_raw.bin
      python tools/read_raw_log.py --from 10:12:00 --to 10:13:00 --mode hex logs/2026-06-12_raw.bin
      python tools/read_raw_log.py --dir send --limit 20 logs/2026-06-12_raw.bin

用法（作为模块被 AI 调用）：
    from read_raw_log import parse_raw_log, format_entry

    entries = parse_raw_log('logs/2026-06-12_raw.bin',
                            time_from='10:12:00', time_to='10:13:00',
                            direction='recv', limit=50)
    for e in entries:
        print(format_entry(e, mode='text'))
"""

import re
import sys
import argparse
from datetime import datetime
from dataclasses import dataclass


# 行首时间戳+方向匹配
_LINE_RE = re.compile(
    rb'\[(\d{2}:\d{2}:\d{2}\.\d+)\] (>>>|<<<) '
)


@dataclass
class RawEntry:
    """一条原始日志记录"""
    timestamp: str       # "HH:MM:SS.mmm"
    direction: str       # "send" 或 "recv"
    raw_bytes: bytes     # 原始负载数据（不含时间戳和方向标记）


def parse_raw_log(path, time_from=None, time_to=None, direction='all', limit=0):
    """解析 .bin 日志文件，返回 RawEntry 列表。

    参数:
        path:       日志文件路径
        time_from:  起始时间 "HH:MM:SS"（可选）
        time_to:    结束时间 "HH:MM:SS"（可选）
        direction:  "send" / "recv" / "all"
        limit:      最大条数，0 表示不限

    返回:
        list[RawEntry]
    """
    entries = []

    def _time_key(ts_str):
        # "HH:MM:SS.mmm" → 可比较的字符串
        return ts_str[:8]

    from_key = _time_key(time_from) if time_from else None
    to_key = _time_key(time_to) if time_to else None

    with open(path, 'rb') as f:
        buf = f.read()

    i = 0
    length = len(buf)
    while i < length:
        m = _LINE_RE.match(buf, i)
        if not m:
            i += 1
            continue

        ts_raw = m.group(1).decode('ascii')   # "HH:MM:SS.mmm"
        marker = m.group(2)                    # b">>>" or b"<<<"
        data_start = m.end()

        # 找下一条消息的开头（下一个时间戳行首），或者文件末尾
        next_m = _LINE_RE.search(buf, data_start)
        if next_m:
            data_end = next_m.start()
        else:
            data_end = length

        # 原始数据 = 标记之后到下一条之前，去掉末尾的 \n
        raw = buf[data_start:data_end]
        if raw.endswith(b'\n'):
            raw = raw[:-1]

        # 时间过滤
        ts_key = _time_key(ts_raw)
        if from_key and ts_key < from_key:
            i = data_end
            continue
        if to_key and ts_key > to_key:
            break

        # 方向过滤
        dir_str = 'send' if marker == b'>>>' else 'recv'
        if direction != 'all' and dir_str != direction:
            i = data_end
            continue

        entries.append(RawEntry(
            timestamp=ts_raw,
            direction=dir_str,
            raw_bytes=raw,
        ))

        if limit and len(entries) >= limit:
            break

        i = data_end

    return entries


def format_entry(entry, mode='text'):
    """将 RawEntry 格式化为可读字符串。

    参数:
        entry: RawEntry 实例
        mode:  "text"  → GBK 解码 + ANSI strip
               "hex"   → 十六进制 dump
               "mixed" → GBK 解码，不可解码部分显示为 hex
    """
    marker = '>>>' if entry.direction == 'send' else '<<<'
    prefix = f'[{entry.timestamp}] {marker} '

    if mode == 'hex':
        hex_str = entry.raw_bytes.hex(' ')
        return f'{prefix}({len(entry.raw_bytes)}B) {hex_str}'

    if mode == 'mixed':
        text = _decode_mixed(entry.raw_bytes)
        return f'{prefix}{text}'

    # mode == 'text'
    text = _decode_text(entry.raw_bytes)
    return f'{prefix}{text}'


def _decode_text(data):
    """GBK 解码，去除不可打印控制字符（保留 ANSI），替换解码失败字符。"""
    try:
        text = data.decode('gbk', errors='replace')
    except Exception:
        text = data.decode('utf-8', errors='replace')
    return text


def _decode_mixed(data):
    """GBK 解码，对解码失败的字节显示为 \\xHH 形式。"""
    result = []
    i = 0
    while i < len(data):
        # 尝试 GBK 双字节解码
        if i + 1 < len(data):
            try:
                ch = data[i:i+2].decode('gbk')
                result.append(ch)
                i += 2
                continue
            except (UnicodeDecodeError, ValueError):
                pass
        # 单字节
        b = data[i]
        if 0x20 <= b < 0x7f or b in (0x0d, 0x0a, 0x1b, 0x09):
            result.append(chr(b))
        else:
            result.append(f'\\x{b:02x}')
        i += 1
    return ''.join(result)


def main():
    parser = argparse.ArgumentParser(
        description='读取 .bin 原始字节日志'
    )
    parser.add_argument('file', help='日志文件路径')
    parser.add_argument('--from', dest='time_from', help='起始时间 HH:MM:SS')
    parser.add_argument('--to', dest='time_to', help='结束时间 HH:MM:SS')
    parser.add_argument('--dir', dest='direction', default='all',
                        choices=['send', 'recv', 'all'], help='方向过滤')
    parser.add_argument('--mode', default='text',
                        choices=['text', 'hex', 'mixed'], help='输出模式')
    parser.add_argument('--limit', type=int, default=0, help='最大条数')
    args = parser.parse_args()

    entries = parse_raw_log(
        args.file,
        time_from=args.time_from,
        time_to=args.time_to,
        direction=args.direction,
        limit=args.limit,
    )

    for entry in entries:
        print(format_entry(entry, mode=args.mode))

    print(f'\n共 {len(entries)} 条记录')


if __name__ == '__main__':
    main()
