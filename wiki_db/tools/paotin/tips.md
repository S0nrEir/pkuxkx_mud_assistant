tools:paotin:tips

- PaoTin++ 教程集锦

- 常见问题

- 1. Windows 下怎么查看游戏内聊天信息

- 2. macOS/Linux 下怎么查看游戏内聊天信息

- 3. Windows 下如何复制屏幕内容

- 4. macOS 下如何复制屏幕内容

- 5. PaoTin++ 可以和 TinTin++ 共存吗？

- 6. 自己做的触发怎么才能不被别人的任务影响？

- 7. 怎么关闭自动 HP 摘要

- 8. 怎么关闭自动吃喝

- 9. 门派的新手任务有没有地方可以查询？

- 10. 为啥 pt 上 jobquery/localmaps 没有效果？

- 11. 如何直接在主屏内显示 chat 等聊天信息

- 用户心得

PaoTin++ 教程集锦

新人入门必读：

-  HELP NEWBIE（注意不是 help newbie） ———— **只看一次不行，反复多看，多尝试，常看常新。**

-  小九九的《给从未接触过MUD萌新的代码入门》

-  本炮的超新手教程

-  三千院鏡的《给 PaoTin++ 萌新的从0开始机器人编写系统性教程》

-  小豆米的【PaoTin++】入门系列之一：《客户端基础》

-  小豆米的【PaoTin++】入门系列之二：《机器基础》

-  小豆米的【PaoTin++】入门系列之三：《最常用内置变量和别名》

-  小豆米的【PaoTin++】入门系列之四：《最常用内置函数》

-  小豆米的【PaoTin++】入门系列之五：《事件驱动编程》

-  本雪的《新手向炮艇驾驶手册》

-  本炮的《PaoTin++/TinTin++ 语法入门》

门派攻略：

-  独孤残的明教教程，如何用 PaoTin++ 从拜师到 10w

-  小豆米的武当教程，武当新人门派任务0-10w

-  雪万剑的雪山派教程，从雪山新手任务聊一下Paotin++的学习过程

-  雪万剑的华山派教程，为华山派继绝学

-  雪万剑的古墓派新手攻略，我在北侠养蜜蜂

-  雪万剑的峨嵋派攻略，一个可以解毒的门派

-  雪万剑的天龙寺攻略，为了六脉神剑我出家了

-  阮寧玉的青城派攻略，我在青城山担水找蝙蝠的日子

* 精彩小品

-  李二狗的《2024年给第一次接触MUD的新人玩家之——超超超新手攻略》

-  李二狗的《给从未接触过MUD萌新的代码入门》

-  李二狗的《萌新的PaoTin++超初级机器人思路》

-  铁少羽的《PaoTin++ 新人打坐机器——记一次愉快的学习过程》

-  一色彩羽的《新人里程碑-游方天下任务》攻略（即神行千里 title 拿法）

-  看花人的《PaoTin++ 千里通 path.BotStep 用法详解》

常见问题

1. Windows 下怎么查看游戏内聊天信息

新开一个 PowerShell 窗口，然后输入以下命令就可以了：

```
Get-Content C:\my-paotin\log\dzp\chat.log -Tail 100 -Wait -encoding UTF8
```

注意其中的路径需要自己照猫画虎改一下，dzp 是你的 ID，除了 chat.log，还有 jh.log，qq.log，等等。

详细教程及更多相关话题请参考 Windows Terminal 使用技巧。

2. macOS/Linux 下怎么查看游戏内聊天信息

用 tmux 新开一个 shell，然后在其中输入 `mtail`，即可获得进一步指引。

3. Windows 下如何复制屏幕内容

按住 `Shift` 键，用鼠标选择。另外，同时按住 `Ctrl`+`Alt` 键也可以进行矩形选择，分屏模式下非常好用。

4. macOS 下如何复制屏幕内容

按住 `Shift` 或 `Option` 键，用鼠标选择。另外，同时按住 `Ctrl`+`Cmd` 键也可以进行矩形选择，分屏模式下非常好用。

5. PaoTin++ 可以和 TinTin++ 共存吗？

可以。因为：

- PaoTin++ 安装在独立的目录，属于绿色软件，不会对系统造成任何影响。当然也不会影响之前已经安装的 TinTin++。

- PaoTin++ 底层其实就是 TinTin++，所有的 TinTin++ 脚本都是合法的 PaoTin++ 脚本。可以直接使用。

6. 自己做的触发怎么才能不被别人的任务影响？

两个思路：

- 尽量用别致的文本做触发，比如那些别人接任务时你看不到的文本。

- 尽量缩短触发的生命周期，也就是说，没用别开，用完就关。

7. 怎么关闭自动 HP 摘要

按下 `ctrl+o`，然后松开双手，再按下大写字母 `H` 即可。

8. 怎么关闭自动吃喝

修改你的 ID 启动配置文件，然后在其中写入以下内容即可：

```
#var char[favorite][water] {NOTHING};
#var char[favorite][food]  {NOTHING};
```

9. 门派的新手任务有没有地方可以查询？

- 手动模式，NOTE xxx，需要提前做触发，面板实时可见

- 自动模式，jobLog xxx，需要提前做触发，log 方便查询

- 如果没做触发，想看以前的，翻看 buffer.log，内容比较多，可以用 grep 命令搜索

10. 为啥 pt 上 jobquery/localmaps 没有效果？

答：jobquery 请用 jq 代替，localmaps 请用 lm 代替。

北侠有一些命令，天生就有一长一短两个版本，像是 localmaps，输入起来比较麻烦，就可以用 lm，效果是一样的。这是服务器的设置。

然而，由于有些信息内容非常冗长，而且通常 pt 都已经做了触发，把内容解析好了存在变量里面备用，那么对于玩家来说，就显得有些刷屏。为此 pt 有个设计原则，就是对这种情况下，不易输入的长名字约定好只供脚本使用，可以在机器人里触发并访问相应的变量，也不再刷屏。但是短名称留给玩家手动输入。

由于新玩家对这些命令不够熟悉，有时候是先学到了 jobquery 命令和 localmaps 命令，却不知道它们的别名，那么就容易被 pt 搞懵圈。类似的命令共有如下这些：

- jq => jobquery，对应变量为 gJobState

- lm => localmaps

- mz => loyalty，对应变量为 gLoyalty

- sm => status_me，对应变量为 char[STATUS]

- sk => skills，对应变量为 char[Skills]

11. 如何直接在主屏内显示 chat 等聊天信息

pt 的 channel 信息配置文件是 `mud/pkuxkx/etc/ui-chat.tin`，里面包含如下内容：

```
#list chat-channel create {
{{pattern}{求助}                    {action}{helpmeLog} {gag}{true}}
{{pattern}{北侠QQ群}                {action}{qqLog}     {gag}{true}}
{{pattern}{{闲聊|副本|谣言}}        {action}{chatLog}   {gag}{true}}
{{pattern}{{门派|帮派|队伍}}        {action}{chatLog}   {gag}{true}}
{{pattern}{{江湖|任务|交易}}        {action}{jhLog}     {gag}{true}}
{{pattern}{{本地|区域|亡灵}}        {action}{bdLog}     {gag}{true}}
{{pattern}{{表决|醒目}}             {action}{chatLog}   {gag}{false}}
{{pattern}{{答问如流|备选答案}}     {action}{answerLog} {gag}{false}}
{{pattern}{私聊}                    {action}{tellLog}   {gag}{false}}
};
```

这里的`{gag}{true}`就代表屏蔽了对应的频道。如果我们想要解除屏蔽的话，就要通过pt的补充式加载（如果想知道什么是补充式加载，可以阅读`HELP load-file`）来实现自定义配置。

修改文件 `var/mud/pkuxkx/etc/ui-chat.extra.tin`（var其实就是my-paotin，如果发现子目录/文件不存在，依次创建即可），在里面写下如下内容：

```
///=== {
// ## chatChannel.Ungag <频道名称>
//    解除对特定频道的屏蔽
//    参数可以是
//        求助
//        北侠QQ群
//        闲聊、帮派、队伍
//        江湖、任务、交易
//        本地、区域、亡灵
//        表决、醒目
//        答问如流、备选答案
//        私聊
//    同行的参数实际上是在同一个屏蔽组中，因此你只需ungag其中一个即可。
// };
#alias chatChannel.Ungag {
#local channel {%1};
#if {{$channel} == {}} {
xtt.Usage {chatChannel.Ungag};
#return;
};
#local index {};
#foreach {*chat-channel[]} {index} {
#if {{$chat-channel[$index][pattern]} == {%*$channel%*}} {
#variable chat-channel[$index][gag] {false};
};
};
};

chatChannel.Ungag {北侠QQ群};
chatChannel.Ungag {闲聊};
```

其它channel的类似，只需将参数替换为对应的channel名就行。

用户心得

Windows Terminal 推荐配置：

显示效果：

> 来源: https://www.pkuxkx.net/wiki/tools/paotin/tips
