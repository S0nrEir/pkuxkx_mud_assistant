"""
MUD 命令日志 skill
读取代理记录的原始日志，提取玩家发送的命令，按分类写入 MD 文档
用法: python skill_cmdlog.py [日期]
"""

import re
import os
from datetime import datetime
from collections import defaultdict

import config


def parse_raw_log(filepath):
    """解析原始日志，提取玩家发送的命令"""
    entries = []
    if not os.path.exists(filepath):
        return entries

    with open(filepath, "r", encoding=config.LOG_ENCODING, errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 只取玩家发送的命令: [HH:MM:SS] >>> content
            match = re.match(r"\[(\d{2}:\d{2}:\d{2})\]\s*>>>\s*(.*)", line)
            if match:
                entries.append({
                    "time": match.group(1),
                    "content": match.group(2),
                })
    return entries


def classify_cmd(cmd_text):
    """根据命令的第一个词分类"""
    cmd_text = cmd_text.strip()
    if not cmd_text:
        return None, None

    first_word = cmd_text.split()[0].lower()

    # 跳过纯数字重复（zMUD 的 #3 {cmd} 语法，不算独立命令）
    if first_word.startswith("#"):
        return None, None

    for category, keywords in config.CMD_CATEGORIES.items():
        if first_word in keywords:
            return category, first_word

    return "其他", first_word


def build_cmdlog(date_str=None):
    """构建命令日志 MD 文件"""
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    log_dir = os.path.join(os.path.dirname(__file__), config.LOG_DIR)
    raw_file = os.path.join(log_dir, f"{date_str}_raw.log")
    entries = parse_raw_log(raw_file)

    if not entries:
        print(f"[命令日志] {date_str} 没有日志数据，请先启动代理并游戏")
        return

    # 分类收集: { category: { cmd: [完整命令行列表] } }
    classified = defaultdict(lambda: defaultdict(list))
    cmd_count = defaultdict(int)

    for entry in entries:
        cat, cmd = classify_cmd(entry["content"])
        if cat is None:
            continue
        # 去重：同一分类下相同的完整命令只记录一次（保留时间信息）
        full_cmd = entry["content"].strip()
        if full_cmd not in classified[cat][cmd]:
            classified[cat][cmd].append(f"`[{entry['time']}]` `{full_cmd}`")
        cmd_count[cmd] += 1

    # 生成 MD
    md = f"# MUD 命令日志 - {date_str}\n\n"
    md += f"共发送 {len(entries)} 条命令\n\n"

    # 分类展示
    for cat in ["移动", "战斗", "物品", "技能", "沟通", "查询", "系统", "其他"]:
        cmds = classified.get(cat)
        if not cmds:
            continue
        md += f"## {cat}\n\n"
        # 按使用次数排序
        for cmd, examples in sorted(cmds.items(), key=lambda x: -cmd_count[x[0]]):
            md += f"### `{cmd}` (使用 {cmd_count[cmd]} 次)\n\n"
            for ex in examples[:5]:
                md += f"- {ex}\n"
            if len(examples) > 5:
                md += f"- ... 还有 {len(examples) - 5} 条\n"
            md += "\n"

    # 写入文件
    output_dir = os.path.join(os.path.dirname(__file__), "cmdlog")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{date_str}_commands.md")
    with open(output_path, "w", encoding=config.LOG_ENCODING) as f:
        f.write(md)

    print(f"[命令日志] 已保存到 {output_path}")
    return output_path


if __name__ == "__main__":
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else None
    build_cmdlog(date)
