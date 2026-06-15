(function() {
    // ─── 终端初始化 ───
    const term = new Terminal({
        fontSize: 15,
        fontFamily: '"Sarasa Mono SC", "Cascadia Mono", "Microsoft YaHei Mono", Consolas, monospace',
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
        lineHeight: 1.12,
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
    const scrollBottomBtn = document.getElementById('scrollBottomBtn');
    const quickCommandSuggestEl = document.getElementById('quickCommandSuggest');
    const btnTriggers = document.getElementById('btnTriggers');
    const fullmePanel = document.getElementById('fullmePanel');
    const fullmeImage = document.getElementById('fullmeImage');
    const fullmeFrame = document.getElementById('fullmeFrame');
    const fullmeSource = document.getElementById('fullmeSource');
    const fullmeInput = document.getElementById('fullmeInput');
    const fullmeCommandMode = document.getElementById('fullmeCommandMode');
    const fullmeSubmitBtn = document.getElementById('fullmeSubmitBtn');
    const fullmeCloseBtn = document.getElementById('fullmeCloseBtn');
    const fullmeRefreshBtn = document.getElementById('fullmeRefreshBtn');
    const fullmeCopyUrlBtn = document.getElementById('fullmeCopyUrlBtn');
    const fullmeOpenUrlBtn = document.getElementById('fullmeOpenUrlBtn');
    const triggerPanel = document.getElementById('triggerPanel');
    const toolbarTriggerCurrentNameEl = document.getElementById('toolbarTriggerCurrentName');
    const triggerCurrentNameEl = document.getElementById('triggerCurrentName');
    const triggerListEl = document.getElementById('triggerList');
    const triggerDetailEl = document.getElementById('triggerDetail');
    const triggerLoadBtn = document.getElementById('triggerLoadBtn');
    const triggerDeleteBtn = document.getElementById('triggerDeleteBtn');
    const triggerNameEl = document.getElementById('triggerName');
    const triggerNotesEl = document.getElementById('triggerNotes');
    const triggerRulesEl = document.getElementById('triggerRules');
    const triggerNewBtn = document.getElementById('triggerNewBtn');
    const triggerCopyBtn = document.getElementById('triggerCopyBtn');
    const triggerAddRuleBtn = document.getElementById('triggerAddRuleBtn');
    const triggerSaveBtn = document.getElementById('triggerSaveBtn');
    const triggerStopBtn = document.getElementById('triggerStopBtn');
    const triggerStatusEl = document.getElementById('triggerStatus');
    const quickCommandButtonsEl = document.getElementById('quickCommandButtons');
    const quickCommandCurrentNameEl = document.getElementById('quickCommandCurrentName');
    const quickCommandDetailEl = document.getElementById('quickCommandDetail');
    const quickCommandListEl = document.getElementById('quickCommandList');
    const quickCommandNewBtn = document.getElementById('quickCommandNewBtn');
    const quickCommandCopyBtn = document.getElementById('quickCommandCopyBtn');
    const quickCommandAddStepBtn = document.getElementById('quickCommandAddStepBtn');
    const quickCommandSaveBtn = document.getElementById('quickCommandSaveBtn');
    const quickCommandDeleteBtn = document.getElementById('quickCommandDeleteBtn');
    const quickCommandStatusEl = document.getElementById('quickCommandStatus');
    const quickCommandNameEl = document.getElementById('quickCommandName');
    const quickCommandAliasEl = document.getElementById('quickCommandAlias');
    const quickCommandNotesEl = document.getElementById('quickCommandNotes');
    const quickCommandStepsEl = document.getElementById('quickCommandSteps');
    let triggerItems = [];
    let selectedTriggerId = '';
    let activeTriggerId = '';
    let quickCommandItems = [];
    let selectedQuickCommandId = '';
    let selectedQuickCommandPinned = true;
    let pendingQuickCommandPinnedId = '';
    let quickCommandSuggestionItems = [];
    let quickCommandSuggestionIndex = 0;
    let chatInitialized = false;
    let fullmePendingMode = 'report';
    let fullmeCurrentUrl = '';
    let fullmeCurrentImageUrl = '';

    function setStatus(connected) {
        statusDot.className = 'status-dot' + (connected ? ' connected' : '');
        statusText.textContent = connected ? '已连接' : '未连接';
    }

    // ─── WebSocket ───
    function sanitizeTerminalText(text) {
        return String(text).replace(/[\x00-\x1f\x7f-\x9f]/g, '');
    }

    function showSentCommand(cmd) {
        const visibleCmd = sanitizeTerminalText(cmd).trim();
        if (!visibleCmd) return;
        term.writeln('\r\n\x1b[48;5;236m\x1b[38;5;220m\x1b[1m[CMD]\x1b[0m \x1b[38;5;220m' + visibleCmd + '\x1b[0m\r\n');
    }

    function sendMudCommand(cmd) {
        if (!cmd.trim() || !ws || ws.readyState !== WebSocket.OPEN) return false;
        const cleanCmd = cmd.trim();
        if (/^fullme(?:\s|$)/i.test(cleanCmd)) {
            fullmePendingMode = 'fullme';
        } else if (/^(?:report|reprot)(?:\s|$)/i.test(cleanCmd) || /^ask\s+.+\s+about\s+(?:job|工作|口令)/i.test(cleanCmd)) {
            fullmePendingMode = 'report';
        }
        showSentCommand(cmd);
        ws.send(cmd + '\r');
        ws.send(JSON.stringify({ type: 'command', data: cleanCmd }));
        return true;
    }

    function updateFullmeModeFromText(text) {
        const clean = sanitizeTerminalText(text);
        if (/fullme\s+验证码|请输入你看到的图片上的内容/.test(clean)) {
            fullmePendingMode = 'fullme';
            return;
        }
        if (/记住你的工号|report\s+口令|报上你的口令/.test(clean)) {
            fullmePendingMode = 'report';
        }
    }

    function isFullmeUrl(url) {
        try {
            const host = new URL(String(url || '').replace(/&amp;/g, '&'), location.href).hostname.toLowerCase();
            return host === 'fullme.pkuxkx.net'
                || host === 'fullme.pkuxkx.com'
                || (host.startsWith('fullme.') && host.endsWith('.pkuxkx.com'))
                || host.endsWith('.fullme.pkuxkx.com');
        } catch (e) {
            return false;
        }
    }

    function proxyFullmeUrl(url) {
        return '/fullme-proxy?url=' + encodeURIComponent(String(url || '').replace(/&amp;/g, '&'));
    }

    function cacheBustUrl(url) {
        const value = String(url || '').replace(/&amp;/g, '&');
        if (!value) return '';
        try {
            const parsed = new URL(value, location.href);
            parsed.searchParams.set('_refresh', Date.now().toString());
            return parsed.href;
        } catch (e) {
            return value + (value.indexOf('?') === -1 ? '?' : '&') + '_refresh=' + Date.now();
        }
    }

    function pageUrlFromFullmeUrl(url) {
        const value = String(url || '').replace(/&amp;/g, '&');
        if (!value) return '';
        try {
            const parsed = new URL(value, location.href);
            if (!isFullmeUrl(parsed.href)) return value;
            const jpgMatch = parsed.pathname.match(/\/zmud\/([^/?#]+)\.jpg$/i);
            if (jpgMatch) {
                parsed.pathname = '/robot.php';
                parsed.search = '?filename=' + encodeURIComponent(decodeURIComponent(jpgMatch[1]));
                parsed.hash = '';
                return parsed.href;
            }
            return parsed.href;
        } catch (e) {
            return value;
        }
    }

    function imageUrlFromFullmeUrl(url) {
        const value = String(url || '').replace(/&amp;/g, '&');
        if (!value) return '';
        try {
            const parsed = new URL(value, location.href);
            if (/\/zmud\/[^/?#]+\.jpg$/i.test(parsed.pathname)) return parsed.href;
            const match = parsed.search.match(/[?&]filename=([^&#]+)/i);
            if (match && isFullmeUrl(parsed.href)) {
                parsed.pathname = '/zmud/' + encodeURIComponent(decodeURIComponent(match[1])) + '.jpg';
                parsed.search = '';
                parsed.hash = '';
                return parsed.href;
            }
            return parsed.href;
        } catch (e) {
            return value;
        }
    }

    function showFullmePanel(url, imageUrl, mode) {
        const sourceUrl = String(url || imageUrl || '').replace(/&amp;/g, '&');
        const resolvedImageUrl = imageUrlFromFullmeUrl(imageUrl || sourceUrl);
        const pageUrl = pageUrlFromFullmeUrl(sourceUrl || resolvedImageUrl);
        if (!resolvedImageUrl && !pageUrl) return;

        fullmeCurrentUrl = pageUrl || sourceUrl || resolvedImageUrl;
        fullmeCurrentImageUrl = resolvedImageUrl;
        fullmeSource.textContent = fullmeCurrentUrl;
        fullmeCommandMode.value = mode || fullmePendingMode || 'report';
        fullmeInput.value = '';
        fullmeFrame.hidden = true;
        fullmeFrame.removeAttribute('src');
        fullmeImage.hidden = false;
        fullmeImage.src = isFullmeUrl(resolvedImageUrl) ? proxyFullmeUrl(resolvedImageUrl) : resolvedImageUrl;
        fullmePanel.classList.add('visible');
        fullmePanel.setAttribute('aria-hidden', 'false');
        setTimeout(function() { fullmeInput.focus(); }, 0);
    }

    fullmeImage.addEventListener('error', function() {
        if (!fullmeCurrentUrl || !isFullmeUrl(fullmeCurrentUrl)) return;
        fullmeImage.hidden = true;
        fullmeFrame.hidden = false;
        fullmeFrame.src = proxyFullmeUrl(fullmeCurrentUrl);
    });

    function inspectFullmeText(text) {
        updateFullmeModeFromText(text);

        const imgMatch = String(text).match(/<img\b[^>]*\bsrc=(?:"([^"]+)"|'([^']+)'|(\S+))[^>]*>/i);
        if (imgMatch) {
            const imgUrl = imgMatch[1] || imgMatch[2] || imgMatch[3] || '';
            if (isFullmeUrl(imgUrl)) {
                showFullmePanel(imgUrl, imgUrl, fullmePendingMode);
                return;
            }
        }

        const urlMatch = String(text).match(/https?:\/\/(?:fullme\.pkuxkx\.net|fullme\.pkuxkx\.com|fullme\.[a-z0-9-]+\.pkuxkx\.com|[a-z0-9-]+\.fullme\.pkuxkx\.com)\/[^\s<>"']+/i);
        if (urlMatch) {
            showFullmePanel(urlMatch[0], imageUrlFromFullmeUrl(urlMatch[0]), fullmePendingMode);
        }
    }

    function connect() {
        const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
        ws = new WebSocket(proto + '//' + location.host + '/ws');
        ws.binaryType = 'arraybuffer';

        ws.onopen = function() {
            setStatus(true);
            term.writeln('\x1b[32m[已连接到 MUD 服务器]\x1b[0m\r\n');
            cmdInput.focus();
            syncMutedToBackend();
            sendTriggerMessage('list');
            loadQuickCommands();
        };

        ws.onmessage = function(event) {
            if (event.data instanceof ArrayBuffer) {
                // 终端数据 (UTF-8 文本 + ANSI + MXP 标签)
                const text = new TextDecoder('utf-8').decode(event.data);
                inspectFullmeText(text);
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
                    } else if (msg.type === 'trigger_list') {
                        handleTriggerList(msg);
                    } else if (msg.type === 'trigger_status') {
                        handleTriggerStatus(msg);
                    } else if (msg.type === 'trigger_event') {
                        handleTriggerEvent(msg);
                    } else if (msg.type === 'quick_command_list') {
                        handleQuickCommandList(msg);
                    } else if (msg.type === 'quick_command_status') {
                        handleQuickCommandStatus(msg);
                    } else if (msg.type === 'quick_command_event') {
                        handleQuickCommandEvent(msg);
                    } else if (msg.type === 'map') {
                        // 地图数据 → 渲染到地图面板（垂直居中）
                        mapTerm.clear();
                        var mapLines = msg.data.split('\n').filter(function(l) { return l.trim(); });
                        var totalRows = mapTerm.rows;
                        var padding = Math.max(0, Math.floor((totalRows - mapLines.length) / 2));
                        for (var pi = 0; pi < padding; pi++) {
                            mapTerm.writeln('');
                        }
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
        const quickCommandItem = getExactQuickCommandFromInput(cmd);
        if (quickCommandItem) {
            if (!executeQuickCommandItem(quickCommandItem)) return;
            inputHistory.push(cmd);
            historyIndex = -1;
            savedDraft = '';
            cmdInput.value = '';
            hideQuickCommandSuggestions();
            return;
        }
        const quickCommandQuery = getQuickCommandQueryFromInput(cmd);
        if (quickCommandQuery !== null) {
            setQuickCommandStatus('未找到快捷命令：$' + quickCommandQuery, 'error');
            renderQuickCommandSuggestions();
            return;
        }
        if (!sendMudCommand(cmd)) return;

        // 本地输入历史
        inputHistory.push(cmd);
        historyIndex = -1;
        savedDraft = '';
        cmdInput.value = '';
        hideQuickCommandSuggestions();
    }

    sendBtn.addEventListener('click', sendCommand);

    quickCommandSuggestEl.addEventListener('mousedown', function(e) {
        var itemEl = e.target.closest('.quick-command-suggest-item');
        if (!itemEl) return;
        e.preventDefault();
        executeQuickCommandSuggestionById(itemEl.getAttribute('data-id'));
    });

    scrollBottomBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        term.scrollToBottom();
        cmdInput.focus();
    });

    cmdInput.addEventListener('input', function() {
        historyIndex = -1;
        savedDraft = '';
        renderQuickCommandSuggestions();
    });

    cmdInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (executeSelectedQuickCommandSuggestion()) return;
            sendCommand();
        } else if (e.key === 'ArrowUp') {
            if (!quickCommandSuggestEl.hidden) {
                e.preventDefault();
                moveQuickCommandSuggestion(-1);
                return;
            }
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
            renderQuickCommandSuggestions();
        } else if (e.key === 'ArrowDown') {
            if (!quickCommandSuggestEl.hidden) {
                e.preventDefault();
                moveQuickCommandSuggestion(1);
                return;
            }
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
            renderQuickCommandSuggestions();
        } else if (e.key === 'Escape' && !quickCommandSuggestEl.hidden) {
            e.preventDefault();
            hideQuickCommandSuggestions();
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
                                    sendMudCommand(link.command);
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

            // <IMG src="..."> → fullme 图片显示，其他图片忽略
            if (text[i] === '<' && isTagWithAttrs(text, i, 'IMG')) {
                const gtIdx = text.indexOf('>', i);
                if (gtIdx !== -1) {
                    const attrStr = text.substring(i + 4, gtIdx).trim();
                    const attrs = parseMxpAttrs(attrStr);
                    const imgUrl = attrs.src || attrs._pos0 || '';
                    if (isFullmeUrl(imgUrl)) {
                        showFullmePanel(imgUrl, imgUrl, fullmePendingMode);
                    }
                    i = gtIdx + 1;
                    continue;
                }
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

    // ─── fullme 工号 / 验证码面板 ───
    function hideFullmePanel() {
        fullmePanel.classList.remove('visible');
        fullmePanel.setAttribute('aria-hidden', 'true');
        fullmeInput.value = '';
    }

    function submitFullmeCode() {
        const code = fullmeInput.value.trim();
        if (!code) {
            fullmeInput.focus();
            return;
        }
        const mode = fullmeCommandMode.value === 'fullme' ? 'fullme' : 'report';
        if (sendMudCommand(mode + ' ' + code)) {
            hideFullmePanel();
        }
    }

    function refreshFullmeImage() {
        const imageUrl = fullmeCurrentImageUrl || imageUrlFromFullmeUrl(fullmeCurrentUrl);
        const pageUrl = fullmeCurrentUrl || pageUrlFromFullmeUrl(imageUrl);
        if (!imageUrl && !pageUrl) return;

        const refreshedImageUrl = cacheBustUrl(imageUrl || pageUrl);
        fullmeInput.focus();

        if (!fullmeImage.hidden && refreshedImageUrl) {
            fullmeImage.src = isFullmeUrl(refreshedImageUrl)
                ? proxyFullmeUrl(refreshedImageUrl)
                : refreshedImageUrl;
            return;
        }

        const refreshedPageUrl = cacheBustUrl(pageUrl || imageUrl);
        if (refreshedPageUrl) {
            fullmeFrame.src = isFullmeUrl(refreshedPageUrl)
                ? proxyFullmeUrl(refreshedPageUrl)
                : refreshedPageUrl;
        }
    }

    fullmeCloseBtn.addEventListener('click', hideFullmePanel);
    fullmeSubmitBtn.addEventListener('click', submitFullmeCode);
    fullmeRefreshBtn.addEventListener('click', refreshFullmeImage);
    fullmeInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            submitFullmeCode();
        } else if (e.key === 'Escape') {
            e.preventDefault();
            hideFullmePanel();
        }
    });
    fullmeCopyUrlBtn.addEventListener('click', function() {
        const url = fullmeCurrentUrl || fullmeCurrentImageUrl;
        if (!url) return;
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(url).catch(function() {});
        }
    });
    fullmeOpenUrlBtn.addEventListener('click', function() {
        const url = fullmeCurrentUrl || fullmeCurrentImageUrl;
        if (url) window.open(url, '_blank', 'noopener');
    });

    // ─── 工具函数 ───
    function escapeHtml(s) {
        const div = document.createElement('div');
        div.textContent = String(s == null ? '' : s);
        return div.innerHTML;
    }
    function escapeAttr(s) {
        return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
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

    // ─── 触发器 ───
    function setTriggerStatus(text, kind) {
        triggerStatusEl.textContent = text || '';
        triggerStatusEl.className = 'trigger-status' + (kind ? ' ' + kind : '');
        triggerStatusEl.classList.remove('flash');
        void triggerStatusEl.offsetWidth;
        triggerStatusEl.classList.add('flash');
    }

    function sendTriggerMessage(action, data) {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            setTriggerStatus('未连接，无法操作', 'error');
            return;
        }
        ws.send(JSON.stringify(Object.assign({ type: 'trigger', action: action }, data || {})));
    }

    function setQuickCommandStatus(text, kind) {
        quickCommandStatusEl.textContent = text || '';
        quickCommandStatusEl.className = 'trigger-status' + (kind ? ' ' + kind : '');
        quickCommandStatusEl.classList.remove('flash');
        void quickCommandStatusEl.offsetWidth;
        quickCommandStatusEl.classList.add('flash');
    }

    function sendQuickCommandMessage(action, data) {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            setQuickCommandStatus('未连接，无法操作', 'error');
            return false;
        }
        ws.send(JSON.stringify(Object.assign({ type: 'quick_command', action: action }, data || {})));
        return true;
    }

    function loadQuickCommands() {
        return sendQuickCommandMessage('list');
    }

    function saveQuickCommandConfig(id, config, options) {
        options = options || {};
        setQuickCommandStatus(options.status || '正在保存快捷命令', 'ok');
        return sendQuickCommandMessage('save', { id: id || '', config: config });
    }

    function deleteQuickCommandConfig(id) {
        setQuickCommandStatus('正在删除快捷命令', 'ok');
        return sendQuickCommandMessage('delete', { id: id || '' });
    }

    function addTriggerRule(keyword, command, delay) {
        const row = document.createElement('div');
        row.className = 'trigger-rule-row';
        row.innerHTML =
            '<input type="text" class="trigger-keyword" placeholder="消息关键词" value="' + escapeAttr(keyword || '') + '">' +
            '<input type="text" class="trigger-command" placeholder="发送指令" value="' + escapeAttr(command || '') + '">' +
            '<input type="number" class="trigger-delay" placeholder="延时秒" min="0" max="3600" step="0.1" value="' + escapeAttr(delay || '') + '">' +
            '<button class="trigger-small-btn danger trigger-rule-delete" type="button">×</button>';
        triggerRulesEl.appendChild(row);
    }

    function clearTriggerForm() {
        triggerNameEl.value = '';
        triggerNotesEl.value = '';
        triggerRulesEl.innerHTML = '';
        addTriggerRule('', '');
    }

    function startNewTrigger() {
        selectedTriggerId = '';
        clearTriggerForm();
        triggerDetailEl.textContent = '正在新建触发器';
        triggerDetailEl.classList.remove('flash');
        void triggerDetailEl.offsetWidth;
        triggerDetailEl.classList.add('flash');
        triggerLoadBtn.disabled = true;
        triggerDeleteBtn.disabled = true;
        triggerCopyBtn.disabled = true;
        triggerListEl.querySelectorAll('.trigger-item').forEach(function(el) {
            el.classList.remove('active');
        });
        setTriggerStatus('正在新建触发器', 'ok');
    }

    function fillTriggerForm(config) {
        config = config || {};
        triggerNameEl.value = config.name || '';
        triggerNotesEl.value = config.notes || '';
        triggerRulesEl.innerHTML = '';
        const rules = config.rules || [];
        if (!rules.length) addTriggerRule('', '');
        rules.forEach(function(rule) {
            addTriggerRule(rule.keyword, rule.command, rule.delay || '');
        });
    }

    function getTriggerFormConfig() {
        const rules = [];
        let hasNegativeDelay = false;
        triggerRulesEl.querySelectorAll('.trigger-rule-row').forEach(function(row) {
            const keyword = row.querySelector('.trigger-keyword').value.trim();
            const command = row.querySelector('.trigger-command').value.trim();
            const delayRaw = row.querySelector('.trigger-delay').value.trim();
            let delay = parseFloat(delayRaw);
            if (Number.isFinite(delay) && delay < 0) {
                hasNegativeDelay = true;
                row.querySelector('.trigger-delay').focus();
                return;
            }
            if (!Number.isFinite(delay)) delay = 0;
            if (delay > 3600) delay = 3600;
            if (keyword || command) rules.push({ keyword: keyword, command: command, delay: delay });
        });
        if (hasNegativeDelay) {
            return null;
        }
        return {
            name: triggerNameEl.value.trim(),
            notes: triggerNotesEl.value,
            rules: rules,
        };
    }

    function formatTriggerDetail(config) {
        if (!config) return '选择一个触发器查看详情';
        const lines = [
            '名称: ' + (config.name || ''),
            '分支数: ' + ((config.rules || []).length),
            '',
            '规则:',
        ];
        (config.rules || []).forEach(function(rule, index) {
            const delay = Number(rule.delay || 0);
            const suffix = delay > 0 ? '（延时 ' + delay + ' 秒）' : '';
            lines.push((index + 1) + '. ' + rule.keyword + ' -> ' + rule.command + suffix);
        });
        if (config.notes) {
            lines.push('', '备注:', config.notes);
        }
        return lines.join('\n');
    }

    function updateActiveTriggerDisplay() {
        var item = triggerItems.find(function(x) { return x.id === activeTriggerId; });
        setActiveTriggerDisplay(activeTriggerId ? ((item && item.name) || activeTriggerId) : '无');
    }

    function setActiveTriggerDisplay(name) {
        var text = name || '无';
        triggerCurrentNameEl.textContent = text;
        toolbarTriggerCurrentNameEl.textContent = text;
    }

    function renderTriggerList(items) {
        triggerItems = items || [];
        updateActiveTriggerDisplay();
        if (!triggerItems.length) {
            triggerListEl.innerHTML = '<div class="empty-hint">暂无触发器</div>';
            triggerDetailEl.textContent = '选择一个触发器查看详情';
            triggerLoadBtn.disabled = true;
            triggerDeleteBtn.disabled = true;
            triggerCopyBtn.disabled = true;
            selectedTriggerId = '';
            return;
        }
        triggerListEl.innerHTML = triggerItems.map(function(item) {
            var cls = '';
            if (item.id === activeTriggerId) cls += ' loaded';
            if (item.id === selectedTriggerId) cls += ' active';
            var badge = item.id === activeTriggerId ? '<span class="trigger-loaded-badge">已加载</span>' : '';
            return '<div class="trigger-item' + cls + '" data-id="' + escapeAttr(item.id) + '">' +
                '<div class="trigger-item-title"><span class="trigger-item-name">' + escapeHtml(item.name || item.id) + '</span>' + badge + '</div>' +
                '<div class="trigger-item-meta">' + item.rules_count + ' 个分支</div>' +
                '</div>';
        }).join('');
        triggerListEl.querySelectorAll('.trigger-item').forEach(function(el, index) {
            el.classList.add('list-enter');
            el.style.animationDelay = Math.min(index * 18, 180) + 'ms';
        });
        triggerLoadBtn.disabled = !selectedTriggerId || (selectedTriggerId === activeTriggerId);
    }

    function selectTrigger(id) {
        selectedTriggerId = id || '';
        var item = triggerItems.find(function(x) { return x.id === selectedTriggerId; });
        triggerDetailEl.textContent = formatTriggerDetail(item && item.config);
        triggerDetailEl.classList.remove('flash');
        void triggerDetailEl.offsetWidth;
        triggerDetailEl.classList.add('flash');
        if (item && item.config) fillTriggerForm(item.config);
        triggerDeleteBtn.disabled = !item;
        triggerLoadBtn.disabled = !item || (selectedTriggerId === activeTriggerId);
        triggerCopyBtn.disabled = !item;
        triggerListEl.querySelectorAll('.trigger-item').forEach(function(el) {
            var elId = el.getAttribute('data-id');
            el.classList.toggle('active', elId === selectedTriggerId);
            var title = el.querySelector('.trigger-item-title');
            if (title) {
                var badge = title.querySelector('.trigger-loaded-badge');
                if (elId === activeTriggerId) {
                    if (!badge) {
                        badge = document.createElement('span');
                        badge.className = 'trigger-loaded-badge';
                        badge.textContent = '已加载';
                        title.appendChild(badge);
                    }
                } else {
                    if (badge) badge.remove();
                }
            }
        });
    }

    function handleTriggerList(msg) {
        activeTriggerId = msg.active_id || '';
        renderTriggerList(msg.items || []);
        if (activeTriggerId && !selectedTriggerId) selectedTriggerId = activeTriggerId;
        if (selectedTriggerId) selectTrigger(selectedTriggerId);
        if (msg.status) setTriggerStatus(msg.status, 'ok');
    }

    function handleTriggerStatus(msg) {
        if (msg.config) fillTriggerForm(msg.config);
        if (msg.id && msg.active) activeTriggerId = msg.id;
        if (msg.active === false) activeTriggerId = '';
        if (msg.id) selectedTriggerId = msg.id;
        if (msg.status) setTriggerStatus(msg.status, msg.ok === false ? 'error' : 'ok');
        if (msg.active === false) {
            setActiveTriggerDisplay('无');
        } else if (msg.id && msg.active && msg.config) {
            setActiveTriggerDisplay(msg.config.name || msg.id);
        } else {
            updateActiveTriggerDisplay();
        }
        renderTriggerList(triggerItems);
        if (activeTriggerId && !selectedTriggerId) selectedTriggerId = activeTriggerId;
        if (selectedTriggerId) selectTrigger(selectedTriggerId);
    }

    function handleTriggerEvent(msg) {
        if (msg.command) showSentCommand(msg.command);
    }

    function normalizeQuickCommandAlias(alias) {
        return String(alias || '').trim().replace(/^\$+/, '');
    }

    function getQuickCommandAlias(item) {
        if (!item || !item.config) return '';
        return normalizeQuickCommandAlias(item.config.alias || item.alias || '');
    }

    function getQuickCommandSearchText(item) {
        const config = (item && item.config) || {};
        const commands = (config.commands || []).map(function(step) { return step.command || ''; }).join(' ');
        return [
            item && item.id,
            item && item.name,
            config.name,
            config.alias,
            config.notes,
            commands,
        ].join(' ').toLowerCase();
    }

    function quickCommandFuzzyTextMatch(text, query) {
        let pos = 0;
        for (let i = 0; i < query.length; i++) {
            pos = text.indexOf(query[i], pos);
            if (pos === -1) return false;
            pos += 1;
        }
        return true;
    }

    function getQuickCommandMatchRank(item, query) {
        const normalizedQuery = String(query || '').trim().toLowerCase();
        const alias = getQuickCommandAlias(item).toLowerCase();
        if (!alias) return -1;
        if (!normalizedQuery) return 0;
        if (alias.indexOf(normalizedQuery) === 0) return 1;
        if (alias.indexOf(normalizedQuery) !== -1) return 2;
        const text = getQuickCommandSearchText(item);
        if (text.indexOf(normalizedQuery) !== -1) return 3;
        return quickCommandFuzzyTextMatch(text, normalizedQuery) ? 4 : -1;
    }

    function getQuickCommandMatches(query) {
        return quickCommandItems.map(function(item, index) {
            return {
                item: item,
                index: index,
                rank: getQuickCommandMatchRank(item, query),
            };
        }).filter(function(entry) {
            return entry.rank >= 0;
        }).sort(function(a, b) {
            if (a.rank !== b.rank) return a.rank - b.rank;
            const aliasA = getQuickCommandAlias(a.item).toLowerCase();
            const aliasB = getQuickCommandAlias(b.item).toLowerCase();
            if (aliasA !== aliasB) return aliasA < aliasB ? -1 : 1;
            return a.index - b.index;
        }).slice(0, 8).map(function(entry) {
            return entry.item;
        });
    }

    function getQuickCommandQueryFromInput(value) {
        const text = String(value || '').trim();
        if (!text.startsWith('$')) return null;
        return text.slice(1).trim();
    }

    function findQuickCommandByAlias(alias) {
        const normalizedAlias = normalizeQuickCommandAlias(alias).toLowerCase();
        if (!normalizedAlias) return null;
        return quickCommandItems.find(function(item) {
            return getQuickCommandAlias(item).toLowerCase() === normalizedAlias;
        }) || null;
    }

    function findDuplicateQuickCommandAlias(alias, currentId) {
        const normalizedAlias = normalizeQuickCommandAlias(alias).toLowerCase();
        if (!normalizedAlias) return null;
        return quickCommandItems.find(function(item) {
            if (currentId && item.id === currentId) return false;
            return getQuickCommandAlias(item).toLowerCase() === normalizedAlias;
        }) || null;
    }

    function getUniqueQuickCommandName(baseName) {
        const base = String(baseName || '快捷命令').trim() || '快捷命令';
        let candidate = base + '_副本';
        let suffix = 2;
        while (quickCommandItems.some(function(item) {
            return (item.name || item.id) === candidate || item.id === candidate;
        })) {
            candidate = base + '_副本' + suffix;
            suffix += 1;
        }
        return candidate;
    }

    function getUniqueQuickCommandAlias(baseAlias) {
        const base = normalizeQuickCommandAlias(baseAlias) || 'quick';
        let candidate = base + '_copy';
        let suffix = 2;
        while (findQuickCommandByAlias(candidate)) {
            candidate = base + '_copy' + suffix;
            suffix += 1;
        }
        return candidate;
    }

    function getExactQuickCommandFromInput(value) {
        const query = getQuickCommandQueryFromInput(value);
        if (query === null) return null;
        return findQuickCommandByAlias(query);
    }

    function hideQuickCommandSuggestions() {
        quickCommandSuggestEl.hidden = true;
        quickCommandSuggestEl.innerHTML = '';
        quickCommandSuggestionItems = [];
        quickCommandSuggestionIndex = 0;
    }

    function updateQuickCommandSuggestionActive() {
        quickCommandSuggestEl.querySelectorAll('.quick-command-suggest-item').forEach(function(el, index) {
            const active = index === quickCommandSuggestionIndex;
            el.classList.toggle('active', active);
            if (active) el.scrollIntoView({ block: 'nearest' });
        });
    }

    function moveQuickCommandSuggestion(delta) {
        if (!quickCommandSuggestionItems.length) return;
        quickCommandSuggestionIndex = (quickCommandSuggestionIndex + delta + quickCommandSuggestionItems.length) % quickCommandSuggestionItems.length;
        updateQuickCommandSuggestionActive();
    }

    function executeQuickCommandSuggestionItem(item) {
        if (!item) return false;
        const alias = getQuickCommandAlias(item);
        const historyText = '$' + alias;
        if (!executeQuickCommandItem(item)) return false;
        inputHistory.push(historyText);
        historyIndex = -1;
        savedDraft = '';
        cmdInput.value = '';
        hideQuickCommandSuggestions();
        cmdInput.focus();
        return true;
    }

    function executeQuickCommandSuggestionById(id) {
        const item = quickCommandSuggestionItems.find(function(x) { return x.id === id; }) ||
            quickCommandItems.find(function(x) { return x.id === id; });
        return executeQuickCommandSuggestionItem(item);
    }

    function executeSelectedQuickCommandSuggestion() {
        if (quickCommandSuggestEl.hidden || !quickCommandSuggestionItems.length) return false;
        return executeQuickCommandSuggestionItem(quickCommandSuggestionItems[quickCommandSuggestionIndex] || quickCommandSuggestionItems[0]);
    }

    function renderQuickCommandSuggestions() {
        const query = getQuickCommandQueryFromInput(cmdInput.value);
        if (query === null) {
            hideQuickCommandSuggestions();
            return;
        }
        const matches = getQuickCommandMatches(query);
        quickCommandSuggestionItems = matches;
        quickCommandSuggestionIndex = 0;
        if (!matches.length) {
            quickCommandSuggestEl.innerHTML = '<div class="empty-hint">没有匹配的快捷命令</div>';
            quickCommandSuggestEl.hidden = false;
            return;
        }
        quickCommandSuggestEl.innerHTML = matches.map(function(item, index) {
            const alias = getQuickCommandAlias(item);
            return '<button class="quick-command-suggest-item' + (index === 0 ? ' active' : '') + '" type="button" data-id="' + escapeAttr(item.id) + '">' +
                '<span class="quick-command-suggest-alias">$' + escapeHtml(alias) + '</span>' +
                '<span class="quick-command-suggest-name">' + escapeHtml(item.name || item.id) + '</span>' +
                '<span class="quick-command-suggest-meta">' + item.commands_count + ' 条</span>' +
                '</button>';
        }).join('');
        quickCommandSuggestEl.hidden = false;
    }

    function addQuickCommandStep(command, delay) {
        const row = document.createElement('div');
        row.className = 'quick-command-step-row';
        row.innerHTML =
            '<input type="text" class="quick-command-step-command" placeholder="实际发送指令" value="' + escapeAttr(command || '') + '">' +
            '<input type="number" class="quick-command-step-delay" placeholder="延时秒" min="0" max="3600" step="0.1" value="' + escapeAttr(delay || '') + '">' +
            '<button class="trigger-small-btn danger quick-command-step-delete" type="button">×</button>';
        quickCommandStepsEl.appendChild(row);
    }

    function clearQuickCommandForm() {
        quickCommandNameEl.value = '';
        quickCommandAliasEl.value = '';
        quickCommandNotesEl.value = '';
        quickCommandStepsEl.innerHTML = '';
        addQuickCommandStep('', '');
        quickCommandCurrentNameEl.textContent = '未选择';
        selectedQuickCommandPinned = true;
    }

    function startNewQuickCommand() {
        selectedQuickCommandId = '';
        clearQuickCommandForm();
        quickCommandDetailEl.textContent = '正在新建快捷命令';
        quickCommandDeleteBtn.disabled = true;
        quickCommandCopyBtn.disabled = true;
        quickCommandListEl.querySelectorAll('.trigger-item').forEach(function(el) {
            el.classList.remove('active');
        });
        setQuickCommandStatus('正在新建快捷命令', 'ok');
        quickCommandNameEl.focus();
    }

    function fillQuickCommandForm(config) {
        config = config || {};
        quickCommandNameEl.value = config.name || '';
        quickCommandAliasEl.value = config.alias || '';
        quickCommandNotesEl.value = config.notes || '';
        selectedQuickCommandPinned = config.pinned !== false;
        quickCommandStepsEl.innerHTML = '';
        const commands = config.commands || [];
        if (!commands.length) addQuickCommandStep('', '');
        commands.forEach(function(step) {
            addQuickCommandStep(step.command, step.delay || '');
        });
    }

    function getQuickCommandFormConfig() {
        const commands = [];
        let hasNegativeDelay = false;
        quickCommandStepsEl.querySelectorAll('.quick-command-step-row').forEach(function(row) {
            const command = row.querySelector('.quick-command-step-command').value.trim();
            const delayRaw = row.querySelector('.quick-command-step-delay').value.trim();
            let delay = parseFloat(delayRaw);
            if (Number.isFinite(delay) && delay < 0) {
                hasNegativeDelay = true;
                row.querySelector('.quick-command-step-delay').focus();
                return;
            }
            if (!Number.isFinite(delay)) delay = 0;
            if (delay > 3600) delay = 3600;
            if (command) commands.push({ command: command, delay: delay });
        });
        if (hasNegativeDelay) return null;
        return {
            name: quickCommandNameEl.value.trim(),
            alias: normalizeQuickCommandAlias(quickCommandAliasEl.value),
            notes: quickCommandNotesEl.value,
            pinned: selectedQuickCommandPinned !== false,
            commands: commands,
        };
    }

    function validateQuickCommandConfig(config, currentId) {
        if (!config.name) {
            quickCommandNameEl.focus();
            return '必须填写快捷命令名称';
        }
        if (!config.alias) {
            quickCommandAliasEl.focus();
            return '必须填写触发词';
        }
        if (/\s/.test(config.alias)) {
            quickCommandAliasEl.focus();
            return '触发词不能包含空格';
        }
        const duplicate = findDuplicateQuickCommandAlias(config.alias, currentId);
        if (duplicate) {
            quickCommandAliasEl.focus();
            return '触发词已被「' + (duplicate.name || duplicate.id) + '」使用';
        }
        if (!config.commands.length) {
            const firstInput = quickCommandStepsEl.querySelector('.quick-command-step-command');
            if (firstInput) firstInput.focus();
            return '至少填写一条指令';
        }
        return '';
    }

    function formatQuickCommandDetail(config) {
        if (!config) return '选择一个快捷命令查看详情';
        const commands = config.commands || [];
        const lines = [
            '名称: ' + (config.name || ''),
            '触发词: ' + (config.alias ? ('$' + config.alias) : '未设置'),
            '主页面显示: ' + (config.pinned === false ? '否' : '是'),
            '指令数: ' + commands.length,
            '',
            '指令:',
        ];
        commands.forEach(function(step, index) {
            const delay = Number(step.delay || 0);
            const suffix = delay > 0 ? '（延时 ' + delay + ' 秒）' : '';
            lines.push((index + 1) + '. ' + step.command + suffix);
        });
        if (config.notes) {
            lines.push('', '备注:', config.notes);
        }
        return lines.join('\n');
    }

    function renderQuickCommandButtons(items) {
        const visibleItems = (items || []).filter(function(item) {
            const config = item.config || {};
            return config.pinned !== false && item.pinned !== false;
        });
        if (!visibleItems.length) {
            quickCommandButtonsEl.innerHTML = '<div class="empty-hint">暂无快捷命令</div>';
            return;
        }
        quickCommandButtonsEl.innerHTML = visibleItems.map(function(item) {
            const alias = getQuickCommandAlias(item);
            return '<button class="quick-command-run" type="button" data-id="' + escapeAttr(item.id) + '">' +
                '<span class="quick-command-run-title">' + escapeHtml(item.name || item.id) + '</span>' +
                '<span class="quick-command-run-meta">' + (alias ? '$' + escapeHtml(alias) + ' · ' : '') + item.commands_count + ' 条指令</span>' +
                '</button>';
        }).join('');
    }

    function renderQuickCommandList(items) {
        quickCommandItems = items || [];
        renderQuickCommandButtons(quickCommandItems);
        renderQuickCommandSuggestions();
        if (!quickCommandItems.length) {
            quickCommandListEl.innerHTML = '<div class="empty-hint">暂无快捷命令</div>';
            if (selectedQuickCommandId) quickCommandDetailEl.textContent = '选择一个快捷命令查看详情';
            quickCommandDeleteBtn.disabled = true;
            quickCommandCopyBtn.disabled = true;
            return;
        }
        quickCommandListEl.innerHTML = quickCommandItems.map(function(item) {
            var cls = item.id === selectedQuickCommandId ? ' active' : '';
            var alias = getQuickCommandAlias(item);
            var checked = item.pinned === false || (item.config && item.config.pinned === false) ? '' : ' checked';
            return '<div class="trigger-item quick-command-list-item' + cls + '" data-id="' + escapeAttr(item.id) + '">' +
                '<label class="quick-command-list-check" title="显示在主页面快捷命令栏">' +
                    '<input type="checkbox" class="quick-command-list-visible"' + checked + '>' +
                '</label>' +
                '<div class="quick-command-list-info">' +
                    '<div class="trigger-item-title">' + escapeHtml(item.name || item.id) + '</div>' +
                    '<div class="trigger-item-meta">' + (alias ? '$' + escapeHtml(alias) + ' · ' : '') + item.commands_count + ' 条指令</div>' +
                '</div>' +
                '</div>';
        }).join('');
        quickCommandListEl.querySelectorAll('.trigger-item').forEach(function(el, index) {
            el.classList.add('list-enter');
            el.style.animationDelay = Math.min(index * 18, 180) + 'ms';
        });
    }

    function selectQuickCommand(id) {
        selectedQuickCommandId = id || '';
        var item = quickCommandItems.find(function(x) { return x.id === selectedQuickCommandId; });
        quickCommandCurrentNameEl.textContent = item ? (item.name || item.id) : '未选择';
        quickCommandDetailEl.textContent = formatQuickCommandDetail(item && item.config);
        quickCommandDetailEl.classList.remove('flash');
        void quickCommandDetailEl.offsetWidth;
        quickCommandDetailEl.classList.add('flash');
        if (item && item.config) fillQuickCommandForm(item.config);
        quickCommandDeleteBtn.disabled = !item;
        quickCommandCopyBtn.disabled = !item;
        quickCommandListEl.querySelectorAll('.trigger-item').forEach(function(el) {
            el.classList.toggle('active', el.getAttribute('data-id') === selectedQuickCommandId);
        });
    }

    function executeQuickCommandById(id) {
        var item = quickCommandItems.find(function(x) { return x.id === id; });
        executeQuickCommandItem(item);
    }

    function executeQuickCommandItem(item) {
        if (!item || !item.config) return false;
        return sendQuickCommandMessage('execute', { id: item.id, config: item.config });
    }

    function setQuickCommandPinned(id, pinned) {
        const item = quickCommandItems.find(function(x) { return x.id === id; });
        if (!item || !item.config) return;
        const config = JSON.parse(JSON.stringify(item.config));
        config.pinned = pinned !== false;
        item.pinned = config.pinned;
        item.config.pinned = config.pinned;
        pendingQuickCommandPinnedId = id;
        if (selectedQuickCommandId === id) {
            selectedQuickCommandPinned = config.pinned;
            quickCommandDetailEl.textContent = formatQuickCommandDetail(config);
        }
        renderQuickCommandButtons(quickCommandItems);
        saveQuickCommandConfig(id, config, { status: '正在保存显示设置' });
    }

    function handleQuickCommandList(msg) {
        renderQuickCommandList(msg.items || []);
        if (selectedQuickCommandId) {
            var exists = quickCommandItems.some(function(item) { return item.id === selectedQuickCommandId; });
            if (exists) {
                selectQuickCommand(selectedQuickCommandId);
            } else {
                selectedQuickCommandId = '';
                clearQuickCommandForm();
                quickCommandDetailEl.textContent = '选择一个快捷命令查看详情';
                quickCommandDeleteBtn.disabled = true;
                quickCommandCopyBtn.disabled = true;
            }
        }
        if (msg.status) setQuickCommandStatus(msg.status, 'ok');
    }

    function handleQuickCommandStatus(msg) {
        if (msg.ok === false) {
            if (msg.id && msg.id === pendingQuickCommandPinnedId) pendingQuickCommandPinnedId = '';
            if (msg.status) {
                setQuickCommandStatus(msg.status, 'error');
                alert(msg.status);
            }
            return;
        }
        if (msg.id && msg.id === pendingQuickCommandPinnedId) {
            pendingQuickCommandPinnedId = '';
            if (msg.status) setQuickCommandStatus(msg.status, 'ok');
            return;
        }
        if (msg.id) selectedQuickCommandId = msg.id;
        if (msg.config) {
            fillQuickCommandForm(msg.config);
            quickCommandCurrentNameEl.textContent = msg.config.name || msg.id || '未选择';
            quickCommandDetailEl.textContent = formatQuickCommandDetail(msg.config);
            selectedQuickCommandPinned = msg.config.pinned !== false;
        }
        if (msg.status) setQuickCommandStatus(msg.status, 'ok');
    }

    function handleQuickCommandEvent(msg) {
        if (msg.command) showSentCommand(msg.command);
    }

    document.querySelectorAll('.tab-btn[data-page]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const pageId = btn.getAttribute('data-page');
            document.querySelectorAll('.tab-btn[data-page]').forEach(function(tab) {
                tab.classList.toggle('active', tab === btn);
            });
            document.querySelectorAll('.page').forEach(function(page) {
                page.classList.toggle('active', page.id === pageId);
            });
            btn.classList.remove('tab-hit');
            void btn.offsetWidth;
            btn.classList.add('tab-hit');
            if (pageId === 'triggerPage') sendTriggerMessage('list');
            if (pageId === 'quickCommandPage') loadQuickCommands();
            if (pageId === 'gamePage') setTimeout(function() { fitAddon.fit(); }, 0);
        });
    });

    document.querySelectorAll('.left-tab-btn[data-left-page]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const pageId = btn.getAttribute('data-left-page');
            document.querySelectorAll('.left-tab-btn[data-left-page]').forEach(function(tab) {
                tab.classList.toggle('active', tab === btn);
            });
            document.querySelectorAll('.left-pane').forEach(function(page) {
                page.classList.toggle('active', page.id === pageId);
            });
            if (pageId === 'mapPane') setTimeout(function() { mapFitAddon.fit(); }, 0);
            if (pageId === 'quickPane') loadQuickCommands();
        });
    });

    triggerListEl.addEventListener('click', function(e) {
        var item = e.target.closest('.trigger-item');
        if (!item) return;
        e.stopPropagation();
        selectTrigger(item.getAttribute('data-id'));
    });

    triggerLoadBtn.addEventListener('click', function() {
        if (!selectedTriggerId) return;
        sendTriggerMessage('load', { id: selectedTriggerId });
    });

    triggerDeleteBtn.addEventListener('click', function() {
        if (!selectedTriggerId) return;
        var item = triggerItems.find(function(x) { return x.id === selectedTriggerId; });
        var name = item ? (item.name || item.id) : selectedTriggerId;
        if (!confirm('确定要删除触发器「' + name + '」吗？')) return;
        sendTriggerMessage('delete', { id: selectedTriggerId });
    });

    triggerAddRuleBtn.addEventListener('click', function() {
        addTriggerRule('', '');
    });

    triggerRulesEl.addEventListener('click', function(e) {
        var btn = e.target.closest('.trigger-rule-delete');
        if (!btn) return;
        e.preventDefault();
        e.stopPropagation();
        var row = btn.closest('.trigger-rule-row');
        if (row && row.parentNode) row.parentNode.removeChild(row);
        setTriggerStatus('已删除分支，保存后生效', 'ok');
    });

    triggerNewBtn.addEventListener('click', function() {
        startNewTrigger();
    });

    triggerCopyBtn.addEventListener('click', function() {
        if (!selectedTriggerId) return;
        var item = triggerItems.find(function(x) { return x.id === selectedTriggerId; });
        if (!item || !item.config) return;
        var copiedConfig = JSON.parse(JSON.stringify(item.config));
        copiedConfig.name = (copiedConfig.name || selectedTriggerId) + '_副本';
        sendTriggerMessage('save', { id: '', config: copiedConfig });
    });

    triggerSaveBtn.addEventListener('click', function() {
        const config = getTriggerFormConfig();
        if (!config) {
            setTriggerStatus('延时秒不能填写负数', 'error');
            alert('延时秒不能填写负数');
            return;
        }
        sendTriggerMessage('save', { id: selectedTriggerId, config: config });
    });

    triggerStopBtn.addEventListener('click', function() {
        sendTriggerMessage('stop');
    });

    clearTriggerForm();

    quickCommandButtonsEl.addEventListener('click', function(e) {
        var btn = e.target.closest('.quick-command-run');
        if (!btn) return;
        executeQuickCommandById(btn.getAttribute('data-id'));
    });

    quickCommandListEl.addEventListener('click', function(e) {
        if (e.target.closest('.quick-command-list-check')) return;
        var item = e.target.closest('.trigger-item');
        if (!item) return;
        e.stopPropagation();
        selectQuickCommand(item.getAttribute('data-id'));
    });

    quickCommandListEl.addEventListener('change', function(e) {
        var input = e.target.closest('.quick-command-list-visible');
        if (!input) return;
        var item = input.closest('.trigger-item');
        if (!item) return;
        e.stopPropagation();
        setQuickCommandPinned(item.getAttribute('data-id'), input.checked);
    });

    quickCommandNewBtn.addEventListener('click', function() {
        startNewQuickCommand();
    });

    quickCommandCopyBtn.addEventListener('click', function() {
        if (!selectedQuickCommandId) return;
        var item = quickCommandItems.find(function(x) { return x.id === selectedQuickCommandId; });
        if (!item || !item.config) return;
        var copiedConfig = JSON.parse(JSON.stringify(item.config));
        copiedConfig.name = getUniqueQuickCommandName(copiedConfig.name || selectedQuickCommandId);
        copiedConfig.alias = getUniqueQuickCommandAlias(copiedConfig.alias || selectedQuickCommandId);
        setQuickCommandStatus('正在复制快捷命令', 'ok');
        saveQuickCommandConfig('', copiedConfig);
    });

    quickCommandAddStepBtn.addEventListener('click', function() {
        addQuickCommandStep('', '');
        var rows = quickCommandStepsEl.querySelectorAll('.quick-command-step-row');
        var lastCommand = rows.length ? rows[rows.length - 1].querySelector('.quick-command-step-command') : null;
        if (lastCommand) lastCommand.focus();
    });

    quickCommandStepsEl.addEventListener('click', function(e) {
        var btn = e.target.closest('.quick-command-step-delete');
        if (!btn) return;
        e.preventDefault();
        e.stopPropagation();
        var row = btn.closest('.quick-command-step-row');
        if (row && row.parentNode) row.parentNode.removeChild(row);
        if (!quickCommandStepsEl.querySelector('.quick-command-step-row')) addQuickCommandStep('', '');
        setQuickCommandStatus('已删除指令，保存后生效', 'ok');
    });

    quickCommandSaveBtn.addEventListener('click', function() {
        const config = getQuickCommandFormConfig();
        if (!config) {
            setQuickCommandStatus('延时秒不能填写负数', 'error');
            alert('延时秒不能填写负数');
            return;
        }
        const error = validateQuickCommandConfig(config, selectedQuickCommandId);
        if (error) {
            setQuickCommandStatus(error, 'error');
            alert(error);
            return;
        }
        saveQuickCommandConfig(selectedQuickCommandId, config);
    });

    quickCommandDeleteBtn.addEventListener('click', function() {
        if (!selectedQuickCommandId) return;
        var item = quickCommandItems.find(function(x) { return x.id === selectedQuickCommandId; });
        var name = item ? (item.name || item.id) : selectedQuickCommandId;
        if (!confirm('确定要删除快捷命令「' + name + '」吗？')) return;
        deleteQuickCommandConfig(selectedQuickCommandId);
    });

    clearQuickCommandForm();

    // ─── 地图终端 ───
    const mapFitAddon = new FitAddon.FitAddon();
    const mapTerm = new Terminal({
        fontSize: 12,
        fontFamily: '"Sarasa Mono SC", "Cascadia Mono", "Microsoft YaHei Mono", Consolas, monospace',
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
        rows: 20,
    });
    mapTerm.open(document.getElementById('mapTerminal'));
    mapTerm.loadAddon(mapFitAddon);
    mapFitAddon.fit();
    new ResizeObserver(() => mapFitAddon.fit()).observe(document.getElementById('mapTerminal'));

    // ─── 退出游戏 ───
    var btnQuit = document.getElementById('btnQuit');
    btnQuit.addEventListener('click', function() {
        if (!ws || ws.readyState !== WebSocket.OPEN) return;
        if (btnQuit.dataset.quitting) return;
        btnQuit.dataset.quitting = '1';
        btnQuit.textContent = '保存中...';
        btnQuit.disabled = true;
        term.writeln('\x1b[33m[正在保存并退出游戏...]\x1b[0m\r\n');
        ws.send(JSON.stringify({ type: 'quit_game' }));
    });

    // ─── 启动 ───
    loadSettings();
    connect();
})();
