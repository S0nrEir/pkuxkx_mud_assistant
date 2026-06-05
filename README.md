# MUD Assistant (北大侠客行助手)

为 [北大侠客行](https://pkuxkx.net) MUD (`mud.pkuxkx.net:5555`) 开发的辅助工具集，提供浏览器客户端、Telnet 代理和命令统计分析等功能。

## 快速开始

### 环境要求

- Python 3.7+
- 依赖: `starlette`, `uvicorn`

```bash
pip install starlette uvicorn
```

### 启动方式

```bash
# Web 客户端（推荐）— 浏览器直接玩 MUD
python start.py web
# 或双击 启动Web客户端.bat

# Telnet 代理 — 配合 zMUD 使用
python start.py proxy

# 命令统计 — 查看命令分类报告
python start.py cmdlog
python start.py cmdlog 2026-06-04  # 指定日期
```

## 功能概览

### Web 客户端 (`python start.py web`)

启动后自动打开浏览器访问 `http://127.0.0.1:58080`。

- 基于 xterm.js 的全功能终端，完整 ANSI 颜色支持
- MXP 协议支持（交互式元素）
- 命令历史记录（最近 20 条，点击回填）
- 实时聊天面板（自动捕获闲聊、谣言、交易、QQ群等频道）
- 游戏地图截取（`lm`/`localmaps` 命令）
- 频道过滤（可在主终端中屏蔽指定聊天频道）
- 断线自动重连
- 支持多标签页登录不同角色

```
┌──────────────────────────────┬──────────────┐
│                              │  命令历史     │
│     游戏终端                  │  聊天频道     │
│     (完整颜色+可回看5000行)   │              │
│──────────────────────────────│              │
│  [输入命令...            ] 发送│              │
└──────────────────────────────┴──────────────┘
```

### Telnet 代理 (`python start.py proxy`)

传统模式，配合 zMUD 客户端使用：

1. 启动代理
2. zMUD 连接地址改为 `127.0.0.1:6666`
3. 自动转发到 MUD 服务器并记录日志

数据流: `zMUD <-> 代理(localhost:6666) <-> MUD服务器(mud.pkuxkx.net:5555)`

功能:
- 双向通信日志自动记录到 `logs/YYYY-MM-DD_raw.log`
- 自动弹出独立聊天监听窗口
- Telnet 协议 (IAC) 完整处理
- GBK/UTF-8 编码自动转换

### 命令统计 (`python start.py cmdlog`)

分析游戏日志，生成 Markdown 格式的命令分类报告，保存到 `cmdlog/YYYY-MM-DD_commands.md`。

分类维度: 移动、战斗、物品、技能、沟通、查询、系统

### Wiki 离线工具

```bash
python wiki_spider.py   # 爬取北大侠客行 Wiki 到本地
python wiki_clean.py    # 清理和格式化 Wiki 内容
```

## 项目结构

```
mud_assistant/
├── start.py              # 主入口 — 分发到各模式
├── config.py             # 配置（服务器地址、端口、命令分类规则）
├── web_mud.py            # Web 客户端后端 (Starlette + WebSocket)
├── proxy.py              # Telnet 代理
├── chat_monitor.py       # 聊天消息过滤模块
├── skill_cmdlog.py       # 命令分类统计
├── wiki_spider.py        # Wiki 爬虫
├── wiki_clean.py         # Wiki 内容清理
├── 启动Web客户端.bat      # 一键启动脚本
├── logs/                 # 原始通信日志
├── cmdlog/               # 命令统计报告
└── wiki_db/              # 本地 Wiki 缓存
```

## 入口说明（供 AI 工具参考）

| 文件 | 作用 |
|------|------|
| `start.py` | **唯一入口**。通过命令行参数分发到 proxy / web / cmdlog 三种模式 |
| `web_mud.py` → `run_server()` | Web 模式入口，启动 Starlette 服务在 `0.0.0.0:58080` |
| `proxy.py` → `MudProxy` | 代理模式入口，监听 `127.0.0.1:6666`，转发到 MUD 服务器 |
| `config.py` | 全局配置，所有模块共享的服务器地址、端口、分类规则 |
| `skill_cmdlog.py` → `build_cmdlog(date)` | 命令统计入口，传入日期字符串或 None（当天） |

## 配置

编辑 `config.py`:

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `MUD_HOST` | `mud.pkuxkx.net` | MUD 服务器地址 |
| `MUD_PORT` | `5555` | MUD 服务器端口 |
| `PROXY_HOST` | `127.0.0.1` | 代理监听地址 |
| `PROXY_PORT` | `6666` | 代理监听端口 |
| `LOG_DIR` | `logs` | 日志目录 |
| `LOG_ENCODING` | `utf-8` | 日志文件编码 |

Web 客户端端口 `58080` 定义在 `web_mud.py` 的 `run_server()` 函数中。

## 技术栈

- **Web 框架**: Starlette + Uvicorn (ASGI)
- **前端终端**: xterm.js (CDN 引入)
- **通信**: WebSocket（Web 模式）/ 原始 Socket（代理模式）
- **协议**: Telnet (IAC 协商) + MXP 标签解析
- **编码**: GBK ↔ UTF-8 双向转换

## 详细文档

使用指南详见 [GUIDE.md](GUIDE.md)。
