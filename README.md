# MUD Assistant（北大侠客行助手）

面向 [北大侠客行](https://pkuxkx.net) MUD 的本地辅助工具集，默认连接 `mud.pkuxkx.net:5555`。

当前项目主要包含：

- Web 浏览器客户端：终端、聊天、地图、命令历史、触发器管理。
- Telnet 代理：兼容 zMUD 等传统客户端，并记录通信日志。
- 命令统计：从日志中提取玩家命令并生成分类报告。
- Wiki 离线工具：爬取、清理北大侠客行 Wiki 内容。

## 快速开始

### 环境要求

- Python 3.7+
- 依赖：`starlette`、`uvicorn`

```bash
pip install starlette uvicorn
```

### 启动 Web 客户端（推荐）

```bash
python start.py web
```

启动后访问：

```text
http://127.0.0.1:58080
```

Windows 可以双击：

```text
启动Web客户端_windows.bat
```

macOS 可以运行：

```bash
./启动Web客户端_mac.sh
```

### 启动 Telnet 代理

```bash
python start.py proxy
```

然后在 zMUD 或其他 Telnet 客户端中连接：

```text
127.0.0.1:6666
```

代理会转发到：

```text
mud.pkuxkx.net:5555
```

### 生成命令统计

```bash
python start.py cmdlog
python start.py cmdlog 2026-06-10
```

输出文件位于：

```text
cmdlog/YYYY-MM-DD_commands.md
```

## Web 客户端

Web 后端入口是 `web_mud.py`，前端模板是 `templates/web_mud.html`。

### 游戏页

- 基于 xterm.js 的 MUD 终端。
- 支持 ANSI 颜色显示。
- 支持 MXP 标签解析和交互元素。
- 右侧显示命令历史和聊天频道。
- 左侧显示频道屏蔽设置和地图面板。
- 支持屏蔽闲聊、谣言、交易、QQ群、帮派、组队、大喊等频道。
- 支持断线重连。
- 支持多浏览器标签页登录不同角色。

### 触发器页

顶部页签中点击“触发器”即可切换到触发器管理页面。

- 左侧显示当前加载的触发器、当前选中触发器详情、功能按钮和编辑表单。
- 右侧显示所有触发器列表，触发器较多时可滚动浏览。
- 支持新建、加载、保存、停用、删除触发器。
- 删除触发器前会弹出确认提示。
- 页签切换、触发器列表、状态提示带有轻量动画效果。

触发器配置存放在：

```text
triggers/*.json
```

触发器配置服务位于 `triggers.py`：

- `TriggerConfigService`：负责触发器配置的读取、保存、删除、列表、校验和标准化。
- `TriggerRuntime`：负责当前加载状态和服务器消息匹配。

触发器配置示例：

```json
{
  "name": "示例触发器",
  "notes": "说明文字",
  "rules": [
    {
      "keyword": "服务器消息关键词",
      "command": "look;hp",
      "delay": 0
    }
  ]
}
```

`command` 支持用分号或换行分隔多条命令。

## Telnet 代理

代理入口是 `proxy.py`。

数据流：

```text
zMUD <-> 本地代理 127.0.0.1:6666 <-> MUD 服务器 mud.pkuxkx.net:5555
```

功能：

- 双向转发 Telnet 数据。
- 处理 Telnet IAC 协商。
- 自动记录原始通信日志。
- 自动启动独立聊天监听窗口。
- 对服务器内容做 GBK/UTF-8 解码处理。

日志默认保存到：

```text
logs/YYYY-MM-DD_raw.log
```

## 命令统计

命令统计入口是 `skill_cmdlog.py`。

它会从 `logs/YYYY-MM-DD_raw.log` 中提取玩家发送的命令，并按 `config.py` 中的 `CMD_CATEGORIES` 分类。

默认分类包括：移动、战斗、物品、技能、沟通、查询、系统、其他。

## Wiki 离线工具

```bash
python wiki_spider.py
python wiki_clean.py
```

相关数据默认写入：

```text
wiki_db/
```

## 目录结构

```text
mud_assistant/
├── start.py                         # 主入口，分发 web/proxy/cmdlog 模式
├── config.py                        # 服务器、端口、日志、命令分类配置
├── web_mud.py                       # Web 客户端后端服务
├── mud_session.py                   # WebSocket 与 MUD Telnet 会话桥接
├── mud_telnet.py                    # Telnet IAC 协商和 GBK 安全处理
├── templates/
│   └── web_mud.html                 # Web 客户端页面模板
├── triggers.py                      # 触发器配置服务和运行时
├── triggers/                        # 触发器 JSON 配置
├── proxy.py                         # Telnet 代理
├── chat_monitor.py                  # 聊天频道监听器
├── skill_cmdlog.py                  # 命令统计工具
├── wiki_spider.py                   # Wiki 爬虫
├── wiki_clean.py                    # Wiki 清理工具
├── areas.json                       # 区域和房间数据
├── logs/                            # 运行日志，本地生成
├── cmdlog/                          # 命令统计报告，本地生成
└── wiki_db/                         # Wiki 离线缓存，本地生成
```

## 配置项

主要配置位于 `config.py`。

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `MUD_HOST` | `mud.pkuxkx.net` | MUD 服务器地址 |
| `MUD_PORT` | `5555` | MUD 服务器端口 |
| `PROXY_HOST` | `127.0.0.1` | 本地 Telnet 代理监听地址 |
| `PROXY_PORT` | `6666` | 本地 Telnet 代理监听端口 |
| `LOG_DIR` | `logs` | 日志目录 |
| `LOG_ENCODING` | `utf-8` | 日志文件编码 |

Web 客户端端口当前定义在 `web_mud.py` 的 `run_server()` 中，默认是 `58080`。

## Web 端字体替换

当前字体主要在 `templates/web_mud.html` 中配置：

- 全局页面字体：`html, body` 的 `font-family`。
- 主终端字体：创建 `new Terminal({ fontFamily: ... })` 的地方。
- 地图终端字体：创建 `mapTerm` 的地方。

MUD 客户端建议优先使用等宽字体，否则地图、表格、房间布局容易错位。

### Windows 推荐

```css
font-family: "Cascadia Mono", "Microsoft YaHei Mono", Consolas, monospace;
```

```css
font-family: "Maple Mono NF CN", "Cascadia Mono", "Microsoft YaHei Mono", monospace;
```

```css
font-family: "Sarasa Mono SC", "Microsoft YaHei Mono", Consolas, monospace;
```

### macOS 推荐

```css
font-family: "SF Mono", Menlo, Monaco, "PingFang SC", monospace;
```

```css
font-family: "Maple Mono NF CN", "SF Mono", "PingFang SC", monospace;
```

### 跨平台推荐

```css
font-family: "Maple Mono NF CN", "Sarasa Mono SC", "Cascadia Mono", "Microsoft YaHei Mono", monospace;
```

```css
font-family: "JetBrains Mono", "Microsoft YaHei Mono", "PingFang SC", monospace;
```

### 选择建议

- 中文和英文都想整齐：优先试 `Maple Mono NF CN` 或 `Sarasa Mono SC`。
- Windows 默认观感改善：试 `Cascadia Mono` + `Microsoft YaHei Mono`。
- 代码风格更强：试 `JetBrains Mono`，但中文需要后备字体。
- 不建议只用非等宽中文字体，例如只用 `Microsoft YaHei`，地图和表格可能错位。

如果只想快速改善观感，可以先把终端字体改成：

```js
fontFamily: '"Maple Mono NF CN", "Sarasa Mono SC", "Cascadia Mono", "Microsoft YaHei Mono", monospace'
```

## 开发提示

- Web 页面目前集中在 `templates/web_mud.html`，适合小步迭代。
- 触发器逻辑已经通过 `TriggerConfigService` 收敛，后续可以继续扩展搜索、分组、导入导出。
- `logs/`、`cmdlog/`、`wiki_db/` 多为本地生成数据，提交前请按需要检查。
