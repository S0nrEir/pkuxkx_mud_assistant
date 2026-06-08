"""Telnet and byte-buffer helpers for the web MUD client."""

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

