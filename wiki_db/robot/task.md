- ** 通告**

- 新手任务

- 红豆

- Zmud4.62版红豆机器人

- Cmud版红豆机器人

- Mush版红豆机器人 by Sure

- Mush版红豆机器人 by emyt

- Mush版红豆机器人 by Maper

- GRE

- Mush版GRE机器人

- 对诗

- Mush版茶馆对诗机器人

- 钓鱼

- 最简易的钓鱼机器人

- Mush版钓鱼机器人

- huoyu全注释版mush钓鱼机器人

- [MUSH]sure钓鱼机器人增强版

- 唱戏舞剑

- 新手唱戏舞剑机器人

- Zmud4.62版唱戏舞剑机器人

- 送信

- Mush版送信机器人

- 配药

- 抄经

- Mush版抄经+工号查询机器人

- 公共任务

-

- Mush版朱熹question机器人

- Mush版朱熹Question+读书、学习、练习机器人

- Zmud7.21版朱熹Question机器人

- Zmud4.62版朱熹Question机器人

- Cmud版朱熹Question机器人

- 北京茶馆对诗

- Mush版北京茶馆对诗机器人

- 华山送信

- 慕容信件

- TASK

- Zmud4.62+Mushclient版task机器人

- 灵鹫护卫

- 护镖任务

- Zmud4.62版半自动护镖机器人 of zgbl

- Zmud4.62版半自动护镖机器人 of lkyun

- Zmud4.62手动护镖辅助机器人

- Zmud4.62版全套机器人

- 萧峰任务

- 胡一刀任务

- 胡一刀机器人

- 护卫任务

- 保卫襄阳

- 保卫襄阳自动释仇机器人

- 门派任务

- 门忠任务

- 门派quest

- 白托放蛇

- 星宿炼毒

- 灵鹫扫雪

- Zmud4.62版灵鹫扫雪机器人

- 灵鹫扫雪机器人

- 朝廷系列

- Mush版朝廷守门机器人

- Mush版朝廷监斩机器人

- Zmud4.62朝廷系列机器人

- Zmud7.21朝廷通用机器人

---

** 通告**

因为北侠屡经修改和发展，本页面的所有机器人几乎都已经不适用了，请大家下载后当作学习使用而不是直接作为机器使用，使用也用不起来。

新手任务

红豆

Zmud4.62版红豆机器人

出品人：Engle原版，Zgbl改进，Sure编写题库

使用方法：载入后把reconnect里面的id和密码改成你自己的，然后再扬州客栈按F1就可以自动开始红豆答题

北大侠客行新手指南

Cmud版红豆机器人

出品人：Xxxcc

使用方法：在setting里面import，在CMUD里面设定好用户名和密码。

有人需要CMUD红豆机器，发一个

Mush版红豆机器人 by Sure

出品人：Sure

使用方法：指定jscript文件的位置，把解压开的kxcd目录放在worlds目录下，修改variables中的player和passwd

优点：Mush运行稳定，此机器人能自动更新题库

缺点：遇见不会的问题自动answer 1，可能回答错误导致中断连续回答正确次数，很难拿到15w pot

mush版红豆（开心词典）机器人

Mush版红豆机器人 by emyt

mush版红豆机器人

**此机器人为最新数据库，更新于2012年1月8日**

Mush版红豆机器人 by Maper

出品人：Maper

使用方法：

```
mush，lua语言，下载后解压到mushclient下的worlds文件夹。再安装数据源：控制面板---性能和维护----管理工具----数据源(ODBC)

如果编译错误，打开机器人后
文件---全局属性---lua：选中“允许载入DLL文件”，前面三行的true和false和下面的对照一下，按下面的来
trust_all_worlds = true    -- change to true to trust all the worlds
trust_all_plugins = true   -- change to true to trust all the plugins
warn_if_not_trusted = false -- change to true to show warnings
文件---游戏属性---scripts(脚本)：脚本语言选择lua，选中“启用脚本”

如果无法自动重连，文件---全局属性---常规---“游戏断线时显示警告对话框”，把前面的勾去掉试试看
```

mush，lua语言，下载后解压到mushclient下的worlds文件夹。再安装数据源：控制面板—性能和维护—-管理工具—-数据源(ODBC)。

```
打开mush后，在变量那里设置id和passwd，会自动开始。
如果出现什么问题，自行解决，不提供技术支持。
最后对sure表示感谢！
```

关于这个机器人使用的一些补充说明

-  使用者请仔细看看几个跟帖中的说明,跟着改一下相关内容

-  文件解压后其中一个红豆.MCL文件,里面的路径要改一下

-  script_filename=“E:\MUSHclient\worlds\hongdoutest\hongdoutest.lua”

-  就是这一行,就记事本打开就可以看见,把相应的路径改掉

-  如果还是不能运行顺利,那可能是MC的luaBox那搞鬼,具体原因可能较复杂,下面给出一个万金油式的解决方案—呵,可能有危险—点菜单上的–文件–>全局设置–>lua–>编辑,把luaBox里的全部清掉(记得删除之前要保留副本),这样就应该不会有问题了

游戏log：

```
ask hongdou about test
你向红豆打听有关『test』的消息。
红豆说道：看来不来点狠的是难不住你了！
红豆说道：准备好了吗？我开始出题了哦。

李商ョ隐《无题》ュ中运用神话传说抒┿情╁的句是子

1.  东风无力百花残
2.  青鸟殷勤为探看
3.  夜吟应觉月光寒
4.  蜡炬成灰泪始干

红豆说道：请用answer来回答(例如“answer 3”，表示你认为
第三个答案是正确的)，你只有3分钟的时间。你可以求助广大的bt们。
answer 2
> 红豆说道：恭喜你，答对了！
你的经验和潜能提高了！
你已经连续答对50道题了，真是大牛啊!
你获得了10000潜能的额外奖励！
```

[MUSH]红豆机器人

---

GRE

Mush版GRE机器人

出品人：Sure

使用说明：指定jscript文件的位置，把解压开的gre目录放在worlds目录下，修改variables中的player和passwd

挂机效率：500道gre大概要6-8小时

mush版gre机器人

对诗

Mush版茶馆对诗机器人

出品人：Sure

使用说明：在天桥s处save，压出来的poem.mdb文件要放在worlds/poem下

北京茶馆对诗trigger

钓鱼

最简易的钓鱼机器人

```
#TRIGGER {^??钓什么钓} {enter;u;do 9 n;hp} {diaoyu} 519
#TRIGGER {^??【%s饮水%s】*【%s经验%s】%s(%d)} {exp=%1;#if (%1>50000) {quit} {gua yuer;diao yu}} {diaoyu} 519
#TRIGGER {^??【%s食物%s】*【%s潜能%s】%s(%d)} {pot=%1} {diaoyu} 519
#TRIGGER {^??你的潜能增加了} {#wa 10000;diao yu} {diaoyu} 519
#TRIGGER {^??你一提杆，钓到了一条} {drop fish} {diaoyu} 519
#TRIGGER {^??你太累了} {#t- diaoyu;#wa 2500;do 5 s;#wa 2500;do 4 s;d;out;fadai;#t+ diaoyu} {diaoyu} 519
#TRIGGER {^??你发呆了一会儿} {#wa 5000;enter;u;do 4 n;#wa 2500;do 5 n;gua yuer;diao yu} {diaoyu} 519
#TRIGGER {^??你猛地一拉鱼线} {hp} {diaoyu} 519
```

使用方式：买鱼钩，足够多的鱼饵（一百、两百、三百，越多越好），汉水南岸gua yuer；diao yu开始

诸葛不亮（Zgbl）出品

最简单的钓鱼机器人……

Mush版钓鱼机器人

出品人：Sure

使用方法：有几两银子启动即可，注意变量里设定player、passwd

mush钓鱼trigger

huoyu全注释版mush钓鱼机器人

出品人：开水里养活鱼(huoyu)

```
-------------------钓鱼机器人 start--------------------------
require "wait"
require "tprint"
function diaoyu_start()
wait.make (function ()  --- coroutine below here
wait.regexp ("这里是城市的正中心，一个很宽阔的广场，铺着青石地面。一些游手好闲") -- 设置一个等待事件,只有在出现括号中的语句时,这行之后 end of coroutine 之前 代码才会被执行
wait.time (1) -- 等待1秒
Note( '回到ct了' ) -- 提示到达目的地
diaoyu_cttomatou() -- 从ct走道岸边
end)  -- end of coroutine
diaoyu_maiyuer() -- 去买鱼饵
end

function diaoyu_maiyuer()
wait.make (function ()  --- coroutine below here
wait.regexp ("你一走进杂货铺，老板就笑眯眯的跟你打招呼。这里卖一些杂七杂八的东西")-- 设置一个等待事件,只有在出现括号中的语句时,这行之后 end of coroutine 之前 代码才会被执行
wait.time (1) -- 等待1秒
Note( '到杂货铺了' ) -- 提示到达目的地
-- 以下是购买钓鱼物品
Send( 'buy yugou' )
wait.time (2)
Send( 'buy yuer 95;' )
wait.time (2)
Send( 'buy yuer 100;' )
wait.time (2)
Send( 'buy yuer 100;' )
--wait.time (2)
wait.time (2)
diaoyu_suzhoub()-- 从杂货铺返回ct
end)  -- end of coroutine
diaoyu_suzhou()-- 从ct到杂货铺去
end

function diaoyu_cttomatou()--从ct到岸边
create_trigger( 'diaoyu_to_matou', "面前是一条波涛翻滚的大江\\(river\\)。浊流滚滚，万舟竞", "", "diaoyu_diaoyu" ) --设置一个一次性触发器，当到达岸边时触发并执行diaoyu_diaoyu
Send( "do 9 n" )--到岸边去
wait.make (function ()  --- coroutine below here
wait.time (3)
Send( 'l' ) --到达岸边后look一次
end)  -- end of coroutine
end

function diaoyu_diaoyu()--开始钓鱼
Note( "开始钓鱼" ) -- 提示
local jingshen = tonumber( GetVariable ("jingshen") ) -- 提取现在精神值
local jingyan = tonumber( GetVariable ("jingyan") ) -- 提取现在经验值
if jingyan >= 50000 then --当经验大于5w，停止钓鱼并提醒
utils.msgbox ( "别钓拉，再钓也没有经验了" .. jingyan, "恭喜你" )
return false
end
if jingshen < 20 then --如果精神值小于20，跳到发呆函数
diaoyu_fadai()
return false
end

create_trigger( 'diaoyu_to_matou_ok', "你一提杆，钓到了一条(.*)，恭喜，恭喜。 ", "", "diaoyu_diaoyu_ok" ) --设置一个一次性触发器，当钓到鱼的时候执行diaoyu_diaoyu_ok函数
create_trigger( 'diaoyu_to_matou_no', "你猛地一拉鱼线，感到手上一沉", "", "diaoyu_diaoyu_end" ) --设置一个一次性触发器，当钓鱼完毕时执行diaoyu_diaoyu_end函数
create_trigger( 'diaoyu_to_no_jingshen', "你太累了，歇会再钓吧！", "", "diaoyu_fadai" )--设置一个一次性触发器，当"你太累了，歇会再钓吧！"时执行diaoyu_fadai函数去发呆
Note( "定时器返回：" )
Note(create_timer( 'diaoyu_to_matou_timeout', 50, '', 'diaoyu_to_matou_timeout' ) )--设置一个一次性定时器,如果50秒没有钓鱼成功,执行 diaoyu_to_matou_timeout 钓鱼超时函数

wait.make (function ()  --- coroutine below here
wait.time (1)
Send( "gua yuer" ) --
wait.time (1)
Send( "diao yu" ) --钓鱼

end)  -- end of coroutine
end

function diaoyu_to_matou_timeout() --超时后重新开始钓鱼
Note( "超时了重来" )
diaoyu_diaoyu() --重新开始钓鱼
end

function diaoyu_diaoyu_ok (name, line, wildcards) --成功钓到鱼
Note( "成功钓到鱼" )
Send( 'drop fish' ) --丢掉鱼
end

function diaoyu_diaoyu_end (name, line, wildcards) --钓鱼完毕
Send( 'hp' )
DeleteTimer( 'diaoyu_to_matou_timeout' ) --删除钓鱼超时触发器
wait.make (function ()  --- coroutine below here
wait.time (1)
diaoyu_diaoyu() --重新开始钓鱼
end)  -- end of coroutine
end

function diaoyu_report( yu ) --恶搞
local jingshen = GetVariable ("jingshen" )
local jingyan = GetVariable ("jingyan" )
local str = ""
--if yu == "" then
--        str = str .. "活鱼什么也没有掉到" .. "，"
--else
--        str = str .. "活鱼钓到了一条" .. yu .. "，"
--end
str = str .. "钓鱼钓的累死了，搞的我精神(" .. jingshen .. ")低落，经验高涨(" .. jingyan .. ") 待我去发呆室享受一次福利先"
Send( "chat " .. str )
end

function diaoyu_fadai() --发呆函数
diaoyu_report( "" )
create_trigger( 'diaoyu_fadai', "你发呆了一会儿", "", "diaoyu_fadaied" )--设置一个一次性触发器，当发呆完毕后执行diaoyu_fadaied函数去发呆
wait.make (function ()  --- coroutine below here
wait.time (1)
Send( 'do 9 s' )
wait.time (1)
Send( 'd' )
Send( 'out' )
wait.time (2)
Send( 'fadai' )
end)  -- end of coroutine
end

function diaoyu_fadaied()  --发呆完毕
wait.make (function ()  --- coroutine below here
Send( 'hp' )
wait.time (1)
Send( 'do 10 drink' )
wait.time (1)
Send( 'do 10 eat ganliang' )
wait.time (1)
Send( 'enter' )
Send( 'u' )
wait.time (1)
diaoyu_cttomatou() --执行从ct到岸边的函数重新开始钓鱼
end)  -- end of coroutine
end

function diaoyu_suzhou() -- 从ct到杂货铺
Execute( "e;e;e;e;e;e;se;s;e;n;n;n;n;n;nw;w;s" )
wait.make (function ()  --- coroutine below here
wait.time (3)
Send( 'l' )
end)  -- end of coroutine
end

function diaoyu_suzhoub() -- 从杂货铺到ct
Execute( "n;e;se;s;s;s;s;s;w;n;nw;w;w;w;w;w;w;l" )
wait.make (function ()  --- coroutine below here
wait.time (3)
Send( 'l' )
end)  -- end of coroutine
end

-------------------钓鱼机器人 end--------------------------

-- 创建一个临时的一次性触发器
-- AddTrigger的api见 http://mc.chinaido.com/help.php?function=AddTrigger
function create_trigger( t_name, t_match, t_response, t_function )
return AddTrigger(
t_name,
t_match,
t_response,
trigger_flag.Enabled + trigger_flag.RegularExpression + trigger_flag.Replace + trigger_flag.Temporary + trigger_flag.OneShot,
-1,
0,
"",
t_function
)
end
-- 创建一个临时的一次性定时器
-- AddTimer的api见 http://mc.chinaido.com/help.php?function=AddTimer
function create_timer( t_name, t_time, t_com, t_function )
return AddTimer (
t_name,
0,
0,
t_time,
t_com,
timer_flag.Enabled        + timer_flag.OneShot + timer_flag.TimerSpeedWalk + timer_flag.Replace        + timer_flag.Temporary,
t_function
)
end
```

mush lua 钓鱼机器人完全注释版

---

[MUSH]sure钓鱼机器人增强版

作者：小刀（Lzkd）

最近新人较多，有不少选择了钓鱼做为进入北侠的第一步。其中sure的钓鱼机器人挺受欢迎，不过，这个机器人也不是没有问题。

针对这些问题，花了点时间做了一下修改。呃……总的思路虽然没变，但部分核心代码和防出错的算法是重新写过了，所以个人觉得说是增强版是当之无愧的。

简单介绍一下新增内容。

-  sure当初写的时候，进ＭＵＤ时没有fullme提示，这导致现在用sure的机器人会有机率不能跑。

-  修改了钩一条鱼，买一条鱼的情况，一口气买50个yuer，效率上应该高一些了吧。

-  解决了之前的－－yuer莫名其妙不见的问题。

-  把js版本改成lua版本了（相当于重写一遍）

-  重写机器人的过程中，多写了不少注释，有兴趣的兄弟可以顺便学习一下。

用法就不多说了，相当简单。主要是修改player就passwd两个变量，给小号一点银子，就ＯＫ了。我挂了一天了，没啥问题，应该一切搞定了。欢迎下载使用。

[MUSH]sure钓鱼机器人增强版

唱戏舞剑

新手唱戏舞剑机器人

出品人：Akis

发个我修改的新手用舞剑唱曲机器人

Zmud4.62版唱戏舞剑机器人

出品人：Zgbl（不记得谁原创的……貌似就是akis……）
使用说明：

修改下autolog触发，这个是自动登录

唱戏/舞剑描述不同，修改下那个触发和别名中的ff指令就可以了

登录后客栈look自动触发

```
#ALIAS acc {pkuxkxuser;pkuxkxpassword}
#ALIAS ahb {ask lin about 护镖}
#ALIAS ahzb {ask lin about 护重镖}
#ALIAS aj {set brief 1;ask guo about 奖励;set brief 0}
#ALIAS alj {ask lin about 奖励}
#ALIAS andao {set brief 1;enter shudong;say 天堂有路你不走呀;d;set brief 0}
#ALIAS ar {l east;l south;l west;l north}
#ALIAS askarmor {ask chanshi about 铁护腕;ask chanshi about 皮手套;ask chanshi about 皮围脖;ask chanshi about 僧鞋;ask chanshi about 铁背心}
#ALIAS baituo {set brief 1;n;w;ask qian about 白驼山;give qian 1 gold;set brief 0}
#ALIAS baituob {set brief 1;nw;s;ask zhang about 扬州;e;s;set brief 0}
#ALIAS baoku {set brief 1;ask wu about 射月弓;give wu gong;push desk;#wa 1000;d;light lampn;light lamps;light lampe;light lampw;d;break men;d;set brief 0}
#ALIAS beijing {un;set brief 1;andao;7;set brief 1;n;do 2 ne;n;out;s;ne;do 6 n;set brief 0;wi}
#ALIAS beijingb {set brief 1;do 6 s;sw;n;zuan dong;s;do 2 sw;s;s;u;out;set brief 0}
#ALIAS bladebook {set brief 1;do 2 w;do 3 n;ask tian about 淫贼;set brief 0}
#ALIAS bladebookb {set brief 1;do 3 s;do 2 e;set brief 0}
#ALIAS bywc {ask guan shi about 完成}
#ALIAS ccc {pkuxkx.net~:8080}
#ALIAS ce {set brief 1;cemote $NOR$$ME$$HIY$纵声长啸：;set brief 0}
#ALIAS chaojing {e;n;ask zhu about job;ask zhu about 工号;#wa 2000;s;do 5 e;ne;do 2 n;do 3 nu;eu;write jing}
#ALIAS chl {w;n;w;s;s;e;e;w;w}
#ALIAS chlb {e;s;n;w;n;n;e;s;e}
#ALIAS chn2num {Years=%1;Abc_1=0;TotalDX=0;#if (%pos("十",@Years)=1) {#math TotalDX {@TotalDX+10}} {counter};#if (%pos("零十",@Years)<>0) {#math TotalDX {@TotalDX+10}};Def_2=%rightback(@Years,2);#math Abc_6 {(%pos(@Def_2,"一二三四五六七八九")+1)/2};#math TotalDX {@TotalDX+@Abc_6};chn2num=@TotalDX}
#ALIAS counter {#forall @lists {#math Abc_1 {@Abc_1+1};Abc_2=%pos(%i,@Years);#if (@Abc_2<>0) {#math Abc_3 {@Abc_2-2};Def_1=%copy(@Years,@Abc_3,2);#math Abc_4 {(%pos(@Def_1,"一二三四五六七八九")+1)/2};Abc_5=1;#loop @Abc_1 {#math Abc_5 {@Abc_5*10}};#math TotalDX {@TotalDX+@Abc_4*@Abc_5}}}}
#ALIAS dali {set brief 1;enter shudong;say 天堂有路你不走呀;d;8;se;s;do 2 sw;s;w;do 6 s;set brief 0}
#ALIAS dalib {set brief 1;do 9 n;tui bei;#wa 500;e;n;do 2 ne;n;nw;n;u;out;set brief 0}
#ALIAS dalunsi {set brief 1;andao;set brief 1;9;sw;s;do 3 sw;out;sw;wu;nw;knock gate;set brief 0}
#ALIAS dalunsib {set brief 1;se;ed;ne;zuan dong;do 3 ne;n;ne;e;u;out;set brief 0}
#ALIAS damo {set brief 1;open door;n;sw;se;n;s;w;e;#wa 500;w;do 2 e;s;w;n;nw;n;set brief 0}
#ALIAS duanyu {set brief 1;climb yafeng;do 4 s;push stone;s;do 2 e;do 2 ed;push men;do 2 e;set brief 0}
#ALIAS dusheku {set brief 1;do 6 e;s;do 2 e;nd;w;set brief 0}
#ALIAS dushekub {set brief 1;e;su;do 2 w;n;nw;do 6 w;set brief 0}
#ALIAS ef {yun regenerate}
#ALIAS emei {set brief 1;do 9 s;sw;do 2 w;nw;#wa 1000;do 2 w;nw;w;nw;n;nu;unwield right;unwield left;nu;n;e;eu;do 2 nu;eu;n;wi;set brief 0}
#ALIAS emei1 {set brief 1;do 9 s;sw;w;w;nw;#wa 1000;do 2 w;nw;w;nw;n;nu;unwield right;unwield left;nu;wield all;n;e;set brief 0}
#ALIAS emeib {set brief 1;s;wd;do 2 sd;wd;w;s;sd;#wa 1000;sd;s;se;e;se;do 2 e;se;do 2 e;ne;#wa 1000;do 9 n;set brief 0}
#ALIAS er {yun recover}
#ALIAS feng {set brief 1;ask yue about 令狐冲;ask yue about 思过崖;n;northwest;w;wu;sd;eu;ask linghu about 岳灵珊;ask linghu about 风太师叔;enter dong;south;set brief 0}
#ALIAS fengb {set brief 1;n;out;wd;nu;ed;e;se;s;set brief 0}
#ALIAS fudi {set brief 1;climb yafeng;do 4 s;push stone;s;do 2 e;do 2 ed;push men;do 2 e;set brief 0}
#ALIAS fumoquan {set brief 1;w;e;s;e;do 2 n;e;w;s;set brief 0}
#ALIAS gai {set brief 1;enter shudong;say 天堂有路你不走呀;d;2;ne;ne;u;enter;e;set brief 0}
#ALIAS gaibang {set brief 1;#4 e;n;e;n;w;n;e;n;w;n;set brief 0}
#ALIAS gaibangb {set brief 1;s;s;#4 w;;set brief 0}
#ALIAS gb {give bao wu to qu qing}
#ALIAS gd {gan che to down}
#ALIAS ge {gan che to east}
#ALIAS ged {gan che to eastdown}
#ALIAS genter {gan che to enter}
#ALIAS geu {gan che to eastup}
#ALIAS gg {get gold from corpse;get silver from corpse;get xi from corpse}
#ALIAS ggg {get sword;get di;get whip}
#ALIAS gn {gan che to north}
#ALIAS gnd {gan che to northdown}
#ALIAS gne {gan che to northeast}
#ALIAS gnu {gan che to northup}
#ALIAS gnw {gan che to northwest}
#ALIAS gout {gan che to out}
#ALIAS gs {gan che to south}
#ALIAS gsd {gan che to southdown}
#ALIAS gse {gan che to southeast}
#ALIAS gsu {gan che to southup}
#ALIAS gsw {gan che to southwest}
#ALIAS gu {gan che to up}
#ALIAS guiquan {wudang2;set brief 1;e;drink}
#ALIAS guiyun {set brief 1;do 6 e;se;n;se;n;w;n;do 5 e;do 5 e;do 2 nu;set brief 0}
#ALIAS guiyunb {set brief 1;do 8 w;e;#wa 1000;do 2 sd;do 5 w;taihub;set brief 0}
#ALIAS gumu {quanzhen;set brief 1;#wa 500;do 5 n;#wa 500;do 6 n;#wa 500;nd;wd;ed;ask yang about 进墓;set brief 0}
#ALIAS gumub {set brief 1;ask sun about 出墓;do 3 s;wu;eu;su;#wa 500;do 6 s;open door;do 6 s;#wa 1000;quanzhenb;set brief 0}
#ALIAS gw {gan che to west}
#ALIAS gwd {gan che to westdown}
#ALIAS gwu {gan che to westup}
#ALIAS hlm {hit liu mang;hit liu mang 2;hit liumang tou;hit qin;hit he;hit gonggong;hit yin;hit li;hit di pi}
#ALIAS huashan {set brief 1;do 5 n;nw;do 6 n;#wa 1000;do 5 e;#wa 1000;se;su;eu;su;eu;do 2 su;#wa 1000;sd;su;do 2 s;s;do 2 w;set brief 0}
#ALIAS huashanb {set brief 1;do 3 e;w;do 3 n;nd;nu;do 2 nd;#wa 1000;wd;nd;wd;nd;nw;do 3 w;#wa 500;do 2 w;do 6 s;se;#wa 500;do 5 s;set brief 0}
#ALIAS huyidao {andao;7;set brief 1;n;do 2 ne;n;out;set brief 0}
#ALIAS huyidaob {set brief 1;zuan dong;s;do 2 sw;do 2 s;u;out;set brief 0}
#ALIAS hzxw {e;n;w;do 2 s;w}
#ALIAS jiaxing {set brief 1;do 6 e;se;s;do 2 e;set brief 0}
#ALIAS jiaxingb {set brief 1;do 2 w;w;n;nw;do 6 w;set brief 0}
#ALIAS jiema {set brief 1;#2 e;#2 n;w;ask ma fu about 借马;e;#2 s;e;s;ask guo fu about 小红马;ask guo fu about 白雕;give diao chu to guo;#wa 2000;n;w;do 2 n;w;get ma;e;do 2 s;do 2 w;set brief 0}
#ALIAS jiuyin {swim river;do 2 n;e;do 2 n;w;enter xuanwo}
#ALIAS kxcd {do 2 n;w;u;ask hongdou about 开心辞典}
#ALIAS lcc {look corpse}
#ALIAS le {look east}
#ALIAS linghub {set brief 1;wd;nu;ed;e;se;s;set brief 0}
#ALIAS lingjiu {set brief 1;do 6 w;nu;nd;do 2 w;nw;w;#wa 1000;do 2 nw;nu;do 2 n;do 2 nu;set brief 0}
#ALIAS lingjiub {set brief 1;do 2 sd;do 2 s;sd;do 2 se;e;#wa 1000;se;do 2 e;su;sd;do 6 e;set brief 0}
#ALIAS lingzhou {set brief 1;do 6 w;nu;nd;do 2 w;nw;#wa 1000;w;do 2 nw;nu;n;do 5 w;set brief 0}
#ALIAS lingzhoub {set brief 1;do 5 e;s;sd;do 2 se;#wa 1000;e;se;do 2 e;su;sd;do 6 e;set brief 0}
#ALIAS litiezui {set brief 1;do 5 n;nw;#wa 1000;do 6 n;#wa 1000;do 5 e;n;set brief 0}
#ALIAS litiezuib {set brief 1;s;do 5 w;#wa 1000;do 6 s;#wa 1000;se;do 5 s;set brief 0}
#ALIAS lll {l ju mang}
#ALIAS ln {look north}
#ALIAS lr {look robber}
#ALIAS ls {look south}
#ALIAS luoyang {set brief 1;enter shudong;say 天堂有路你不走呀;d;1;n;do 3 nw;n;nw;#wa 500;u;do 2 e;s;sw;nw;do 4 w;#wa 500;wu;wd;do 3 w;set brief 0}
#ALIAS luoyangb {set brief 1;do 3 e;eu;ed;do 4 e;#wa 500;se;ne;n;do 2 w;enter dong;#wa 500;se;s;do 3 se;do 2 s;u;out;set brief 0}
#ALIAS lvliu {set brief 1;do 6 w;nu;nd;do 2 w;nw;w;nw;do 2 wu;nw;#wa 1000;do 7 w;do 3 n;do 3 w;sw;w;se;set brief 0}
#ALIAS lvliub {set brief 1;nw;e;ne;do 4 e;s;do 3 s;#wa 1000;do 4 e;e;se;do 2 ed;se;e;se;do 2 e;#wa 1000;su;sd;do 6 e;set brief 0}
#ALIAS lvzhou {set brief 1;sw;do 2 nw;sw;se;ne;set brief 0}
#ALIAS lw {look west}
#ALIAS meizhuang {set brief 1;do 5 e;n;knock gate 4;knock gate 2;knock gate 5;knock gate 3;set brief 0}
#ALIAS menggu {set brief 1;do 2 e;n;ask nvyong about 郭大侠;s;#wa 500;do 4 w;do 2 s;ask guojing about 报国;#wa 1000;do 2 n;do 2 e;do 4 n;give ling to jiang;#wa 2000;ride ma;do 8 n;answer 送信;set brief 0}
#ALIAS mhz {set brief 1;give shou yin to shen ling;#wa 2000;s;e;n;w;s;w;do 3 e;n;break men;s;set brief 0}
#ALIAS mingjiao {andao;set brief 1;6;do 2 w;nw;w;nw;u;s;w;nw;do 4 nu;set brief 0}
#ALIAS mingjiaob {set brief 1;do 2 s;n;do 4 sd;se;e;n;zuan dong;se;e;se;do 3 e;u;out;set brief 0}
#ALIAS mishi {say 明教密室;ask xiao zhao about 张无忌;ask xiao zhao about 乾坤大挪移;ask xiao zhao about 密室;follow xiao zhao}
#ALIAS murong {suzhou;set brief 1;#wa 1000;n;nw;do 5 w;s;ask girl about 拜庄;enter boat;set brief 0}
#ALIAS murongb {set brief 1;n;do 5 e;se;s;#wa 1000;suzhoub;set brief 0}
#ALIAS paladin {set brief 1;climb yafeng;do 2 s;do 3 sw;s;e;n;w;n;w;climb cliff;set brief 0}
#ALIAS paladinb {set brief 1;d;e;s;do 3 ne;s;push stone;s;#wa 500;e;do 2 ed;push men;do 2 e;set brief 0}
#ALIAS pingxi {set brief 1;do 9 s;#wa 1000;sw;do 2 w;nw;do 3 sw;#wa 1000;do 5 n;ask tou about 自立为王;set brief 0}
#ALIAS pingxib {drop ling;set brief 1;do 9 s;n;#wa 1000;do 3 ne;#wa 1000;se;do 2 e;ne;#wa 1000;do 9 n;set brief 0}
#ALIAS pker {set brief 1;do 6 w;wu;nu;wu;do 3 e;set brief 0}
#ALIAS pkerb {set brief 1;do 3 w;ed;sd;ed;do 6 e;set brief 0}
#ALIAS ptz {set brief 1;w;e;s;e;n;n;e;w;s;enter;ask du nan about 菩提子;set brief 0}
#ALIAS pxy {perform xiyang}
#ALIAS qiuqianren {set brief 1;do 5 s;#wa 1000;do 4 s;se;set brief 0}
#ALIAS qiurao {perform parry.qiurao}
#ALIAS qj {perform unarmed.hqgy}
#ALIAS qqq {halt;quit}
#ALIAS quanzhen {set brief 1;do 5 n;nw;#wa 500;do 6 n;#wa 500;do 2 nw;w;do 2 nw;#wa 500;n;nw;do 2 nu;n;nu;#wa 500;do 2 n;set brief 0}
#ALIAS quanzhenb {set brief 1;do 2 s;sd;s;do 2 sd;#wa 500;se;s;do 2 se;e;#wa 500;do 2 se;#wa 500;do 6 s;se;#wa 500;do 5 s;set brief 0}
#ALIAS quanzhou {set brief 1;do 6 e;se;do 2 s;e;do 5 s;set brief 0}
#ALIAS quanzhoub {set brief 1;do 5 n;w;n;nw;do 6 w;set brief 0}
#ALIAS qujob {ask qu qing about job}
#ALIAS re {huashan}
#ALIAS reb {huashanb}
#ALIAS recall {~recall;#RECALL AutomapperAll}
#ALIAS riyue {set brief 1;do 5 w;do 2 n;ne;do 2 nu;set brief 0}
#ALIAS riyueb {set brief 1;do 2 sd;sw;do 2 s;do 5 e;set brief 0}
#ALIAS ruzhou {huyidao;set brief 1;s;do 2 sw;set brief 0}
#ALIAS ruzhoub {set brief 1;do 2 ne;n;huyidaob;set brief 0}
#ALIAS sandu {ask du nan about 菩提子;ask du e about 伏魔刀;ask du jie about 金刚罩}
#ALIAS shaolin {set brief 1;unwield right;unwield left;enter shudong;say 天堂有路你不走呀;d;3;do 2 ne;u;sw;#wa 500;e;sd;e;do 2 nu;wu;do 3 nu;e;#wa 500;eu;do 3 nu;n;#wa 1000;knock gate;do 2 n;nu;do 3 n;nu;n;wi;set brief 0}
#ALIAS shaolinb {set brief 1;sd;do 4 s;sd;do 3 s;sd;s;open gate;#wa 1000;do 2 s;do 3 sd;wd;w;#wa 500;do 3 sd;ed;do 2 sd;e;#wa 1000;ruzhoub;set brief 0}
#ALIAS shedong {set brief 1;do 6 e;#wa 500;se;n;se;n;w;n;#wa 500;do 5 e;#wa 1000;do 3 nu;w;set brief 0}
#ALIAS shedongb {set brief 1;e;do 3 sd;#wa 500;do 5 w;#wa 500;s;e;s;nw;s;nw;#wa 500;do 6 w;set brief 0}
#ALIAS shenlong {andao;set brief 1;7;n;do 2 ne;n;out;#wa 500;s;ne;se;ask chuan fu about 出海;set brief 0}
#ALIAS shenlong2 {set brief 1;n;do 9 e;#wa 1000;do 5 e;#wa 500;do 2 nu;eu;n;do 2 nu;do 2 n;n;nu;eu;n;do 3 nu;wu;nu;set brief 0}
#ALIAS shenlong2b {set brief 1;sd;ed;do 4 sd;s;wd;sd;do 3 s;#wa 1000;sd;s;wd;do 2 sd;do 5 w;#wa 1000;do 9 w;s;ask chuan fu about 出海;set brief 0}
#ALIAS shenlongb {set brief 1;nw;sw;n;zuan dong;s;do 2 sw;do 2 s;u;out;set brief 0}
#ALIAS shiban {say 上报四重恩，下济三途苦;#4 pull stone up;#3 push stone down}
#ALIAS shuikao {set brief 1;do 6 e;se;s;do 2 e;nd;#wa 500;ask chou diao about 独孤求败;nu;ask yu fu about 过河;se;catch fish;nw;give fish to yu fu;#wa 1500;swim;pick sword;set brief 0}
#ALIAS shuikaob {set brief 1;swim;do 2 sd;su;do 2 w;n;#wa 500;nw;do 6 w;set brief 0}
#ALIAS slmb {set brief 1;sw;se;n;s;w;e;w;e;e;s;w;do 2 n;nw;n;set brief 0}
#ALIAS staffbook {gaibang;ask lu about 棒法秘籍}
#ALIAS staffbookb {gaibangb}
#ALIAS stop {#t- dazuo}
#ALIAS suzhou {set brief 1;do 6 e;se;s;e;do 4 n;set brief 0}
#ALIAS suzhoub {set brief 1;do 4 s;w;n;nw;do 6 w;set brief 0}
#ALIAS swe {swear 我将永远忠于帮主，若有悖逆，天诛地灭!!}
#ALIAS swordbook {set brief 1;do 5 n;nw;#wa 500;do 4 n;w;nw;ask punk about 王小二;#wa 500;se;e;do 2 n;do 2 nw;ne;enter hole;ask wang about 鸡;set brief 0}
#ALIAS swordbookb {set brief 1;w;sw;do 2 se;do 6 s;#wa 500;se;do 5 s;set brief 0}
#ALIAS taihu {set brief 1;do 6 e;se;n;se;n;w;n;#wa 1000;do 5 e;set brief 0}
#ALIAS taihub {set brief 1;do 5 w;s;e;s;nw;s;nw;#wa 1000;do 6 w;set brief 0}
#ALIAS taishan {set brief 1;do 6 e;#wa 500;ne;do 2 n;do 3 nu;#wa 500;eu;do 7 nu;set brief 0}
#ALIAS taishanb {set brief 1;do 7 sd;#wa 500;wd;do 3 sd;#wa 500;do 2 s;sw;#wa 200;do 6 w;set brief 0}
#ALIAS taohua {set brief 1;do 6 e;se;s;do 2 e;#wa 500;nd;do 4 e;n;set brief 0}
#ALIAS taohuab {set brief 1;s;do 4 w;su;do 2 w;n;nw;#wa 500;do 6 w;set brief 0}
#ALIAS taoyuan {wudang;set brief 1;#wa 1000;ed;do 2 e;ed;sd;ed;sd;ed;do 2 e;set brief 0}
#ALIAS taoyuanb {set brief 1;do 2 w;wu;nu;wu;nu;wu;do 2 w;wu;#wa 1000;wudangb;set brief 0}
#ALIAS tdhb {do 4 s;w;do 2 n;e;n;s}
#ALIAS tiandihui {luoyang;set brief 1;#wa 1000;do 3 s;do 3 e;n;do 2 e;#wa 500;knock guancai 3;ed;do 3 s;#wa 300;w;e;do 4 n;e;set brief 0}
#ALIAS tiandihuib {set brief 1;w;do 4 s;w;do 2 n;e;n;s;wu;#wa 1000;do 2 w;s;do 3 w;do 3 n;#wa 500;luoyangb;set brief 0}
#ALIAS tianlong {set brief 1;do 4 s;do 5 s;#wa 500;sw;do 2 w;nw;do 5 sw;#wa 1000;wu;nu;n;set brief 0}
#ALIAS tianlongb {set brief 1;s;sd;ed;do 4 ne;se;#wa 600;do 2 e;ne;do 9 n;set brief 0}
#ALIAS tianshan {set brief 1;enter shudong;say 天堂有路你不走呀;d;4;do 3 w;do 3 nw;ask alamuhan about 马;set brief 0}
#ALIAS tianshanb {set brief 1;do 3 se;e;se;do 2 e;#wa 500;su;sd;do 6 e;set brief 0}
#ALIAS tieshouzhang {set brief 1;w;drop hand;e;ask seng about 铁手掌;l hand;set brief 0}
#ALIAS tufei {set brief 1;do 9 s;#wa 1000;sw;w;su;set brief 0}
#ALIAS tufeib {set brief 1;nd;e;se;do 2 e;e;#wa 500;ne;do 9 n;set brief 0}
#ALIAS tulongdao {set brief 1;n;e;n;w;n;s;do 2 e;do 2 n;ask xie about 屠龙刀;set brief 0}
#ALIAS tulongdaob {set brief 1;do 3 s;w;e;n;nw;set brief 0}
#ALIAS un {unwield left;unwield right}
#ALIAS uq {unwield qud;unwield qus}
#ALIAS uw {unwield all}
#ALIAS wi {wield sword;wield dao;wield all}
#ALIAS wl {do 9 s;sw;do 2 w;nw;do 4 sw;nw;do 3 nu}
#ALIAS wlb {do 3 sd;s;se;do 4 ne;#wa 500;se;do 2 e;ne;#wa 1000;do 9 n}
#ALIAS wudang {set brief 1;do 9 s;#wa 1000;sw;do 2 w;w;nw;do 3 w;wu;#wa 500;do 3 nu;w;do 2 nu;#wa 300;do 2 eu;do 2 nu;set brief 0}
#ALIAS wudang2 {set brief 1;do 9 s;#wa 1000;sw;do 2 w;nw;do 3 w;wu;#wa 500;do 3 nu;w;do 2 nu;#wa 500;do 2 eu;nu;do 2 wu;nu;wu;nu;#wa 1000;do 3 eu;do 5 s;set brief 0}
#ALIAS wudangb {set brief 1;s;sd;#wa 500;sd;do 2 wd;do 2 sd;e;do 3 sd;ed;#wa 1000;do 3 e;se;do 2 e;ne;#wa 1000;do 9 n;set brief 0}
#ALIAS wuliang {set brief 1;do 9 s;#wa 1000;sw;do 2 w;nw;do 4 sw;#wa 500;nw;do 3 nu;set brief 0}
#ALIAS wxd {set brief 1;n;w;n;e;s;u;out;set brief 0}
#ALIAS xf {luoyang;s2;n;w;u;ask xiao about job}
#ALIAS xfan {set brief 1;do 9 s;#wa 800;do 2 wu;do 2 s;s;sd;do 2 e;n;u;set brief 2}
#ALIAS xfanb {set brief 1;d;s;do 7 w;s;e;s;nw;s;nw;do 6 w;set brief 0}
#ALIAS xfb {d;e;s;luoyangb}
#ALIAS xff {luoyang;s2;n;w;u;ask xiao about finish;give shou ji to xiao;ask xiao about test}
#ALIAS xiangyang {huyidao;s;set brief 1;#2 sw;#wa 1000;#5 n;#wa 1000;ask shou jiang about 投军;#4 n;set brief 0}
#ALIAS xiangyangb {set brief 1;drop yao pai;drop bian tiao;#wa 1000;#5 s;#wa 1000;#4 s;#2 ne;n;#wa 500;huyidaob;set brief 0}
#ALIAS xianyangb {set brief 1;drop yao pai;drop bian tiao;#wa 1000;#5 s;#wa 1000;#4 s;#2 ne;n;#wa 500;huyidaob}
#ALIAS xiaocun {set brief 1;#5 n;nw;#6 n;set brief 0}
#ALIAS xiaocunb {set brief 1;#6 s;se;#5 s;set brief 0}
#ALIAS xingxiu {set brief 1;enter shudong;say 天堂有路你不走呀;d;4;w;w;w;#wa 1000;nw;wu;n;set brief 0}
#ALIAS xingxiub {set brief 1;s;ed;se;e;se;#wa 1000;e;e;su;sd;e;e;e;#wa 1000;e;e;e;set brief 0}
#ALIAS xizao {set brief 1;#3 s;#2 w;give zhaodai 30 silver;enter;e;bath;set brief 0}
#ALIAS xuelian {set brief 1;#2 se;#2 wu;ride horse;jump valley;get xuelian;set brief 0}
#ALIAS xuelianb {set brief 1;ed;ride horse;jump valley;#2 ed;#2 nw;drop horse;get armor;wear armor;save;set brief 0}
#ALIAS xxb {set brief 1;s;ed;se;e;se;e;e;su;sd;e;e;e;e;e;e;set brief 0}
#ALIAS xxx {set brief 1;xingxiu;n;nd;n;nw;w;set brief 0}
#ALIAS xyangb {set brief 1;do 9 s;w;do 2 nu;w;wu;wd;wd;wu;w;nw;n;w;do 2 sw;w;do 3 s;wu;eu;su;do 10 s;do 3 s;sd;s;do 2 sd;se;s;do 2 se;e;do 2 se;do 6 s;se;do 5 s;set brief 0}
#ALIAS xyb {set brief 1;do 9 s;w;w;nu;w;ne;zuan dong;sw;sw;sw;u;out;set brief 0}
#ALIAS yashan {set brief 1;#6 e;se;s;e;e;se;#wa 1000;ne;e;ne;ne;#7 e;set brief 0}
#ALIAS yashanb {set brief 1;#7 w;sw;sw;w;sw;#wa 1000;nw;w;w;n;nw;#6 w;set brief 0}
#ALIAS yee {yell 船家}
#ALIAS yinggu {set brief 1;#5 s;#wa 1000;#4 s;#wa 1000;se;e;sw;sw;s;#wa 1000;e;n;w;s;s;w;set brief 0}
#ALIAS yinggub {set brief 1;out;ne;w;nw;#wa 1000;#5 n;#wa 1000;#4 n;set brief 0}
#ALIAS yinzhe {set brief 1;s;w;w;e;s;set brief 0}
#ALIAS yinzheb {set brief 1;#5 n;set brief 0}
#ALIAS yl {yun lifeheal}
#ALIAS yp {yun powerup}
#ALIAS yr {yun recover}
#ALIAS yubi {set brief 1;e;se;#4 sw;s;e;n;w;n;set brief 0}
#ALIAS ywm {set brief 1;do 6 e;se;s;#wa 1000;do 2 e;s;w;s;e;n;e;set brief 0}
#ALIAS ywmb {set brief 1;w;s;w;n;e;n;w;w;#wa 1000;n;nw;do 6 w;set brief 0}
#ALIAS zanpu {set brief 1;do 9 s;sw;do 2 w;#wa 1000;nw;do 2 w;do 4 nw;w;do 3 n;set brief 0}
#ALIAS zanpub {set brief 1;do 3 s;e;do 4 se;#wa 500;do 2 e;se;do 2 e;ne;#wa 1000;do 9 n;set brief 0}
#ALIAS zsf {set brief 1;sw;s;se;e;ne;n;nw;sw;s;e;set brief 0}
#ALIAS zsfb {set brief 1;w;n;ne;se;w;set brief 0}
#ALIAS z {ask fu about 失败}
#ALIAS tianshanmen {enter shudong;say 天堂有路你不走呀;d;4;#3 w;nw;wu}
#ALIAS tianshanmenb {ed;tianshanb}
#ALIAS q {quest}
#ALIAS qq {ask ning about quest}
#ALIAS af {ask fu about job}
#ALIAS gf {give fu yuxi}
#ALIAS wa {wear all}
#ALIAS kp {kill pantu}
#ALIAS h {hp}
#ALIAS yuefeib {w;s;w;n;n;w;n;nw;do 6 w}
#ALIAS yuefei {do 6 e;se;s;e;s;s;e;n;e}
#ALIAS heizhe {do 9 s;se;e;sw;s;e;n;w;s;s;w}
#ALIAS heizheb {out;ne;w;nw;do 9 n}
#ALIAS 听香水榭 {w;do 3 n;tan qin;#wa 1000;row tingxiang}
#ALIAS 燕子坞 {w;do 3 n;tan qin;#wa 1000;row yanziwu}
#ALIAS 曼陀山庄 {w;do 3 n;tan qin;#wa 1000;row mantuo}
#ALIAS 琴韵小筑 {enter boat;row qinyun}
#ALIAS eb {enter boat}
#ALIAS cw {changewield}
#ALIAS fj {fill jiudai;fill hulu}
#ALIAS map {localmaps}
#ALIAS yueer {do 6 w;nu;nd;w;w;nw;climb mount}
#ALIAS yueerb {ne;se;e;e;su;sd;do 6 e}
#ALIAS pkerl {do 9 s;wu;wu;n;n;n}
#ALIAS pkerlb {do 3 s;ed;ed;#9 n}
#ALIAS aaa {s;e;s;s;s;sd;s;s;s;sd;w;shiban;d}
#ALIAS ae {aime;view}
#ALIAS al {load;#wa 8000}
#ALIAS an {aimn;view}
#ALIAS as {aims;view}
#ALIAS aw {aimw;view}
#ALIAS backby {wu;halt}
#ALIAS backsz {dalib;#wa 6000;say 表演回苏州}
#ALIAS bbb {u;e;nu;n;n;n;nu;n;w;n;n;n;sleep}
#ALIAS begin {#t+ dazuo;hp}
#ALIAS bydali {#AL backsz {dalib;#wa 6000;say 表演回苏州}}
#ALIAS byemei {#AL backsz {emei2b;#wa 6000;say 表演回苏州}}
#ALIAS byguiyun {#AL backsz {#wa 3000;taihub;#wa 6000;say 表演回苏州}}
#ALIAS byhuashan {#AL backsz {#wa 3000;huashan1b;#wa 6000;say 表演回苏州}}
#ALIAS bykill {#AL backsz {#wa 3000;sd;ed;do 6 e;#wa 6000;say 表演回苏州}}
#ALIAS bylingzhou {#AL backsz {#wa 3000;do 5 e;s;sd;se;se;e;#wa 1000;se;e;e;su;sd;do 6 e;#wa 12000;say 表演回苏州}}
#ALIAS bypingxi {#AL backsz {#wa 3000;pingxi1b;#wa 6000;say 表演回苏州}}
#ALIAS byquanzhen {#AL backsz {#wa 3000;quanzhen1b;#wa 6000;say 表演回苏州}}
#ALIAS byquanzhou {#AL backsz {#wa 3000;quanzhoub;#wa 6000;say 表演回苏州}}
#ALIAS bysz {#AL backsz {#wa 3000;do 4 n;sw;#wa 3000;22}}
#ALIAS bytaohua {#AL backsz {#wa 3000;taohua1b;#wa 6000;say 表演回苏州}}
#ALIAS bywudang {#AL backsz {#wa 3000;wudangb;#wa 6000;say 表演回苏州}}
#ALIAS byxiaocun {#AL backsz {#wa 3000;do 6 s;se;do 5 s;#wa 6000;say 表演回苏州}}
#ALIAS byyz {#AL backsz {#wa 3000;n;n;#wa 6000;say 表演回苏州}}
#ALIAS chan {perform chan}
#ALIAS chifan {sit chair;knock table;#3 eat shangyueshipin;#3 drink wan}
#ALIAS cm {perform cuiming}
#ALIAS dangpub {s;e;e;e;ed;ed;ed;ed;se;nw;#9 n}
#ALIAS dangpu {w;w;w;w;w;w;wu;nu;wu;e;e;n}
#ALIAS dushe {#6 e;#wa 1000;s;e;e;nd;w}
#ALIAS dusheb {e;su;w;w;n;nw;#wa 1000;#6 w}
#ALIAS ee {exert regenerate}
#ALIAS fan {eat ya;drink jiudai}
#ALIAS fb {linghub;s;w;s}
#ALIAS fd {perform feidao}
#ALIAS ff {#wa 3000;biaoyan wujian}
#ALIAS f {fire}
#ALIAS getbing {do 9 w;do 2 u;zuan dong;get all;}
#ALIAS getling {do 5 e;eu;e;eu;wd;w;wd;do 5 w;do 5 s;do 5 n;do 5 e;eu;e;eu;ed; #t+ searchway;}
#ALIAS getxiang {do 5 e;eu;e;hitall;lt;}
#ALIAS goshedanb {do 2 e;do 3 sd;#wa 1000;do 5 w;#wa 1000;s;e;s;nw;s;#wa 1000;nw;do 6 w;}
#ALIAS goshedan {do 9 s;do 2 wu;#wa 1000;do 2 s;do 2 nu;do 2 w;kill ju;}
#ALIAS h2 {unwield sword 2;wield sword}
#ALIAS hand {ef;#wa 1000;hit liang;#15 study hand;h;#wa 500;h}
#ALIAS jiab {out;e;n;n;n}
#ALIAS jia {s;s;s;w;enter afei;find}
#ALIAS kmg {killall bing;kqb;kqf}
#ALIAS kqb {killall qibing}
#ALIAS kqf {killall zhang}
#ALIAS leaveby {halt;ed}
#ALIAS lh {perform spear.lianhuan}
#ALIAS lt {perform strike.leiting}
#ALIAS lzhb {wd;wd;w;wd;w;w;w;w;w;do 9 s;w;w;nu;w;ne;zuan dong;sw;sw;sw;u;out}
#ALIAS maiyirenb {w;w;#wa 1000;s;e;s;nw;s;nw;#wa 1000;do 6 w}
#ALIAS maiyiren {do 6 e;#wa 1000;se;n;se;n;w;n;#wa 1000;e;e;}
#ALIAS minnvb {s;e;s;nw;s;nw;#wa 1000;do 6 w}
#ALIAS minnv {do 6 e;#wa 1000;se;n;se;n;w;n;}
#ALIAS ns {exert neilisuck}
#ALIAS outxia {s;se;su;su;su;#wa 1000;out;out;wd;ed;nd;#wa 1000;nw;#3 n;#wa 1000;#4 n;enter boat}
#ALIAS paobu {open door;n;sw;se;n;s;w;e;w;#wa 600;#2 e;s;w;n;nw;n;out;s;#wa 1000;hp}
#ALIAS peiy {ask ping about 工作;n;peiyao}
#ALIAS pw {s;give ping yao}
#ALIAS qianchi {n;n;n;n;n;nw;n;n;n;n;n;n;e;e;e;e;e;e;se;su;eu}
#ALIAS sanfeng {w;sw;s;se;e;ne;n;nw;sw;s;e;open door;n}
#ALIAS shaolinb2 {s;#3 sd;wd;w;#3 sd;ed;#2 sd;e;#3 s}
#ALIAS shibai {give 10 silver to guan}
#ALIAS ss {ask guan about job;#wa 4000}
#ALIAS studyjiuyin {#6 ef;getout 4;#10 zuanyan zhenjing;#wa 1000;#6 ef;#wa 500;#15 zuanyan zhenjing;store zhenjing;#wa 1000;pp;sleep}
#ALIAS sword {perform sword.qixing}
#ALIAS t {perform finger.tan}
#ALIAS wearqu {drop cloth;drop shoes;wear qzhitao;wear qhubo;wear qshoutao;wear qyaodai;wear qcap;wear qhuwan;wear qsurcoat;wear qshoes}
#ALIAS wq {wield qud;wield qus}
#ALIAS yh {yun heal}
#ALIAS yqk {yun qiankun}
#ALIAS 吃饭 {sit chair;knock table;eat shangyueshipin;eat shangyueshipin;drink wan;drink wan;}
#ALIAS 毒蛇 {#6 e;#wa 1000;s;e;e;nd;w}
#ALIAS 毒蛇回 {e;su;w;w;n;nw;#wa 1000;#6 w}
#ALIAS 丐帮 {#4 e;n;e;n;w;n;e;n;w;n}
#ALIAS 丐帮回 {s;s;#4 w;}
#ALIAS 李铁嘴 {#5 n;nw;#wa 1000;#6 n;#wa 1000;#5 e;n;}
#ALIAS 李铁嘴回 {s;#5 w;#wa 1000;#6 s;#wa 1000;se;#5 s;}
#ALIAS 卖艺人 {do 6 e;#wa 1000;se;n;se;n;w;n;#wa 1000;e;e;}
#ALIAS 卖艺人回 {w;w;#wa 1000;s;e;s;nw;s;nw;#wa 1000;do 6 w}
#ALIAS 民女 {do 6 e;#wa 1000;se;n;se;n;w;n;}
#ALIAS 民女回 {s;e;s;nw;s;nw;#wa 1000;do 6 w}
#ALIAS 全真 {#5 n;nw;#wa 1000l#6 n;#wa 1000;#2 nw;w;#2 nw;#wa 1000;n;nw;#2 nu;n;nu;#wa 1000;#2 n}
#ALIAS 全真回 {#2 s;sd;s;#2 sd;#wa 1000;se;s;#2 se;e;#wa 1000;#2 se;#wa 1000;#6 s;se;#wa 1000;#5 s}
#ALIAS 蛇洞 {do 6 e;#wa 1000;se;n;se;n;w;n;#wa 1000;do 5 e;#wa 1000;nu;nu;nu;w}
#ALIAS 蛇洞回 {e;sd;sd;sd;sd;#wa 1000;#5 w;#wa 1000;s;e;s;nw;s;nw;#wa 1000;#6 w}
#ALIAS 泰山 {e;e;e;e;e;e;#wa 1000;ne;n;n;nu;nu;nu;#wa 1000;eu;nu;nu;nu;nu;nu;#wa 1000;nu;nu}
#ALIAS 泰山回 {sd;sd;sd;sd;sd;#wa 1000;sd;sd;wd;sd;sd;#wa 1000;sd;s;s;sw;#wa 1000;#5 w;w}
#ALIAS 天龙 {#4 s;#wa 1000;#5 s;#wa 1000;#5 sw;#wa 1000;wu;nu;n}
#ALIAS 天龙回 {s;sd;ed;#wa 1000;#4 ne;se;#wa 1000;#2 e;ne;#wa 1000;#5 n;#wa 1000;#4 n}
#ALIAS 天山 {enter shudong;say 天堂有路你不走呀;d;4;#3 w;#3 nw;ask alamuhan about 马}
#ALIAS 天山回 {se;e;se;#wa 1000;e;e;su;sd;#wa 1000;#6 e}
#ALIAS 土匪 {#5 s;#wa 1000;#4 s;#wa 1000;sw;w;su}
#ALIAS 土匪回 {nd;e;se;e;e;#wa 1000;ne;#4 n;#wa 1000;#5 n}
#ALIAS 武当 {#5 s;#wa 1000;#4 s;#wa 1000;sw;w;w;nw;#3 w;wu;#wa 1000;#3 nu;w;#2 nu;#wa 1000;#2 eu;#2 nu;n;n}
#ALIAS 武当回 {#3 s;#2 sd;#wa 1000;#2 wd;#2 sd;e;#wa 1000;#2 sd;ed;#3 e;#wa 1000;se;#2 e;ne;#wa 1000;#5 n;#wa 1000;#4 n}
#ALIAS 襄阳 {enter shudong;say 天堂有路你不走呀;d;3;#2 ne;u;#wa 1000;sw;e;sd;e;e;#wa 1000;#5 n;#wa 1000;ask shou jiang about 投军;#4 n}
#ALIAS 襄阳回 {drop yao pai;drop bian tiao;#wa 1000;#5 s;#wa 1000;#4 s;w;#wa 1000;#2 nu;wu;#wa 1000;#2 wd;wu;w;nw;#wa 1000;n;w;#2 sw;w;#wa 1000;#3 s;wu;eu;su;#wa 1000;#5 s;#wa 1000;#6 s;#wa 1400;quanzhenb}
#ALIAS 星宿 {enter shudong;say 天堂有路你不走呀;d;4;w;w;w;#wa 1000;nw;wu;n;}
#ALIAS 星宿回 {s;ed;se;e;se;#wa 1000;e;e;su;sd;e;e;e;#wa 1000;e;e;e}
#ALIAS 英姑 {#5 s;#wa 1000;#4 s;#wa 1000;se;e;sw;sw;s;#wa 1000;e;n;w;s;s;w}
#ALIAS 英姑回 {out;ne;w;nw;#wa 1000;#5 n;#wa 1000;#4 n}
#ALIAS 11 {ne;do 3 s;suzhoub}
#ALIAS 22 {#wa 2000;ask guan about 完成}
#ALIAS 33 {#wa 10000;suzhou;#wa 1000;do 3 n;sw;22}
#ALIAS pingxi1 {set brief 1;do 9 s;#wa 1000;sw;do 2 w;nw;do 3 sw;#wa 1000;do 4 n;set brief 0}
#ALIAS pingxi1b {set brief 1;do 5 s;n;#wa 1000;do 3 ne;#wa 1000;se;do 2 e;ne;#wa 1000;do 9 n;set brief 0}
#ALIAS quanzhen1 {set brief 1;do 5 n;nw;#wa 500;do 6 n;#wa 500;do 2 nw;w;do 2 nw;#wa 500;n;nw;do 2 nu;n;nu;set brief 0}
#ALIAS quanzhen1b {set brief 1;sd;s;do 2 sd;#wa 500;se;s;do 2 se;e;#wa 500;do 2 se;#wa 500;do 6 s;se;#wa 500;do 5 s;set brief 0}
#ALIAS aaab {u;sit chair;knock table;#wa 5000;#5 drink wan;#5 eat shangyueshipin;#wa 5000;d}
#ALIAS aaad {d;out;fadai;#wa 4000;enter;u;climb tree}
#ALIAS aaae {xue yue for hunyuan-zhang 40;yun jing akis;#wa 3000}
#ALIAS aaaa {u;u;sit chair;knock table;#wa 5000;#5 drink wan;#5 eat shangyueshipin;#wa 5000;d;d;#wa 2000;dz 200}
#ALIAS aa {suzhou;#wa 3000;n;nw;w;s;buy yuer 100;#wa 3000;#var er 100;#wa 3000;n;e;se;s;#wa 3000;suzhoub}
#ALIAS aaac {u;u;sit chair;knock table;#wa 5000;#5 drink wan;#5 eat shangyueshipin;#wa 5000;d;d;#wa 2000;du book for 10}
#ALIAS 111 {do 3 eat liang;do 3 drink jiudai}
#ALIAS huashan1 {set brief 1;do 5 n;nw;do 6 n;#wa 1000;do 5 e;#wa 1000;se;su;eu;su;eu;do 2 su;#wa 1000;sd;su;set brief 0}
#ALIAS huashan1b {set brief 1;nd;nu;do 2 nd;#wa 1000;wd;nd;wd;nd;nw;do 3 w;#wa 500;do 2 w;do 6 s;se;#wa 500;do 5 s;set brief 0}
#ALIAS lzb {d;drop cloth;drop shoes;drop xue;drop boots;drop pao;drop ma xie;out;draw sword;draw blade;draw armor;draw head;draw cloth;draw surcoat;draw boots;wear all;wield sword;wield blade;#wa 2500;enter;u}
#ALIAS taohua1 {set brief 1;do 6 e;se;s;do 2 e;#wa 500;nd;do 3 e;set brief 0}
#ALIAS taohua1b {set brief 1;do 3 w;su;do 2 w;n;nw;#wa 500;do 6 w;set brief 0}
#ALIAS emei2 {set brief 1;do 9 s;sw;do 2 w;nw;#wa 1000;do 2 w;nw;w;nw;n;nu;unwield right;unwield left;nu;n;e;eu;do 2 nu;wi;set brief 0}
#ALIAS emei2b {set brief 1;do 2 sd;wd;w;s;sd;#wa 1000;sd;s;se;e;se;do 2 e;se;do 2 e;ne;#wa 1000;do 9 n;set brief 0}
#ALIAS g {get all}
#FUNC q2 {@maxqi*0.9-1}
#FUNC maxneili2 {@maxneili/2+1}
#FUNC maxneili3 {@maxneili/3+1}
#FUNC fool {35}
#FUNC maxfool {400}
#FUNC jingli {90}
#FUNC maxjingli {90}
#FUNC jing {122}
#FUNC maxjing {122}
#FUNC neili {40}
#FUNC maxneili {40}
#FUNC qi {110}
#FUNC maxqi {110}
#FUNC qn {29136}
#FUNC exp {37981}
#FUNC er {60}
#FUNC book {book=}
#FUNC expold {66}
#FUNC ko {500 0}
#FUNC who {}
#PATH cun {5nh7n}
#PATH gu {13nfir}
#PATH gui {6elnlnwn8e}
#PATH hua {5nh6n5elcgcg}
#PATH jia {5eelse}
#PATH mei {9sk2wh2wkwhn2aneg2agn3aoa2n}
#PATH ming {soh2wnwnwnwnwnwnwnw}
#PATH quan {5nh6n2hw2hnh2ana}
#PATH sha {6woao3e}
#PATH sha2 {9s2o3nw}
#PATH shao {13nfir3ne2jesler2g3aeg3an}
#PATH su {6else5nh6ws}
#PATH tai {6ej2n3ag6a}
#PATH tao {6els2efa4en}
#PATH temp {6elnlnwn8e}
#PATH temp1 {ne}
#PATH tian {9sk2wh4koan}
#PATH wu {9sk2wh3wo3aw2a2ga}
#PATH xiang {13nfir3ne2jesler2gr2be5n}
#PATH xin {6waf3whwhon}
#TRIGGER {【%s精力%s】%s(%d)%s/%s(%d)(*)} {jingli=%1;maxjingli=%2;} {all} 519
#TRIGGER {【%s潜能%s】%s(%d)%s(*)} {qn=%1;} {all} 519
#TRIGGER {【%s精神%s】%s(%d)%s/%s(%d)%s(*)} {jing=%1;maxjing=%2} {all} 519
#TRIGGER {【%s内力%s】%s(%d)%s/%s(%d)(*)} {neili=%1;maxneili=%2} {all} 519
#TRIGGER {【%s气血%s】%s(%d)%s/%s(%d)%s(*)} {qi=%1;maxqi=%2;} {all} 519
#TRIGGER {【%s食物%s】%s(%d)%s/%s(%d)%s(*)} {fool=%1;maxfool=%2} {all} 519
#TRIGGER {%死了。} {get all from corpse} {all} 519
#TRIGGER {村姑说道：「从这一直往西有座雪峰} {s;s;w;w;w;u;u;zuan dong;#wa 1000;get all;out;d;d;e;e;e;e;e;e;e;e;e} {all} 519
#TRIGGER {虎骨} {get all;} {all} 519
#TRIGGER {老虎死了。} {get gu;} {all} 519
#TRIGGER {灵芝} {get all;} {all} 519
#TRIGGER {万年玄冰} {get bing;} {all} 519
#TRIGGER {麋鹿脚下一个不稳，跌在地上一动也不动了。} {get all from lu;} {all} 519
#TRIGGER {^你从*一柄长剑。} {drop changjian} {all} 519
#TRIGGER {^你从*一柄钢刀。} {drop blade} {all} 519
#TRIGGER {^你从*一件布衣。} {drop cloth} {all} 519
#TRIGGER {^你从*一件黄衣。} {drop huang} {all} 519
#TRIGGER {^你从*一件铁甲。} {drop armor} {all} 519
#TRIGGER {看起来(*)想杀死你！} {wield sword 1;wield sword 2} {all} 519
#TRIGGER {^你从*一把方天画戟。} {drop ji} {all} 519
#TRIGGER {你必须先把木门打开！} {open door} {all} 519
#TRIGGER {搜出一把戒刀。} {drop jie dao} {all} 519
#TRIGGER {搜出一件青布僧衣。} {drop cloth} {all} 519
#TRIGGER {刚刚才有人来这儿唱过戏了，人们都不想再看戏} {#wa 4000;backsz} {wujian} 548
#TRIGGER {管事对你说道：你去白驼山} {111;#wa 4000;shibai;#wa 4000} {wujian} 548
#TRIGGER {管事对你说道：你去峨眉} {#wa 3000;11;#wa 9000;say 去峨嵋} {wujian} 548
#TRIGGER {管事对你说道：你去归云庄} {#wa 3000;11;;#wa 9000;say 去归云庄} {wujian} 548
#TRIGGER {管事对你说道：你去华山表演} {#wa 3000;11;#wa 9000;say 去华山表演} {wujian} 548
#TRIGGER {管事对你说道：你去华山村} {#wa 3000;11;#wa 9000;say 去华山村} {wujian} 548
#TRIGGER {管事对你说道：你去灵州} {111;#wa 4000;shibai;#wa 4000} {wujian} 548
#TRIGGER {管事对你说道：你去苏州表演一下吧} {#wa 3000;ne;s;s;s;ne;fj;#wa 6000;sw;do 3 n;sw;#wa 3000;bysz;ne;do 4 s;ff} {wujian} 548
#TRIGGER {管事对你说道：你去泉州} {#wa 3000;11;#wa 9000;say 去泉州} {wujian} 548
#TRIGGER {管事对你说道：你去桃花岛} {#wa 3000;11;#wa 9000;say 去桃花} {wujian} 548
#TRIGGER {管事对你说道：你去杀手帮} {#wa 3000;11;#wa 9000;say 去杀手帮} {wujian} 548
#TRIGGER {管事对你说道：你去武当山} {#wa 3000;11;#wa 9000;say 去武当山} {wujian} 548
#TRIGGER {管事对你说道：你去襄阳} {111;#wa 4000;shibai;#wa 4000} {wujian} 548
#TRIGGER {管事对你说道：你去全真派} {#wa 3000;11;#wa 9000;say 去全真派} {wujian} 548
#TRIGGER {管事对你说道：你去扬州} {#wa 3000;11;#wa 9000;say 去扬州} {wujian} 548
#TRIGGER {管事对你说道：你去平西王府} {#wa 3000;11;#wa 9000;say 去平西王府} {wujian} 548
#TRIGGER {你拿出十两白银} {#wa 5000;ss} {wujian} 548
#TRIGGER {你说道：「去峨嵋} {byemei;#wa 1000;emei2;#wa 5000;ff} {wujian} 548
#TRIGGER {你说道：「去灵州} {bylingzhou;#wa 1000;do 6 w;nu;nd;w;w;nw;w;nw;#wa 1000;nw;nu;n;do 5 w;ff} {wujian} 548
#TRIGGER {你说道：「去归云庄} {byguiyun;#wa 3000;taihu;#wa 5000;ff} {wujian} 548
#TRIGGER {你说道：「去大理} {bydali;#wa 1000;dali;#wa 5000;ff} {wujian} 548
#TRIGGER {你说道：「表演回苏州} {33} {wujian} 548
#TRIGGER {你没有那么多的白银} {halt;11;#wa 4000;n;w;qu 200 silver;#wa 5000;e;s;#wa 5000;say 表演回苏州} {wujian} 548
#TRIGGER {你说道：「去华山村} {byxiaocun;#wa 1000;do 5 n;nw;do 6 n;#wa 5000;ff} {wujian} 548
#TRIGGER {开始表演的时候，人群里突然冲出个小流氓} {kill rascal} {wujian} 548
#TRIGGER {你身上没有 silver 这样东西} {halt;11;#wa 4000;n;w;qu 200 silver;#wa 5000;e;s;#wa 5000;say 表演回苏州} {wujian} 548
#TRIGGER {你说道：「去平西王府} {bypingxi;#wa 1000;pingxi1;#wa 5000;ff} {wujian} 548
#TRIGGER {管事对你说道：做得不错！给你些奖励吧。} {backup;#wa 6000;ss} {wujian} 548
#TRIGGER {小流氓死了} {ff} {wujian} 548
#TRIGGER {你说道：「去泉州} {byquanzhou;#wa 1000;quanzhou;#wa 5000;ff} {wujian} 548
#TRIGGER {你说道：「去扬州} {byyz;#wa 1000;s;s;#wa 5000;ff} {wujian} 548
#TRIGGER {你说道：「去杀手帮} {bykill;#wa 1000;do 6 w;wu;nu;#wa 5000;ff} {wujian} 548
#TRIGGER {你说道：「去武当山} {bywudang;#wa 1000;wudang;#wa 5000;ff} {wujian} 548
#TRIGGER {你说道：「去华山表演} {byhuashan;#wa 1000;huashan1;#wa 5000;ff} {wujian} 548
#TRIGGER {你说道：「去桃花} {bytaohua;#wa 1000;taohua1;#wa 5000;ff} {wujian} 548
#TRIGGER {你说道：「去全真派} {byquanzhen;#wa 1000;quanzhen1;#wa 5000;ff} {wujian} 548
#TRIGGER {这里没有这个人。} {quit} {wujian} 548
#TRIGGER {快去表演吧} {shibai;#wa 4000} {wujian} 548
#TRIGGER {管事对你说道：你去大理} {halt;#wa 3000;11;#wa 9000;say 去大理} {wujian} 548
#TRIGGER {【%s经验%s】%s(%d)*} {exp = %1;#if (%1>100000) {quit}} {all} 519
#TRIGGER {客店 - } {hp;save;#wa 1000;w;n;e;#wa 2000;buy liang 50;#wa 3000;buy jiudai;#wa 2000;w;do 2 s;lzb;wa;wi;#wa 2000;#t+ wujian;suzhou;do 3 n;sw;ss} {wujian} 519
#TRIGGER {武庙 - } {quit} {wujian} 548
#TRIGGER {你的精力不济，需要调整一下才能表演} {tuna 45} {all} 519
#TRIGGER {你吐纳完毕} {biaoyan wujian} {all} 519
#TRIGGER {您的英文名字} {zgwm;svgsfv} {autolog} 963
#TRIGGER {你只见好大的块砖头应声而碎，旁人看得张大口说不出话来} {hp;#wa 5000;backsz} {wujian} 548
```

发个唱戏舞剑机器人

---

送信

全自动机器人，删除

Mush版送信机器人

出品人：Sure

使用方法：修改变量player、passwd

送信mush版

配药

---

抄经

Mush版抄经+工号查询机器人

出品人：Ddid

强大至极，在Mush中利用Lua脚本，自动查询抄经工号，并且显示在小窗口内

机器人运行：

Login PKUXKX，找朱熹去ask zhu xi about job机器人开始运行，MUSH右上角会显示“工号”图片。

ask zhu xi about job之后1分钟内，ask zhu xi about 口令 可以刷新图片，如果第一次显示的图片看不清楚，可以通过这个方法刷新出一个新的图片。

close_mini_window 命令可以将图片窗口关闭。

全新升级！～ 新手抄经——工号查询机器人（MUSH)

---

公共任务

===== 朱熹question =====   朱熹任务已经无法获得潜能，此类机器人只能做研究用了

Mush版朱熹question机器人

出品人：Sure

效率：10w+ pot/day

- ——–朱熹任务已经无法获得潜能，此类机器人只能做研究用了

，现发布mush版朱熹question机器人

使用说明

Mush版朱熹Question+读书、学习、练习机器人

出品人：Sure

变量设定：

-  player=玩家id（必须设置）

-  passwd=密码（必须设置）

-  zhu=1（必须设置，固定值1）

下面的可以是空值

-  getcmd=从家中柜子里取东西的命令，例如天龙是第8号物品，getcmd=getout 8

-  putcmd=保存东西的命令，如 pcmd=store tianlong

-  scmd=读书、practice、向师父学习的命令，如scmd=do 9 read tianlong3、xue master for skill 50等

-  yuncmd=恢复指令，practice时用yuncmd=yun recover，学习、读书时用yuncmd=yun regenerate

没有dazuo的，要的自己加吧，迟点把机器人都改成插件发布。

朱熹＋读书、练习、tuna机器人

---

Zmud7.21版朱熹Question机器人

出品人：Zmeng

1、根据sure的mush机器人思路改写而成。对sure表示崇高的敬意。

2、适合对mush不熟悉的新人使用，老鸟估计也看不见这点潜能了。

3、在zmud721版测试通过，不清楚462如何，有兴趣的同学可以导入看看。（测试结果，462无法导入，并且因为462不支持list型变量，在非自虐的工作量下无法转为462版）

4、限于程序本身问题，zmud的运算速度完全比不上JS.不过，朱老太爷45秒才给一个任务，在此时间内计算出来还是没有问题的。

5、我没有做过朱熹的任务，对朱熹任务还有什么变数，比如“让你出去”等等的触发没有加上，请使用的同学注意。如果还有什么不足，希望大家指出来，利于改进。

发个zmud版的朱熹question机器人

---

Zmud4.62版朱熹Question机器人

出品人：Zmeng提供7.21原版，Minix移植至4.62

把zmeng的朱熹机器人移植到了4.62上

---

Cmud版朱熹Question机器人

出品人：Alchemy

优势：使用lua语言编写而成，执行效率远远高于用Zscript编写的Zmud版，同样运算，Zscript需要4s，此机器人仅需0.016s

发一个cmud的朱熹

---

北京茶馆对诗

Mush版北京茶馆对诗机器人

出品人：Sure

要求：

-  懂mush

-  在天桥s处save

北京茶馆对诗trigger

---

华山送信

---

慕容信件

TASK

Zmud4.62+Mushclient版task机器人

出品人：Religiose

完整版task机器人(zmud4.62)

---

灵鹫护卫

全自动机器人违反北侠条例，删除！

护镖任务

Zmud4.62版半自动护镖机器人 of zgbl

出品人：Zgbl

变量修改：

-  yourid：你的id

-  yourpassword：你的密码

-  yourname：你的中文名字

-  weapon_right：右手兵器

-  weapon_left：左手兵器

-  yourpfm：你见到robber的第一个pfm，比如sword.chan

---

每秒自动pfm时，设定为自动放yourfirstpfm，频率为一秒五次，建议设置成busy类pfm
如果想增加pfm，就修改 ** hubiao_ex ** 类别的

```
林震南说道：「@yourname把这批红货送到(%x)那里，他已经派了个伙计名叫(%x)附近接你，把镖车送到他那里
```

这个触发

```
#alarm -* {}
```

里面的就是每秒执行一次的指令，可以在里面加别的pfm
(**仅对2010-08-24的最新版本有效，所以推荐更新**)

---

ct输入hubiao或者点按钮就开始了

按钮作用

-  进一步：镖车被劫匪推进了一步

-  退一步：镖车被劫匪推退了一步

-  继续走：镖车被劫匪推出路线，自己推回来再点

如果到地点还没遇到伙计，就要手动找了，战斗和路上基本是自动的，送完手动回来输入hubiao继续

-  hubiao：修兵器，疗伤，把杂物丢家里，然后去领任务

-  ww：装备兵器

-  wb：卸兵器

-  身上必须有一匹马horse

-  新加入杭州路径

-  gc=继续走，方便键盘党

声音文件请至http://pkuxkx.net/forum/viewthread.php?tid=13771&page=6&fromuid=4420#pid155369下载，然后保存至zmud.exe所在文件夹

下载地址：wiki护镖机器人

---

Zmud4.62版半自动护镖机器人 of lkyun

出品人：Zgbl，lkyun改良

变量里的yourname填你的中文名字，yourid填你的英文id，pfm填你用来busy劫匪的pfm

别名里的ww是装备武器，请根据门派不同进行修改，atconnect是自动连线，请自己修改id和密码

触发里的自己busy成功和不成功的语句请自行修改，我是用的武当的

```
推车cooltime我是吐纳，大家可以自行修改
中毒后我一般不吃药的，全用疗伤，大家觉得不安全可以改掉
身上带了匹马，主要放左右手装备的武器类型和盾牌，具体武器自己改
```

计时器我设置的1s发一次pfm，某些门派要换武器才能出pfm最好自己修改

如果到地点还没遇到伙计，就要手动找了，战斗和路上基本是自动的，送完手动回来继续

发个诸葛不亮推车机器人的改良版

护镖声音提示的有关设置和相应附件：http://pkuxkx.net/forum/viewthread.php?tid=13771&page=6&fromuid=4420#pid155369

---

Zmud4.62手动护镖辅助机器人

出品人：Angelei

功能：图形化界面，按钮操纵镖车行走、人物战斗等行为，简化推车操作，提高推车效率

说明：整个机器人采用按钮集成推车方向，适合那种懒得打字又怕自动推车死人的

-  第一个kill，其他均hit，采用#2 hit robber %i

-  门派是武当，pf为perform sword。chan的别名，timer依然使用，目的是告诉自己目的地。

-  每一个方向键上面都有个pf，我是懒人嘛，懒得去另外摁按钮，方向键上久直接写好了perform。遇到劫匪拼命按方向缠。

-  不捡垃圾免得负重太大。

-  如果需要look，点中间的u，d，集成了look命令。

发一个手动推车的，在诸葛不亮基础上调整的

Zmud4.62版全套机器人

出品人：诸葛不亮（Zgbl）

内容：打坐、吐纳、学习、练习、跳楼、胡一刀、萧峰、护镖、万安塔、慕容

```
推车无聊，加了几个偷懒的按钮。。。
发现效果不错，干脆发上来分享算了
```

** 强烈建议使用推车时，在zmud的“常规”设置里关闭“回应指令行” **

```
胡一刀那里直接look就开始hyd任务
开始慕容后，慕容复那里look就开始慕容
万安塔门口look自动触发ask，进入每一层后输入wat，会自动侦测武士，若有明教则mess提示

hyd、hydb是hyd的往返path
mr是从慕容复走到ct，方便走路
kdb是杀盗宝人
db是pp盗宝人
cc是缠
ll是连
ww是装备兵器
wb是unwield all
boat是yell boat并且推车上船
shout和roar是两个很华丽的闲聊cemote效果
cure是在平一指处解毒并且找西门吹牛治疗的指令，感谢西门吹牛

貌似没什么特殊的alias了吧。。。
```

```
最轻松的还是推车，每秒自动提示目的地，并且每0.1秒发一个缠，只要用鼠标点点走路就ok了
装备和宝石自动放horse里面。ct输入hubiao，自动找平一指和西门吹牛（感谢西门吹牛），自动修兵器，自动在家里放下玉竹杖之类的杂物，然后自动去领任务
北京永安门外look可以自动unwield all然后ask，推车进去之后别忘了ww
永安门内look会自动ask出城

开始护镖按钮一定要在ct点
hubiao指令只能在ct输入
确认你有房子和horse，horse拿在身上

请set skip_combat 2
在Zmud的“常规”设置里面，关闭“回应指令行”
```

按钮位置按照1280*800分辨率设置，如有错位，修改屏幕分辨率即可

原帖地址：zgbl全套机器人

---

萧峰任务

---

胡一刀任务

胡一刀机器人

出品人：Thu

需修改busy和干掉盗宝人的pfm

1.见到盗宝人后，自动出招busy,如果不能成功busy,自己手动cc出busy,成功busy后，用kd切换剑法直到盗宝人挂掉,然后自动拣图，收集齐以后，自动合并。

2.完成任务后在hyd处修炼内功等下一个任务，没有搜魂特技的请自行添加bot找vast定位盗宝人位置。

```
#ALIAS hyd {#t+ hyd;enter shudong;say 天堂有路你不走呀;d;7;#2 n;#2 ne;n;out;#wa 1000;give hu

cangbao tu;ask hu about job}
#ALIAS ahj ask hu about job
----------------------------找胡问任务
#ALIAS hydb {enter shudong;s;#2 sw;#2 s;u;out}
----------------------------胡一刀回ct

#ALIAS cc {jifa sword taiji-jian;perform sword.chan @daobao;perform sword.chan;jifa sword liumai

-shenjian;}
－－－－－－－－－－－－－busy盗宝人
#ALIAS kd {hit @daobao;jifa sword liumai-shenjian;perform sword.qifa2 @daobao}
------------------------------------busy后干掉盗宝人
#FUNC daobao {dusong}
------------------------------------盗宝人的英文名字
#FUNC tasknpc {dusong}
-----------------------------------盗宝人的中文名字

#TRIGGER {你从玄幻之境回过神来，顿觉内功修为增进不小。} {ask hu about job} {hyd} 548
#TRIGGER {你掐指一算，感觉*现在好象在(*)一带活动。} {weizhi=%1} {hyd} 548
#TRIGGER {胡一刀说道：“我收到消息，听说(*)有盗宝人(*)~((*)~)找到了闯王宝藏的地图,你可否帮忙找回

来！”} {where=%1;tasknpc=%2;daobao=%3;cdb;#mess 开始hyd;#wa 3000;yp;hydb} {hyd} 548
#TRIGGER {*叹道：“人算不如天算，想不到我兄弟五人都栽在你的手中！”} {#wa 3000;get all from

corpse;combine;drop bishou;drop bian} {hyd} 548
#TRIGGER {看见你，阴笑一声：天堂有路你不走，地狱无门你来投！} {hit @daobao;jifa sword taiji-

jian;perform sword.chan @daobao} {hyd} 548
#TRIGGER {盗%s宝%s人%s「????龙」@tasknpc~(@daobao~)} {#stop;follow @daobao;hit @daobao;jifa sword

taiji-jian;perform sword.chan @daobao;jifa sword liumai-shenjian;jiali 100;set brief 3} {hyd} 548
-----------------------------这是核心的一句，在此感谢xhao玩友的帮助.
#TRIGGER {你有种去(*)找我兄弟(*)~((*)~)*} {#wa 2000;get all from corpse;where=%1;tasknpc=%

2;daobao=%3;perceive @daobao;drop bishou;drop bian;jiali 0} {hyd} 548
#TRIGGER {@tasknpc向后一纵，} {#wa 3000;kd} {hyd} 548
#TRIGGER {你的*运行完毕，将内力收回丹田。} {yun powerup} {yun powerup} 519
#TRIGGER {胡一刀说道：你刚刚不是要过任务么，你先下去休息吧!} {#wa 1000;eat niurou;drink

jiudai;xiulian taiji-shengong} {hyd} 548
```

庆祝胡家刀完成，发个hjd的bot

---

护卫任务

---

保卫襄阳

保卫襄阳自动释仇机器人

wiki链接：保卫襄阳释仇机器人

原帖地址：鉴于现在很多保卫的玩家都不加自动释仇的trigger

门派任务

门忠任务

---

门派quest

---

白托放蛇

---

星宿炼毒

炼毒指南(newgrin出品)

---

灵鹫扫雪

Zmud4.62版灵鹫扫雪机器人

出品人：Moxie

扫雪到门忠1000很快，石嫂那里输入ask shi about  扫雪

灵鹫扫雪机器人trigger

---

灵鹫扫雪机器人

出品人：Msquare

使用方法：问石嫂要任务可触发

附有zmud入门教程

```
#CLASS {Status} {enable}
#VAR exp {0}
#VAR jingli {0}
#VAR jingshen {0}
#VAR neili {0}
#VAR pot {0}
#VAR qixue {0}
#VAR jingli_max {0}
#VAR jingshen_max {0}
#VAR neili_max {0}
#VAR qixue_max {0}
#VAR qixue_health {0}
#VAR jingshen_health {0}

#TRIGGER {【%s潜能%s】%s(%d)} {#var pot %1}
#TRIGGER {【%s经验%s】%s(%d)} {#var exp %1}
#TRIGGER {【%s精神%s】%s(%d)%s/%s(%d)%s~[(*)~%~]%s【%s精力%s】%s(%d)%s/%s(%d)} {
#var jingshen %1
#var jingshen_max %2
#var jingshen_health %3
#var jingli %4
#var jingli_max %5
}
#TRIGGER {【%s气血%s】%s(%d)%s/%s(%d)%s~[(*)~%~]%s【%s内力%s】%s(%d)%s/%s(%d)} {
#var qixue %1
#var qixue_max %2
#var qixue_health %3
#var neili %4
#var neili_max %5
}
#CLASS 0
```

机器人知识基础讲解]

朝廷系列

Mush版朝廷守门机器人

出品人：Sure

朝廷守门trigger mush版

Mush版朝廷监斩机器人

出品人：Sure

朝廷监斩mush trigger

Zmud4.62朝廷系列机器人

出品人：Winding

我用的朝廷系列机器人

Zmud7.21朝廷通用机器人

出品人：Zhh

朝廷通用机器人

> 来源: https://www.pkuxkx.net/wiki/robot/task
