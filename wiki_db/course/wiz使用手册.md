course:wiz使用手册

Wiz使用手册

此为《天下》mud的Wiz使用手册，内含mud编写中所有系统指令的详细讲解与举例，由于内容过多，在此不详细列出，需要下载的请点最下方的链接

另附一篇mud安全漫谈，来自清华bbs

```
发信人: heyusong (松), 信区: Mud_Builder

标  题: 《安全漫谈》

发信站: BBS 水木清华站 (Thu May 18 21:37:19 2000)

《安全漫谈》

这篇文章主要针对提供正式开放的游戏，如果你

只是在单机游戏上玩一玩，请不要费神阅读，因

为这对你毫无用处。

前一段时间经常看到什么 mud 被黑，某某自称

“黑客”者要挟某游戏之说，由此产生感慨写下

这篇文章。这里无意贬低任何人的能力，如果您

真是一位高手而并非一知半解的翻翻安全公报、

在网上找点所谓“黑客工具”试试的那种，鄙人

愿意随时怀着敬仰的心情聆听您的教诲。

既然是漫谈，就是想到哪说到哪，内容难免有离题

之处。

有些人采用正式开放的游戏里不设巫师，而启动另

一个游戏的副本来开发以为就万事大吉了，或者我

根本不给巫师提供 edit，首先不说这完全抛弃了

LPMUD 的优越性，还不如改动一下将 OS 和 LIB

编译后运行，还能极大的提高效率，如果开发环境

本身是一个不安全的环境，又有谁能保证从这里拿

走的代码是安全的呢。可能会有人说：比如我根本

不招收巫师、我们游戏的巫师一生一世都能团结一

致的象一个人、用人不疑疑人不用，我们的机器是

请专家配置的，你算什么，等等超过 100 条理由

来反驳对安全措施的看法，对此我不提出任何意见，

记得有人说过一句笑话：使服务器最安全的方法就

是拔掉网线。对于无谓的争论我不感兴趣，如果你

认为安全是一个不值得一提的话题，请立刻停止阅

读本文章以免耽误宝贵的时间。

最初接触 LPC 就是看的 es2 的 MUDLIB，还是 big5

码的，读完以后对于其作者 Annihilator 充满敬仰

之情，虽说是一个“游戏”之作，但绝对只有本着严

谨的治学态度才能写到这种程度，虽说也存在着不少

问题，但那都是细枝末节。es2 的 mudlib 由于是一

个人由一个统一的思路指导创作而成，其明晰整洁的

模块化结构，科学直观的继承关系，极大的简化了区

域编程的难易程度和给与极大的灵活性，致使以后的

文字 mud 在 es2 的沃土上迅速的繁衍生息，而将

es2 类的 mud 推上 LPMUD 的主流地位，里面有很大

的必然性。

*** 先从 mudlib 内部入手 ***

首先要注意几个特别的文件

第一位的就是 MASTER_OB ，一般位于 /adm/obj/master.c

所有限制都是由这个物件里的函数通知 mudos，

当然也包括读、写的禁止与允许，一般的 mudlib

都把有关安全的部分集中到一个叫 SECURITY_D 模块里

统一管理，一般位于 /adm/daemons/securityd.c，

将 MASTER_OB 的读写判断用 call_other 方式

引用到这个物件里。这两个文件如果有机会被改写，

会将 mudlib 的安全机制完全打破，所以在正式运行

的游戏里应当禁止对这两个文件的写，需要对这两个

文件进行改写的机会是很少的，如果遇到这种需要

可在 shell 里进行。

巫师列表文件，一般为 /adm/etc/wizlist ，这个文

件里保存了所有巫师的列表和对应的等级，对这个文件

的写应当设定成只有 SECURITY_D 物件允许，其它物件

一律不允许。

提升巫师命令，一般叫 promote ，位于 /cmds/arch/

目录下，（这个命令里应当注意的基本原则例如传入物件

应当为 this_player(1)，提升的等级不可超过命令执行

者的等级等基本问题你应当非常熟悉，此文章的其它部

分也假设你对一些基本的问题已经有了透彻的了解，而

不会再与提及，如果你未能了解，请立刻停止阅读本文

章，以免造成不应有的误解而适得其反。）此文件一经

写好应当不需要再更改，因此在 mudlib 应当禁止对此

文件的写。promote 需要呼叫 SECURITY_D 里的相应函数

实现巫师等级的提升，一般为 set_status() 函数，这个

函数里应当首先判断他的前物件 previous_object(0)

是否为 find_object("/cmds/arch/promote") ，当然不

能是 clonep 了，如果不是，立刻 return 0 就是了。

MASTER_OB 里的 valid_seteuid() 函数很重要，要小心

配置，一般 call_other 到 SECURITY_D 里处理，普通情

况应当只有 seteuid(getuid()) 、 ROOT_UID 和

SIMUL_EFUN_OB 允许 seteuid。如根据需要扩展须小心配置。

玩家档案（当然包括巫师）的读和写是应当小心管理的

地方，LOGIN_OB 保存档案的读应当除了 restore_object

函数和神，其它都不能读。由于 LOGIN_OB 的 query_save_file()

函数的返回值是由 query("id",1) 决定的，所以对 LOGIN_OB

的 set 应当除了 ROOT_UID 其它都禁止，也就是在文件里

写入同名函数 nomask mixed set(string prop, mixed data)

作提前判断，此函数里第一行就应当是

if( geteuid(previous_object()) != ROOT_UID )

return 0;

关于玩家档案的写，应当以物件的文件名和它的 euid 作依据，

文件名是否为 LOGIN_OB 和 USER_OB，在 valid_write 里可以

象这样判断：

if( func=="save_object" )

{

if( sscanf(file,"/obj/login/%*s")

|| sscanf(file,"/obj/user/%*s") )

{

string id;

if(sscanf(file,sprintf("/obj/login/%c/%%s.o",euid[0]),id)

&& (id == euid) )

return 1;

if(sscanf(file,sprintf("/obj/user/%c/%%s.o",euid[0]),id)

&& (id == euid) )

return 1;

}

else

......

}

不符合就直接进入权限检查，建议除了神和 ROOT_UID，其它都

过滤掉。对于 LOGIN_OB 和 USER_OB 这两个文件的写应当经受

最严格的安全检查。对于 LOGIN_OB->query("password")，如

果不是 ROOT_UID，不用说 return 0 就是了，写一个 query

的同名函数即可。

/feature 目录应当只有 admin 才能写，尤其是 save.c 、

dbase.c 和 command.c 。

SIMUL_EFUN_OB，这个物件的 euid 绝对不能是 ROOT_UID。

有一个 cat() 函数写的很不好，根据基本的配置这个函数

可以完全超越读权限的限制而且毫无实际用处，只是表现了

编写者对 unix 的钟爱，建议取消。还有一个函数 assure_file()

用于越权创建原来没有而又必须的目录，在里面要执行

seteuid(ROOT_UID)，但是 es2 里面却没有还原，致使执行过

此函数会使 SIMUL_EFUN_OB 以后以 ROOT_UID 运行，这可是不

得了的事情，在此函数的末尾返回前要加上 seteuid(getuid())

来还原。

log 记录是系统运行状况的晴雨表，此记录的真实性和完整性

对于管理者至关重要，一般都造一个 log_file() simul_efun 函

数，这个函数只接受两个字符串作为参数，这就保证只能以

append 方式写，而不能 write_file("/log/xxx","xxx",1)这种

形式覆盖写，这个目录应该只有 SIMUL_EFUN_OB 和神才能写，

或者连神也不能写也无所谓。

bind() 函数在 MASTER_OB 的 valid_bind 里限制，最起码的

对于玩家物件是绝对不能的。

关于需要保护的一些函数：

MASTER_OB 里的 valid_override专门就是干这个的，当这个函数返

回 0 时，你就不能用 efun::xxxx() 的形式使用系统函数的原型，

而必须用 SIMUL_EFUN_OB 里提供的同名函数。

** move_object 和 destruct 由于根据游戏情节需要进行预处理比如

重量的调整，所以是需要的。

** shutdown 函数应当只有 shutdown 命令才能呼叫，处理方法参考

提升权限命令的部分，必须保护。

** localtime 函数当传入一个 <= 0 的参数时正常情况下会当机，

必须保护。

** ctime 函数同理 localtime 函数，必须保护。

** interactive 函数当传入一个 0 作为参数时正常情况下会当机，

必须保护。

** snoop 不用说了，不能允许 snoop 高于自己权限的人，比如

你正在 more 一个我没有读权限的文件。。。必须保护。

** exec 要命的东西，一般只有 LOGIN_D 才需要，如果你想提供

update 玩家的能力，update 命令也应当允许，其它一律禁止，

当然还要注意 LOGIN_D 执行 exec 的部分函数必须是 private，

update 玩家需要调用 enter_world 函数，这样 enter_world

里必须先判断 origin()，如果是 local 可以，如果是 call_other

则 previous_object(0) 必须是 ROOT_UID，其它情况一律禁止。

MASTER_OB 里的 creator_file 函数是至关重要的，一般引导到

SIMUL_EFUN_OB 里的同名函数处理。它的返回值决定着物件的 uid，

也就是被 Mudos 制造出来时的 euid，它的返回值必须要将第一个

字母转换成大写以避免和玩家的 id 发生混淆，需要 ROOT_UID 的

一般只有 /adm 目录，里面的 SIMUL_EFUN_OB 必须设成一个特殊的

ID(注意大写开头)，还有极少数的命令需要，其它的都不需要！！

对于这些目录应当除了神以外任何其它的巫师都不能写。

有一个特殊情况就是巫师的工作目录可不能大写开头，因为要和巫师

的等级对齐，不过一定要先判断 this_palyer(1)，如果存在必须优

先返回 this_player(1) 的 euid，否则你目录下的东西被别人 clone

走以后物件的 euid 还是你的 euid，如果碰巧你写了一个权限测试

物件或者其他什么不像话的东西忘了删掉，后果不堪设想。执行命令

里需要 ROOT_UID 的玩家命令是很有限的，最好将这几个命令单开一

个目录赋予 ROOT_UID，小心的检查每一行代码，其它的目录都赋予

一个奇怪的 uid，例如："Nobody"。

说到巫师工作目录，由于上面的理由可以知道工作目录的上一级目

录的写权限是多么的重要，这应该只有神才能写，其它一律禁止。

再有除了神绝对不能允许写别人的工作目录，这绝对是必要的。

global include file 也是一个非常重要的文件，

一般定义为 /include/globals.h ，一般 ROOT_UID

就是由这个文件定义的，如果我把 ROOT_UID 改成

我自己的 ID "find"，我的 euid 就是 ROOT_UID，后果

不言而喻，所以在正式开放的游戏里这个文件应该定义

为不可写。再有一个叫 command.h 的头文件用来定义可

执行命令的搜索路径，要瞪大眼睛仔细看，对于此文件

的写应当只有神允许。

对于除了巫师写自己的工作目录以外的写都应当作记录。对于

/adm 目录下的载入物件应当除了神和 ROOT_UID 以外不允许

摧毁。

mudos 的 OLD_ED 是一般游戏都使用的编辑器，在使用者

断线后保存 ed_buffer 之前不进行写检查，保存的文件名

由 MASTER_OB 里的 get_save_file_name 返回值决定。这

绝对不是件好事请，应当在 mudos 的源代码里 ed.c 的

void save_ed_buffer P1(object_t *, who) 函数中把

stmp = safe_apply_master_ob(APPLY_GET_ED_BUFFER_SAVE_FILE_NAME, 2);

一直到 free_ed_buffer(who); 前一行的内容用

if (getfn(1) != NULL) { } 括起来。

MASTER_OB 里的 get_save_file_name 应该返回一个奇怪

而又难以重复的名字，es2 里是 sprintf("%s.%d", fname , time())

就很好，如果想以后对此文件操作时少输入几个数字用

uptime() 也很好。

巫师的档案应当是不允许 purge 的，purge 之前应当

先降为玩家，同理，巫师也应当不允许自杀。

区域文件的 euid 应当定义为区域名较容易管理，

它的 euid 应当把第一个字母置换成大写以避免

和用户 id 冲突。

在所有的读写权限安排好以后，还有一个巨大的安全

隐患，就是 dbase.c ，一般位于 /feature/dbase.c

这一般不太会引起人的注意但又是很致命的弱点，这

个物件里的主变量 mapping dbase 保存所有的变量

设置，这是 es2 类的 mudlib 极大的优点，把所有的

变量处理集中模块化，充分的利用了继承性极大的简

化了编程和执行效率。但由于它极强的通用性在某些

方面如果不作限制会造成安全隐患。问题在于这个物

件里的 query_entire_dbase() 函数，由于 mudos 是

用 c 语言编写充分利用了指针的特性，这个函数返回

的是 dbase 的指针而不是它的副本，由于通过这个函

数取得了 dbase 的地址指针，所以就可对它为所欲为

而完全超越 mudlib 的安全限制。例如：

object user; // 是一个玩家物件。

mapping my;

my = user->query_entire_dbase();

my["max_force"] = 1000000;

my["force"] = 1000000;

哈，这个玩家的内力就变成 100 万了，有什么东西能

检查出我干了这事情？

更有甚者：

比如我有一个密码的密文 "Tn/2pfZd4HtKc"

它的明文只有我知道是 "12345"

这个密文是很容易得到的，随便一个单机 mud 设置好

密码一 save 就得到了。

object user; // 是一个在线的天神物件

object link;

mapping my;

if(objectp(link = user->query_temp("link_ob"))

{

my = link->query_entire_dbase();

my["password"] = "Tn/2pfZd4HtKc";

}

在其毫无知觉的情况下把他的密码改掉了，等他退线，

这个密码就会保存好，那位神由于不知道新密码就进

不来了，这个账号的密码明文只有你知道，怎么说呢，

现在你就是神！

所以应当作一些小限制，在 LOGIN_OB 里应当加入：

// 这对系统毫无用处，return 0

nomask mapping query_entire_dbase()

{

return 0;

}

// 避免以后扩展可能带来问题

nomask mapping query_entire_temp_dbase()

{

return 0;

}

// 连接物件只允许系统设置

nomask mixed set_temp(string prop, mixed data)

{

if(( prop == "body_ob")

&& (!previous_object()

|| (geteuid(previous_object()) != ROOT_UID)) )

return 0;

return ::set_temp(prop, data);

}

// 除了系统不允许取得密码的密文，避免互相了解以后

// 缩小猜测范围，用猜谜码软件取得明文

nomask varargs mixed query(string prop, int raw)

{

if(( prop == "password")

&& (!previous_object()

|| (geteuid(previous_object()) != ROOT_UID)) )

return 0;

return ::query(prop,raw);

}

对于 USER_OB 不能这么限制，首先应当写一个 simul_efun

用于复制变量，也就是强制产生一个变量副本而不是指针，

比如这个函数叫 mixed duplicate(mixed var)

在 USER_OB 里加入：

mapping query_entire_dbase() // Find.

{

// 非系统需要返回 dbase 的副本而非指针

if( previous_object()

&& (previous_object() != this_object())

&& (geteuid(previous_object()) != ROOT_UID) )

return duplicate(dbase);

else

return dbase;

}

mapping query_entire_temp_dbase() 同理。需要注意的还有

保存武功的 skill.c

// link_ob 除了系统决不能允许别人设置

nomask mixed set_temp(string prop, mixed data)

{

if((prop == "link_ob"))

{

if(!previous_object() || (geteuid(previous_object()) != ROOT_UID) )

return 0;

else

return ::set_temp(prop, data);

}

}

再有一个忠告，对于安全至关重要的物件绝对不要用

F_DBASE 来管理变量！！！！！！！切记！！

关于巫师的一些特有设置：

比如隐身或者根据某些标记察看系统的运行状态，一般为了

方便巫师都集中在 set 玩家命令里，这些标记应该单开一

个区域存放，如果沿用 es2 的处理方法，需要有几点要

注意:

在设置时进行检查，如果都是单层设置可以：

int i = strsrch(arg,'/');

if(!i)

错误返回

if(i>0)

arg = arg[0..i-1];

再进行设置标记判断。

如果有多层设置：

arg = implode( (explode(arg,"/") - ({""})),"/");

再进行设置标记判断。

在标记的作用模块里应当进行 wizardp() 的检查，这是好

的作风。

对于巫师物件和来源于巫师的物件应当在自己的系统里严格的

标记出来，对于这些物件上的 action 应当绝对禁止玩家执行，

对于这些物件对玩家产生的任何影响都应当毫无例外的详细的

记录，如果想给自己留一个方便之门最后只会使自己深受其害。

对于这套系统的建立方法由于牵涉面比较广通用性也很差，说

起来连篇累牍，就不详细说了，需要根据自己的系统特点小心

的选择方法详细的考察。

对于非法 action 的过滤到是可以举个例子供参考，这个工作

应当在玩家物件的 process_input() 函数里进行，在返回之前

应当通过一个过滤函数进行过滤，比如

if(userp(this_object()) && !wizardp(this_object()))

action = control_action(action);

control_action 函数的内容应该大概象下面这个样子：

private string control_action(string cmd)

{

mixed *cmds;

int i;

string str;

if(!stringp(cmd) || cmd == "")

return "";

sscanf(cmd,"%s %*s",str);

if(str == "")

return str;

if(!str)

str = cmd;

cmds = this_object()->query_commands();

// 后面乱了，请自己看此页的源码

for(i=0;iquery_wiz_flag()) // 巫师或来源于巫师的物件

return "";

}

}

return cmd;

}

这样的结果例如巫师 clone 一个鸡腿给玩家，玩家是

没法“吃”的，或者有巫师 clone 一个乱七八糟的衣服

之类的东西给玩家，玩家拿着它什么也干不了。这样的行

为应当根据记录受到严厉的处罚。不过在 give 命令里应

当作个判断来禁止这种“给”从而提醒巫师或者自己这样

作是非法的！窃以为这是'仁慈'的做法，不要不教而诛。

对于巫师的密码应当有特殊的要求，必须8位同时包含字母、数字

和特殊字符，否则应当禁止登陆。巫师账号的密码过一定时间

应当强制更改，一般 30 天比较合适。对于巫师账号的密码输

入错误应当作详细的记录，至少也应当包括时间和来源。对于

连续几次输入错误应当将这个账号 block 住禁止登陆来防止

密码猜测，一般为 3-5 次较好。当然还要设立灵活安全的恢

复机制，否则游戏所有的巫师都无法进入就闹笑话了。应当将

被 block 的账号记录在一个只有 ROOT_UID 才能写的文件里，

block 管理物件定时根据此文件的内容进行更新，一般 30 分

钟为宜，这样管理者就可以在 shell 里去除某个账号的封锁

状态。这种保护应当监视所有的连入手段，包括 ftp。

最好不要在 mudlib 提供 http 服务，有的甚至在 mudlib 提

供游戏主页的服务，主页制作的丰富多姿，这种情况应该是坚

决杜绝的！ www 页面上的每一个元素都要引起一个并发请求，

对于复杂的页面即使浏览的人不多，瞬间的并发请求也会超出

一般人的想象，mudos 操作是一个大循环，大量的请求会严重

影响游戏的执行速度和占用大量的带宽，如果实在难以抑制这

种冲动可以只提供一些反映游戏内部状况的 cgi 生成一些简

单的信息页面供你游戏的主页调用嵌入。

如果想提供网际互连，应当明确的指定几个允许互连的游戏，

并将其它的屏蔽掉避免过重的端口负担。由于一般网际互连的

服务程序都以 ROOT_UID 运行，所以要严格检查这些程序代码

里是否被人留了一手，最好将此部分移出 /adm 目录，但这要

改变很多头文件很麻烦，简便的方法在前面提到的 creator_file

函数里将此目录下的物件设定成一个特殊的 ID，例如：

case "adm":

if( sscanf(file,"/adm/daemons/network/services/%*s"))

return "Netservice";

如果你的这些服务代码里有对 ROOT_UID 的需求，将其移至

DNS_MASTER 或者方便的模块里统一处理。如果你的 valid_seteuid()

函数里允许了 /adm 目录，请先将这个目录抛除.

如果 receive 函数接受的字串有超过字串最大长度设定（一般为 8k）

的行，有可能会造成当机，应当有适当的措施处理。

关键部分不要编制晦涩难懂的代码，这只会带来安全和 bug 隐患，

代码要尽量的简洁清晰。

前一段时间听别人谈起过游戏的数据备份问题，沉重的备份（比如

对整个游戏代码或者所有动态档案的备份）工作应当在 shell 里

用 crontab 编制 shell script 来完成。由于 mudos 的工作机制

做这种事情实在是哪壶不开提哪壶，如果难以避免进行这类沉重的

工作（比如想提供符合实际的玩家排名就需要对所有的玩家档案进

行检索），应当采用均衡负担的技巧不对游戏的运行产生可感受的

影响。要注意的是，这类工作对于 mud 来说有一件都嫌多。

对于一个设置良好的 mudlib 可以在安全的前提下赋予巫师最大的

自由度，这对一个游戏的建设应当是必要的。

*** 从外部来说：***

首先应该能保证服务器的物理安全，没有这个前提根本谈不上安全

两个字，试想一个左手拿着锤子右手拿着螺丝刀的人站在你的机器

面前，你除了表现出一副什么都不在乎的样子，还能作些什么呢。

选用操作系统，由于 MUD 一般都是非盈利性的，所以应当选用一个

免费的低成本操作系统，例如 linux、FreeBSD、Solaris 8 等，

以大家熟识的 linux 为例，其它都同理。安装系统时不需要的软件

包一律不装，如果已经安装了就将其卸掉，linux 是 rpm -e

FreeBSD 是 pkg_delete。保证系统的所有软件都已经升级到了最新

的稳定版本。

服务器应当提供尽可能少的服务，应当做到专机专用，只提供 mud

服务，如果提供其它的服务请参考相关的说明，对于一些“臭名昭著”

的服务，例如 rpc netbios 等除非你对它有透彻的了解，否则一定

要关闭。

首先绝对不要以 Root 运行游戏，应当单设一个用户作为 mud

管理者。一般用户的主目录都是 /home/id ，而在游戏中很容易

得到执行档的路径 get_config(__BIN_DIR__)，这样就可以知道

管理者的 id，为攻击明确目标，所以管理者的 home 目录应当

设定成一个别的目录，比如 /home/mud，使人无法从执行档路径

得知游戏管理者的 id，游戏管理者的 ID 不要起和游戏有关的

id , 例如 game games mud mudadm mudmud tianxia txia tianx

等等这类的 id 都是很不好的，甚至是自己在游戏中的 id，应该

是一个另类的 ID 而且毫无普遍的意义，密码的设定不要使用游

戏中或电子邮件等其它地方用过的密码，专码专用，设定原则同

游戏中巫师密码的设定原则。

使用 shadow 保存密码，/etc/shadow，FreeBSD 里面叫

/etc/master.passwd 这个文件应当是 root root 400。

去除所有不需要的账号，一些系统账号设置成不可能登陆。

一般只保留 root 和游戏管理者两个可能登陆账号，root

除了控制台不允许登陆。将 home 目录的权限设定为 700，

umask 设定为 077。

为了便于远程维护需要 telnet ftp 的服务，不要启动 inetd

服务，而代之以 sshd2 这种加密方式的连接，其设置有几点要

注意：

PermitEmptyPasswords 一定要是 no

PasswordGuesses  设成 2 足以

PermitRootLogin  不用说 no

Ssh1Compatibility no

AllowedAuthentications  publickey,password

RequiredAuthentications  publickey,password

必须通过 publickey 和 password 的双重验证

其它的请查询相关的手册

一个干净的系统应当只提供 sshd2 和游戏这两个服务。

尽量减少此账号的使用人数，定期更换密码

经常用 ifconfig -a 检查你的网卡是否处于混杂模式。

经常阅读记录档，并打包下载备份。

定期察看自己系统所使用的程序升级版本信息以确定是否要

升级。定期察看安全公报看自己所使用的系统是否出现了对

你产生影响的漏洞，及相关的安全补丁。

发现了新的安全工具，拿来先搞明白原理，然后不用考虑，先

照着自己的系统来一通。

其它的一些安全问题请参考相应的文章。

对于一个 mud 服务器很难有条件再架一台服务器作为专门的

防火墙，所以只能自己保护自己，一般采用 ipfilter 类型的

防火墙，对于包过滤类的防火墙的具体配置由于各系统的方法

不同，所以只谈原则。

一般是两个网络设备，lo 本地环路，eth0 网卡（外部通道）

不信任任何源地址

禁止 forward

禁止任何来自 eth0 的包声称自己来自本地（ip 欺骗）

对于源地址进行核对

提供 SYN cookies 保护

禁止任何来自外部的广播包

对于本地设备 lo 都放行,

对于 ICMP ：

应当只允许 destination-unreachable(网络不可到达)、

echo-request(ping) 和 echo-reply (ping 回应，如果

不需要尽可过滤掉)这三个进入，其它一律过滤掉。

对于 UDP：

一个是需要一个外部 dns_server 帮你进行解析，比如

它的 ip 地址为 a.b.c.d ，所以对于来源于 a.b.c.d 53

的目的地为本地高端端口(1023-65535)的包放行，

如果你提供 mud 互连，对于目的地为这个端口的包也应当

放行，如果你只和有限的几个 mud 互相，也可以将其定义

在防火墙里，对于来源于这几个互连端口目的地正确的才

放行。

其它一律过滤掉。

对于 tcp:

对于你的 ssh 端口，如果你是固定 isp 拨号上网应当对源

地址进行判断，比如你的 isp 的动态 ip 分配的都是

a.b.xxx.xxx，你可以设定源地址为 a.b.0.0/16 的才放行。

如果你是固定 ip ，可以指定 a.b.c.d/32 放行。

对于提供游戏服务的端口，目的地为本地此端口的包一律放行。

Mudlib 一般为了巫师的工作都要提供 ftp 服务，这部分代码

要注意绝对不要提供被动模式的 ftp 连接，也就是 passive

命令是不可执行的，只能采用主动模式。规则应当这样：

对于目的地为这个 ftp 端口的包放行，ftp 还要建立第二条

数据连接，由于 port 方式这个连接是由 ftp server 发起的，

tcp 的连接过程是一个三次握手的过程，发起连接的包的控制

位需要置 SYN，所以只要是包的控制位没有置 SYN ，目的地为

本地高端端口的才放行。

其它的包一律过滤掉。

要注意的是 防火墙不等于安全！！！

一个安全牢靠的系统环境是游戏成功的基本保障

由于安全部分是很早以前作的，难免有一些细节被遗忘疏漏，

再加上本人水平有限，只是作为一个参考。而且所说的不保

证 100% 正确，如果你按照本文设置造成系统崩溃、机器爆

炸等灾难后果，本人概不负责。

绝对不要给自己留任何后门，也许会有暂时的欣喜感和某种

心理上的满足，但这是要以长期的痛苦甚至不可逆转的恶果

作代价的！！

总之，安全不是代码，安全是意识，只要你时时想着安全，

你所处的环境就会越来越安全。否则原有的问题不能解决，

而且还会由于你的粗疏不断产生新的问题，最后只能无奈

的说：es2 类的 mudlib 是全世界最不安全的 mudlib。

绝对的安全是不存在的！

如果你觉得这篇文章对你有所启发，我将会感到荣幸，如果大多

数人都认为毫无用处我也会很欣慰，因为游戏的安全状况比我的

想象要好得多。

如有缺失欢迎来信指正，jytong@263.net，如有人愿意以次为

基础共同来维护一个 MUD 安全 FAQ 之类的东西，本人愿意在

精力允许的情况下积极参与。

《天下》mud.263.net 6666

发现号(Find)

--
```

wiz使用手册

> 来源: https://www.pkuxkx.net/wiki/course/wiz%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C
