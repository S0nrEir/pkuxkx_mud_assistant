---
name: mud-agent-control
description: 操作本地 MUD Assistant 的 agent 控制接口，用于有边界地自主控制 Web MUD 客户端。用户要求 Codex 在当前对话中控制 MUD Web 客户端、观察服务器返回或运行日志、根据用户意图决定下一条游戏指令，或使用 /agent/status、/agent/observe、/agent/command、/agent/batch、/agent/pause、/agent/resume 时使用本技能。
---

# MUD Agent Control

只在本地 MUD Assistant Web 客户端控制模式下使用本技能。目标是通过现有 Web MUD 会话完成用户的游戏意图，除此之外不做别的事。

## 控制接口

本地服务提供以下仅限 localhost 访问的接口：

- `GET http://127.0.0.1:58080/agent/status`
- `GET http://127.0.0.1:58080/agent/observe?since=<seq>&limit=<n>`
- `POST http://127.0.0.1:58080/agent/command`
- `POST http://127.0.0.1:58080/agent/batch`
- `POST http://127.0.0.1:58080/agent/pause`
- `POST http://127.0.0.1:58080/agent/resume`

发送单条指令时使用 JSON：

```json
{ "command": "look", "reason": "查看当前房间", "approved": false }
```

批量发送时使用：

```json
{
  "commands": [
    { "command": "look", "reason": "查看当前房间" },
    { "command": "hp", "reason": "检查角色状态", "delay": 0.5 }
  ]
}
```

## 行动循环

1. 先检查 `/agent/status`。如果没有活跃会话，告诉用户打开 Web 客户端，不要自行创建新的 Telnet 连接。
2. 读取 `/agent/observe`，并保存 `last_seq` 作为下一次增量观察的起点。
3. 根据最近的 `recv`、`chat`、`map`、`send`、`agent_event` 事件以及 `runtime_tail` 推断当前游戏状态。
4. 选择最小且有用的下一条指令。不确定时优先观察和查询状态，避免直接执行不可逆操作。
5. 通过 `/agent/command` 或 `/agent/batch` 发送指令；不要绕过 API 直接连接 MUD 服务器。
6. 每次动作或短批量动作后重新观察，再决定下一步。
7. 当用户目标完成、遇到阻塞、进入暂停状态或需要用户确认时停止。

## 安全规则

始终以用户最新指令为目标，不做无关的刷收益、社交、账号修改、配置修改或额外优化。

涉及转移价值、摧毁或丢弃物品、发起战斗、退出游戏、修改账号或安全状态、改变门派/帮派/阵营关系，或其他看起来不可逆的指令，都必须获得用户明确确认。如果 API 返回 `needs_approval`，先询问用户，得到确认后才可以带 `"approved": true` 重试。

除非用户明确要求并提供所需内容，不要自主处理 captcha/fullme 图片。如果出现验证码或 fullme 验证提示，报告给用户并暂停行动。

批量指令要短。导航、任务推进或状态判断不确定时，一次只发送一到两条指令，然后观察服务器返回。

## 沟通规范

连续行动超过少量指令时，给出简短状态更新。说明当前意图、下一类指令和阻塞点即可。

不要主动贴出大段原始日志，除非用户要求。默认总结和转述与决策相关的服务器返回。

遇到阻塞时，明确说明具体原因：没有活跃会话、需要用户确认、需要验证码、目标不清楚，或服务器返回与预期状态不一致。
