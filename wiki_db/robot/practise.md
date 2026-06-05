- 领悟

- 462傻瓜式领悟机器人

- Zmud7.21版领悟机器人（武当推荐）

- Zmud领悟机器人

- Mush领悟机器人

- Mush领悟机器人改进版

- Mush领悟机器人改进版之再改进

- Mush冥想机器人

- Cmud领悟机器人

- 跳楼

- Mush版跳楼机器人

- Zmud4.62版跳楼机器人

- 练习

- Zmud7.21版自动练功机器人

- Zmud7.21全自动领悟机器人

- 左右互博

- Zmud462左右互博机器人

- 星宿天龙吸内力

- Zmud4.62版全套机器人

---

领悟

462傻瓜式领悟机器人

```
#ALIAS shaolinb {sd;#4 s;sd;#3 s;sd;s;open gate;#wa 1000;#2 s;#3 sd;wd;w;#wa 500;#3 sd;ed;sd;sd;e;#wa 1000;ruzhoub}
#ALIAS shaolin {unwield right;unwield left;enter shudong;say 天堂有路你不走呀;d;3;#2 ne;u;sw;#wa 1000;e;sd;e;#2 nu;wu;#3 nu;e;eu;#3 nu;n;#wa 1000;knock gate;#2 n;nu;#3 n;nu;n;n;n;nu;u;ww;}
#ALIAS lw {lingwu @skills 100}
#ALIAS fan {drink jiudai;eat ganliang;}
#ALIAS yg {exert regenerate}
#ALIAS lanyao {hp}
#ALIAS lianxi {exert recover;lian @skills 50}
#FUNC jingli {2186}
#FUNC maxjingli {3111}
#FUNC jing {1696}
#FUNC maxjing {1696}
#FUNC neili {1862}
#FUNC maxneili {3490}
#FUNC qi {3050}
#FUNC maxqi {3050}
#FUNC qn {54662}
#FUNC exp {3002218}
#FUNC effjing {}
#FUNC skills {sword}
#FUNC skilldj {244}
#FUNC skills2 {sword}
#FUNC skills3 {sword}
#FUNC skills1 {sword}
#FUNC skilldj1 {244}
#FUNC skilldj3 {244}
#FUNC skilldj2 {244}
#TRIGGER {等级：%s%x%s(%d)/%s(%d)} {skilldj=%1} {} 519
#TRIGGER {^达摩院} {#t- lingwu3;#wa 1000;d;sd;w;n;sleep} {lingwu3} 518
#TRIGGER {^和尚院四部} {#t- lingwu3;#wa 1000;n;sleep} {lingwu3} 518
#TRIGGER {^练武场} {#t- lingwu3;#wa 1000;w;n;sleep} {lingwu3} 518
#TRIGGER {^??你现在过于疲倦} {#wa 5000;yg} {lingwu} 518
#TRIGGER {^??你现在精力充沛} {lw} {lingwu} 518
#TRIGGER {^??你略一凝神} {#wa 100;lw} {lingwu} 518
#TRIGGER {^??你领悟了*次基本} {yg} {lingwu} 518
#TRIGGER {^??哎哟，你一头撞在墙上} {#t- lingwu2;#t+ lingwu3;l} {lingwu2} 519
#TRIGGER {^??你刚在三分钟内睡过一觉} {#t+ lian;#wa 3000;s;e;nu;u;lianxi;#t+ lianxi;#time on} {lian2} 518
#TRIGGER {^??你一觉醒来} {skills;#t+ lianxi;#t+ lian;#time on;lanyao;#t+ lingwu2;#wa 1000;fan;#wa 3000;s;e;nu;u;#wa 1000;unwield all;lianxi} {lian2} 518
#TRIGGER {^??你需要提高基本功} {skills;unwield all;#t- lianxi;#wa 1000;#t+ lianxi2;skills=@skills2;lianxi} {lianxi} 518
#TRIGGER {^??你需要提高基本功} {skills;unwield all;#t- lianxi2;#wa 1000;#t+ lianxi3;skills=@skills3;lianxi} {lianxi2} 518
#TRIGGER {^??你需要提高基本功} {skills;unwield all;#t- lianxi3;#t- lian;#t- lian2;#wa 1000;#t+ lingwu;#t+ lingw;#t+ huan1;skills=@skills1;lw} {lianxi3} 518
#TRIGGER {^??你要装备%s(*)%s类武器} {unwield all;wield %1;lianxi} {} 519
#TRIGGER {你的基本功夫比你的高级功夫还高！} {skills;#t- huan2;skills=@skills3;#wa 1000;#t+ huan3;lw} {huan2} 518
#TRIGGER {你的基本功夫比你的高级功夫还高！} {skills;#timer off;#t- huan3;#t- lingwu;#t- lingw;skills=@skills1;#wa 1000;#t+ lian;#t+ lian2;#t+ lianxi;#t- lianxi2;#t- lianxi3;unwield all;lianxi} {huan3} 518
#TRIGGER {你的基本功夫比你的高级功夫还高！} {skills;#t- huan1;skills=@skills2;#wa 1000;#t+ huan2;lw} {huan1} 519
#TRIGGER {你使用的武器不对。} {#wa 500;changewield;#wa 1000;lianxi} {lian} 518
#TRIGGER {^??你的太极拳火候太浅} {skills;unwield all;#t- lianxi3;#t- lian;#t- lian2;#wa 1000;#t+ lingwu;#t+ lingw;#t+ huan1;skills=@skills1;lw} {lianxi3} 518
#TRIGGER {^??你*练习} {lianxi} {lian} 518
#TRIGGER {^??【%s气血%s】%s(%d)%s/%s(%d)*~%*【%s内力%s】%s(%d)%s/%s(%d)} {qi=%1;maxqi=%2;maxneili=%4} {hp} 519
#TRIGGER {^??【%s精神%s】%s(%d)%s/%s(%d)*~%*【%s精力%s】%s(%d)%s/%s(%d)} {jing=%1;maxjing=%2;maxjingli=%4} {hp} 519
#TRIGGER {^??【%s食物%s】*【%s潜能%s】%s(%d)%s(*)} {qn=%1} {hp} 519
#TRIGGER {^??【%s饮水%s】*【%s经验%s】%s(%d)*} {exp = %1} {hp} 519
#TRIGGER {基本*%s~((*)~)*-%s*%s(%d)/} {#if (%1=@skills1) {skilldj1=%2};#if (%1=@skills2) {skilldj2=%2};#if (%1=@skills3) {skilldj3=%2}} {} 519
#TRIGGER {^??你使用的武器不对} {unwield all;wield sword;wield blade} {} 519
#TRIGGER {^??你的内力不够} {#t- lianxi;#t- lianxi2;#t- lianxi3;#t- lian;#time off;#wa 1000;d;sd;w;n;sleep} {lian} 518
#TRIGGER {^??你的内力不够。} {#t- lingwu;#time off;#wa 1000;d;sd;w;n;sleep} {lingwu} 518
#TRIGGER {^??你的精力不够} {#t- lianxi;#t- lianxi2;#t- lianxi3;#t- lian;#time off;#wa 1000;d;sd;w;n;sleep} {lian} 518
#TRIGGER {^??你的精力不够} {#t- lingwu;#time off;#wa 1000;d;sd;w;n;sleep} {lingwu} 518
#TRIGGER {【} {#cap chat} {} 519
#TRIGGER {^??你的基本招架的级别还没有太极拳的级别高} {skills;unwield all;#t- lianxi3;#t- lian;#t- lian2;#wa 1000;#t+ lingwu;#t+ lingw;#t+ huan1;skills=@skills1;lw} {lianxi3} 518
#TRIGGER {^??你一觉醒来} {skills;#ts 100;#time on;lanyao;#t+ lingwu2;#wa 1000;fan;#wa 3000;s;e;nu;u;#wa 1000;lw;#t+ lingwu;#t+ huan} {lingw} 519
#TRIGGER {^??你刚在三分钟内睡过一觉} {#ts 100;#time on;#wa 3000;s;e;nu;u;lw;#t+ lingwu;#t+ huan;#time on} {lingw} 519
#BUTTON 1 {领悟技能点俺} {tune channel all;set brief 1;#show ;#show ;#show ;#show 第一个空填第一个领悟的技能,如parry;#show 第二个空填第二个领悟的技能,如staff;#show 第三个空填第三个领悟的技能,如force;#show 第一个空填写的技能领悟完了以后,自动转到第二个,依次类推，更多的也可以搞,自己想办法改改,我懒得弄....;#show ;#show   　　　　　　　　　　　　　　　　　　　　　　　　令狐大葱出品，诸葛不亮修整;#show ;#show ;#show ;#t+ huan1;#t- huan2;#t- huan3;#t- lian;#t- lian2;#t- lianxi;#t- lianxi2;#t- lianxi3;#prompt skills1;#prompt skills2;#prompt skills3;#t+ lingwu;#t- lingwu3;skills=@skills1;lw} {} {} {} {} {} {Size} {100} {23} {Pos} {1} {300} {121} {52} {} {}
```

状态栏指令：

```
@skills1 等级 ：@skilldj1  |  @skills2 等级 ：@skilldj2  |  @skills3 等级 ：@skilldj3
```

使用方式：买好酒袋干粮，达摩院二楼点击按钮，按照提示操作

令狐大葱（lhdc）出品，诸葛不亮（zgbl）修整

令狐大葱原版

诸葛不亮修整版

---

Zmud7.21版领悟机器人（武当推荐）

出品人：Danfeng

由于武当太极系列技能的特殊要求，市面上的领悟机器人直接放进去都不能完美的运行，故danfeng同学专门写了武当专用领悟机器人

说明：

1。本人是武当的号，会的功夫为纯武当的，公共功夫仅会一门英雄剑法，太极爪不练，基本爪法不领悟。

2 。机器人没有做掉线自动连线。

3。 对于非武当的号要在按钮中修改以下4个变量

```
#var lingwu_skill_list {blade|sword|cuff|force|parry}
#var lingwu_skill_list2 {taiji-dao|taiji-jian|taiji-quan|taiji-shengong|taiji-quan}

#var lian_skill_list {hero-jianfa|tiyunzong|taiji-dao|taiji-jian|taiji-quan}
#var lian_skill_list2 {parry|dodge|parry|parry|parry}
```

前两个是一对修炼的技能，后两个是练习的技能。

4。 身上要背 干粮和酒袋，要装备 sword和blade

5. 在达摩院二楼 按下领悟按钮输入你的exp所支持技能上限后开始工作。

6。版本是zmud7.21的

发布一版武当的领悟机器人

---

Zmud领悟机器人

出品人：Seagate

具体用法参见1.0版：http://pkuxkx.net/forum/thread-10010-1-1.html

1.15版：http://pkuxkx.net/forum/thread-10064-1-4.html

特别注明：我这个版本在full_sk3类执行完后自动切换到修禅类，如果有其他发呆形式请自行修改

1.5版修改明细：

-  提高机器人的稳定性

-  提高单位时间的领悟效率

-  提高跳楼效率

-  增加训练记录文件（pkuxkx/技能训练记录.txt）

-  变量增加_sp_sk，存放特殊技能练习的时候精气内力全耗的技能，练习的时候不作领悟消耗精神。

-  【目前仅有大韦陀杵和凌波微步，其他技能自己增加】

-  其他小Bug和小修改。

-  武器列表这个变量如果设置为SPEC1则表示对应的特殊技能是不可练习技能，不会做练习，仅作领悟基本技能用。比如金刚不坏神功、乾坤大挪移之类技能。

1.6版修改明细：

-  提高练习技能的效率，增加变量_pr_cost_flag这个变量存放特殊技能的练习技能消耗情况，100表示仅消耗气，101表示消耗气血+内力，111表示消耗气血+精神+内力，会根据标志决定练习的时候如何作恢复。可以查看lianxi这个alias看看特殊处理情况，默认写死消耗内力技能在气血/内力比⇐5的时候恢复气血，消耗精神技能在气血/精神比>2的时候恢复精神

-  修改同一种兵器有两种以上技能需要练习的时候技能切换的Bug

-  优化重连买兵器的触发（如果有兵器就不会重复买了）

-  提供alias-enable_init存放恢复原始enable技能的命令，自己修改成战斗默认enable方式，会在所有练习完毕后恢复到原始技能

下载地址：技能训练自动机器人1.6版

---

Mush领悟机器人

出品人：Maper

自动连线，买10个干粮，10个酒袋，一把钢刀，一把长剑，一把钢杖，然后去少林达摩院领悟；可以平衡提升预定的各项技能。

设置方法：

-  lua语言，设置脚本位置；

-  设置相关变量：

-  id：游戏英文id，

-  passwd：游戏密码

-  skills_basic：要领悟的基本技能，之间用“;”隔开，例如force;sword;dodge;claw

-  skills_special：与基本技能对应的特殊技能，用“;”隔开，例如：taiji-shengong;taiji-jian;tiyunzong;taiji-zhao

-  skills_weapon：特殊技能使用的武器，用“;”隔开，如果空手或内功则为none，刀法为blade，杖法为gangzhang，剑法为jian，例如：none;jian;gangzhang;blade

-  设置完成后把定时器打开，就可以自动去领悟了。

-  登陆房间是扬州客店！！！！！！

-  优先领悟基本内功force，然后领悟预设基本技能中等级最低的，逐一平衡提升。

-  内力不够了就睡觉，没有打坐。

-  没有考虑特技和玉女心法！！！有需要自己加吧！

**` 不管是maper的还是小刀的还是zgbl的，走路都必须set brief 1或者2或者3，不可unset brief或者set brief 0！ `**

————-第一次更新—————-

增加了一个技能列表小窗口，可以显示预设技能的目前等级。

[MUSH]领悟机器人

---

Mush领悟机器人改进版

出品人：小刀（Lzkd）

经过一段时间的测试，应该是完美了，不会再有什么问题了，欢迎下载使用。另，追求极限效率的，还是不要用这个，去下seagate的Cmud版本吧。

这个就是根据maper的领悟机器人改写的，大概修正了20%左右的代码（可能更少），核心思想和算法都有所改变，还增加了少量的注释，希望能够对大家有帮助。

-  首先，要感谢maper，没有他的那个机器人，就没有这个，这个先说。

-  其次，要感谢八科，他借了个小号给我测试领悟，小刀惭愧，连测试的小号都拿不出来。

-  第三，作为小刀在北侠发的第一个机器人，欢迎大家过来捧场。

功能增加的地方

-  可以设置领悟到多少级了，在lingwu.lua文件中第一行设置，如果该值小于根据经验可领悟到的最高等级，领悟的时候按该值，如果该值设置的时候超过了，则自动领悟到经验允许的最高等级。

-  可以让基本功夫对应的特殊功夫的等级相同的，maper的版本总是少一级，这个改了。

-  设置领悟的顺序有效了，也就是说－－－大家应该先设内功（基本内功高了对领悟有帮助），然后武当先设太极拳（别的功夫等级受太极拳影响），再设别的功夫。

-  领悟完了以后，自动修改mush中预设的密码，自动断线，不会再不停的连进来了。

-  理论上，可以把所有设置的项目都练到满再quit。

-  基本内功是直接领悟到比特殊内功高一级，无需设置基本内功要领悟到的级数。

好象就这么多了吧？

更新记录

-  2010-2-22　修改领悟到等级的默认值为2000

-  2010-2-22　发现一个很奇怪的bug,很难得出现,但出现就很要命,改掉了,欢迎重新下载,应该比较完美了

-  2010-2-21　根据八科提醒,应该可以彻底解决领悟完基本内功后在达摩院二楼直接退出问题,代码修改已完成,请重新下载.

-  ps：tistrya你在maper领悟机器人的帖里的问题我看了，那个茶室在哪里？可以直接加进lua文件中的。你说一下，我加进去就是。睡觉起来，有点卡的时候，浪费１０秒，这个我好象没碰到这问题，暂时无法解决。

-  ps2：沙发，板凳，地板啥的，我都留给各位了。

**` 不管是maper的还是小刀的还是zgbl的，走路都必须set brief 1或者2或者3，不可unset brief或者set brief 0！ `**

-  使用说明，没用过的先去看maper的帖，点这里

-  下载地址：[MUSH]maper领悟机器人增强版

---

Mush领悟机器人改进版之再改进

出品人：诸葛不亮（Zgbl）

使用说明：

-  载入方式——打开按钮，选择“领悟技能.mcl”载入

-  打开游戏设置（mush中间部分的那排按钮），找到“脚本”或者“scripts”选项，载入lingwu.lua脚本，脚本语言选择lua，点击打开脚本

-  注意选中自动连线和断线重连

-  修改变量，具体参考http://pkuxkx.net/forum/viewthread.php?tid=9886&extra=page%3D&page=1

-  脚本中可以设置领悟级别数目，超过上限按照上限计算

-  注意领悟顺序

-  领悟的兵器设置中，id请与铁匠铺买到的兵器id相同

改良内容：

-  买兵器地点改为铁匠铺，以免当铺无兵器

-  食物吃光后自动quit重新登录买食物（小刀太可恶了，就10份食物，还不更新，我挂了一晚无用功……）

-  加入exert regenerate的有关触发（原来的木有这触发，我的flatter就没练上去）

适用于任何门派，只要没运气差到一句话断成两句（话说从没见过mush出这问题），保证可以完美挂机

**` 不管是maper的还是小刀的还是zgbl的，走路都必须set brief 1或者2或者3，不可unset brief或者set brief 0！ `**

-  变量设置请参考[MUSH]领悟机器人

-  下载地址小刀改良maper领悟机器人之再改良

---

Mush冥想机器人

出品人：Hba

自动连线，买1个干粮，1个酒袋，然后去莫高窟冥想；

设置方法：

-  lua语言，设置脚本位置；

设置相关变量：

-  player：游戏英文id，

-  passwd：游戏密码

[MUSH]冥想机器人

---

Cmud领悟机器人

出品人：Seagate
基本上从我以前zmud721版本的训练机器人沿袭下来，不过cmud版本维护上简便了许多。功能上强大了许多。

现在只有两个大步骤：第一个步骤是跳楼。【可省略】第二个步骤是领悟+练习。

其中第二个大步骤领悟+练习分为四个小步骤：内功领悟，parry领悟+第一特殊功夫练习，轻功练习，特殊攻击功夫练习和基本功夫领悟。

这四个步骤会根据合适的条件自动切换，设置非常简单。

执行下面命令：

```
#raiseevent sfSkillInit
```

按照提示一步步来就可以完成所有初始化工作。其中初始化的iron被动防御技能类型实际上是无效的，我没有开发这部分iron-cloth的领悟，因为使用面太狭窄了所以在cmud版本的开发中就给省略了，但是参数初始化还保留。算是为以后留下接口吧。

初始化完参数以后在中央广场买好吃喝和常备武器，执行命令start_full就开始训练之旅了。start_full命令后面可以跟参数jump就表示从跳楼开始，默认不进行跳楼。注意的是start_full命令里面有一些类开关，没有的类开关请删除，自己一些特色类要在训练过程中关闭请添加上去。注意在训练过程中一定要将消息捕捉的类给关闭了。我这里在start_full设置23点到8点之间启动start_full关闭消息捕捉类，但是xml脚本里面没有提供消息捕捉类，这个是出于稳定性考虑。

如果需要这个消息捕捉类可以通过我的另外一篇文章：http://pkuxkx.net/forum/thread-11985-1-2.html获得这个类的具体代码。

现在传上去的机器人整个代码都更新过了，去掉了大多数使用#wa命令的地方，稳定性方面测试一周没有发现明显的问题。

另外我说明一下初始化设置里面的消耗模式的含义：消耗模式是一个三位的字符串，一共支持三种模式：

100-仅消耗气血，101-消耗气血和内力，111-消耗气血，内力和精神。

消耗模式起作用是在练习模式下起作用，他会根据不同消耗模式有针对性的分配内力，但是领悟的时候辅助练习的时候是不会关心消耗模式的，消耗模式在选择辅助练习技能的时候也不会起作用。

bug修订：

-  20100306：修改了由于网速延迟或者其他原因导致命令叠加，单位命令超过限制，并且命令在辅助技能练习完毕要切换到正常技能的时候中断，导致正常技能领悟出现混乱，正常技能练习的时候结束判断出现混乱。修订版增加了一些保护措施。

-  20100505：具体修改：

-  修改parry阶段没有做武器切换的bug

-  重连的一系列bug

-  根据新手特点作了一系列优化，在特定环境下提高效率在33%左右。

下载地址：训练机器人【Cmud稳定版】

---

跳楼

Mush版跳楼机器人

出品人：Maper

mush版跳楼机器人

---

Zmud4.62版跳楼机器人

出品人：Archangel

适合精神比气血短的id使用，精神不足会自动睡觉，避免晕倒，气血比精神短的请修改触发判定。

无杀僧兵触发，请先过罗汉大阵再使用。

应景，发一个zmud462的跳楼机器人吧

---

练习

Zmud7.21版自动练功机器人

出品人：Msquare

手动导入状态提取触发器

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

使用说明

开始命令：sleep_transfer

开始前请确认sleep_condi和sleep_lian两个类别被disable，其他3个类别均enable。

不要随便移动别名、变量和触发器的位置，不要随便改子分类名，除非你确认你完全看透了代码。

sleep_accomplish别名会在所有练习完成以后被执行，你可以加一些想要的东西把这个变态的自动链连得更长。

默认运行地点是自己家里，用完了精气神就会睡觉，所以名字机器人叫sleep。

其他可以睡觉的地方理论上也可。但是需要修改断线重连（人物已经离线情况–主要是服务器重启）后的路径，即“客店留言板”触发器的内容。

没有包含断线自动重连（断线但人物未离线）的触发，请把你自己的断线重连触发器指向sleep_recon_cmd别名

这个机器人用到了数据库，想要保持机器人自动运行的话，需要导入数据库文件，并且在机器人运行过程中数据库窗口要保持打开！（可以最小化，我觉得这应该是ZMUD的BUG）

数据库项目说明

id:武功英文id

name:武功中文名

type:武功的enable类型

wield:练习武功需要装备的武器id(请自行保证身上有该武器)

lian_type:武功分为两种类型：练习时消耗内力的(condi)和练习时不消耗内力的(lian)

qixue_bound:练习武功要求的最低气血值

neili_bound:练习武功要求的最低内力值

注：以上3项(lian_type,qixue_bound,neili_bound)的类型和数据可以通过help menpai-xxxx查到，但是不一定对，最好自己试验确定。例如灵鹫的两种空手功夫都没写会消耗内力，但是实际上都要消耗。

附件里有一个我创建好了的数据库作为例子。依葫芦画瓢填你的武功就行了，数据库武功数据，前面几项都应该是永远固定的，只有aim_lvl是目标等级是需要根据需要每次都要填写的，cur_lvl是当前等级，触发器会自动抓取写入，不用填，填了也没用。

变量sleep_list是需要修炼的武功列表（数据库不是），顺序是由这个变量里的武功顺序决定的，一定要按照需要的顺序填。注意自行理清武功等级限制关系排序，比如太极剑不能超过太极拳等等。填写的是武功的英文id。

sleep_list里的英文id，数据库里的英文id必须和sk出来的英文id完全一致。

中文名必须和武功升级信息中显示的完全一致。

修炼的武功数据数据库里必须有，即sleep_list里的id必须对应一个数据库里的id，并且条目的数据要完备(除了cur_lvl)。

每次使用前把sleep_cnt置零。“每次”的定义为每次修改sleep_list列表之后

或者将

#VAR skill_id %item( @sleep_list, @sleep_cnt)
替换为:
#VAR skill_id %pop(sleep_list)

#IF (@sleep_cnt>%numitems( @sleep_list)) {sleep_accomplish} {sleep_transfer_sign}
替换为:
#IF (%numitems(@sleep_list)==0) {sleep_accomplish} {sleep_transfer_sign}

替换之后与之前的区别在于练完一个技能就会从列表里删一个。替换坏处是如果出问题机器人提前认为技能练完了之后想改回去的话得手动重新写。好处是不用在每次使用时把sleep_cnt置零，这个变量可以删掉。

发一个BT点的：[全]自动练功机器人

---

Zmud7.21全自动领悟机器人

出品人：Seagate

平台：Zmud 7.21 （低版本Zmud未作迁移测试）
版本更新：

-  0.75–实现了动态调整每时间间隔的指令执行数（增加参数high_times和lower_times）High_times最好设置成睡醒第一次执行指令能够将所有内力消耗完，lower_times消耗回复的内力，判定条件是内力<5%的时候执行lower_times，内力在5%-10%区间内执行lower_times+2。

-  0.76–Bug修正，部分优化

-  0.90–所有代码完成，等待我自测通过；优化状态显示界面【显示技能的汉字名称，显示两个技能】；优化领悟parry的时候交替领悟和联系的效率。

-  0.95–优化练习时候的执行效率，增加练习特色功夫的时候领悟对应的基本功夫50×@lower_times次数，免得精神浪费掉。

-  0.96–修正full_sk2类say start触发器启动相关的Bug。

-  0.97–增加类出错自救，主要两种情况自救：Busy，没有回到睡觉地点。碰到这个时候会自动look一下，然后根据地名自己走回去，say start。大概就是这个原理。注意的是跳楼类和Full_sk1-3类处理原则是不一样的，这里引用了一个内部参数：里程碑（auto_milestone）表示处于哪个联系阶段。本处仅仅表示一个示例，其他可能性需要使用过程中自己加（因为我是少林派的，其他门派在少林体验可能不一样，没办法加全）。另外增加参数spec_dodge表示你Enable的特殊轻功，会在Full_sk1类中把它放入_skill3中进行取样，下一步1.×版本可能会用到。

1.0—终于出稳定版了。基本上该测试的地方都测试里一遍，做了一些优化。赋值这块全部重写了，改用#VA形式来赋值以增强系统稳定性。另外就是Full_Sk1当轻功练完之后会自动找_pr_sk列表中武功选择非拳脚功夫（因为拳脚功夫练习耗内力降低主流程效率）练习。还有小问题的话发帖子说明一下我会尽早修改的。
设置参数：

-  修炼技能Var类里面的参数

-  wa_interval—表示取技能情况的间隔时间，如果网速慢的可以适当加大间隔。本参数仅在第一次开始的时候和每次睡醒的时候会发生作用。

-  _pr_sk——–表示特殊技能列表；

-  _pr_wp——–表示特殊技能使用的武器，空手请用none；

-  _bs_sk——–表示特殊技能对应的基本技能，注意列表中第一个技能是优先技能，会先在full_sk1类的时候就把特殊功夫满经验对应的技能。

-  high_times—-每时间间隔执行的最大重复指令数；

-  lower_times—每时间间隔执行的最小重复指令数；

-  spec_force —指定特殊内功，领悟Force的时候查看的特殊内功

-  spec_dodge–指定特殊轻功，目前并无实际用处，预留参数。

-  tick_sec——决定ticktime工具中定时作业多少时间执行一次批处理

-  auto_milestone-内部参数，表示机器人走到那个阶段，值和类名一致，会在类执行开始赋值。出错的时候会用到，让出错判定在应该判定的阶段执行该执行的指令。

-  full_sk1类中触发条件你说道：「start」中设置的_skill2技能是特殊内功，需要自己修改。

-  修炼技能Var类里面Alias中的命令lianxi,lingwu_force,lingwu_lx,lingwu_other是每定时作业执行的各种指令，分别代表练习特殊功夫指令【仅parry对应功夫】、领悟内功、练习的时候领悟基本功夫、领悟其他功夫。

使用说明：

使用开始之前最好执行一下skills;enable;hp三个命令联合，让系统自动扑捉参数，防止可能的问题。【因为很多参数是自动计算的，如果不自动计算一遍，使用默认参数，那运行就可能不合你的实际情况】

如果从跳楼开始，则关闭full_sk1,full_sk2,full_sk3三个类，打开out_l类（表示跳楼类），到鼓楼小院，执行命令say start就会开始。跳楼到满经验对应的技能等级会自动执行full_sk1类，full_sk1类执行完会执行full_sk2类，以此往下直到所有技能都满经验。其中full_sk1类先把force满到特殊内功对应的等级，然后领悟parry和_pr_sk第一技能满经验，接着执行full_sk2类，用parry把其他特殊技能满经验，然后执行full_sk3类把其他基本功夫满经验。基本就这个流程。

当然如果前面的过程想跳过，full_sk1,full_sk2,full_sk3三个类只要在“和尚院五部 -  ”执行命令say start就可以开始执行。

暂停可以执行命令#timer 0暂停，然后办完事情回到原先地点，执行say start命令就可以继续执行了或者在原先地点打开定时器也是一样可以继续执行机器人的。

下载链接：满技能机器人正式版

---

左右互博

Zmud462左右互博机器人

出品人：令狐大葱（Lhdc）

买点丹、药，带点水粮食，站在中央广场点一下“问黄药师”就可以开始互搏了。

中间可能有些参数自己修改一下，比如打坐的气血数等等。

练习互搏，要么打坐双倍内力的时候去，要么气血精力比较足的时候去。学互搏没有想象中那么可怕，睡觉前打开机器人，第二天该护镖护镖，该慕容慕容，到了睡觉的时候继续挂互搏，一般悟性20的话两个晚上就差不多了，根本不耽误正事。

适用于4.62版本，比较粗糙，临时做出来的，高手见笑了。

PS：如果站在桃花岛没反应，就在海港look一下。

发一个小小的互博机器人

---

星宿天龙吸内力

---

Zmud4.62版全套机器人

出品人：诸葛不亮（Zgbl）

内容：打坐、吐纳、学习、练习、跳楼、胡一刀、萧峰、护镖、万安塔、慕容

推车无聊，加了几个偷懒的按钮。。。

发现效果不错，干脆发上来分享算了

** 强烈建议使用推车时，在zmud的“常规”设置里关闭“回应指令行” **

-  胡一刀那里直接look就开始hyd任务

-  开始慕容后，慕容复那里look就开始慕容

-  万安塔门口look自动触发ask，进入每一层后输入wat，会自动侦测武士，若有明教则mess提示

-  hyd、hydb是hyd的往返path

-  mr是从慕容复走到ct，方便走路

-  kdb是杀盗宝人

-  db是pp盗宝人

-  cc是缠

-  ll是连

-  ww是装备兵器

-  wb是unwield all

-  boat是yell boat并且推车上船

-  shout和roar是两个很华丽的闲聊cemote效果

-  cure是在平一指处解毒并且找西门吹牛治疗的指令，感谢西门吹牛

貌似没什么特殊的alias了吧。。。

-  最轻松的还是推车，每秒自动提示目的地，并且每0.1秒发一个缠，只要用鼠标点点走路就ok了

-  装备和宝石自动放horse里面。ct输入hubiao，自动找平一指和西门吹牛（感谢西门吹牛），自动修兵器，自动在家里放下玉竹杖之类的杂物，然后自动去领任务

-  北京永安门外look可以自动unwield all然后ask，推车进去之后别忘了ww

-  永安门内look会自动ask出城

-  开始护镖按钮一定要在ct点

-  hubiao指令只能在ct输入

-  确认你有房子和horse，horse拿在身上

-  请set skip_combat 2

-  在Zmud的“常规”设置里面，关闭“回应指令行”

按钮位置按照1280*800分辨率设置，如有错位，修改屏幕分辨率即可

原帖地址：zgbl全套机器人

---

> 来源: https://www.pkuxkx.net/wiki/robot/practise
