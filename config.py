"""
MUD 助手配置文件
"""

import json
import os

# ===== 服务器配置 =====
MUD_HOST = "mud.pkuxkx.net"
MUD_PORT = 5555

# ===== 代理配置 =====
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 6666

# ===== 日志配置 =====
LOG_DIR = "logs"
LOG_ENCODING = "utf-8"

# ===== 命令分类规则 =====
# key = 分类名, value = 匹配命令关键字的列表
CMD_CATEGORIES = {
    "移动": ["n", "s", "e", "w", "nu", "su", "eu", "wu", "nd", "sd", "ed", "wd",
             "u", "d", "north", "south", "east", "west", "up", "down",
             "enter", "out", "go", "climb", "swim", "jump"],
    "战斗": ["kill", "k", "fight", "f", "hit", "attack", "flee", "surrender"],
    "物品": ["get", "drop", "give", "buy", "sell", "wear", "wield", "unwield",
             "remove", "put", "eat", "drink", "open", "close", "lock", "unlock"],
    "技能": ["exercise", "exert", "enable", "study", "learn", "practice",
             "perform", "conjure", "cast", "invoke"],
    "沟通": ["say", "tell", "chat", "shout", "whisper", "reply", "ask", "yell"],
    "查询": ["look", "l", "hp", "score", "skills", "inventory", "i", "id",
             "where", "who", "finger", "describe"],
    "系统": ["set", "unset", "alias", "unalias", "save", "quit", "recall",
             "brief", "hibernate", "suicide"],
}

# ===== 区域配置 =====
# 从 areas.json 加载，构建 房间名 -> (区域代码, 区域名) 反向索引
AREA_MAP = {}       # code -> {"name": ..., "rooms": [...]}
ROOM_TO_AREA = {}   # 房间名 -> (code, area_name)


def load_areas():
    """加载区域配置，构建房间名反向索引"""
    global AREA_MAP, ROOM_TO_AREA
    path = os.path.join(os.path.dirname(__file__), 'areas.json')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        AREA_MAP = json.load(f)
    ROOM_TO_AREA = {}
    for code, info in AREA_MAP.items():
        for room in info.get('rooms', []):
            ROOM_TO_AREA[room] = (code, info['name'])


load_areas()
