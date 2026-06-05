- GMCP参数说明

- 详细参数

- 一、战斗相关

- 二、BUFF相关

- 三、聊天信息

- 四、移动信息

- 五、人物状态

- 使用方法

- Mudlet客户端

- 注意事项

GMCP参数说明

- GMCP(Generic MUD Communication Protocol)是MUD客户端与服务器之间的标准化数据通信协议，基于JSON格式，用于提供丰富的客户端界面体验。也特别适合用于开发移动端游戏的数据交互。

详细参数

一、战斗相关

- **gmcp.GMCP.Combat**

| 参数名称 | 描述 | 通知类型 | 是否Bool |
|---|---|---|---|
| enemy_in | 敌人加入 | 通知对手 立刻 | 否 |
| qi_damage | 气血伤害 | 通知对手 立刻 | 否 |
| jing_wound | 精血受损 | 通知对手 立刻 | 否 |
| qi_wound | 气血受损 | 通知对手 立刻 | 否 |
| eff_jing_pct | 有效精血百分比 | 通知对手 立刻 | 否 |
| enemy_out | 敌人退出 | 通知对手 立刻 | 否 |
| eff_qi_pct | 有效气血百分比 | 通知对手 立刻 | 否 |
| jing_pct | 精血百分比 | 通知对手 立刻 | 否 |
| jing_damage | 精血伤害 | 通知对手 立刻 | 否 |
| qi_pct | 气血比率 | 通知对手 立刻 | 否 |
| perform_name | 绝招名称 | 通知自身 立刻 | 否 |
| perform_cd | CD时长 | 通知自身 立刻 | 否 |
| perform_id | 绝招ID | 通知自身 立刻 | 否 |

二、BUFF相关

- **gmcp.GMCP.Buff**

| 参数名称 | 描述 | 通知类型 | 是否Bool |
|---|---|---|---|
| type | 效果类型 | 通知对手 立刻 | 否 |
| is_end | 效果结束 | 通知对手 立刻 | 是 |
| last_inc | 效果延时 | 通知对手 立刻 | 否 |
| name | 效果名称 | 通知对手 立刻 | 否 |
| effects | 具体效果 | 通知对手 立刻 | 否 |
| last_time | 持续时间 | 通知对手 立刻 | 否 |
| terminated | 将中止的效果 | 通知对手 立刻 | 否 |

三、聊天信息

- **gmcp.GMCP.Message**

| 参数名称 | 描述 | 通知类型 | 是否Bool |
|---|---|---|---|
| channel | 频道 | 通知自身 立刻 | 否 |
| type | 信息类型 | 通知自身 立刻 | 否 |
| seq | 图片编号 | 通知自身 立刻 | 否 |
| no | QQ号码 | 通知自身 立刻 | 否 |
| name | 姓名 | 通知自身 立刻 | 否 |
| url | 下载地址 | 通知自身 立刻 | 否 |

四、移动信息

- **gmcp.GMCP.Move**

| 参数名称 | 描述 | 通知类型 | 是否Bool |
|---|---|---|---|
| result | 成功 | 通知自身 立刻 | 是 |
| dir | 出口信息 | 通知自身 立刻 | 否 |
| short | 房间名 | 通知自身 立刻 | 否 |

五、人物状态

- **gmcp.GMCP.Status**

| 参数名称 | 描述 | 通知类型 | 是否Bool |
|---|---|---|---|
| max_qi | 最大气血 | 通知对手 立刻 | 否 |
| qi | 气血 | 通知对手 立刻 | 否 |
| jingli | 精力 | 通知自身 立刻 | 否 |
| food | 食物 | 通知自身 立刻 | 否 |
| eff_jing | 有效精神 | 通知对手 立刻 | 否 |
| jing | 精神 | 通知对手 立刻 | 否 |
| title | 头衔 | 通知自身 立刻 | 否 |
| family/family_name | 门派 | 通知自身 立刻 | 否 |
| combat_exp | 经验 | 通知自身 立刻 | 否 |
| vigour/qi | 真气 | 通知自身 立刻 | 否 |
| max_jing | 最大精神 | 通知对手 立刻 | 否 |
| level | 级别 | 通知自身 立刻 | 否 |
| vigour/yuan | 真元 | 通知自身 立刻 | 否 |
| max_jingli | 最大精力 | 通知自身 立刻 | 否 |
| neili | 内力 | 通知自身 立刻 | 否 |
| water | 饮水 | 通知自身 立刻 | 否 |
| eff_qi | 有效气血 | 通知对手 立刻 | 否 |
| max_neili | 最大内力 | 通知自身 立刻 | 否 |
| is_busy | 忙 | 通知自身 延迟 | 是 |
| per | 容貌 | 通知自身 延迟 | 否 |
| int | 悟性 | 通知自身 延迟 | 否 |
| fighter_spirit | 战意 | 通知自身 延迟 | 否 |
| is_fighting | 战斗中 | 通知自身 延迟 | 是 |
| dex | 身法 | 通知自身 延迟 | 否 |
| con | 根骨 | 通知自身 延迟 | 否 |
| potential | 潜能 | 通知自身 延迟 | 否 |
| str | 膂力 | 通知自身 延迟 | 否 |

使用方法

Mudlet客户端

- 创建一个脚本，定义脚本名称例如GMCP_event

- 添加用户事件gmcp.GMCP

- 编写代码（以LUA举例）

-
```
function GMCP_event()
display(gmcp)  --显示获取到的gmcp所有内容信息
echo("气血："..gmcp.GMCP.Status.qi)  --显示获取到的气血数值
end
```

注意事项

- 很多参数只在登录游戏时会传送一次，后续数值发生变化才会再次传送，例如（gmcp.GMCP.Status.max_qi）

- 战斗中会在Status中传来对方的ID和信息，如不加以判断，将导致自己的数值出错，例如（gmcp.GMCP.Status.qi）

- 以上仅为范例，可以到扬州武庙中的巫师会客室查看最新说明(look shuoming)

- 有些参数说明里也未曾提及，可以自行display(gmcp)分析研究

> 来源: https://www.pkuxkx.net/wiki/robot/gmcp
