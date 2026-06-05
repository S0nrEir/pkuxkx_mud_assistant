- Muder

- 一. 概述

- 二. 特点

- 三. 登录

- 四. 首页

- 五. 工具栏

- 1. 脚本

- 2. 聊天

- 3. 识图

- 4. 录图

- 5. 配置

- 6. 地图

- 六. 逍遥游

- 七. 机器人编写

- 1. 基础篇

- 2. 系统函数介绍

- 3. 高级篇

- 4. 常见任务分析

最近的更新可以参考论坛地址 https://www.pkuxkx.net/forum/thread-50529-1-1.html

Muder

一. 概述

Muder 是 2025 年基于北大侠客行研发的专属客户端，采用浏览器方式使用，直接部署在 pkuxkx.net 服务器上；访问地址：`https://muder.pkuxkx.net`。

二. 特点

- 功能完整，常用客户端的主要功能都有。

- 辅助功能内置集成在一个界面里，不像很多客户端需要搭配多种插件。

- 访问方便，不需要安装，在任何支持浏览器的系统和设备上都可以随时访问。

- 使用 JavaScript 作为机器人的脚本，可以利用 AI 来帮忙实现。

- 机器人脚本存储在服务器上，不需要单独管理和保存。

- 内置逍遥游，可以实现城市之间的快速移动。

三. 登录

1. 登录完整地址：

- 如果没有游戏账户，玩家 ID 输入 `new`，密码和角色名称都不需要填

- 如果有游戏账户，玩家 ID 和密码都必须输入，角色名称最好也填一下，如果不填不影响使用，但是主页面显示名称的地方会有问题

- 登录过的账户会保存在底部，下次只需要点击记住的用户就可以自动带出用户 ID 和角色名称，密码每次都需要输入

- 账户相关信息不会保存在服务器上，只会保存在浏览器本地存储中（清理浏览器数据/更换设备会丢失）

2. 直接在地址后面加玩家 ID 登录

比如我的玩家 ID 叫 `but`，则可以直接在浏览器输入地址

`https://muder.pkuxkx.net/index.htm?id=but`

四. 首页

首页主要分为 9 个区域（对应 `main.png` 的编号），便于一眼掌握输出、指令输入与常用功能入口：

-

**角色信息面板**

显示当前角色名、等级、经验、潜能几个关键数值，便于随时确认状态。数据会自动更新。

-

**记事区**

用于放置不经常变化的数据。我一般用来记录当前所有经验加成的任务列表，一般每 2 小时切换一次。修改内容可以通过系统函数 `sys.note()` 来更新。

-

**日志区（游戏信息流）**

一般用于显示游戏里的动态信息（战斗、任务提示等）。比如任务 NPC 会告知做任务的地点，记录在这个区，否则聊天刷过去后就得往前翻主输出区才能看到。修改内容可以通过系统函数 `sys.log()` 来更新。

-

**右上工具栏（常用功能入口）**

集中放置常用开关与入口（例如消息/频道、地图/导航、设置等）。这个后续会单独讲解。

-

**状态条（核心资源）**

底部彩色条展示主要资源的当前值/上限（如气血、精力、内力等），方便战斗与恢复时快速判断风险。数据会自动刷新。

-

**位置信息**

显示当前所在地点名称，配合逍遥游等移动功能用于确认移动是否成功。当移动到能开始执行 `walk` 指令和逍遥游指令的位置时，会显示很多可达的其它位置点；可以用鼠标点击这些位置，迅速到达对应地点。

-

**计时/统计区域**

展示计时或倒计时，主要用于辅助多任务场景。后续做任务的速度很快，做完一个任务需要等待 CD 若干秒，可以记录倒计时，便于一到时间立刻去接新的任务。修改内容可以通过系统函数 `sys.timer()` 来更新。这个区域总共提供 5 个倒计时。

-

**命令输入框**

-

左边是历史记录按钮，点击会弹出最近输入的所有指令；点击某条指令会自动在输入框带出该指令。

-

中间是输入框，用于输入游戏指令（例如 `look`、`help`、`say 你好`）。回车发送；支持多指令用 `;` 隔开。

-

指令如果以 `##` 开头表示执行函数，比如 `##sys.info('test')`。

-

执行完一个指令后输入框会清空；但可以连续按回车键，重复执行最后一次的指令。

- 输入至少一个字母后，再按上下键，可以选择以该字母或已输入文字开头的历史记录。

- 输入框为空白时，按上下左右键会实现行走。这里多说一句：上下左右只有 4 个方向，但游戏里有十几种方向，4 个方向如何实现？其实是根据当前房间的所有出口来动态判断“上下左右”分别映射到哪个方向；极少数情况下仍需要手动敲方向指令。大家尝试一下上下左右就能体会到，非常方便。

-

输入框还支持截图 `Ctrl+V` 粘贴输入，但一般只能用于在 QQ 频道里发截图；在 `chat` 频道里发也可以，但对方必须也使用 Muder 才能看到。图片输入后会自动变成一个特殊格式的文本，如图：

-

**主区域**

- 这是 MUD 的主输出区域，支持向上翻页查看历史输出，但历史记录并非无限保存。

- 不支持右键复制内容；只支持选中文本后按 `Ctrl+C` 复制。复制后会自动将复制内容回填到输入框，便于二次编辑/转发。

- 输出内容的样式（字体大小、颜色等）可以在设置里修改。

五. 工具栏

1. 脚本

玩家可以在这个界面设置别名、触发器等与机器人相关的脚本。这里的功能比较多也比较复杂，我们先介绍基本能力，后续会在“机器人编写”章节里再详细展开。

如图，脚本管理包含 3 个子页面，以及右上角的导入/导出按钮：

1.1 系统子页面

这一页不能编辑，只提供系统函数的查询/帮助文档。

1.2 通用子页面

用于管理多角色公用的机器人脚本。

1.3 玩家子页面

用于管理当前角色独有的机器人脚本。

1.4 导入/导出按钮

可以将机器人脚本导出为 `JSON` 文件，并在另一个角色登录后从脚本界面导入该 `JSON` 文件。

“通用子页面”和“玩家子页面”的划分是为了适配多角色场景：多数玩家会有多个角色，脚本里往往存在大量复用逻辑。“通用”用来存放可复用的脚本；“玩家”则记录该角色特有的脚本。

2. 聊天

聊天功能比较直观：用于显示多个频道的内容。底部有按钮可选择显示哪些频道（前提是相应频道已打开）。比较特殊的一点是：聊天界面可以显示聊天对应的图片，这是其它客户端没有的能力。

3. 识图

`fullme` 是北大侠客行特有的功能：无论是手动执行 `fullme`，还是被动自动触发 `fullme`，这个界面都会自动弹出。关闭方式除了手动点关闭外，还可以通过系统函数 `sys.closeFullme()` 关闭。
界面上方还有左右 2 个按钮，可用来查看历史 `fullme` 图片。

4. 录图

“录制路径”不是绘制地图，而是用来手动录制行走路径。它支持图形化录制，可以很直观地看到路线；同时会给出起点到终点的最短路径。例如：先走 `north` 一步，再走 `south` 两步，实际行走指令是 `north;south;south`，但起点到终点的最短路径是 `south`。

基本操作：

- 点击 `开始录制`

- 通过上下左右键或直接输入方向指令进行行走（路径会自动记录）

- 点击 `停止录制`

- 点击 `复制路径`，再选择需要的路径，按 `Ctrl+C` 复制

5. 配置

配置包括几个主要功能：

5.1 显示配置

- 主题选择：配置附带了近百种主题，每个主题会修改多种元素的颜色搭配；玩家可以用上下键实时预览不同主题的效果。

- 字体：配置附带了 20+ 种字体，但有些字体并不是选了就立刻生效，需要先下载安装到操作系统里才会生效。比如我一直使用的字体 Maple Mono。如果你有喜欢的字体不在列表中，可以找我，我会更新列表增加新字体选项。

- 字体大小

- 线高：行间距，通常为 `1`

- 普通字体粗细：普通/粗体，玩家可以自行选择查看效果

- 粗体字体粗细：普通/粗体，玩家可以自行选择查看效果

- 字间隔：有不少字体显示时字与字之间间隔偏大，可以设置成负数，效果会更紧凑

5.2 小键盘配置

上下左右键用来行走已经很方便了，但仍有一些玩家更习惯使用键盘右侧的小键盘区域来行走。这里可以配置每个按键对应的指令；这些指令不止于方向，也可以是任何指令。

5.3 下载日志

点击后会下载最近 3 天的所有游戏日志，包括：屏幕显示的文本、原始文本（带颜色）、以及 GMCP 数据。这些数据可用于分析与编写更复杂的机器人逻辑。

6. 地图

地图功能是一套完整的地图文件管理系统：可以自由创建新地图、维护旧地图，并提供强大且灵活的地图编辑能力。编辑器融合了“手动精调”和“自动录制”两种模式，以适应不同使用场景。

在录制模式下，你在游戏中的每一次移动（无论是通过上下左右方向键还是输入移动指令），都会在地图上自动创建对应的房间节点与连线。推荐“先录制，再微调”的工作方式：先通过录制功能快速生成地图草稿，再利用手动编辑功能精修。

地图录制完成后，会提供 2 个基础系统函数用于读取数据；剩余的自动寻路/任务逻辑等，需要玩家基于这些数据自行编写机器人脚本。

六. 逍遥游

其实更准确的名称应该叫“城际通”。整个大地图由多个城市（city）组成，每个城市里包含许多房间（room）。通常每个城市有 1–2 个“中心房间”，这些中心房间之间可以通过游戏自带的 walk 功能快速行走（但一般仅限两个房间之间的快速到达）。

要实现跨城市移动，则需要客户端支持。目前长期支持“逍遥游/城际通”的客户端主要是 paotin++ 和 Muder。

原理很简单：客户端维护一份“各城市中心房间”的索引表，再用最短路径算法选路。例如从扬州到北京：先到达扬州中心房间“中央广场”，执行 `xy 北京`，客户端会自动多次 walk 并处理中途过河等步骤，最终到达北京的“永安门”。

侠客行地图会不定期变化，因此索引文件也需要更新。比如新增“佛山镇”后，需要更新索引才能支持通过 `xy 佛山镇` 快速到达。paotin++ 通常需要玩家手动更新或等待他人分享更新文件；Muder 发布新版本后会自动对所有玩家生效。

要注意的是：

- 要使用逍遥游，必须先走到当前城市的中心房间。

- 刚登录游戏时，即使已经在中心房间，也可能无法立即逍遥游；通常手动走动 1–2 步即可（原因是刚登录时客户端可能尚未获取到准确位置）

七. 机器人编写

- 创建一个分组

- 删除一个分组

- 在一个分组下创建一个变量

- 在一个分组下创建一个函数

- 在一个分组下创建一个别名

- 在一个分组下创建一个触发器

- 删除一个变量、函数、别名和触发器

- 保存对变量、函数、别名和触发器的内容编辑

1. 基础篇

最基础的就是别名和触发器，这 2 个概念应该很好理解，我们以实际例子来讲解。

1.1 别名和触发器

别名是比较短的字符串，方便在输入框里输入。对应的值可以是字符串，也可以是函数；函数又分同步函数和异步函数（后面会讲解区别）。

**例 1：** 过河的时候，有的时候需要用 `ride`，有的时候需要 `enter boat`，所以设置一个别名，让过河时 2 个指令都执行。

```
'gogo': 'ride;enter boat;',
```

**例 2：**
答题的时候每次都要输入 `answer b` 之类的，简化一下，改成 `a b`。其中 `a` 是别名，`$1` 表示第一个不定参数。

```
'a': 'answer $1',
```

**例 3：**
把身上的一个绑定的装备取消绑定。比如要把第 2 个戒指解除绑定，正常的指令是：

```
remove ring 2;
disload ring 2;
yes;
```

设置成别名 `dl`，对应的用法就是 `dl ring 2`。

- `arg` 表示函数参数，是一个数组；例如 `arg[0]` 是 `ring`，`arg[1]` 是 `2`，`arg.join(' ')` 就是 `ring 2`

- `sys.send()` 是最基础的系统函数：发送一条指令

```
'dl': function (arg) {
sys.send('remove ' + arg.join(' '))
sys.send('disload ' + arg.join(' ') + ';yes;')
},
```

**例 4：**
在临安给装备安装宝石。比如给第 2 个戒指镶嵌宝石，戒指有 2 个洞，需要先放 2 个宝石到桌子上，然后把装备放到桌子，然后镶嵌宝石；最终希望只输入 `xiangqiang 2 ring 2`。

等同于以下完整指令：

```
put gem on zhuo;
put gem on zhuo;
put ring 2 on zhuo;
ask shangren about 篆刻铭文;
yes;
```

这个别名对应的函数对不熟编程的同学可能不太直观，不过可以把这个函数发给 AI 让它帮忙解释，也可以让 AI 按你的需求生成/改写。

```
'xiangqiang': function (arg) {
if (arg.length <= 1) { return }
let count = arg[0] || 1
let zb = arg[1]
if (arg.length > 2) { zb = zb + ' ' + arg[2] }
for (let i = 0; i < count; i++) {
sys.send('put gem on zhuo')
}
sys.send(`put ${zb} on zhuo;ask shangren about 篆刻铭文;yes`)
}
```

触发器和别名的本质是一样的：别名是玩家手动输入触发，触发器是游戏文本（含正则）触发，两者都可以执行一串指令或一个函数。

**例 5：**
只要看到钱，都自动捡起来，`|` 是`或`的意思。

```
/两白银(Silver)|两黄金(Gold)|银票(Cash)/:  'get cash;get gold;get silver;'
```

**例 6：**
系统推送 fullme 的时候，会自动打开 fullme 的窗口，所以需要快速关闭窗口，如下面的触发器和别名，也就是玩家输入`cf`可以关闭窗口，也可以在某些条件下自动触发

```
/获得了答问如流许可，|为找到闯王宝藏的线索/: 'cf'
'cf': function () { sys.closeFullme() }
```

**例 7：**
在战斗中，如果敌人的快要晕倒了，我星宿派的角色会尝试去吸敌人的内力。这个正则匹配了 2 个部分，一个是中文名称，一个是当前气血百分比
`[\u4e00-\u9fa5]+` 这个表示一个或多个中文字，`\d`表示一个或多位数字，这些都是正则的基本写法，所有语言都统一，有很小的差异。
arg[1] 相当于获取到中文名字再和 `sys.name` （玩家自己的中文名称）比较，如果不是自己晕倒那么就判断 arg[2] 也就是血量是否<=0,
最后调用 my.suckneili 这个函数，这个函数是我定义用来吸取内力的独立函数

```
/『([\u4e00-\u9fa5]+).*?气血:(\d+)%/: function (arg) {
if (arg[1] && arg[1] != sys.name) {
if (arg[2] <= 0) {
my.suckneili(true)
}
}
}
```

1.2 同步函数和异步函数

先用最直白的比喻：

- 同步：像排队办事，前一个没办完，后一个不能开始。

- 异步：像取号办事，前台告诉你“号码已取”，你可以先做别的，等叫号或通知再继续。

在游戏里也是类似的：有的函数会立刻完成（同步），有的函数会等到某个事件完成才算结束（异步）。如果不知道谁会“等”，就很容易把行走、战斗步骤搅在一起。

下面用回城存钱的别名 `home` 来说明：

```
'home': function () {
sys.send('xy 扬州;')
sys.send('n;w;cun all gold')
}
```

这两行会几乎同时发出，行走还没到扬州就开始往北/西，结果行动会乱掉。

那加个 `await` 会好吗？

```
'home': async function () {
await sys.send('xy 扬州;')
sys.send('n;w;cun all gold')
}
```

还是不行，因为 `sys.send` 是同步的——它发完指令就算结束，不会等你真的到扬州，自然也没法“等待”。

最简单的权宜之计是“傻等”：

```
'home': async function () {
sys.send('xy 扬州;')
await sys.sleep(30) // 等 30 秒
sys.send('n;w;cun all gold')
}
```

缺点是可能等太久（浪费时间），或等不够（还没到就走了）。

推荐的写法是用真正“会等待到结果”的异步函数：

```
'home': async function () {
await sys.xy('扬州')   // 直到真的到达扬州再往下走
sys.send('n;w;cun all gold')
}
```

这里 `sys.xy` 是异步的，只有到达目的地后才继续执行后面的命令。

小结（非开发背景也能记住的要点）：

- 看函数是不是需要“等结果”。需要等的，就当作异步；不需要等的，就是同步。

- 想等待异步函数的完成，用 `await`，但前提是它本身支持等待。

- 如果不确定函数是不是异步，翻翻 README 或试一下：能否用 `await` 并得到预期结果；实在不行，用 `sys.sleep` 兜底，但记得时间要留余量。

- 只要用了 `await`，当前函数就必须加上 `async` 修饰（否则语法会报错）。

- 后面章节还有大量异步示例，可以多看几遍，结合自己的场景来套用。

1.3 更多异步函数示例

包括别名和触发器，以下列出更多示例并分析解释。

**例 8：**

```
'jingong': async function (arg) {
sys.send('give 1 gold to qian')
await sys.sleep(2)
sys.send('ask qian about 进宫')
},
```

说明：北京先给钱老板钱，再等 2 秒，最后询问“进宫”，他会给你一个牌子，你就可以进宫不会被阻拦。
**例 9：**

```
'lianshow': async function () {
sys.send('n;e;up;enter;')
sys.send('bei none;bei xingxiu-duzhang;')
await sys.try('sleep', '你一觉醒来，精神抖擞地活动了几下手脚。', 60)
sys.send('lian show')
},
```

说明：从扬州城中心，自动走到店里睡觉，醒来自动`lian show` ,sys.try 是系统提供的函数，后续会再讲一下函数的用法。
**例 10：**

```
/在(.*)欺男霸女，为恶一方，你快去清理门户吧。/: async function (arg) {
sys.send("s;sw;sw;s;s;s;up;out")
await my.waitToRoom('中央广场')
let temps = arg[1].split('的')
await sys.xy(temps[0])
await my.map.gpsInCity(null, temps[1])
let result = await my.findByEnglishname(sys.id + ' ', 'fuzzy')
if (result) {
sys.send('fk ' + result)
await my.waitToCombatEnd()
sys.send('home')
} else {
sys.warn('未找到目标人物：' + sys.id)
}
}
```

说明：接到“清理门户”任务后，自动回中央广场、定位目标城市与地点，找到人则开打并等战斗结束，再回家；找不到则提示。这里用到了地图相关的函数，和根据名称模糊查询的函数。
**例 11：**

```
'tunaall': async function () {
while (true) {
sys.send('auto_food_water');
let max_jingli = sys.status().max_jingli;
let jingli = sys.status().jingli;
if (jingli >= (max_jingli * 2 - 20)) {
await sys.try("tuna 10", '你吐纳完毕，睁开双眼，站了起来。', 10);
} else {
sys.send('e2')
await sys.try("tuna max", '你吐纳完毕，睁开双眼，站了起来。', 60, ['你现在精力接近圆满状态。', '你现在精严重不足，无法满足吐纳最小要求']);
}
await sys.sleep(1);
}
}
```

说明：循环吐纳脚本，先补给，再看精力高低选择 10 级或最大吐纳，遇到提示自动跳出等待，适合挂机恢复。一个函数可以实现无限吐纳。
**例 12：**

```
liandugo: async function () {
await sys.xy('星宿');
sys.send('sheshui')
await sys.sleep(3)
sys.send('w;l jingji lin')
await sys.sleep(2)
sys.send('southwest;southeast;west;southwest;southeast;westdown')
await sys.sleep(2)
sys.send('north;northdown;north;north;juan zhulian;north;east;north;east;north;north;north;east')
await sys.sleep(5)
my.liandu();
sys.send('xian')
}
```

说明：自动跑星宿路线做“练毒”流程，按步骤走图、涉水、穿行毒林并调用自定义 `my.liandu()`。
**例 13：**

```
tuocoin: async function () {
sys.send('n;w;qu 100 coin')
await sys.sleep(1)
sys.send('e;s;')
await sys.sleep(1)
await sys.xy('代州')
await my.map.gpsInCity(null, '佛光寺')
sys.send('tou coin')
await sys.sleep(1)
sys.send('home')
}
```

说明：自动取 100 枚铜币，传送到代州佛光寺投币祈福增加幸运值，再回家（扬州），途中适当等待防止卡步。

2. 系统函数介绍

Muder 提供了很多系统函数，sys 对象里都是系统相关的函数和变量。还有一个 com 对象和 my 对象后面也会提到。

2.1 系统变量（无需调用，直接读取）

-

**2.1.1 `sys.id`**：玩家 ID

示例：

```
sys.info(`我的ID是：${sys.id}`);
```

-

**2.1.2 `sys.name`**：玩家中文名称

示例：

```
sys.info(`你好，${sys.name}`);
```

2.2 系统函数（常用 API 与示例）

-

**2.2.1 `sys.send`**：发送指令给 Mud 服务器，这是最常见的函数

```
sys.send("look");
```

-

**2.2.2 `sys.batch`**：批量顺序执行命令，间隔秒数

```
await sys.batch(["look", "east"], 2);
```

说明：执行 look 指令后等待 2 秒再执行 east 指令，适合执行批量指令，比如边走路边检破烂，不过每个指令之间的时间是固定的。

-

**2.2.3 `sys.repeat`**：重复执行命令

```
sys.repeat("look", 3);
```

-

**2.2.4 `sys.info` / `sys.warn` / `sys.error`**：在界面打印信息/警告/错误

```
sys.info("hello");
sys.warn("This is a warning.");
sys.error("error: hello");
```

-

**2.2.5 `sys.log`**：首页左边的日志区域追加内容，

```
sys.log("hello", "green");
```

说明：第二个参数可以是颜色，方便区分不同日志

-

**2.2.6 `sys.note`**：记事本区域覆盖内容

```
sys.note("hello", "green");
```

说明：可以让 AI 把第一个参数转成 h5 格式，带各种颜色的文本。

-

**2.2.7 `sys.timer`**：界面定时器（索引 1-5）

```
sys.timer(1, "FULLME", 15 * 60, true, "ss");
```

说明：第一个参数是索引，第二个是显示的文字，第三个是时间 15*60 表示 15 分钟，第四个参数为 true 是表示倒计时，否则表示正计时，最后一个参数是时间的格式，ss 表示显示秒。这个示例就是用来执行 fullme 后，重新开始倒计时 15 分钟计时。

-

**2.2.8 `sys.closeFullme`**：关闭 fullme 窗口

```
sys.closeFullme();
```

-

**2.2.9 `sys.delay` / `sys.undelay`**：延迟执行与取消

```
const id = sys.delay(2, "look"); //过2秒后再执行look，有时候可以替代await sys.sleep(2)
sys.undelay(id); //取消延时执行
```

-

**2.2.10 `sys.tick` / `sys.untick`**：循环定时与清除

```
const tid = sys.tick(5, "look"); //每隔5秒执行一次look
sys.untick(tid); //取消循环
```

-

**2.2.11 `sys.sleep`**：异步等待秒数

```
await sys.sleep(2); //这个函数用的很多
```

-

**2.2.12 `sys.alias` / `sys.unalias`**：别名管理

```
sys.alias("k", "killall");
sys.unalias("k"); //取消别名
```

-

**2.2.13 `sys.action` / `sys.unaction`**：文本/正则触发器

```
const aid = sys.action("id1", "看到了", function () {
sys.send("hi");
});
sys.unaction(aid);
```

说明：很多情况触发器不希望一直生效，是希望在特定的情况下生效，然后过一会让它再失效。

-

**2.2.14 `sys.actionOnce`**：仅触发一次

```
sys.actionOnce("id1", "官兵拦住你说道：站住，把", "unwield all");
```

说明：有的时候短时间内会触发多次，比如问 NPC 任务，其他人也在问 NPC 任务，可以通过这个函数来触发一次就不会被再次触发。然后过 5 秒或更长时间后又恢复触发。

-

**2.2.15 `sys.test`**：模拟文本触发器测试

```
sys.test("看到了", false);
```

说明：这个通常用于测试一个触发器是否生效，相当于模拟发送一段文本来触发自己写的触发器

-

**2.2.16 `sys.xy`**：逍遥游移动，`xy` 为异步可等待

```
sys.go("扬州"); //不等待，直接发送
await sys.xy("扬州"); //等待到达
```

-

**2.2.17 `sys.reversePath`**：反转路径字符串

```
sys.reversePath("w;w;s");
```

说明：这个函数用的也很多，用来反转路径，相当于走过去，然后再方向走回来。

-

**2.2.18 `sys.loadMap` / `sys.listMaps`**：加载与列出地图，都是异步函数

```
await sys.loadMap("扬州");
await sys.listMaps();
```

说明：本来想提供更多地图相关的函数，包括城市内、跨城市的快速行走和遍历，但是这些函数有很多特例，个性化太强，所以放弃了，只提供了最基础的函数。

-

**2.2.19 `sys.try` / `sys.retry`**：等待文本或重试直到成功

```
await sys.try("tuna 10", "你吐纳完毕，睁开双眼，站了起来。", 10);
await sys.retry("dalao", "也许你可以返航了。可以使用hua back命令", 4, 60);
```

说明：这 2 个函数用的很多，
try 表示执行一个指令 `tuna 10`，就执行一次，执行完就开始等待，如果出现 `你吐纳完毕，睁开双眼，站了起来。`这个函数就执行结束，如果 10 秒钟还没出现这个文本，也结束，超时结束。
retry 差不多，只不过是执行多次，上面的示例就是每隔 4 秒执行一次`dalao`指令，总共执行 60 次，也就是 240 秒

-

**2.2.20 `sys.find`**：当前房间查找物品/NPC（带超时）

```
await sys.find("girl", "一个卖东西的小贩", 3);
```

说明：这个函数用于查询一个 NPC 或物品，通过 `look girl` 指令去看它，看它的描述有没有包含`一个卖东西的小贩`的内容，如果有，就返回 true
这个函数通常用于遍历的时候，一个个人来查询其特征。

-

**2.2.21 状态查询**：`sys.status()` / `sys.isbusy()` / `sys.isfighting()` / `sys.room()`

```
const st = sys.status();
if (sys.isfighting()) sys.send("yun heal");
```

说明：这些函数也经常用到，获取完整的状态，判断是否忙，判断是否在战斗中，当前所在房间的信息

-

**2.2.22 发送/接收钩子**：`sys.onSend` / `sys.offSend` / `sys.onReceive` / `sys.offReceive`

```
sys.onSend("id", function (cmd) {
/* ... */
});
sys.offSend("id");
sys.onReceive(
"id",
function (msg) {
/* ... */
},
true
);
sys.offReceive("id");
```

说明：这是最底层的基础函数，我们在高级篇里再讲

-

**2.2.23 GMCP 处理**：`sys.onGmcp` / `sys.offGmcp`

```
sys.onGmcp("char.vitals", function (data) {
sys.info(data);
});
sys.offGmcp("char.vitals");
```

说明：这是最底层的基础函数，我们在高级篇里再讲

-

**2.2.24 `sys.random`**：生成随机数（时间戳+随机值）

```
const r = sys.random();
```

-

**2.2.25 音频控制**：`sys.playaudio` / `sys.stopaudio`

```
const audio = sys.playaudio("http://.../sound.wav", 0.5, true);
sys.stopaudio(audio);
```

2.3 com 和 my

com 和 my 对应 `通用` 和 `玩家` 页面
我们在通用界面上创建的变量会保存在 com.vars 下，在通用界面上创建的函数会保存在 com. 下，my 也是同样的。com 的示例如下截图

3. 高级篇

所谓高级篇也没什么特别，只不过就是除了基本的别名和触发器外，还会使用 Javascript 的所有特性，包括大量变量和函数，还会使用基础的系统函数来构建自己的完整体系，其实和做 Javascript 开发没有太多区别了，不过我们的场景单一，来来回回就是这些功能。
最后说一句 Javascript 是非常灵活和成熟的语言，可以说是无所不能，而且 AI 非常擅长。

3.1 基础函数

先解释一下最基础的几个函数，我们的游戏客户端和 Mud 服务器是标准的客户端-服务端模式：

- 客户端发送指令给服务端，服务端返回文本，文本可以在主界面看到，我们的触发器就是根据这些文本来触发的。

- 即使客户端没有发送，服务端也返回文本。

- 服务端主动返回一些结构化的 GMCP 数据，里面包含了当前玩家的基本状态（变化值），房间状态，战斗状态和其它一些数据

对应的基本函数：

- onSend/offSend : 监控发送的指令。这个用的比较少

- onReceive/offReceive: 监控收到的文本，这个是必须要用到的

- onGmcp/offGmcp: 监控收到的 gmcp 数据，这个不一定需要用到，因为相关的数据客户端已经封装在 sys.status(),sys.room()

我们来看一些示例，基本上都是 AI 帮忙写的。

3.2 更多示例

**例 13：**

```
my.onReceive = function (callback, timeout = 3, raw = false) {
let id = sys.random();
sys.onReceive(
id,
function (msg) {
callback(msg, id);
},
raw
);
sys.delay(timeout, function () {
delete sys.vars._onreceives[id];
});
};
```

说明：短时监听服务端文本，3 秒后自动取消。常用于：先 look 一次拿到房间描述，再 look 第二次对比差异（如慕容任务中敌人隐藏位置）。

**例 14：**

```
sys.onGmcp("huxiao_gmcp", function (data) {
if (data && data.command == "GMCP.Combat") {
sys.info(data.content);
}
});
```

说明：监控 GMCP 战斗数据，便于获取自己和敌人的基础信息。

**例 15：**

```
my.action(/你决定开始跟随(.+?)一起行动。/, function (arg) {
const nameMap = {
"独孤": "dugu", "龚": "gong", "梁": "liang", "曹": "cao", "姬": "ji", "亲": "qin", "于": "yu", "董": "dong", "阮": "ruan",
"金": "jin", "荆": "jing", "吕": "lv", "关": "guan", "李": "li", "方": "fang", "戴": "dai", "郝": "hao", "萧": "xiao",
"左": "zuo", "樊": "fan", "范": "fan", "单": "shan", "喻": "yu", "刘": "liu", "燕": "yan", "王": "wang", "阳": "yang",
"潘": "pan", "黄": "huang", "朱": "zhu", "辛": "xin", "颜": "yan", "毛": "mao", "刑": "xing", "郑": "zheng", "童": "tong",
"武": "wu", "周": "zhou", "包": "bao", "陶": "tao", "鲍": "bao", "公孙": "gongsun", "林": "lin", "呼延": "huyan", "岳": "yue",
"钱": "qian", "费": "fei", "索": "suo", "牛": "niu", "马": "ma", "傅": "fu", "鲁": "lu", "冯": "feng", "欧阳": "ouyang",
"封": "feng", "侯": "hou", "齐": "qi", "何": "he", "雷": "lei", "危": "wei", "张": "zhang", "邹": "zou", "贾": "jia",
"余": "yu", "扬": "yang", "孟": "meng", "郭": "guo", "霍": "huo", "孔": "kong", "申": "shen", "孙": "sun", "廉": "lian",
"崔": "cui", "时": "shi", "凌": "ling", "花": "hua", "卢": "lu", "陈": "chen", "魏": "wei", "尉迟": "yuchi", "柴": "chai",
"解": "xie", "吴": "wu", "韩": "han", "安": "an", "穆": "mu", "史": "shi", "石": "shi", "高": "gao", "薛": "xue", "徐": "xu",
"许": "xu", "邓": "deng", "唐": "tang", "段": "duan", "杜": "du", "令狐": "linghu", "顾": "gu", "宋": "song", "杨": "yang",
"上官": "shangguan", "南宫": "nangong", "赵": "zhao", "司马": "sima", "闻人": "wenren", "施": "shi", "彭": "peng", "项": "xiang",
"蒋": "jiang", "宏久": "hongjiu", "慕容": "murong"
};
const fullName = arg[1];
const pinyin = Object.keys(nameMap).find((surname) =>
fullName.startsWith(surname)
);
if (pinyin) {
const english = nameMap[pinyin];
sys.info(`匹配姓氏: ${pinyin}, 拼音: ${english}`);
if (my.quests.tx.data.flag) {
my.quests.tx.hit(english);
} else {
sys.send(`sh;kill ${english};`);
}
} else {
sys.info("未找到匹配的姓氏");
}
});
```

说明：胡一刀/刺杀任务场景，跟随目标后监控其中文姓名，转换为英文名并自动攻击。此版本直接用姓氏映射，未使用自动拼音。

**例 16：**

```
my.action(/\(([A-Za-z]+ [A-Za-z]+)\)/g, function (arg) {
if (com.vars.find_people_flag) {
com.vars.current_peoples = [];
for (let i = 0; i < arg.length; i++) {
const en = arg[i][1].trim().toLowerCase(); // 英文名
com.vars.current_peoples.push(en);
}
}
});
```

说明：遍历房间时，将房间内 NPC/物品英文名存入 `com.vars.current_peoples`，供后续匹配。开关变量 `com.vars.find_people_flag` 为 true 时才记录。

**例 17：**

```
my.action(
/([\u4e00-\u9fa5]{2,5})[^│]*│仍需(.+?)才能接到下个任务。/,
function (arg) {
const taskName = arg[1]; // 捕获的任务名，比如 “韩世忠”
const jqcontent = arg[2]; // 捕获的时间字符串，比如 “一分四十八秒”
if (taskName && taskName == "鄱阳湖寻宝") {
return;
}
let index = my.compute_jq_index_fun();
sys.timer(index, taskName, my.chineseToSeconds(jqcontent), true, "ss");
}
);
//中文数字转时间
my.chineseToSeconds = function (timeStr) {
const timeUnits = {
秒: 1,
分钟: 60,
分: 60,
小时: 3600,
时: 3600,
};
let totalSeconds = 0;
let buffer = "";
for (let i = 0; i < timeStr.length; i++) {
let char = timeStr[i];
let unit = char;
if (i + 1 < timeStr.length) {
const twoCharUnit = char + timeStr[i + 1];
if (timeUnits[twoCharUnit]) {
unit = twoCharUnit;
i++;
}
}

if (timeUnits[unit]) {
const num = my.parseChineseNumber(buffer);
totalSeconds += (num || 1) * timeUnits[unit];
buffer = "";
} else {
buffer += char;
}
}

if (buffer.length > 0) {
totalSeconds += my.parseChineseNumber(buffer);
}

return totalSeconds;
};
//解析中文数字
my.parseChineseNumber = function (str) {
const digits = {
零: 0,
一: 1,
二: 2,
三: 3,
四: 4,
五: 5,
六: 6,
七: 7,
八: 8,
九: 9,
};
let result = 0;
let temp = 0;

if (str.includes("十")) {
const parts = str.split("十");
const tens = parts[0] === "" ? 1 : digits[parts[0]];
const ones = parts[1] ? digits[parts[1]] : 0;
result = tens * 10 + ones;
} else {
for (let i = 0; i < str.length; i++) {
if (digits[str[i]] !== undefined) {
temp = temp * 10 + digits[str[i]];
}
}
result = temp;
}

return result;
};
```

说明：执行 jq 时扫描任务列表，把处于 CD 的任务写入底部计时器；鄱阳湖寻宝因 CD 太长被过滤。交完任务跑一遍 jq，就能在右下角看到下次可做时间。

**例 18：**

```
my.waitToCombatEnd = async function (timeout = 60) {
if (my.readyfight) {
await my.readyfight();
}
await sys.sleep(5);
let i = 0;
while (sys.isfighting()) {
sys.info("等待战斗结束..." + i);
i++;
await sys.sleep(1);
timeout--;
if (timeout <= 0) {
sys.warn("等待战斗结束超时...");
return false;
}
}
sys.info("战斗结束...");
await sys.sleep(1);
return true;
};
```

说明：等待战斗结束的通用异步封装，用于后续拾取/交任务等。先等 5 秒（`sys.isfighting()` 可能有延迟），总超时 60 秒，超时则提示。

**例 19：**

```
my.action(/│\s+([\u4e00-\u9fa5]{2,5})\s+│[\u4e00-\u9fa5]/, function (arg) {
if (!my.vars.bestquests) {
my.vars.bestquests = {};
}
my.vars.bestquests.level0 = arg[1];
my.notebestquests();
});
my.action(/↑(.*)。/, function (arg) {
if (!my.vars.bestquests) {
my.vars.bestquests = {};
}
my.vars.bestquests.level1 = arg[1];
my.notebestquests();
});
my.action(/→(.*)。/, function (arg) {
if (!my.vars.bestquests) {
my.vars.bestquests = {};
}
my.vars.bestquests.level2 = arg[1];
my.notebestquests();
});
my.action("奖励最佳。", my.notebestquests);
my.notebestquests = function () {
let temp = "";
if (my.vars.bestquests.level0) {
temp += `<span style="color:orange">${my.vars.bestquests.level0}</span> `;
}
if (my.vars.bestquests.level1) {
temp += `<span style="color:white">${my.vars.bestquests.level1}</span> `;
}
if (my.vars.bestquests.level2) {
temp += `<span style="color:green">${my.vars.bestquests.level2}</span> `;
}
sys.note(temp);
};
```

说明：执行 time 时，自动把最佳/次佳/第三档任务写到首页记事并着色，便于 CD 中先做其它高收益任务。

4. 常见任务分析

任务的脚本代码是不允许分享的，以下没有任何代码，我只是把我的经验和思路和大家分享供大家讨论。总体来说，每个人写的机器人都有自己的特色，完全把别人的拿过来，用起来很别扭，还是得自己理解，自己实现和调整。但是思路是基本差不多的。
有了地图的帮助，大部分任务可以实现敲一个指令就能自动完成，不过特殊情况很多，只能是说基本实现。这个也是写机器人的乐趣，不断的想办法提高效率。

4.1 慕容任务

我的任务别名习惯是：英文缩写 + a/h/s/f，分别对应问任务/回 NPC/成功交/失败交。例如慕容任务：mra、mrh、mrs、mrf。
在 mrh 里自动串 mrs，mrs 结束再自动 mra：回 NPC 顺手尝试交任务（即使未必完成），稍等或等 NPC 回复再次触发问任务 → 去目标房间 → 打怪 → 捡尸体 → 回去交（mrh），形成循环。
慕容任务 CD 很短（3m 前），可持续循环。若遇 fullme 图，可用 `mrset 临安府 大理寺` 之类指令，指定房间后复用同样流程。

慕容任务的特殊点是 3m 后，第一次询问 NPC 得到的位置并不是敌人的位置，需要 look 二次做比较，得到差异，这个差异的位置才是真正敌人的位置，而且这个位置还会带一些随机的字，所以这一块基本上到这里就得靠手动了。二次房间的字符串先通过正则匹配到，然后字符串比较，让 AI 帮忙。

另外慕容敌人经常走来走去，不在原地，我增加了一个`mrbl`的别名，意思是慕容遍历，也慕容敌人的位置为其实点，广度遍历 4 层，也就是离当前位置 4 步的所有房间，这个需要提前准备好地图才能实现，至于遍历的代码完全用 AI 来实现。

4.2 保卫任务

我级别比较低，保卫玩的不多，主要是靠胡家刀法，但是攻击力太低了。脚本没有啥特殊，就是每秒加力 max，然后使用胡家刀法的技能，如果打晕了，醒过来之后判断一下当前房间 sys.room().short == '伤兵营' ，如果是就继续跑回前线去继续砍。

4.3 督抚刺杀任务

问完任务后，需要到一个特定的位置，有一个很大的映射表，类似这样的格式，这个可以通过路径录制来录制位置，也可以在论坛上找，早期很多人分享了这个映射表，如果制作了地图，就很简单了，一个函数就可以。我还保留了这个老的写法。

```
case "绛云楼":
sys.send('south;south;south;south;south;west;west;southwest');
com.vars.mengb = 'ne;e;e;n;n;n;n;n;';
return;
case "睡房":
sys.send('w;w;w;s;s;w;s;enter');
com.vars.mengb = 'out;north;east;north;north;east;east;east';
return;
.......
```

接下来这个位置获取有点难度，需要解析甲乙丙丁戊己庚辛壬癸这些文本，正则匹配并算出位置，可以寻求 AI 帮助，但是还是不简单。

4.4 护镖任务

护镖现在挺难，早期去很容易死，即使是初级镖。有了一定防御，就好多了。
首先接任务的时候需要通过正则匹配出所有空闲的任务对应的城市和房间，城市是准确的，但是房间不准确，还需要执行 jq 指令，再从任务列表里匹配出正确的房间。
如果已经有了地图，就需要通过计算得到当前位置到目的位置的完整路径。
然后开始循环沿着路径赶镖车，碰到敌人需要战斗，战斗结束后需要走，走到位置后，再触发返回。需要用到前面提到的 my.onReceive 函数。

4.5 韩式忠任务

这个任务的机器人比较简单，制作地图后，自动到到目的，执行 hani 进入副本，然后手动输入方向，然后使用前面提到的 my.waitToCombatEnd 函数等待战斗结束，结束后自动捡尸体并返回交任务。

4.6 胡一刀任务

这个任务和很多任务都有一个共同点，就是到位置后会自动提示到下一个位置，需要匹配的正则如下：

```
/(和周围的人打听之后，你判断应该是在|直觉告诉你到|你仔细观察之后，觉得很可能应该就在|直觉告诉你，下一步的线索应该在)(.*)。/;
```

如果有地图，就比较方便，可以自动触发从一个位置到另外一个位置，如果没有地图，需要把位置记录到一个全局变量，然后 lm 查看，然后走过去。我一般是加一个别名 `lmm` 这个指令会自动 lm 记录的位置变量，这样在地图上就能看到高亮。
另外一个难点是地宫模式的胡一刀任务，需要进入到一个迷宫副本，这里需要用到自动行走，没有地图数据，只能靠 AI 帮忙实现 DFS 的行走，然后碰见敌人，每杀一个还需要计数+1，而且如果没杀够 4 个，进入到小木屋里就得马上退出来，所以逻辑上是有点复杂的。

4.7 韩元外任务

任务比较繁琐，多种情况，狡兔三窟运气不好需要遍历 3 个地方，遍历需要用到前面提到的 npc 列表。

4.8 纪晓芙任务

这个任务唯一的难点是自动记录密钥，这个正则不好写，有多种情况，让 AI 帮忙吧。

4.9 裘千仞任务

需要遍历宝箱，其它也没什么特殊，不过这个任务有风险，很容易被砍死，需要比较强的防御。

4.10 南宫围猎

需要实现尽可能的自动，需要维护一个很大的映射表，格式如下:

```
com.vars.weimap = {
"` |==.":"buy 野猪图",
"b`~~`":"buy 牛头图",
".-.  |------|  .-.": "buy 五毒教卧房图",
"<_> <_>": "buy 算盘图",
"子  坞": "buy 燕子坞大门图",
"vVVVv": "buy 花园图",
"&&& X": "buy 火山图",
。。。。。。
}
```

到了看地图的文字通过 my.onReceive 获取到文件，然后遍历这个映射表，找到对应的图，然后自动去购买，这个映射表维护没个完，因为图还在不断增加，而且每次显示的都是部分。所以一个图可能对应多个关键字符串。

4.11 漂流任务

设置了一个别名`plset`,比如看图后，设置示例为`plset 十三 north 三`,意思是漂流 13 里，然后向北划 3 里，通过 plset 把这 3 个值记录到变量，然后通过触发器来匹配，匹配到十三后，停船开始划船，可以使用 sys.retry 函数来不断的划船和打捞直到完成为止。
总体上这个不算麻烦。
如果是重宝就麻烦一点，经常会额外增加几里路，所以需要手动再次调用`plset`

4.12 破阵任务

这个需要一个比较复杂的正则表达式记录下当前所有可能的方向，然后每走一个方向，从可能方向列表里删除错误的方向，这样就能走最少的步骤到达终点和恶人战斗。继续 AI 帮忙。
从进入迷宫到离开迷宫基本可以做到自动。

4.13 宋远桥任务

难点是带颜色的色块正则匹配，需要使用 onReceive 函数最后一个参数改成 true，表示匹配带颜色的文本，这个文本可以在下载日志里找到对应的原始文件里获取。
我还加了一个 songprint 别名，可以打印需要匹配的色块，这样即使手动，忘了以前的也可以打印一下。
另外就是需要到城市中心开始特殊的遍历，每次比较当前房间的色块和记录的色块，当然还是靠 AI

4.14 天珠任务

对我来说，太难，每次都很紧张，基本不自动，全靠手动。哈哈。

4.15 偷学任务

这个匹配有点难，因为需要匹配招数，还没仔细研究，现在就是完全不管招数，和敌人 hit 的时候，不反抗，然后每秒偷学一次，交任务的成功率有一半吧

4.16 万安塔任务

这个没有什么特殊，唯一早期的时候每次战斗完，都判断一下内力是否足够，如果不够就循环等待。大家记得 set 战斗报告打开，我一般都是通过“战斗报告”来匹配是否战斗结束。

> 来源: https://www.pkuxkx.net/wiki/tools/muder
