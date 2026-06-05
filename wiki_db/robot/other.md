- 小蜜蜂新手机器人

- Mush抓取聊天信息颜色机器人

- Mush版抄经+工号查询机器人

- 物品鉴定机器人

- Zmud批量鉴定物品机器人

- Mush批量鉴定物品机器人（新版随机装备可用）

- Zmud7.21及Cmud2.37鉴定机器人（新版随机装备使用）

- Cmud2.37鉴定机器人

- Mush版HP窗口机器人

- Mush版小时钟

- fullme显示

- Mush版fullme显示插件

- Zmud4.62版fullme显示插件

- Python版fullme显示插件

- 论坛mud log自动上色工具

- Mush点歌、播歌机器人

- 基于Mushclient api的Python框架

- 雅黑等宽字体

- 保卫襄阳释仇机器人

---

小蜜蜂新手机器人

出品人：Inspector

非常适合新手使用的机器人，图形界面，操作简便，适用版本：zmud7.21

功能：

-  显示地图行动按钮

-  显示当前房间的人物、物品和相应操作菜单

-  显示人物状态，点击按钮自动疗伤

-  统计exp、pot的增长和效率

-  自动回复tell

-  定时关机功能

-  设置机器人任务列表，自动切换机器人

小蜜蜂机器人（新手专用）

相关图片：

---

Mush抓取聊天信息颜色机器人

出品人：Maper

以前在mush中抓取聊天信息使用的是AppendToNotepad函数，不过这样抓出来的聊天信息仅仅是文本，没有丰富多彩的颜色。今天逛mush官网发现了一个真正实现zmud中#cap命令的方法，与大家共享。

首先新建一个聊天窗口：file—new world，名称为“chats_pkuxkx”,ip地址为0.0.0.0，保存位置为主窗口文件所在的文件夹（如果不清楚，在主窗口中立即执行print(GetInfo(67))即可清楚）。然后在主窗口中载入插件color_chat，这样就可以将聊天信息原原本本的抓取到chats_pkuxkx聊天窗口了。

另外如果在聊天窗口中载入插件color_chat_chat,并修改world_name = “pkuxkx” 中pkuxkx为主窗口的名称，这样在聊天窗口中输入命令可以在主窗口中反应。

```
插件的修改：
1、color_chat

<!--  Triggers  -->
<triggers>
<trigger
enabled="y"
match="^(>)*( )*【(闲聊| 天色 |谣言|保卫|动作|江湖传闻|北侠公告|北侠QQ群|江湖逸事)】"  增加或减少频道修改这里。
omit_from_output="y" ：这里y表示在主窗口中不显示聊天信息，改成"n"表示在主窗口中显示聊天信息。
regexp="y"
script="color_chats"
sequence="100"
>
</trigger>
<trigger
enabled="y"
match="^(>)*( )*(你告诉|.+告诉你|你回答|.+回答你)"
omit_from_output="y" ：同上。
regexp="y"
script="color_chats"
sequence="100"
>
</trigger>
</triggers>

<!--  Script  -->
<script>
<![CDATA[
chat_world = "chats_pkuxkx"  这里可以修改聊天信息窗口的名称。
local first_time = true

function color_chats (name, line, wildcards, styles)

-- try to find "chat" world
local w = GetWorld (chat_world)  -- get "chat" world

-- if not found, try to open it
if first_time and not w then
local filename = GetInfo (67) .. chat_world .. ".mcl"
Open (filename)
w = GetWorld (chat_world)  -- try again
if not w then
ColourNote ("white", "red", "Can't open chat world file: " .. filename)
first_time = false  -- don't repeatedly show failure message
end -- can't find world
end -- can't find world first time around

if w then  -- if present
for _, v in ipairs (styles) do
w:ColourTell (RGBColourToName (v.textcolour),
RGBColourToName (v.backcolour),
v.text)
end -- for each style run
w:Note ("")  -- wrap up line

end -- world found

end -- function redirect
]]>
</script>
</muclient>

2、color_chat_chat

<!--  Script  -->
<script>
<![CDATA[
world_name = "pkuxkx" pkuxkx是主窗口的名称。

function OnPluginCommandEntered (command)

local w = GetWorld (world_name)  -- find world

-- not found? show error
if not w then
ColourNote ("white", "red", "World " .. world_name .. " is not open")
else
w:Execute (command)  -- execute command (handle aliases, etc.)
PushCommand (command)  -- save in command history
end -- if

return ("\t")  -- clear command

end -- OnPluginCommandEntered

]]>
</script>
```

参考mush官网：http://www.gammon.com.au/forum/?id=7991

mush抓取聊天信息颜色，真正实现zmud的#cap功能

---

Mush版抄经+工号查询机器人

出品人：Ddid

强大至极，在Mush中利用Lua脚本，自动查询抄经工号，并且显示在小窗口内

机器人运行：

Login PKUXKX，找朱熹去ask zhu xi about job机器人开始运行，MUSH右上角会显示“工号”图片。

ask zhu xi about job之后1分钟内，ask zhu xi about 口令 可以刷新图片，如果第一次显示的图片看不清楚，可以通过这个方法刷新出一个新的图片。

close_mini_window 命令可以将图片窗口关闭。

全新升级！～ 新手抄经——工号查询机器人（MUSH)

---

物品鉴定机器人

Zmud批量鉴定物品机器人

出品人：Duno

使用方法：

```
先建立各类型筛选条件，即增加或修改条件变量（condi_sword, condi_staff, condi_boots等）
以及默认条件 condi_default
修改筛选结果处理行为 res_act
最后，点击 start_identify 或者 执行 start_identify
```

注：没有测试，凑或能用 囧

[zmud] 批量鉴定物品

---

Mush批量鉴定物品机器人（新版随机装备可用）

出品人：Maper

随机装备的处理分成：

```
一孔armor防小于400的drop掉，二孔armor防小于200的drop掉；
其他的盔甲和饰品都是一孔防小于100的drop掉，二孔的防小于50的drop掉；
武器是一孔伤害小于180的drop掉，二孔伤害小于150的drop掉；
三孔的全部保留；
没有在上面之列的保留在身上。
```

以上设定可以根据各人需要修改相应数值，如果想要分的更详细的，请参照armor的处理方式修改并在“hands|wrists|ring|cloth|necklace|surcoat|head|boots|shield|waist”和“blade|sword|axe|staff|hammer|whip|halberd|dagger|spear”中去掉对应项即可。

使用方法：

载入自动鉴定物品.MCL，再手动载入脚本文件identify.lua，登录

若不要的物品要drop在家里，直接在家里输入jdwp

若要卖掉不要的物品，修改脚本，把items_do_with = “drop”的值drop为sell，在荣宝斋输入jdwp就能自动卖掉

自动鉴定物品机器人（此为老版随机装备机器人）

---

新版装备鉴定机器人请看Mush新版批量鉴定机器人

出品人：诸葛不亮（Zgbl）

```
参照maper的大作http://pkuxkx.net/forum/viewthread.php?tid=4662修改而成
也就是改了触发器和脚本，变成新版装备的格式而已
盾牌被单独提出来作为一类进行筛选
使用方法和maper的那个一样
需要注意的是，需要一定的鉴定之术，jianding xxx时能看见可塑性就可以了

由于家里地上能放的物品现在有了上限，所以切勿使用drop来处理不要的东西，否则会因为放不下而留在身上，影响筛选
切勿用sell来处理不要的东西，因为sell有busy
目前机器人使用的处理指令是ph，对应的是alias ph put $* in horse，这样只要horse里放得下都不会出问题
```

---

Zmud7.21及Cmud2.37鉴定机器人（新版随机装备使用）

出品人：Seagate

```
大体上和上一个版本差不多：
http://pkuxkx.net/forum/viewthread.php?tid=10647&highlight=%2Bseagate
这个版本是应虫子的版本升级而升级。主要提供两个版本，
.txt的是zmud721版本，.xml的是cmud237版本。这一次
鉴定.txt文件的路径是写死的，具体在触发：你说道：「jianding」
中，请根据自己的实际情况修改。
细微修改：鉴定一次将会清理一次鉴定结果。
鉴定种类增加spear。【原先少写了一个鉴定种类】
```

原帖地址：鉴定机器人【新版】

Cmud2.37鉴定机器人

出品人：Seagate

```
上一个版本：http://pkuxkx.net/forum/blog.php?tid=12326

修改：
1.修改了对重要物品中镶嵌宝石物品的判断依据，并且修改了显示重要物品的顺序，先显示所有镶嵌宝石的重要物品，再显示所有未镶嵌宝石的重要物品，使使用上更合理。如果你要把鉴定和你的售卖或者自动保存结合起来，可以根据@import_objlist列表中物品属性键值usedHole来判定是否镶嵌宝石，大于0就是镶嵌宝石的，=0为未镶嵌宝石。
2.变量和alias放在一个子类idPara里面了。其中下面的default是对外接口，可以自己修改里面的设置！
```

鉴定机器人【Cmud237版】

---

Mush版HP窗口机器人

出品人：Ddid

山寨版HP状态窗口 -- MUSH

---

Mush版小时钟

出品人：Ddid

要求：MUSHClient 4.42 版本以上。需要bgd.dll和luagd.dll与MUSHClient.exe在同一文件夹下。

源程序其实是LUA-GD的一个demo，小小修改了一下，MUSHClient从4.42版本以后开始支持从内存中直接读取图片，不用再把图片成文件，方便了很多。

有兴趣的可以试一下，一个小时钟挂在右上角，玩MUD的同时，随时知道现实时间。

送给MUSHer们的小时钟

---

fullme显示

Mush版fullme显示插件

出品人：Ddid

close_fullme可以关闭显示的小窗口。

附件中的3个DLL文件需要与MUSHClient.exe在同一文件夹下。

另外，需要注意把MUSHClient的沙箱打开，打开沙箱的方法，见14#楼。

已更新版本至2.00

fullme验证码在屏幕中心显示。

验证码输入完成后，显示窗口自动关闭。也可使用close_fullme命令强制关闭该窗口。

登录时检测Server端MXP支持，如Server端提供MXP支持，则从MXP标签提取图片文件；如不支持，则从Web页面提取图片文件。

【MUSHClient】 fullme 验证码显示插件

---

Zmud4.62版fullme显示插件

出品人：Ddid

因ZMUD 4.62只有DDE可以与其它程序交互，所以用C#写了个EXE，通过它实现fullme验证码图片的下载和显示。

因为是C#编译的，所以需要微软的.NET FrameWork 2.0的支持，fullmecodeviewer.exe才能执行。一般XP以上都应该安装了，没有的话，需要到微软的网站上下载

下载地址

fullmecodeviewer.exe 下载后，需要和zmud.exe在同一文件夹下，且这个文件夹的名字最好不要有空格等特殊字符。

fullmecodeviewer.exe 正确执行后，会在zmud.exe所在的文件夹下生成一个fullme_CODE.jpg的文件，可以不用管它。

fullme 验证码图片是根据触发自动显示的，验证码输入完成后，自动消失，如果没有消失，用鼠标点一下图片就可以消失了。

【ZMUD 4.62】fullme 验证码显示机器人

---

Python版fullme显示插件

出品人：Ddid

能够支持mush的低级版本显示fullme图片，如4.18

要使用这个插件，必须安装Python环境，以及wxPython。这两个都放在附件里了，但需要注意安装顺序：

-  先安装Pythong 2.6.4。安装完成后，可能会被要求重启系统。

-  再安装wxPython 2.8.10。根据提示走就好了。

-  在MUSH里安装fullme_Python_v1.xml的插件。

【MUSHClient】fullme验证码显示插件--Python版

---

论坛mud log自动上色工具

出品人：Qdcan

功能：

-  支持zMud 4.62或更高版本；

-  支持GBK（国标扩展码），可以处理繁体字；

-  输出到剪切板的格式有UNICODE和TEXT格式，可以用于中英文Windows。

使用：

-   运行qdcan.exe；

-  在zMud中选中要转换的文本(zMud自动把选中的文本拷贝到剪贴板)；

-  选 编辑(E) | 粘贴(P)，zMud原始文本就显示在窗口中，其中会有ANSI颜色控制符；

-  重复2, 3直到你认为足够。

-  选 编辑(E) | 转换(N)，转换成论坛格式的文本就出现在窗口中。

-  选 编辑(E) | 拷贝(N)，把转换成的文本拷贝的剪贴板。

-  贴到论坛。

在论坛上贴带zmud内格式颜色文本的方法

---

Mush点歌、播歌机器人

出品人：Ddid

这个MUSH的插件，可以自动从百度搜索到MP3的地址并播放。

附件中的playmp3_compent.rar包含3个必要组件，需要将它们复制到MUSHClient.exe同一文件夹下。

该插件运行后，会在MUSHClient文件夹下产生1或2个文件，分别为result2.htm和real_mp3_url.txt，无所谓，对机器人来说是数据文件，留不留均可，不会有什么影响。

这个机器人极其依赖百度，如果百度的网站有变化，这个机器人不一定能继续工作。

```
用法：playmp3 query keys

例子：
playmp3 蝶恋 仙剑奇侠传
playmp3 稻香 周杰伦
playmp3 王菲 eyes on me
playmp3 水木年华 一生
playmp3 听 是谁在唱歌
```

发布点歌、播歌机器人（测试版）[MUSH]

---

基于Mushclient api的Python框架

出品人：Zzyb

大家好，我最近写了一个Python框架用于开发Mushclient机器人。这个基于mushclient的api，和mushclient api的区别是，这个是一个更“pythonic”的方法，并且更方便使用

-  详细介绍和代码举例：MushPy: a Python framework on top of Mushclient's API

-  Mush官网原帖

-  下载地址

---

雅黑等宽字体

提供人：Killunix

雅黑混合Consolas英文字体的等宽字体，适合mud和编程使用

混合版雅黑字体

---

保卫襄阳释仇机器人

提供人：Rafle

使用方式：

用zmud导入，或者直接在命令行执行

721版代码：

```
#CLASS {baowei}
#VAR ID_cname {}
#TRIGGER {(@ID_cname)(%s)= (%x)} {shichou %3;tell %3 shichou}
#TRIGGER {(%x)喝道：「你，看招！」} {ID_cname=%1;halt;id here}
#TRIGGER {(%x)喝道：「你，我们的帐还没算完，看招！」} {ID_cname=%1;halt;id here}
#TRIGGER {(%x)一见到你，愣了一愣，大叫：「我宰了你！」} {ID_cname=%1;halt;id here}
#TRIGGER {(%x)一眼瞥见你，「哼」的一声冲了过来！} {ID_cname=%1;halt;id here}
#TRIGGER {(%x)和你一碰面，二话不说就打了起来！} {ID_cname=%1;halt;id here}
#TRIGGER {(%x)对著你大喝：「可恶，又是你！」} {ID_cname=%1;halt;id here}
#TRIGGER {(%x)和你仇人相见分外眼红，立刻打了起来！} {ID_cname=%1;halt;id here}
#TRIGGER {*~((*)~)告诉你：shichou} {shichou %1}
#TRIGGER {你喝道：「(%x)，看招！」} {halt;ID_cname=%1;halt;id here}
#TRIGGER {你和(%x)仇人相见分外眼红，立刻打了起来！} {halt;ID_cname=%1;halt;id here}
#TRIGGER {你和(%x)一碰面，二话不说就打了起来！} {halt;ID_cname=%1;halt;id here}
#TRIGGER {你喝道：「(%x)，我们的帐还没算完，看招！」} {halt;ID_cname=%1;halt;id here}
#TRIGGER {你一眼瞥见(%x)，「哼」的一声冲了过来！} {halt;ID_cname=%1;halt;id here}
#TRIGGER {你一见到(%x)，愣了一愣，大叫：「我宰了你！」} {halt;ID_cname=%1;halt;id here}
#TRIGGER {你对著(%x)大喝：「可恶，又是你！」} {halt;ID_cname=%1;halt;id here}
#CLASS 0
```

462版代码

```
#TRIGGER {(@ID_cname)(%s)= (%x)} {shichou %3;tell %3 shichou} {baowei} 519
#TRIGGER {(%x)喝道：「你，看招！」} {ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {(%x)喝道：「你，我们的帐还没算完，看招！」} {ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {(%x)一见到你，愣了一愣，大叫：「我宰了你！」} {ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {(%x)一眼瞥见你，「哼」的一声冲了过来！} {ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {(%x)和你一碰面，二话不说就打了起来！} {ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {(%x)对著你大喝：「可恶，又是你！」} {ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {(%x)和你仇人相见分外眼红，立刻打了起来！} {ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {*~((*)~)告诉你：shichou} {shichou %1} {baowei} 519
#TRIGGER {你喝道：「(%x)，看招！」} {halt;ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {你和(%x)仇人相见分外眼红，立刻打了起来！} {halt;ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {你和(%x)一碰面，二话不说就打了起来！} {halt;ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {你喝道：「(%x)，我们的帐还没算完，看招！」} {halt;ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {你一眼瞥见(%x)，「哼」的一声冲了过来！} {halt;ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {你一见到(%x)，愣了一愣，大叫：「我宰了你！」} {halt;ID_cname=%1;halt;id here} {baowei} 519
#TRIGGER {你对著(%x)大喝：「可恶，又是你！」} {halt;ID_cname=%1;halt;id here} {baowei} 519
```

原帖地址：鉴于现在很多保卫的玩家都不加自动释仇的trigger

---

> 来源: https://www.pkuxkx.net/wiki/robot/other
