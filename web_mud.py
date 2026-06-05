"""
MUD Web 客户端
浏览器 (xterm.js) ←WebSocket→ 本后端 ←TCP socket→ MUD 服务器

用法: python start.py web
"""

import os
import sys
import json
import re
import asyncio
import webbrowser
import threading
from datetime import datetime

import config
from chat_monitor import is_chat_message

# ═══════════════════════════════════════════
#  前端 HTML (内嵌)
# ═══════════════════════════════════════════

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MUD Web Client</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.css">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; overflow: hidden; background: #0d1117; color: #d4dce7; font-family: 'Consolas', 'Courier New', monospace; }

.container { display: flex; height: 100vh; }

/* 左侧设置栏 */
.settings-panel {
    width: 15%;
    min-width: 180px;
    background: #161b22;
    border-right: 1px solid #30363d;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
}
.settings-header {
    padding: 8px 12px;
    font-size: 12px;
    color: #8b949e;
    border-bottom: 1px solid #30363d;
}
.settings-body {
    flex: 1;
    overflow-y: auto;
    padding: 8px 8px;
}
.setting-group { margin-bottom: 10px; }
.setting-group-title {
    color: #8b949e;
    font-size: 11px;
    padding: 4px 0 4px;
    border-bottom: 1px solid #21262d;
    margin-bottom: 4px;
}
.setting-row {
    display: flex;
    align-items: center;
    padding: 3px 4px;
    border-radius: 3px;
    cursor: pointer;
    transition: background 0.15s;
}
.setting-row:hover { background: #1f2937; }
.setting-row input[type="checkbox"] {
    margin-right: 6px;
    accent-color: #58a6ff;
    cursor: pointer;
}
.setting-row label {
    cursor: pointer;
    font-size: 12px;
    flex: 1;
    color: #c9d1d9;
}
.setting-row .ch-hint {
    color: #484f58;
    font-size: 10px;
    margin-left: 2px;
}
.settings-footer {
    padding: 6px 10px;
    font-size: 10px;
    color: #484f58;
    border-top: 1px solid #21262d;
}

/* 中间区域（终端 + 底部地图/输入） */
.center-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
}

/* 中间终端 */
.terminal-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
}
.terminal-panel .header {
    background: #161b22;
    padding: 6px 12px;
    font-size: 13px;
    color: #8b949e;
    border-bottom: 1px solid #30363d;
    display: flex;
    align-items: center;
    gap: 8px;
}
.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #f85149;
    display: inline-block;
}
.status-dot.connected { background: #3fb950; }
#terminal { flex: 1; padding: 4px; }

/* 底部面板 */
.bottom-panel {
    height: 15vh;
    min-height: 100px;
    border-top: 1px solid #30363d;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
}
.bottom-top { display: flex; flex: 1; min-height: 0; }
.map-panel {
    flex: 7;
    background: #0d1117;
    min-width: 0;
}
.map-panel .panel-label {
    background: #161b22;
    padding: 2px 10px;
    font-size: 11px;
    color: #6e7681;
    border-bottom: 1px solid #21262d;
}
#mapTerminal { height: calc(100% - 22px); }
.bottom-right {
    flex: 3;
    background: #161b22;
    border-left: 1px solid #30363d;
    min-width: 120px;
}
.bottom-right .panel-label {
    padding: 2px 10px;
    font-size: 11px;
    color: #6e7681;
    border-bottom: 1px solid #21262d;
}
/* 输入框 */
.input-bar {
    background: #161b22;
    border-top: 1px solid #30363d;
    padding: 6px 12px;
    display: flex;
    gap: 8px;
    flex-shrink: 0;
}
.input-bar input {
    flex: 1;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 4px;
    padding: 6px 12px;
    color: #d4dce7;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 14px;
    outline: none;
}
.input-bar input:focus {
    border-color: #58a6ff;
    box-shadow: 0 0 0 2px rgba(88,166,255,0.15);
}
.input-bar input::placeholder { color: #484f58; }
.input-bar .send-btn {
    background: #238636;
    color: #fff;
    border: none;
    border-radius: 4px;
    padding: 6px 16px;
    font-size: 13px;
    cursor: pointer;
    font-family: inherit;
    flex-shrink: 0;
}
.input-bar .send-btn:hover { background: #2ea043; }

/* 右侧面板 */
.side-panel {
    width: 18%;
    min-width: 200px;
    display: flex;
    flex-direction: column;
    border-left: 1px solid #30363d;
    flex-shrink: 0;
}
.panel-section {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
}
.panel-section + .panel-section { border-top: 1px solid #30363d; }
.panel-header {
    background: #161b22;
    padding: 6px 12px;
    font-size: 12px;
    color: #8b949e;
    border-bottom: 1px solid #30363d;
    flex-shrink: 0;
}
.panel-body {
    flex: 1;
    overflow-y: auto;
    padding: 6px 8px;
    font-size: 13px;
}

/* 命令历史 */
.cmd-item {
    padding: 3px 6px;
    margin: 2px 0;
    border-radius: 3px;
    cursor: pointer;
    color: #79c0ff;
    word-break: break-all;
    transition: background 0.15s;
}
.cmd-item:hover { background: #1f2937; }
.cmd-item .cmd-time { color: #484f58; font-size: 11px; margin-right: 6px; }

/* 聊天消息 */
.chat-msg {
    padding: 4px 6px;
    margin: 3px 0;
    border-radius: 3px;
    background: #161b22;
    word-break: break-all;
    line-height: 1.5;
}
.chat-msg .chat-time { color: #6e7681; font-size: 11px; margin-right: 6px; }

/* 空状态 */
.empty-hint {
    color: #6e7681;
    font-style: italic;
    padding: 12px;
    text-align: center;
    font-size: 12px;
}

/* 滚动条 */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
</style>
</head>
<body>
<div class="container">
    <div class="main-area">
        <div class="settings-panel">
            <div class="settings-header">设置</div>
            <div class="settings-body" id="settingsPanel">
                <div class="setting-group">
                    <div class="setting-group-title">终端消息屏蔽</div>
                    <div class="setting-row"><input type="checkbox" id="mute_chat" data-ch="chat"><label for="mute_chat">闲聊 <span class="ch-hint">chat</span></label></div>
                    <div class="setting-row"><input type="checkbox" id="mute_rumor" data-ch="rumor"><label for="mute_rumor">谣言 <span class="ch-hint">rumor</span></label></div>
                    <div class="setting-row"><input type="checkbox" id="mute_jy" data-ch="jy"><label for="mute_jy">交易 <span class="ch-hint">jy</span></label></div>
                    <div class="setting-row"><input type="checkbox" id="mute_qq" data-ch="qq"><label for="mute_qq">QQ群 <span class="ch-hint">qq</span></label></div>
                    <div class="setting-row"><input type="checkbox" id="mute_group" data-ch="group"><label for="mute_group">帮派 <span class="ch-hint">group</span></label></div>
                    <div class="setting-row"><input type="checkbox" id="mute_team" data-ch="team"><label for="mute_team">组队</label></div>
                    <div class="setting-row"><input type="checkbox" id="mute_shout" data-ch="shout"><label for="mute_shout">大喊 <span class="ch-hint">shout</span></label></div>
                </div>
            </div>
            <div class="settings-footer">屏蔽后终端不显示，聊天面板始终显示</div>
        </div>
        <div class="terminal-panel">
            <div class="header">
                <span class="status-dot" id="statusDot"></span>
                <span id="statusText">未连接</span>
            </div>
            <div id="terminal"></div>
        </div>
        <div class="side-panel">
            <div class="panel-section">
                <div class="panel-header">命令历史</div>
                <div class="panel-body" id="cmdHistory">
                    <div class="empty-hint">暂无命令</div>
                </div>
            </div>
            <div class="panel-section">
                <div class="panel-header">聊天频道</div>
                <div class="panel-body" id="chatPanel">
                    <div class="empty-hint">等待聊天消息...</div>
                </div>
            </div>
        </div>
    </div>
    <div class="bottom-panel">
        <div class="bottom-top">
            <div class="map-panel">
                <div class="panel-label" id="mapLabel">地图</div>
                <div id="mapTerminal"></div>
            </div>
            <div class="bottom-right">
                <div class="panel-label">预留</div>
            </div>
        </div>
        <div class="input-bar">
            <input type="text" id="cmdInput" placeholder="输入命令..." autocomplete="off" autofocus>
            <button class="send-btn" id="sendBtn">发送</button>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xterm-addon-web-links@0.9.0/lib/xterm-addon-web-links.js"></script>
<script>
(function() {
    // ─── 终端初始化 ───
    const term = new Terminal({
        fontSize: 15,
        fontFamily: 'Consolas, "Courier New", monospace',
        theme: {
            background: '#0f1419',
            foreground: '#e6e1cf',
            cursor: '#e6b450',
            cursorAccent: '#0f1419',
            selectionBackground: '#2a3344',
            black: '#1a1f29',
            red: '#f07178',
            green: '#7fd962',
            yellow: '#ffb454',
            blue: '#59c2ff',
            magenta: '#d2a6ff',
            cyan: '#95e6cb',
            white: '#c7c7c7',
            brightBlack: '#626a75',
            brightRed: '#ff8e8e',
            brightGreen: '#a8e6a3',
            brightYellow: '#ffd68a',
            brightBlue: '#7dccff',
            brightMagenta: '#e4bfff',
            brightCyan: '#b8f0e0',
            brightWhite: '#ffffff',
        },
        scrollback: 5000,
        convertEol: true,
        cursorBlink: true,
        cols: 80,
        rows: 24,
    });

    const fitAddon = new FitAddon.FitAddon();
    const webLinksAddon = new WebLinksAddon.WebLinksAddon();
    term.loadAddon(fitAddon);
    term.loadAddon(webLinksAddon);
    term.open(document.getElementById('terminal'));
    fitAddon.fit();

    window.addEventListener('resize', () => fitAddon.fit());
    new ResizeObserver(() => fitAddon.fit()).observe(document.getElementById('terminal'));

    // ─── 状态 ───
    let ws = null;
    let historyIndex = -1;  // 输入框历史导航索引
    let inputHistory = [];  // 本地输入历史（含未提交的）
    let savedDraft = '';    // 翻历史时暂存当前输入
    const cmdHistoryEl = document.getElementById('cmdHistory');
    const chatPanelEl = document.getElementById('chatPanel');
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    const cmdInput = document.getElementById('cmdInput');
    const sendBtn = document.getElementById('sendBtn');
    let chatInitialized = false;

    function setStatus(connected) {
        statusDot.className = 'status-dot' + (connected ? ' connected' : '');
        statusText.textContent = connected ? '已连接' : '未连接';
    }

    // ─── WebSocket ───
    function connect() {
        const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
        ws = new WebSocket(proto + '//' + location.host + '/ws');
        ws.binaryType = 'arraybuffer';

        ws.onopen = function() {
            setStatus(true);
            term.writeln('\x1b[32m[已连接到 MUD 服务器]\x1b[0m\r\n');
            cmdInput.focus();
        };

        ws.onmessage = function(event) {
            if (event.data instanceof ArrayBuffer) {
                // 终端数据 (UTF-8 文本 + ANSI + MXP 标签)
                const text = new TextDecoder('utf-8').decode(event.data);
                const processed = processMXP(text);
                term.write(processed);
            } else {
                // JSON 事件
                try {
                    const msg = JSON.parse(event.data);
                    if (msg.type === 'chat') {
                        addChatMessage(msg.data);
                    } else if (msg.type === 'history') {
                        renderHistory(msg.data);
                    } else if (msg.type === 'map') {
                        // 地图数据 → 渲染到地图面板
                        mapTerm.clear();
                        mapTerm.write(msg.data);
                        var label = document.getElementById('mapLabel');
                        if (msg.area) {
                            label.textContent = '地图 · ' + msg.area.name;
                        }
                    } else if (msg.type === 'mxp_reply') {
                        // 后端通知需要发送 MXP 回复
                        if (ws && ws.readyState === WebSocket.OPEN) {
                            ws.send(msg.data);
                        }
                    }
                } catch(e) {}
            }
        };

        ws.onclose = function() {
            setStatus(false);
            term.writeln('\r\n\x1b[31m[连接已断开，3秒后重连...]\x1b[0m\r\n');
            setTimeout(connect, 3000);
        };

        ws.onerror = function() {};
    }

    // ─── 输入框发送命令 ───
    function sendCommand() {
        const cmd = cmdInput.value;
        if (!cmd.trim() || !ws || ws.readyState !== WebSocket.OPEN) return;

        // 发送到服务器
        ws.send(cmd + '\r');
        // 通知后端记录命令历史
        ws.send(JSON.stringify({ type: 'command', data: cmd.trim() }));

        // 本地输入历史
        inputHistory.push(cmd);
        historyIndex = -1;
        savedDraft = '';
        cmdInput.value = '';
    }

    sendBtn.addEventListener('click', sendCommand);

    cmdInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendCommand();
        } else if (e.key === 'ArrowUp') {
            // 上翻历史
            e.preventDefault();
            if (inputHistory.length === 0) return;
            if (historyIndex === -1) {
                savedDraft = cmdInput.value;
                historyIndex = inputHistory.length - 1;
            } else if (historyIndex > 0) {
                historyIndex--;
            }
            cmdInput.value = inputHistory[historyIndex];
        } else if (e.key === 'ArrowDown') {
            // 下翻历史
            e.preventDefault();
            if (historyIndex === -1) return;
            if (historyIndex < inputHistory.length - 1) {
                historyIndex++;
                cmdInput.value = inputHistory[historyIndex];
            } else {
                historyIndex = -1;
                cmdInput.value = savedDraft;
            }
        }
    });

    // 点击终端区域时自动聚焦输入框
    document.getElementById('terminal').addEventListener('click', function() {
        cmdInput.focus();
    });

    // ═══ MXP 引擎 ═══
    const mxpElements = {};   // 自定义元素: name → {open, definition, attrs, tagNum}
    const mxpEntities = {};   // 实体/变量: name → value
    let mxpSendLinks = [];    // 活跃 SEND 链接: [{text, command}]
    let mxpLinkProvider = null;

    // ANSI 颜色名 → 代码
    const MXP_COLORS = {
        black:0, red:1, green:2, yellow:3, blue:4, magenta:5, cyan:6, white:7,
        'default':9, gray:8, grey:8, brown:3, purple:5, orange:3,
    };
    function mxpColorCode(name) {
        if (!name) return '';
        name = name.toLowerCase().trim();
        if (MXP_COLORS[name] !== undefined) return '\x1b[' + (30 + MXP_COLORS[name]) + 'm';
        if (/^[0-9]+$/.test(name)) return '\x1b[38;5;' + name + 'm';
        if (/^#[0-9a-f]{6}$/i.test(name)) return '\x1b[38;2;' + parseInt(name.slice(1,3),16) + ';' + parseInt(name.slice(3,5),16) + ';' + parseInt(name.slice(5,7),16) + 'm';
        return '';
    }

    // 解析 MXP 属性字符串 "attr1=val1 attr2=val2" → {attr1: val1, ...}
    function parseMxpAttrs(s) {
        const attrs = {};
        if (!s) return attrs;
        // 匹配 key="val" key='val' key=val "val"
        const re = /(\w+)=(?:"([^"]*)"|'([^']*)'|(\S+))|"(?:([^"]*))"/g;
        let m, pos = 0;
        while ((m = re.exec(s)) !== null) {
            if (m[1]) attrs[m[1].toLowerCase()] = m[2] || m[3] || m[4] || '';
            else if (m[5] !== undefined) attrs['_pos' + pos++] = m[5];
        }
        return attrs;
    }

    // 注册 link provider
    function updateLinkProvider() {
        if (mxpLinkProvider) { try { mxpLinkProvider.dispose(); } catch(e){} }
        mxpLinkProvider = term.registerLinkProvider({
            provideLinks: function(row, callback) {
                const links = [];
                for (const link of mxpSendLinks) {
                    if (link._row === row) {
                        links.push({
                            range: { start: { x: link._col, y: row }, end: { x: link._col + link.text.length - 1, y: row } },
                            text: link.text,
                            activate: function() {
                                if (ws && ws.readyState === WebSocket.OPEN) {
                                    ws.send(link.command + '\r');
                                }
                            }
                        });
                    }
                }
                callback(links);
            }
        });
    }

    function processMXP(text) {
        // 1. 展开 &entity; 引用
        text = text.replace(/&(\w+);/g, function(m, name) {
            if (mxpEntities[name] !== undefined) return mxpEntities[name];
            return m; // 保留未知实体
        });

        let result = '';
        let i = 0;
        const len = text.length;
        mxpSendLinks = [];

        while (i < len) {
            // MXP 行模式标记 \x1b[#z → 直接跳过
            if (text.charCodeAt(i) === 0x1b && i + 2 < len && text[i+1] === '[') {
                const zIdx = text.indexOf('z', i + 2);
                if (zIdx !== -1 && zIdx - (i+2) < 3) {
                    i = zIdx + 1;
                    continue;
                }
            }

            // <!ELEMENT ...> / <!EL ...>
            if (text[i] === '<' && text.substring(i, i+9).toUpperCase() === '<!ELEMENT') {
                const end = text.indexOf('>', i);
                if (end !== -1) {
                    const def = text.substring(i + 9, end).trim();
                    parseElementDef(def);
                    i = end + 1;
                    continue;
                }
            }
            if (text[i] === '<' && text.substring(i, i+4).toUpperCase() === '<!EL') {
                const end = text.indexOf('>', i);
                if (end !== -1) {
                    const def = text.substring(i + 4, end).trim();
                    parseElementDef(def);
                    i = end + 1;
                    continue;
                }
            }

            // <!ATTLIST ...> / <!AT ...>
            if (text[i] === '<' && text.substring(i, i+9).toUpperCase() === '<!ATTLIST') {
                const end = text.indexOf('>', i);
                if (end !== -1) { i = end + 1; continue; }
            }
            if (text[i] === '<' && text.substring(i, i+4).toUpperCase() === '<!AT ') {
                const end = text.indexOf('>', i);
                if (end !== -1) { i = end + 1; continue; }
            }

            // <!ENTITY name "value"> / <!EN ...>
            if (text[i] === '<' && text.substring(i, i+8).toUpperCase() === '<!ENTITY') {
                const end = text.indexOf('>', i);
                if (end !== -1) {
                    const def = text.substring(i + 8, end).trim();
                    parseEntityDef(def);
                    i = end + 1;
                    continue;
                }
            }
            if (text[i] === '<' && text.substring(i, i+4).toUpperCase() === '<!EN') {
                const end = text.indexOf('>', i);
                if (end !== -1) {
                    const def = text.substring(i + 4, end).trim();
                    parseEntityDef(def);
                    i = end + 1;
                    continue;
                }
            }

            // <!TAG ...> → 忽略
            if (text[i] === '<' && text.substring(i, i+5).toUpperCase() === '<!TAG') {
                const end = text.indexOf('>', i);
                if (end !== -1) { i = end + 1; continue; }
            }

            // <!-- ... --> 注释
            if (text[i] === '<' && text.substring(i, i+4) === '<!--') {
                const end = text.indexOf('-->', i);
                if (end !== -1) { i = end + 3; continue; }
            }

            // <SEND ...>text</SEND> 或 <send ...>text</send>
            if (text[i] === '<' && text.substring(i, i+5).toUpperCase() === '<SEND') {
                const gtIdx = text.indexOf('>', i);
                if (gtIdx !== -1) {
                    const attrStr = text.substring(i + 5, gtIdx).trim();
                    const closeTag = findCloseTag(text, gtIdx + 1, 'SEND');
                    if (closeTag !== -1) {
                        const linkText = text.substring(gtIdx + 1, closeTag);
                        const attrs = parseMxpAttrs(attrStr);
                        const cmd = attrs.href || attrs._pos0 || linkText;
                        // 显示文本 + 下划线
                        const startCol = result.length + 1; // 大致列号
                        result += '\x1b[4m' + linkText + '\x1b[24m';
                        mxpSendLinks.push({ text: linkText, command: cmd, _row: term.buffer.active.cursorY, _col: startCol });
                        i = text.indexOf('>', closeTag) + 1;
                        continue;
                    }
                }
            }

            // <A href="url">text</A> → 超链接（web-links addon 处理 URL）
            if (text[i] === '<' && text.substring(i, i+2).toUpperCase() === '<A') {
                const gtIdx = text.indexOf('>', i);
                if (gtIdx !== -1) {
                    const attrStr = text.substring(i + 2, gtIdx).trim();
                    const closeTag = findCloseTag(text, gtIdx + 1, 'A');
                    if (closeTag !== -1) {
                        const linkText = text.substring(gtIdx + 1, closeTag);
                        const attrs = parseMxpAttrs(attrStr);
                        const url = attrs.href || attrs._pos0 || '';
                        if (url) {
                            result += '\x1b[4m' + url + '\x1b[24m';
                        } else {
                            result += linkText;
                        }
                        i = text.indexOf('>', closeTag) + 1;
                        continue;
                    }
                }
            }

            // <B>...</B> → ANSI bold
            if (text[i] === '<' && isTag(text, i, 'B')) {
                result += '\x1b[1m'; i = skipOpenTag(text, i); continue;
            }
            if (text[i] === '<' && isTag(text, i, '/B')) {
                result += '\x1b[22m'; i = skipOpenTag(text, i); continue;
            }
            // <BOLD> <STRONG>
            if (text[i] === '<' && (isTag(text, i, 'BOLD') || isTag(text, i, 'STRONG'))) {
                result += '\x1b[1m'; i = skipOpenTag(text, i); continue;
            }
            if (text[i] === '<' && (isTag(text, i, '/BOLD') || isTag(text, i, '/STRONG'))) {
                result += '\x1b[22m'; i = skipOpenTag(text, i); continue;
            }

            // <I>...</I> → ANSI italic
            if (text[i] === '<' && isTag(text, i, 'I')) {
                result += '\x1b[3m'; i = skipOpenTag(text, i); continue;
            }
            if (text[i] === '<' && isTag(text, i, '/I')) {
                result += '\x1b[23m'; i = skipOpenTag(text, i); continue;
            }

            // <U>...</U> → ANSI underline
            if (text[i] === '<' && isTag(text, i, 'U')) {
                result += '\x1b[4m'; i = skipOpenTag(text, i); continue;
            }
            if (text[i] === '<' && isTag(text, i, '/U')) {
                result += '\x1b[24m'; i = skipOpenTag(text, i); continue;
            }

            // <S>...</S> → ANSI strikethrough
            if (text[i] === '<' && isTag(text, i, 'S')) {
                result += '\x1b[9m'; i = skipOpenTag(text, i); continue;
            }
            if (text[i] === '<' && isTag(text, i, '/S')) {
                result += '\x1b[29m'; i = skipOpenTag(text, i); continue;
            }

            // <H> → high color (bright)
            if (text[i] === '<' && isTag(text, i, 'H')) {
                result += '\x1b[1m'; i = skipOpenTag(text, i); continue;
            }
            if (text[i] === '<' && isTag(text, i, '/H')) {
                result += '\x1b[22m'; i = skipOpenTag(text, i); continue;
            }

            // <COLOR fore=back>...</COLOR> / <C ...>
            if (text[i] === '<' && (isTagWithAttrs(text, i, 'COLOR') || isTagWithAttrs(text, i, 'C '))) {
                const gtIdx = text.indexOf('>', i);
                if (gtIdx !== -1) {
                    const tagName = text.substring(i+1, gtIdx).trim().split(/[\s>]/)[0];
                    const attrStr = text.substring(i + 1 + tagName.length, gtIdx).trim();
                    const attrs = parseMxpAttrs(attrStr);
                    const fg = attrs.fore || attrs._pos0 || '';
                    const bg = attrs.back || attrs._pos1 || '';
                    if (fg) result += mxpColorCode(fg);
                    if (bg) result += '\x1b[' + (40 + (MXP_COLORS[bg.toLowerCase()] || 0)) + 'm';
                    i = gtIdx + 1;
                    continue;
                }
            }
            if (text[i] === '<' && (isTag(text, i, '/COLOR') || isTag(text, i, '/C'))) {
                result += '\x1b[39;49m'; i = skipOpenTag(text, i); continue;
            }

            // <FONT ...>...</FONT> → 提取颜色
            if (text[i] === '<' && isTagWithAttrs(text, i, 'FONT')) {
                const gtIdx = text.indexOf('>', i);
                if (gtIdx !== -1) {
                    const attrStr = text.substring(i + 5, gtIdx).trim();
                    const attrs = parseMxpAttrs(attrStr);
                    if (attrs.color) result += mxpColorCode(attrs.color);
                    if (attrs.back) result += '\x1b[' + (40 + (MXP_COLORS[attrs.back.toLowerCase()] || 0)) + 'm';
                    i = gtIdx + 1; continue;
                }
            }
            if (text[i] === '<' && isTag(text, i, '/FONT')) {
                result += '\x1b[39;49m'; i = skipOpenTag(text, i); continue;
            }

            // <BR> → newline
            if (text[i] === '<' && isTag(text, i, 'BR')) {
                result += '\r\n'; i = skipOpenTag(text, i); continue;
            }
            // <SBR> → space
            if (text[i] === '<' && isTag(text, i, 'SBR')) {
                result += ' '; i = skipOpenTag(text, i); continue;
            }
            // <P> </P> <NOBR> </NOBR> → 忽略
            if (text[i] === '<' && (isTag(text, i, 'P') || isTag(text, i, '/P') || isTag(text, i, 'NOBR') || isTag(text, i, '/NOBR'))) {
                i = skipOpenTag(text, i); continue;
            }

            // <EXPIRE> → 清除活跃链接
            if (text[i] === '<' && isTag(text, i, 'EXPIRE')) {
                mxpSendLinks = [];
                i = skipOpenTag(text, i); continue;
            }

            // <VERSION> → 回复版本信息
            if (text[i] === '<' && isTag(text, i, 'VERSION')) {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: 'mxp_reply', data: '\x1b[1z<VERSION MXP=1.0 CLIENT=web_mud VERSION=1.0>\r\n' }));
                }
                i = skipOpenTag(text, i); continue;
            }

            // <SUPPORT> → 回复支持列表
            if (text[i] === '<' && isTag(text, i, 'SUPPORT')) {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: 'mxp_reply', data: '\x1b[1z<SUPPORTS +B +I +U +S +COLOR +FONT +SEND +A +BR +P +NOBR +VAR +ENTITY +ELEMENT +GAUGE +STAT +EXPIRE +VERSION +SUPPORT>\r\n' }));
                }
                i = skipOpenTag(text, i); continue;
            }

            // <VAR name>value</VAR> → 显示 value 并存储变量
            if (text[i] === '<' && isTagWithAttrs(text, i, 'VAR')) {
                const gtIdx = text.indexOf('>', i);
                if (gtIdx !== -1) {
                    const varName = text.substring(i + 4, gtIdx).trim().split(/[\s>]/)[0].toLowerCase();
                    const closeIdx = findCloseTag(text, gtIdx + 1, 'VAR');
                    if (closeIdx !== -1) {
                        const varValue = text.substring(gtIdx + 1, closeIdx);
                        mxpEntities[varName] = varValue;
                        result += varValue;
                        i = text.indexOf('>', closeIdx) + 1;
                        continue;
                    }
                }
            }

            // <GAUGE ...> <STAT ...> → 提取并存储（不显示）
            if (text[i] === '<' && (isTag(text, i, 'GAUGE') || isTag(text, i, 'STAT'))) {
                i = skipOpenTag(text, i); continue;
            }

            // <FRAME ...> <DEST ...> <IMAGE ...> <SOUND ...> <MUSIC ...> → 忽略
            if (text[i] === '<' && (isTagWithAttrs(text, i, 'FRAME') || isTagWithAttrs(text, i, 'DEST') || isTagWithAttrs(text, i, 'IMAGE') || isTagWithAttrs(text, i, 'SOUND') || isTagWithAttrs(text, i, 'MUSIC'))) {
                i = skipOpenTag(text, i); continue;
            }
            if (text[i] === '<' && (isTag(text, i, '/FRAME') || isTag(text, i, '/DEST'))) {
                i = skipOpenTag(text, i); continue;
            }

            // <MXP> → 忽略（MXP 启用标记）
            if (text[i] === '<' && isTag(text, i, 'MXP')) {
                i = skipOpenTag(text, i); continue;
            }

            // 自定义元素 (来自 <!ELEMENT> 定义)
            let handled = false;
            for (const [elName, elDef] of Object.entries(mxpElements)) {
                if (text[i] === '<' && text.substring(i + 1, i + 1 + elName.length).toUpperCase() === elName.toUpperCase() && (text[i + 1 + elName.length] === '>' || text[i + 1 + elName.length] === ' ')) {
                    const gtIdx = text.indexOf('>', i);
                    if (gtIdx !== -1) {
                        const closeIdx = findCloseTag(text, gtIdx + 1, elName);
                        if (closeIdx !== -1) {
                            const elText = text.substring(gtIdx + 1, closeIdx);
                            // 展开元素定义
                            if (elDef.definition) {
                                let expanded = elDef.definition.replace(/&text;/gi, elText);
                                // 处理元素属性
                                const attrStr = text.substring(i + 1 + elName.length, gtIdx).trim();
                                if (attrStr) {
                                    const attrs = parseMxpAttrs(attrStr);
                                    for (const [k, v] of Object.entries(attrs)) {
                                        expanded = expanded.replace(new RegExp('&' + k + ';', 'gi'), v);
                                    }
                                }
                                // 递归处理展开后的内容
                                result += processMXP(expanded);
                            } else {
                                result += elText;
                            }
                            i = text.indexOf('>', closeIdx) + 1;
                            handled = true;
                            break;
                        }
                    }
                }
                // 自关闭标签 <ElName/> 或空元素
                if (text[i] === '<' && text.substring(i + 1, i + 1 + elName.length).toUpperCase() === elName.toUpperCase() && elDef.empty) {
                    const gtIdx = text.indexOf('>', i);
                    if (gtIdx !== -1) {
                        if (elDef.definition) {
                            result += processMXP(elDef.definition);
                        }
                        i = gtIdx + 1;
                        handled = true;
                        break;
                    }
                }
            }
            if (handled) continue;

            // 未匹配的 <tag> → 尝试跳过（避免在终端显示乱码标签）
            if (text[i] === '<' && i + 1 < len && /[A-Za-z\/!]/.test(text[i+1])) {
                const gtIdx = text.indexOf('>', i);
                if (gtIdx !== -1 && gtIdx - i < 200) {
                    // 可能是未处理的 MXP 标签，跳过
                    i = gtIdx + 1;
                    continue;
                }
            }

            // 普通字符
            result += text[i];
            i++;
        }

        // 更新 link provider
        if (mxpSendLinks.length > 0) {
            updateLinkProvider();
        }

        return result;
    }

    // MXP 辅助函数
    function isTag(text, pos, tagName) {
        const tl = tagName.length;
        if (text.substring(pos, pos + 1 + tl).toUpperCase() !== '<' + tagName.toUpperCase()) return false;
        const next = text[pos + 1 + tl];
        return next === '>' || next === ' ' || next === '/';
    }
    function isTagWithAttrs(text, pos, tagName) {
        return text.substring(pos, pos + 1 + tagName.length).toUpperCase() === '<' + tagName.toUpperCase() && (text[pos + 1 + tagName.length] === ' ' || text[pos + 1 + tagName.length] === '>');
    }
    function skipOpenTag(text, pos) {
        const gt = text.indexOf('>', pos);
        return gt !== -1 ? gt + 1 : pos + 1;
    }
    function findCloseTag(text, start, tagName) {
        const close = '</' + tagName + '>';
        const closeUpper = '</' + tagName.toUpperCase() + '>';
        let idx = start;
        while (idx < text.length) {
            const sub = text.substring(idx);
            if (sub.substring(0, close.length).toUpperCase() === closeUpper) return idx;
            idx++;
        }
        return -1;
    }

    function parseElementDef(def) {
        // 格式: element-name [definition] [ATT=...] [TAG=num] [FLAG=...] [OPEN] [DELETE] [EMPTY]
        const parts = def.match(/^(\S+)(?:\s+'([^']*)')?(.*)/i);
        if (!parts) return;
        const name = parts[1].toLowerCase();
        const definition = parts[2] || '';
        const rest = (parts[3] || '').trim();

        if (/\bDELETE\b/i.test(rest)) {
            delete mxpElements[name];
            return;
        }

        const el = { name, definition, open: /\bOPEN\b/i.test(rest), empty: /\bEMPTY\b/i.test(rest), tagNum: 0 };

        const tagMatch = rest.match(/TAG=(\d+)/i);
        if (tagMatch) el.tagNum = parseInt(tagMatch[1]);

        const attMatch = rest.match(/ATT='([^']*)'/i);
        if (attMatch) el.attrs = attMatch[1];

        mxpElements[name] = el;
    }

    function parseEntityDef(def) {
        // 格式: name "value" 或 name value
        const m = def.match(/^(\S+)\s+(?:"([^"]*)"|'([^']*)'|(\S+))/);
        if (!m) return;
        const name = m[1].toLowerCase();
        if (/\bDELETE\b/i.test(def)) {
            delete mxpEntities[name];
            return;
        }
        mxpEntities[name] = m[2] || m[3] || m[4] || '';
    }

    // ─── 命令历史面板 ───
    function renderHistory(items) {
        if (!items || items.length === 0) {
            cmdHistoryEl.innerHTML = '<div class="empty-hint">暂无命令</div>';
            return;
        }
        cmdHistoryEl.innerHTML = items.map(function(item) {
            return '<div class="cmd-item" data-cmd="' + escapeAttr(item) + '">'
                 + '<span class="cmd-time">&gt;</span> ' + escapeHtml(item)
                 + '</div>';
        }).join('');
        cmdHistoryEl.scrollTop = cmdHistoryEl.scrollHeight;
    }

    cmdHistoryEl.addEventListener('click', function(e) {
        const item = e.target.closest('.cmd-item');
        if (!item) return;
        const cmd = item.getAttribute('data-cmd');
        if (cmd && ws && ws.readyState === WebSocket.OPEN) {
            // 填入输入框并聚焦
            cmdInput.value = cmd;
            cmdInput.focus();
        }
    });

    // ─── 聊天面板 ───
    function addChatMessage(data) {
        if (!chatInitialized) {
            chatPanelEl.innerHTML = '';
            chatInitialized = true;
        }
        const div = document.createElement('div');
        div.className = 'chat-msg';
        div.innerHTML = '<span class="chat-time">' + escapeHtml(data.time) + '</span>' + escapeHtml(data.text);
        chatPanelEl.appendChild(div);

        // 限制数量
        while (chatPanelEl.children.length > 200) {
            chatPanelEl.removeChild(chatPanelEl.firstChild);
        }

        // 自动滚动到底部
        chatPanelEl.scrollTop = chatPanelEl.scrollHeight;
    }

    // ─── 工具函数 ───
    function escapeHtml(s) {
        const div = document.createElement('div');
        div.textContent = s;
        return div.innerHTML;
    }
    function escapeAttr(s) {
        return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    // ─── 设置持久化 ───
    const SETTINGS_KEY = 'mud_muted_channels';
    const muteCheckboxes = document.querySelectorAll('#settingsPanel input[type="checkbox"]');

    function loadSettings() {
        try {
            const saved = JSON.parse(localStorage.getItem(SETTINGS_KEY) || '[]');
            muteCheckboxes.forEach(function(cb) {
                cb.checked = saved.indexOf(cb.getAttribute('data-ch')) !== -1;
            });
        } catch(e) {}
        syncMutedToBackend();
    }

    function saveSettings() {
        const muted = [];
        muteCheckboxes.forEach(function(cb) {
            if (cb.checked) muted.push(cb.getAttribute('data-ch'));
        });
        localStorage.setItem(SETTINGS_KEY, JSON.stringify(muted));
        syncMutedToBackend();
    }

    function syncMutedToBackend() {
        const muted = [];
        muteCheckboxes.forEach(function(cb) {
            if (cb.checked) muted.push(cb.getAttribute('data-ch'));
        });
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'mute_channels', data: muted }));
        }
    }

    muteCheckboxes.forEach(function(cb) {
        cb.addEventListener('change', saveSettings);
    });

    // ─── 地图终端 ───
    const mapTerm = new Terminal({
        fontSize: 12,
        fontFamily: 'Consolas, "Courier New", monospace',
        theme: {
            background: '#0d1117',
            foreground: '#e6e1cf',
            cursor: 'transparent',
            cursorAccent: '#0d1117',
            selectionBackground: '#2a3344',
            black: '#1a1f29', red: '#f07178', green: '#7fd962', yellow: '#ffb454',
            blue: '#59c2ff', magenta: '#d2a6ff', cyan: '#95e6cb', white: '#c7c7c7',
            brightBlack: '#626a75', brightRed: '#ff8e8e', brightGreen: '#a8e6a3',
            brightYellow: '#ffd68a', brightBlue: '#7dccff', brightMagenta: '#e4bfff',
            brightCyan: '#b8f0e0', brightWhite: '#ffffff',
        },
        scrollback: 500,
        convertEol: true,
        cursorBlink: false,
        disableStdin: true,
        cols: 80,
        rows: 6,
    });
    mapTerm.open(document.getElementById('mapTerminal'));

    // ─── 启动 ───
    loadSettings();
    connect();
})();
</script>
</body>
</html>
"""

# ═══════════════════════════════════════════
#  Telnet 协议常量
# ═══════════════════════════════════════════

IAC  = 0xFF
DONT = 0xFE
DO   = 0xFD
WONT = 0xFC
WILL = 0xFB
SB   = 0xFA
SE   = 0xF0
NOP  = 0xF1

# Telnet 选项
OPT_ECHO  = 0x01
OPT_SGA   = 0x03
OPT_TTYPE = 0x18
OPT_NAWS  = 0x1F
OPT_GMCP  = 0x59
OPT_MXP   = 0x5B


# ═══════════════════════════════════════════
#  Telnet 协议处理
# ═══════════════════════════════════════════

async def strip_iac_and_respond(data, writer):
    """剥离 Telnet IAC 序列，同时回应协商请求。返回清理后的字节。"""
    buf = bytearray(data)
    out = bytearray()
    i = 0

    while i < len(buf):
        if buf[i] == 0xFF and i + 1 < len(buf):
            cmd = buf[i + 1]

            # IAC IAC → 转义的 0xFF
            if cmd == 0xFF:
                out.append(0xFF)
                i += 2
                continue

            # 2 字节命令 (SE, NOP, DM, BRK, GA)
            if cmd in (0xF0, 0xF1, 0xF2, 0xF3, 0xF4):
                i += 2
                continue

            # 3 字节命令: WILL / WONT / DO / DONT
            if cmd in (0xFB, 0xFC, 0xFD, 0xFE) and i + 2 < len(buf):
                opt = buf[i + 2]
                response = _handle_negotiation(cmd, opt)
                if response:
                    writer.write(response)
                    await writer.drain()
                i += 3
                continue

            # 子协商 SB ... SE
            if cmd == 0xFA:
                sub_start = i + 2
                i += 2
                while i < len(buf):
                    if buf[i] == 0xFF and i + 1 < len(buf) and buf[i + 1] == 0xF0:
                        sub_data = bytes(buf[sub_start:i])
                        response = _handle_subnegotiation(sub_data)
                        if response:
                            writer.write(response)
                            await writer.drain()
                        i += 2
                        break
                    i += 1
                continue

            # 未知，跳过
            i += 2
            continue

        out.append(buf[i])
        i += 1

    return bytes(out)


def _telnet_response(*parts):
    """将 int/bytes 混合参数拼接为 bytes"""
    out = bytearray()
    for p in parts:
        if isinstance(p, int):
            out.append(p)
        else:
            out.extend(p)
    return bytes(out)


def _handle_negotiation(cmd, opt):
    """处理 3 字节 Telnet 协商，返回要发送的响应字节

    cmd: int (0xFB-0xFE), opt: int (选项编号)
    """
    # DO → 我们需要 WILL 或 WONT
    if cmd == DO:
        if opt == OPT_SGA:
            return _telnet_response(IAC, WILL, opt)
        if opt == OPT_TTYPE:
            return _telnet_response(IAC, WILL, opt)
        if opt == OPT_NAWS:
            return _telnet_response(IAC, WILL, opt)
        if opt == OPT_MXP:
            return _telnet_response(IAC, WILL, opt)
        if opt == OPT_ECHO:
            return _telnet_response(IAC, DO, opt)
        # 其他一律拒绝
        return _telnet_response(IAC, WONT, opt)

    # WILL → 我们需要 DO 或 DONT
    if cmd == WILL:
        if opt == OPT_ECHO:
            return _telnet_response(IAC, DO, opt)
        if opt == OPT_SGA:
            return _telnet_response(IAC, DO, opt)
        return _telnet_response(IAC, DONT, opt)

    # DONT / WONT → 一律回应
    if cmd == WONT:
        return _telnet_response(IAC, DONT, opt)
    if cmd == DONT:
        return _telnet_response(IAC, WONT, opt)

    return None


def _handle_subnegotiation(sub_data):
    """处理子协商请求 (如 TTYPE SEND)"""
    if not sub_data:
        return None

    opt = sub_data[0]

    # TTYPE SEND → 回复终端类型
    if opt == OPT_TTYPE and len(sub_data) > 1 and sub_data[1] == 0x01:
        return _telnet_response(IAC, SB, OPT_TTYPE, 0x00, b'xterm-256color', IAC, SE)

    return None


# ANSI 转义序列正则（用于清洗聊天消息中的颜色码）
_ANSI_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?\x07')

# 频道中文关键字 → 频道 ID 映射（用于本地屏蔽）
_CHANNEL_MAP = {
    '闲聊': 'chat', 'chat': 'chat',
    '谣言': 'rumor', 'rumor': 'rumor',
    '交易': 'jy', 'jy': 'jy',
    'QQ群': 'qq', 'qq': 'qq', 'QQ群转发': 'qq',
    '帮派': 'group', 'group': 'group',
    '组队': 'team',
    '大喊': 'shout', 'shout': 'shout',
    '回答': 'answer',
}


def _get_channel_id(text):
    """从聊天消息文本中提取频道 ID，无法识别返回 None"""
    for keyword, ch_id in _CHANNEL_MAP.items():
        if keyword in text:
            return ch_id
    # 备用：匹配 (chat) (rumor) 等标记
    for marker in ('(chat)', '(rumor)', '(jy)', '(qq)', '(group)'):
        if marker in text:
            return marker.strip('()')
    return None


# ═══════════════════════════════════════════
#  GBK 分包安全处理
# ═══════════════════════════════════════════

def gbk_safe_split(buf):
    """将 buffer 分为可安全 GBK 解码的部分和可能不完整的尾部"""
    if not buf:
        return bytes(buf), b''

    last = buf[-1]
    # GBK 首字节范围 0x81-0xFE
    if 0x81 <= last <= 0xFE:
        return bytes(buf[:-1]), bytes([last])
    return bytes(buf), b''


# ═══════════════════════════════════════════
#  MUD 会话
# ═══════════════════════════════════════════

class MudSession:
    def __init__(self):
        self.reader = None
        self.writer = None
        self.ws = None
        self.running = False
        self.cmd_history = []
        self.log_dir = os.path.join(os.path.dirname(__file__), config.LOG_DIR)
        self._raw_buf = bytearray()   # 原始字节行缓冲
        self.muted_channels = set()   # 本地屏蔽的频道
        self._minimap_active = False  # 是否正在收集小地图行
        self._minimap_lines = []      # 自动捕获的小地图行
        self.muted_channels = set()   # 本地屏蔽的频道（终端不显示，右侧仍显示）

    async def connect(self):
        """连接 MUD 服务器"""
        self.reader, self.writer = await asyncio.open_connection(
            config.MUD_HOST, config.MUD_PORT
        )
        self.running = True
        print(f"[已连接 MUD 服务器] {config.MUD_HOST}:{config.MUD_PORT}")

    async def run(self, websocket):
        """主循环：WebSocket ↔ MUD 双向桥接"""
        self.ws = websocket

        try:
            await self.connect()

            # 并发执行：读 MUD + 读 WebSocket
            mud_task = asyncio.create_task(self._read_mud_loop())
            ws_task = asyncio.create_task(self._read_ws_loop())
            done, pending = await asyncio.wait(
                [mud_task, ws_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for t in pending:
                t.cancel()
        except Exception as e:
            print(f"[会话错误] {e}")
        finally:
            await self.cleanup()

    async def cleanup(self):
        self.running = False
        if self.writer:
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except Exception:
                pass
        print("[会话已关闭]")

    # ─── 小地图检测辅助函数 ───
    _CLEAN_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\[[0-9]*z|<[^>]+>')
    _BOX_CHARS = set('─│┌┐└┘├┤┬┴┼━┃╭╮╰╯╠╣╦╩╬═║╳⊕｜\uff5c')

    @classmethod
    def _clean_line(cls, text):
        """去除 ANSI 转义码和 MXP 标签，返回纯文本"""
        return cls._CLEAN_RE.sub('', text).strip()

    @classmethod
    def _is_minimap_line(cls, text):
        """判断一行是否是小地图行（包含 box-drawing 连接字符或 ----）"""
        clean = cls._clean_line(text)
        if not clean:
            return False
        if '----' in clean:
            return True
        for ch in clean:
            if ch in cls._BOX_CHARS:
                return True
        return False

    @classmethod
    def _get_room_name(cls, text):
        """如果是房间名行，返回房间名；否则返回 None"""
        clean = cls._clean_line(text)
        if clean and clean.endswith(' -'):
            return clean[:-2].strip()
        return None

    @staticmethod
    def _leading_spaces(text):
        """计算行首空格数（跳过 ANSI 转义码）"""
        n = 0
        i = 0
        while i < len(text):
            if text[i] == '\x1b':
                # skip ANSI sequence
                j = text.find('m', i + 1)
                if j != -1:
                    i = j + 1
                    continue
            if text[i] == ' ':
                n += 1
                i += 1
            else:
                break
        return n

    # ─── 读取 MUD 服务器 ───
    async def _read_mud_loop(self):
        """持续读取 MUD 服务器数据，转发到浏览器"""
        while self.running:
            try:
                data = await self.reader.read(4096)
                if not data:
                    break
            except (ConnectionResetError, OSError):
                break

            # 1. 剥离 Telnet IAC 并回应协商
            clean = await strip_iac_and_respond(data, self.writer)

            # 2. 累积到原始字节缓冲区
            self._raw_buf.extend(clean)

            # 3. 按行分割：只解码完整的行（以 \n 结尾）
            #    这样不会在 GBK 字符中间截断
            while b'\n' in self._raw_buf:
                line_raw, rest = self._raw_buf.split(b'\n', 1)
                self._raw_buf = bytearray(rest)
                line_raw = line_raw.rstrip(b'\r')

                # GBK 解码完整行
                try:
                    line_text = line_raw.decode('gbk')
                except (UnicodeDecodeError, ValueError):
                    line_text = line_raw.decode('gbk', errors='replace')

                # 检测聊天消息
                stripped = line_text.strip()
                is_chat = stripped and is_chat_message(stripped)
                channel_id = _get_channel_id(stripped) if is_chat else None

                # 聊天消息始终推送到右侧面板（不受本地屏蔽影响）
                if is_chat:
                    clean_text = _ANSI_RE.sub('', stripped).strip()
                    msg = json.dumps({
                        'type': 'chat',
                        'data': {
                            'time': datetime.now().strftime('%H:%M:%S'),
                            'text': clean_text,
                        }
                    }, ensure_ascii=False)
                    try:
                        await self.ws.send_text(msg)
                    except Exception:
                        pass

                # 主终端：本地屏蔽的频道不显示
                if channel_id and channel_id in self.muted_channels:
                    pass  # 跳过，不发送到终端
                else:
                    utf8_line = line_text.encode('utf-8') + b'\r\n'
                    try:
                        await self.ws.send_bytes(utf8_line)
                    except Exception:
                        return

                # 记录日志
                self._log_data(line_text, 'recv')

                # 自动小地图捕获：检测每行特征
                if self._is_minimap_line(stripped):
                    if not self._minimap_active:
                        self._minimap_active = True
                        self._minimap_lines = []
                    self._minimap_lines.append(line_text)
                elif self._minimap_active:
                    room_name = self._get_room_name(stripped)
                    if room_name is not None:
                        self._minimap_lines.append(line_text)
                        if self._minimap_lines:
                            map_text = '\n'.join(self._minimap_lines) + '\n'
                            map_msg = {'type': 'map', 'data': map_text}
                            area_info = config.ROOM_TO_AREA.get(room_name)
                            if area_info:
                                map_msg['area'] = {'code': area_info[0], 'name': area_info[1]}
                            msg = json.dumps(map_msg, ensure_ascii=False)
                            try:
                                await self.ws.send_text(msg)
                            except Exception:
                                pass
                            _rt_log(f'[MAP] 自动小地图，{len(self._minimap_lines)} 行'
                                    f'{f" · {area_info[1]}" if area_info else ""}')
                        self._minimap_active = False
                        self._minimap_lines = []
                    elif self._leading_spaces(line_text) >= 10:
                        # 高缩进的纯文本行也是地图内容（相邻房间名等）
                        self._minimap_lines.append(line_text)
                    else:
                        self._minimap_active = False
                        self._minimap_lines = []

            # 4. 处理缓冲区中剩余的不完整行（提示符等，无 \n 结尾）
            if self._raw_buf:
                # 确保不在 GBK 字符中间截断
                safe, rest = gbk_safe_split(self._raw_buf)
                self._raw_buf = bytearray(rest)
                if safe:
                    try:
                        text = safe.decode('gbk')
                    except (UnicodeDecodeError, ValueError):
                        text = safe.decode('gbk', errors='replace')

                    utf8_bytes = text.encode('utf-8')
                    try:
                        await self.ws.send_bytes(utf8_bytes)
                    except Exception:
                        return

                    self._log_data(text, 'recv')

                    # 检测编码选择提示
                    if 'Input 1 for GBK' in text:
                        await asyncio.sleep(0.3)
                        self.writer.write(b'1\r\n')
                        await self.writer.drain()

            # 5. 兼容：检测编码选择提示（行内匹配）
            if b'Input 1 for GBK' in clean:
                await asyncio.sleep(0.3)
                self.writer.write(b'1\r\n')
                await self.writer.drain()

            # 6. 自动跳过 MXP 检测兜底
            if b'MXP' in clean:
                for seg in clean.split(b'\n'):
                    try:
                        t = seg.decode('gbk', errors='replace')
                    except Exception:
                        continue
                    if 'MXP' in t and '\u6309\u56de\u8f66' in t:
                        await asyncio.sleep(0.5)
                        self.writer.write(b'\r\n')
                        await self.writer.drain()

    # ─── 读取浏览器 WebSocket ───
    async def _read_ws_loop(self):
        """持续读取浏览器 WebSocket 消息，转发到 MUD 服务器"""
        while self.running:
            try:
                msg = await self.ws.receive()
            except Exception:
                break

            if msg.get('type') == 'websocket.disconnect':
                break

            if msg.get('bytes'):
                # 二进制数据 → 原始转发
                data = bytes(msg['bytes'])
                self.writer.write(data)
                await self.writer.drain()
                # 尝试解码用于日志
                try:
                    text = data.decode('utf-8', errors='replace')
                    self._log_data(text, 'send')
                except Exception:
                    pass
                continue

            text_data = msg.get('text', '')
            if not text_data:
                continue

            # JSON 消息（命令历史追踪 / MXP 回复 / 频道屏蔽）
            if text_data.startswith('{'):
                try:
                    j = json.loads(text_data)
                    if j.get('type') == 'command':
                        self._add_history(j['data'])
                    elif j.get('type') == 'mxp_reply':
                        reply = j.get('data', '')
                        if reply:
                            self.writer.write(reply.encode('gbk', errors='replace'))
                            await self.writer.drain()
                    elif j.get('type') == 'mute_channels':
                        self.muted_channels = set(j.get('data', []))
                except (json.JSONDecodeError, KeyError):
                    pass
                continue

            # 普通文本 → 转码为 GBK 发送到 MUD
            try:
                data = text_data.encode('gbk')
            except Exception:
                data = text_data.encode('utf-8', errors='replace')

            self.writer.write(data)
            await self.writer.drain()
            self._log_data(text_data, 'send')

    # ─── 命令历史 ───
    def _add_history(self, cmd):
        """添加命令到历史，保持最近 20 条"""
        if not cmd or not cmd.strip():
            return
        cmd = cmd.strip()
        # 去重：如果和最后一条相同则跳过
        if self.cmd_history and self.cmd_history[-1] == cmd:
            return
        self.cmd_history.append(cmd)
        if len(self.cmd_history) > 20:
            self.cmd_history = self.cmd_history[-20:]

        # 推送到浏览器
        msg = json.dumps({
            'type': 'history',
            'data': self.cmd_history,
        }, ensure_ascii=False)

        async def _send():
            try:
                await self.ws.send_text(msg)
            except Exception:
                pass

        asyncio.create_task(_send())

    # ─── 日志 ───
    def _log_data(self, text, direction):
        """记录日志（与 proxy.py 格式一致）"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        marker = '>>>' if direction == 'send' else '<<<'
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_path = os.path.join(self.log_dir, f'{date_str}_raw.log')

        text = text.replace('\r\n', '\n').replace('\r', '\n')
        try:
            with open(log_path, 'a', encoding=config.LOG_ENCODING) as f:
                for line in text.split('\n'):
                    if line.strip():
                        f.write(f'[{timestamp}] {marker} {line}\n')
        except Exception:
            pass

        # 运行时日志
        for line in text.split('\n'):
            stripped = line.strip()
            if stripped:
                _rt_log(f'[{marker}] {stripped[:500]}')


# ═══════════════════════════════════════════
#  Starlette 路由
# ═══════════════════════════════════════════

from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.responses import HTMLResponse


async def index_page(request):
    return HTMLResponse(HTML_PAGE)


async def websocket_handler(websocket):
    _rt_log('[WS] 新连接')
    await websocket.accept()
    session = MudSession()
    await session.run(websocket)
    _rt_log('[WS] 连接结束')


routes = [
    Route('/', endpoint=index_page),
    WebSocketRoute('/ws', endpoint=websocket_handler),
]

app = Starlette(routes=routes)


# ═══════════════════════════════════════════
#  运行时日志（每次启动覆盖）
# ═══════════════════════════════════════════

_runtime_log_path = os.path.join(os.path.dirname(__file__), config.LOG_DIR, 'runtime.log')
_runtime_log_file = None


def _rt_log(msg):
    """写入运行时日志"""
    global _runtime_log_file
    if _runtime_log_file is None:
        return
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    try:
        _runtime_log_file.write(f'[{timestamp}] {msg}\n')
        _runtime_log_file.flush()
    except Exception:
        pass


def _init_runtime_log():
    """初始化运行时日志文件（覆盖模式）"""
    global _runtime_log_file
    os.makedirs(os.path.dirname(_runtime_log_path), exist_ok=True)
    _runtime_log_file = open(_runtime_log_path, 'w', encoding='utf-8')
    _rt_log('=== 运行时日志启动 ===')


def _close_runtime_log():
    """关闭运行时日志文件"""
    global _runtime_log_file
    if _runtime_log_file:
        _rt_log('=== 运行时日志结束 ===')
        _runtime_log_file.close()
        _runtime_log_file = None

def run_server():
    import uvicorn

    host = '127.0.0.1'
    port = 58080

    _init_runtime_log()
    _rt_log(f'服务器启动 http://{host}:{port}')
    _rt_log(f'MUD 服务器: {config.MUD_HOST}:{config.MUD_PORT}')
    _rt_log(f'运行时日志: {_runtime_log_path}')

    print('=' * 50)
    print('  MUD Web 客户端')
    print('=' * 50)
    print()
    print(f'  浏览器访问: http://{host}:{port}')
    print(f'  MUD 服务器: {config.MUD_HOST}:{config.MUD_PORT}')
    print(f'  运行时日志: {_runtime_log_path}')
    print()
    print('  即将自动打开浏览器...')
    print()

    # 延迟打开浏览器（等服务器启动）
    def open_browser():
        import time
        time.sleep(1.5)
        webbrowser.open(f'http://{host}:{port}')

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        uvicorn.run(app, host=host, port=port, log_level='warning')
    finally:
        _close_runtime_log()
