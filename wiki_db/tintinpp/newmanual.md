- TinTin++中文手册

- 译者自序

- 正文

- 启动与关闭TinTin++

- 基本特点

- 帮助文档

- 连接到一个mud

- 分屏

- 别名

- 触发

- 快速行走

- 定时器

- 命令文件

- 重复执行

- 历史命令

- 路径

- Action

- All

- Bell

- Break

- Buffer

- Case

- Chat

- 建立一个连接

- Class

- ANSI Colors（ANSI颜色代码）

TinTin++中文手册

- 　２０１３年１２月　alucar 发表于北侠论坛

- 　２０１４年１２月　puzzlist 整理至北侠维基页面。

译者自序

工欲善其事，必先利其器。在红衣影响下，从zmud转投tt门下已有一段时间了，但百度中至今没有搜到TinTin++的中文手册，一时兴起也做一回翻译，希望能降低一些tt的上手难度。

一些说明：

-  tt的主页为tintin.sourceforge.net，后面的内容均译自该站，但目前似乎被墙了，可能需要翻一下。

-  目前的翻译版没有与原作者联系，如今后涉及版权等问题，必要时可能删除。

-  原文中的一些例子均按北侠的环境作了本地化调整。

-  大部分指令在wintin++ 2.00.9环境下测试。

-  翻译不当之处还请指正。

正文

TinTin++ Mud客户端手册

本章节是对TinTin++的一个简要使用说明，更多的帮助信息可以查询每个命令的帮助文件。

启动与关闭TinTin++

TinTin++的启动命令是：./tt++ [命令文件] （译注：对于windows平台下的wintin++，安装后直接点图标启动即可）

有关命令文件的信息可以查询后面的专门章节。有必要说明的是，在TinTin++启动时加载的触发、别名等都会被所有的session继承。

在任意空行输入#end或按下^d将会退出TinTin++，被选中的文字将自动复制到剪贴板，你可以按下shift+insert进行粘贴操作。

基本特点

让我们从一些非常基本但也十分重要的开始：

**所有TinTin++的命令都以“#”号开始。（你可以用#config更改）**

例子：#help——#help是一个客户端命令，不会被发送到服务器。

**所有TinTin++的命令都可以缩写。**

例子：#he——输入#he与输入#help是等效的。

**所有命令都可以用“;”号分隔。**

例子：n;break men;enter;killall——连续执行这四个命令

**有三种方法可以让“;”号作为一个普通字符出现。**

例子：\say Hello;) ——以“\”号开始的行中，所有特殊字符都只作为普通字符出现。

例子：say Hello\;) ——在一行中间出现的“\”号可以强制让后一个字符作为普通字符出现。

例子：#config verbatim off ——设置后，除了以“#“号开头的语句，其他的都会以原貌被发送到服务器。

帮助文档

**命令：#help {主题}**

help命令是你最好的朋友，输入#help可以看到所有的帮助主题，而且内置的帮助文档总会比主页上的更加新一些。

连接到一个mud

**
命令：#session {session名称} {mud地址} {端口}**

*例子：#session alucar pkuxkx.net 8080*

你可以打开多个session，并且用#<session名称>进行切换。

你可以用#session命令显示所有已经打开的session清单，其中标记(active)的为当前活动的session，标记(snooped)的为正在观察的session，标记(mccp)的为使用mud客户端压缩协议的session（mud client compression protocol）。

分屏

**命令：#split**

#split命令可以将屏幕分割为输入区与输出区。

使用#prompt命令可以捕捉并将特定信息显示在分屏栏上，#unsplit命令可以取消分屏。

别名

**
命令：#alias**

**语法：#alias {别名名称} {命令}
**
#alias命令用于定义别名，别名的参数可以用%0，%1……%9来引用，具体如下：
%0代表所有参数；
%1代表第一个参数；
……
%9代表第九个参数。
*
例子：#alias ga get all from %1*

如果定义别名时没有指定参数，在使用别名时，后续内容会自动添加到别名代表的命令之后。

*例子：#alias tan perform throwing.tan——tan pantu相当于perform throwing.tan pantu*

要在一个别名内执行多个命令，需要使用花括号。
*
例子：#alias pu {exert qi;exert powerup}*

#unalias命令可以删除一个已定义的别名。

注意：TinTin++在冗错方面并没有提供婴儿式的服务，比如没有对别名进行循环引用的校验。你可以利用”\”号来避免循环引用。

*例子：#alias put \put %1 in %2*

或者也可以使用#send命令。

*例子：#send put %1 in %2*

触发

命令：#action

语法：#action {触发语句} {命令}

#action命令将生成一个触发，当特定的信息出现时，自动执行指定的命令。在触发语句中最多可以使用99个变量，以通配符%1、%2……%9、%10……%99表示。

例子：

#action {你舔了舔干裂的嘴唇，看来是很久没有喝水了。} {drink jiudai}

#action {%1走了过来。} {hihi} ——当有人走过来的时候打招呼。

#action {%1告诉你：%2} {say %2} ——把别人tell你的内容say出来。

#action {看起来%1想杀死你！} #bell ——当有人想杀死你的时候发声提示。

#ignore action on命令可以暂时关闭所有的触发。

#debug action on命令可以让触发生效时显示所执行的命令。

#unact命令可以删除已定义的触发。

高亮显示

命令：#highlight（还记得你可以使用命令的缩写形式么？）

语法：#high {文本} {颜色}

这个命令的用法与#action很象，它的功能是用你指定的颜色来显示服务器输出的特定内容，相当于#substitute命令的简化版。

例子：

#high {烈火鞭} {light red} ——将“烈火鞭”三个字以亮红色显示。

#high {%1烈火鞭%2} {light red} ——将包含“烈火鞭”三个字的整行文字以亮红色显示。（译注：经测试这条命令不起作用。）

#unhigh命令可以删除已定义的高亮显示。

快速行走

如果输入一个只由数字和方向（n,e, s, w, u, d）组成的命令，那么这个命令会被解释为一个快速行走命令。

例子：ssw2n相当于go south, south, west, north,north

如果你在输入一些确实只包括上面这些字母的命令时遇到了麻烦——比如news指令就可能被当作一个快速行走命令——你可以尝试用大写字母进行输入。（译注：用大写字母在部分中文mud中是不可行的，只能用下面提到的办法关闭快速行走。）

在使用快速行走功能前，必须首先设置#config speedwalk on/off。

定时器

命令：#ticker {名称} {命令} {秒数}

在北大侠客行和其他一些mud里每15分钟会刷新固定npc和物品，所以如果能知道离下一次刷新还有多少时间是一件很棒的事，TinTin++可以帮助你做到这一点。

#ticker {tick} {#delay 840 #show 还有一分钟刷新！;#show 刷新啦！！！} {900}

上面这条命令将会生成一个名为tick的定时器，每15分钟显示“刷新啦！！！”，并且在刷新前一分钟会给出即将刷新的提示。

#untick命令可以删除定时器。

命令文件

当读取一个命令文件的时候，TinTin++将执行该文件中的所有命令。你可以用命令文件来保存别名或触发，登录到一个mud（包括输入id与密码），它最基本的功能就是保存各种命令。

我强烈建议你使用一个文本编辑器来编写命令文件，当然你也可以使用#write命令把当前的设置保存到一个命令文件中。

文件操作命令：

#read 文件名 ——读取并执行一个命令文件。

#write 文件名——将当前session中所有已知的触发/别名/替换等内容写入一个命令文件。

重复执行

你可以使用“#数字 命令”这样的语句来重复执行一个命令。

例子：

#5 e ——向东走五步。
#10 {fill jiudai;put jiudai in bag} ——重复执行这两个命令十次。
#100 chat* poke ——如果你不怕被禁言的话。

历史命令

TinTin++拥有历史命令回溯功能。

! ——重复上一个命令。
!get ——重复上一个以get开头的命令。
ctrl-r ——进入历史命令搜索模式。

路径

当你输入#path new命令后，TinTin++将会开始记录你输入的移动指令——比如north、south、east、west、up、down——并把记录的指令保存在一个路径里，同时生成相应的逆向路径。

路径命令：

#path new ——重置当前路径并开始记录新的路径。
#path end ——停止记录路径。
#path map ——显示当前路径。
#path ins {forward} {backward} ——在当前路径的最后插入移动指令，{forward}与{backward}参数分别为所插入移动指令的正向与逆向。
#path del ——删除当前路径的最后一步。
#path save {forward|backward} {variable} ——将当前路径保存到变量中，{forward|backward}参数指定保存正向/逆向路径。
#path load {variable} ——从变量中读取路径。
#path walk {forward|backward} ——按照当前记录的路径行一步，{forward|backward}参数指令按正向/逆向行走。（译注：每次行走后会删除当前步的内容，所以不能交替使用正向/逆向行走。）

记录路径时的一个有用的触发：
#action {哎哟，你一头撞在墙上，才发现这个方向没有出路。} {#path del}

当当当～下面举一个具体的例子：
比如你想要弄一本飞沙走石十三式，那么你可以在扬州中央广场输入#path new，然后去找田伯光，办完事回来的时候只要输入#path save backward tmp;$tmp就行了。当然，其实这点路自己走回来也比输入这么一串命令要快，但是……好吧，这只是个例子。

Action

语法：#action {触发语句} {命令} {优先级}

#action命令可以对mud服务器发来的特定信息作出回应，并执行一条或多条命令。在触发语句和命令中可以使用%1~99这样的变量，用于替代指定的内容。“优先级”参数是可选的，它决定了这个触发语句生效的优先权，默认值为5。

颜色触发语句以“~”号开头，你可以用#config {convert meta} on命令打开颜色代码显示，以便于制作颜色触发。

TinTin++用“^”号匹配行首触发，“$”匹配行尾触发。

以下内容适用于正则表达式。

在触发语句中使用%1、%2……%99可以实现模糊匹配，模糊匹配的内容将被存入变量，并在触发命令中相应地通过%1、%2……%99进行调用。%0比较特殊，它包含所有的匹配内容。除非你在触发语句中直接使用了%0，在这种情况下，%0就与%1一样了。

Using { } will embed a Perl CompatibleRegular Expression, available at the next available numeric variable, startingout at %1.
运用{ }可以在匹配语句中使用一个与Perl语言兼容的正则表达式，并通过%1这样的变量来调用。

[ ] . + | ( ) ? * are treated as normaltext unlessed used within braces. Keep in mind that { } is replaced with ( ).
在触发语句中，[ ] . +| ( ) ? * 这些符号通常被当作普通文本处理，但在{ }内出现时除外。同时需要注意的是，此时将{ }被( )代替。
（译注：以上关于正则表达式的内容本人没有仔细研究过，也未曾实际使用，不能保证翻译的准确性，因此附上原文供参考）

下面是一些常用的通配符：

```
%w 匹配0到任意个字母。
%W 匹配0到任意个非字母。
%d 匹配0到任意个数字。
%D 匹配0到任意个非数字。
%s 匹配0到任意个空格。
%S 匹配0到任意个非空格。
```

```
%? 匹配0或1个字符。
%. 匹配1个字符。
%+ 匹配1到任意个字符。
%* 匹配0到任意个字符。
```

```
%i 匹配时不区分大小写。
%I 匹配时区分大小写（默认）。
```

例子：#action {%1(%2)告诉你：%3} {tell %2 我是机器人，啦啦啦～}

在使用%d、%*这种不带数字的变量进行触发配置时（译注：相对于%1、%2这样的），引用的时候需要按照其出现的顺序，在上一个数字形式的变量基础上+1。（译注：这段比较绕，对照下面的具体例子会更加清楚一些）

例子：#action {%*(%w)告诉你：%*} {tell %2 目前afk中;say %2 告诉我 %3}
例子：#action {%3(%4)告诉你：%*} {tell %4 目前afk中;say %4 告诉我 %5}

对于一些采用常规方式难以匹配的语句，可以利用“~”号来制作一个颜色触发。输入#configconvert on可以查看mud输出的颜色代码。

例子：#action {~^\e[1;37m%1} {#showme {这是以白色粗体显示的文字：%1}}

触发对#showme命令显示的内容有效。

注：#unaction命令可以删除触发。

如果要删除一个以%*为内容的触发，你需要使用#unaction {*}命令。然而，#action {%*} {command}这样的触发是比较危险的，更好的方法是将这个触发放到一个类里，当你不再需要它的时候，就删除这个类。通过这种方式，你可以避免在使用#unact {%*}时误删所有的触发。

==== Alias ====

语法：#alias {别名名称} {命令}

#alias命令主要用于缩写一些比较长的指令或者是常用的指令。变量%1~99%可以用来引用别名的参数，分别代表别名命令后的第1个至第99个参数。

%0可以用来引用所有的参数，如果别名的命令部分只有一个单词，变量会自动添加到命令之后。

例子：#alias {k} {kill %1;exert yihun}
输入 k pantu 就会对慕容叛徒叫杀并运用九阴神功的移魂大法busy对手。

你可以在别名的名称部分使用变量以制作一些更加复杂的别名，在这种情况下变量的使用方式也会有所变化。

例子：#alias {k%1 with %2} {unwield all;wield %2;kill %1;perform hammer.wushuai}
使用上面这个别名时你就需要输入 k robber with hammer 这样的命令。

如果你想要一个能匹配所有输入内容的别名，你可以将别名的名称定义为%*。

例子：#alias {%*} {#showme 你输入的内容是：%0}
注：你可以使用#unalias命令删除别名。

如果要删除一个以%*为名称的别名，你需要使用#unalias {*}命令。然而，更好的方法是将这个别名放到一个类里，当你不再需要它的时候，就删除这个类。通过这种方式，你可以避免在使用#unalias {%*}时误删所有的别名。

All

语法：#all {命令}

如果打开了多个session，你可以使用#all将一条命令同时发送到所有的session中。

例子：#all quit ——关机了，洗洗睡了。

Bell

语法：#bell

这个命令的作用就是让你的电脑响铃一声。但这个命令已经过时了，最好避免使用，作为替代，你可以用#show {\a}命令向系统发出一个响铃控制符。

例子：#action {【江湖传闻】江湖又暂时恢复了表面的宁静} {#showme {\a}}
当你不能保证每时每刻都面对屏幕，但又不想错过系统更新的时候，这个命令就很有用了。如果觉得系统铃声太过单调，你也可以用#system命令来播放一段合适的音乐。

在一些终端里你可以使用VT100操作系统的命令来改变终端程序的标题行名称，这也是一种可视化的提醒方法。

例子：
#action {【江湖传闻】江湖又暂时恢复了表面的宁静}
{

```
#showme {\e]1;更新啦～\e\\};
#delay 10 #showme {\e]1;TinTin++ MUD client\e\\};
```

};
（译注：以上例子未进行测试）

Break

语法：#break

#break命令用于跳出#foreach、#loop、#parse、#switch，以及#while这些命令的循环进程。当执行#bradk命令时，TinTin++会直接跳到上述这些循环命令的后一条指令并执行下去。

例子：
#math cnt 0;
#while {1}
{

```
#math cnt $cnt+1;
#if {$cnt==2} {#break};
```

};

Buffer

语法：#buffer {home|up|down|end|find|get|lock|write|info}

#buffer命令可以通过不同的参数对缓冲区的显示内容进行操作。

#buffer {home}

移动到缓冲区的开始处并显示页面内容，同时锁定滚动条，推荐在宏键中使用。

#buffer {up}

将缓冲区上翻一页并显示页面内容，同时锁定滚动条，推荐在宏键中使用。

#buffer {down}

将缓冲区下翻一页并显示页面内容，同时锁定滚动条，推荐在宏键中使用。

#buffer {end}

移动到缓冲区的结尾处并显示页面内容，同时解除滚动条锁定，推荐在宏键中使用。

#buffer {find} {[序号]} {<内容>}

在缓冲区里查找指定的内容，<内容>可以使用正则表达式，[序号]是可选项，表示查找第几个指定的对象。

#buffer {get} {<变量名>} {<下界>} {[上界]}

将缓冲区的一行或多行内容（包括颜色代码）保存到一个变量中，下界与上界必须在1到缓冲区的总行数之间。如果省略上界，那么指定行的内容将被保存到一个标准变量中。如果给定上界，那么上下界之间的内容将被逐行保存到一个list变量中。

#buffer {lock}

锁定滚动条或解除锁定。当滚动条被锁定时，新的mud信息不会被显示。输入任意命令将解除锁定状态，当然，有一些缓冲区操作指令会重新锁定滚动条。当解除锁定后，窗口会移动到缓冲区的底部并显示相应的页面。

#buffer {write} {<文件名>}

将缓冲区的内容写入指定的文件。

#buffer {info}

显示内存占用等缓冲区信息。

例子：#macro {(press ctrl-v)(press F1)} {#buffer end}
将F1键设置为滚动到缓冲区底部。

例子：
#alias {colorsearch}
{

```
#var found null;
#loop 2 20 loop
{
#buffer get name $loop;
#if {"$name" == "\e[1;33m%*"}
{
#var found &1;
#break;
}
}
```

}
上面这个例子会创建一个叫colorsearch的别名，当你输入colorsearch时，TinTin++会在屏幕缓冲区的最近20行内容中查找以黄色粗体显示的文字，并保存到found变量中。

Case

语法：#case {条件} {指令}

#case命令只能用在#switch命令的内部，当#case命令中的条件与#switch的一致时，#case命令中的指令部分将被执行。

例子：#switch {1d4} {#case 1 hihi;#case 2 hehe;#default grin}

Chat

（译注：本章和下一章的“MudMaster Chat协议”仅供参考，由于较少用到这两章的命令，对该部分的内容未作核实，部分译文可能不够准确与规范）

语法：#chat {命令} {参数}

#chat命令可以与其他mud客户端建立点对点的连接，通常用于聊天或传输文件。这是一个分散化的聊天系统，这意味着你必须与其他用户交换ip地址和端口号以建立连接。

#chat {initialize} {端口号}

#chat initialize命令将创建一个聊天服务器，端口号是可选的，默认为4050。在创建聊天服务之后，其他人就能通过你的ip地址和端口号连接到你的服务器，你也就与他们建立了连接。

#chat {name} {你的名字}

默认情况下你的名字是TinTin，但大部分服务器会限制同名连接，因此在建立连接前你要做的第一件事是更改你的名字。名字中可以包括颜色代码，但有一些名字是不被TinTin++的聊天服务器接受的，比如“all”或者长度超过20个字符的名字。

#chat {call} {ip地址} {端口号}

#chat call命令用于连接到一个TinTin++聊天服务器，如果你省略端口号，默认的4050端口将被采用。

#chat {color} {颜色}

默认的聊天颜色是红色粗体，你可以用#chat color命令来进行调整。比如：#chat color bold yellow——调整为黄色粗体。或者你也可以使用支持256色的颜色代码，比如：#chatcolor <cde>。

#chat {message} {用户|all} {内容}

这是聊天中使用的主要命令，如果你使用了#chat message all，那么这条消息会被作为广播，发送到所有与你连接的对象。

#chat {emote} {用户|all} {内容}

这个命令的作用与#chatmessage基本一致，只是它会把你的名字加入到发送的消息中。

#chat {paste} {用户|all} {内容}

这个命令用于在消息后添加新的内容，但要注意，大部分mud客户端都不会正确接受超过40行的信息。

#chat {reply} {内容}

#chat reply用于回复上一个给你发消息的人。

#chat {send} {用户|all}

这个命令将向别人发送一个原始的数据串，你需要了解Mud Master Chat协议来使用它。

#chat dnd

DND表示“不要打扰我”（Do Not Disturb），这个命令用于切换DND状态，当处于DND状态时，将自动拒绝所有新的连接请求。

#chat {ip} {地址}

当你没有默认的ip时，这个命令用于设置你的ip地址，在你连接到另一个mud客户端时，这个地址会被发送给对方。TinTin++通常忽略报送的ip地址，直接采用实际地址，但其他mud客户端可能会需要这一报送信息。

#chat {who}

#chat who命令显示所有与你建立连接的人。第一栏为连接号，在给别人发送消息的时候，你可以用这个号码代替他的名字；第二栏为对方的名字；第三栏是标记，可以为P（私人private）、I（忽略ignore）、S（服务serve）、F（转发给forward to）、f（转发自forwardfrom）；之后各栏分别为ip地址、端口号、mud客户端名称。

#chat {info}

这个命令显示你的名字、ip地址、端口号、下载目录、回复（replay）对象，以及DND状态。

#chat {ignore} {用户}

这个命令将忽略一个用户，使你不再收到他的消息，而且对方并不会察觉到这一点。

#chat {private} {用户|all}

这个命令将对指定的用户禁用peek和request命令。

#chat {public} {用户|all}

这个命令是private命令的逆操作，允许指定的用户进行peek和request操作，新建的连接默认是公开（public）的。

#chat {peek} {用户}

这个命令显示指定用户的公开连接。

#chat {request} {用户}

这个命令将获取指定用户的公开连接，并自动与他们建立连接。

#chat {ping} {用户}

这个命令显示你与指定用户之间的连接速度，ping的时间以毫秒为单位。

#chat {zap} {用户|all}

这个命令将关闭指定的连接。

#chat {forward} {用户}

这个命令将把所有消息转发给指定用户。为避免陷入循环，当该用户正在向你转发消息时，转发功能会被自动关闭。

#chat {forwardall} {用户}

这个命令将把屏幕缓冲区里的所有内容转发给指定用户。

#chat {serve} {用户}

这个命令将把所有的公开消息转发给指定用户，并将该用户发给你的所有公开消息转发给其他与你建立连接的用户。为避免陷入循环，以上消息都作为私人消息转发。

#chat {group} {用户} {组名}

这个命令将指定的用户归为一组，你可以在emote、message、send命令中使用组名。不带参数的#chat group命令将显示所有的用户和他们所属的组名，与#chat who类似。

#chat {sendfile} {用户} {文件名}

这个命令用于向指定用户发送一个文件，在对方接受后文件将被传送。

#chat {accept} {用户}

接受对方发来的文件。

#chat {decline} {用户}

拒绝对方发送的文件。

#chat {cancel} {用户}

取消正在传送的文件。

#chat {filestat} {用户}

显示正在传送的文件的相关信息。

#chat {downloaddir} {目录}

这个命令用于设置下载文件的存放目录。

Mud Master Chat Protocol（MudMaster Chat协议）

建立一个连接

呼叫方：

每次新建一个连接的时候，呼叫方发送一条形如“CHAT:<chat name>\n<ip address><port>”的连接字串，字串的格式为：“CHAT:%s\n%s%-5u”。端口号必须是5个字符，位数不足的在右侧添加空格。字串发送后将会等待对方的回复，如果回复为“NO”，呼叫将被取消，如果接收到形如“YES:<chat name>\n”的回复，表示呼叫已被接受。

接收方：

检测到呼叫的时候，TinTin++会等待呼叫方发出一个以“CHAT:”开始的字串，回复“NO”字串将拒绝呼叫，回复“YES:<chat name>\n”字串接受呼叫。

Chat数据包

Chat数据包是形如“<COMMAND BYTE><data><END OF COMMAND>”的字串。所有的数据都需要遵循这一格式，但有两个例外：一是在连接过程中不需要使用数据包；二是在传输文件时数据包是定长的，因此不需要<END OF COMMAND>标识。

<COMMAND BYTE>数值对照表：

CHAT_NAME_CHANGE                      1
CHAT_REQUEST_CONNECTIONS              2
CHAT_CONNECTION_LIST                  3
CHAT_TEXT_EVERYBODY                   4
CHAT_TEXT_PERSONAL                    5
CHAT_TEXT_GROUP                       6
CHAT_MESSAGE                          7
CHAT_DO_NOT_DISTURB                   8

CHAT_VERSION                         19
CHAT_FILE_START                      20
CHAT_FILE_DENY                       21
CHAT_FILE_BLOCK_REQUEST              22
CHAT_FILE_BLOCK                      23
CHAT_FILE_END                        24
CHAT_FILE_CANCEL                     25
CHAT_PING_REQUEST                    26
CHAT_PING_RESPONSE                   27
CHAT_PEEK_CONNECTIONS                28
CHAT_PEEK_LIST                       29
CHAT_SNOOP_START                     30
CHAT_SNOOP_DATA                      31

CHAT_END_OF_COMMAND                 255

<CHAT_NAME_CHANGE><新的名字><CHAT_END_OF_COMMAND>

当一个用户改变他的名字的时候，新的名字将被广播给所有连接的用户。

<CHAT_REQUEST_CONNECTIONS><CHAT_END_OF_COMMAND>

从一个用户处获取所有的公开连接，并与他们建立连接。

<CHAT_CONNECTION_LIST><地址>,<端口号>,<地址>,<端口号><CHAT_END_OF_COMMAND>

接收方需要将所有公开连接的ip地址与端口号用逗号分隔，作为一个连接列表发送回去。

<CHAT_TEXT_EVERYBODY><消息内容><CHAT_END_OF_COMMAND>

用于将消息内容发送给所有人，所有显示的内容都需要由发送方生成，包括换行和“<chat name> chats to everybody”字串。

接收方：

如果你没有忽略一个连接，这个字串将被直接显示出来。如果你有部分连接是标记为“服务”的，你将把这个字串广播给这些连接。同时，如果这个字串来自一个被标记为“服务”的连接，你将把这条字串广播给所有的其他连接。这使得那些无法与每个人直接建立连接的人，可以通过第三方服务实现这一目的。

<CHAT_TEXT_PERSONAL><发送的消息><CHAT_END_OF_COMMAND>

这与CHAT_TEXT_EVERYBODY字串的功能基本一致。当然接收方会从这个字串了解到，这是一条私人消息，从而不会被广播给其他人。

接收方：

如果没有被忽略的话，仅仅是把这条消息显示出来。

<CHAT_TEXT_GROUP><组名><发送的消息><CHAT_END_OF_COMMAND>

用于将消息发送给特定的组，基本功能与其他发送命令一致。组名是一个15字符的字串，如果长度不足的话，需要在右侧加足空格。

接收方：

如果没有被忽略的话，仅仅是把这条消息显示出来。

<CHAT_MESSAGE><消息><CHAT_END_OF_COMMAND>

用于将消息发送到一个连接。这个字串应当被用于系统消息，比如接受或拒绝一个连接请求，将一个连接标记为公开或私人的。为了让你的接收方知道一条消息是系统消息，采用下面这样的格式将是一个比较好的办法：“\n<CHAT> %s has refused your connection because your name istoo long.\n”

接收方：

仅仅显示这条消息。

<CHAT_VERSION><版本信息><CHAT_END_OF_COMMAND>

这用于发送你的mud客户端的名称与版本号。

<CHAT_FILE_START><文件名,文件长度><CHAT_END_OF_COMMAND>

这条字串发送后将开始传送文件。文件名不能是一个目录，文件长度以字节为单位。

接收方：

首先会确认是否允许这个连接向你发送文件，并检查文件名与文件长度的合法性。如果信息不正确或你不想接受这个文件，你需要返回CHAT_FILE_DENY以停止传输。如果希望继续传输，你需要返回CHAT_FILE_BLOCK_REQUEST来请求相应的数据包。

<CHAT_FILE_DENY><消息><CHAT_END_OF_COMMAND>

当你接收到CHAT_FILE_START消息后想中止传输时，你可以使用这条字串。<消息>为拒绝传输的原因，比如，当被传输文件已存在时，你可以回复：“File already exists.”

接收方：

显示拒绝消息，并关闭所有已打开并准备传输的文件。

<CHAT_FILE_BLOCK_REQUEST><CHAT_END_OF_COMMAND>

在文件传输时用于请求下一个数据包。

接收方：

需要创建一个用于发送的数据包。数据包是定长的，因此你不需要指定字节数。如果已到达文件尾部，你需要发送CHAT_FILE_END字串，以关闭文件并通知对方传输完毕。

<CHAT_FILE_BLOCK><数据包>

一个数据包的长度是500字节，这个长度是固定的，因此不需要添加CHAT_END_OF_COMMAND。

接收方：

接收方需要始终关注接收到的每一个字节，以正确写入数据包，并预计什么时候将达到文件的尾部，此时数据包的长度将小于500字节。文件传输是由接收方驱动的，因此每完成一个数据包的接收，你都需要返回一个CHAT_FILE_BLOCK_REQUEST字串，以请求下一个数据包。

<CHAT_FILE_END><CHAT_END_OF_COMMAND>

关闭文件完成传输。TinTin++不需要用到这个字串，因为TinTin++将自动跟踪文件传输进程。

<CHAT_FILE_CANCEL><CHAT_END_OF_COMMAND>

文件传输的双方都可以发出这个字串来中止传输。

<CHAT_PING_REQUEST><时序数据><CHAT_END_OF_COMMAND>

时序数据取决于ping的请求方，TinTin++发送的是64比特的时戳。

<CHAT_PING_RESPONSE><时序数据><CHAT_END_OF_COMMAND>

当接收到一个CHAT_PING_REQUEST字串后，你应当返回一个时序数据。

<CHAT_PEEK_CONNECTIONS><CHAT_END_OF_COMMAND>

发送方请求提供所有的公开连接的情况。

<CHAT_PEEK_LIST><ip地址>~<端口号>~<名字>~<CHAT_END_OF_COMMAND>

接收方需要将所有公开连接的ip地址，端口号，名称以“~”号隔开，作为一个列表发送回去。

<CHAT_SNOOP_START><CHAT_END_OF_COMMAND>

发送方请求启动或停止观察一个连接的信息，接收方可以决定是否允许对方进行观察。

<CHAT_SNOOP_DATA><消息><CHAT_END_OF_COMMAND>

这条字串由一个处于观察或转发状态的mud客户端发出，<消息>将被接收方显示出来，但不会再次转发，以防止陷入循环。

Class

语法：#class {类名} {open|close|read 文件名|write 文件名|kill}

#class {<类名>} {open}

{open}选项将打开一个类并自动关闭上一个打开的类（如果有的话），在此之后新建的所有触发、别名、变量等都会被标记为这个类，直到这个类被关闭。

#class {<类名>} {close}

{close}选项会关闭当前打开的类。

#class {<类名>} {read} {<文件名>}

{read}选项会打开一个类，读入指定的文件，最后关闭这个类。（译注：即把命令文件中的触发、别名、变量等都放到一个类里）

#class {<类名>} {write} {<文件名>}

{write}选项将把指定类中的所有触发（译注：也包括别名、变量等内容）写入文件。这个命令可以用来保存数据，比如你可以先把一个变量放进一个类，然后利用这条命令保存变量的内容。

#class {<类名>} {kill}

{kill}选项将删除一个类，包括属于这个类的所有触发。（译注：也包括别名、变量等）

ANSI Colors（ANSI颜色代码）

语法：<abc>其中a、b、c为参数

参数a：VT100代码

0 – 默认
1 – 亮色
2 – 暗色
4 – 下划线
5 – 闪烁
7 – 反色（前景色与背景色互换）
8 – 跳过
（译注：TinTin++并不支持文字闪烁显示，这里的代码5只是将背景色亮化以突出显示；代码8原文为skip，具体作用不详）

参数b：前景色
参数c：背景色

0 – 黑色       5 – 粉色
1 – 红色       6 – 青色
2 – 绿色       7 – 白色
3 – 黄色       8 – 跳过
4 – 蓝色       9 – 默认

Xterm 256色代码
对于支持xterm 256色的终端，可以用<aaa>到<fff>设置前景色，用<AAA>到<FFF>设置背景色。

对于支持灰度的终端，可以用<g00>到<g23>设置前景色，用<G00>到<G23>设置背景色。

例子：#showme <034>T<025>i<016>n<007>T<043>i<052>n<061>+<070>+<088>
试着在TinTin++中执行上面的命令并观察结果。

例子：#showme <fca> 橙色 <cfa>青绿 <caf>靛紫 <acf>天蓝 <fac>玫红
试着在TinTin++中执行上面的命令并观察结果，你的终端必须支持xterm 256色。

Commands

语法：#commands {命令缩写}

不带参数的#commands显示所有的命令，若指定命令缩写，将显示与之匹配的命令。
（译注：TinTin++自2.00.9版本开始支持不带参数的#commands命令；#commands {a}将显示所有以a开头的命令。）

命令语法

TinTin++的所有命令都以“#”号开始，除非你用#config命令自定义命令符号。如果你用#read命令读入一个命令文件，文件中的第一个符号将被定义为命令符号。TinTin++的命令都可以缩写。

命令分隔

你可以用“;”号分隔命令。如果要输出分号，你需要在分号前加上转义符“\”。位于行首的“\”号将忽略这一行中的所有特殊字符。#config {verbatim}{on}命令将忽略所有输入的特殊字符（在别名中的特殊字符除外）。

例子：smile;say 在下有礼了 \;)
这条命令将作一个smile表情，然后说：在下有礼了;)

Config

语法：#config {选项} {参数}

TinTin++启动的时候会生成一个设置文件，这些设置可以用#config命令修改。输入不带参数的#config将显示当前设置，这些设置可以用#write命令写入一个命令文件。

下列设置选项默认是不可见的：

#CONFIG {COLOR PATCH} {ON|OFF} 对部分mud锁定颜色代码以正常显示颜色，比如Achaea，默认关闭。

#config {CONVERT META} {ON|OFF} 打开/关闭显示颜色代码，默认关闭。

#config {DEBUG TELNET} {ON|OFF} 显示telnet协议信息，默认关闭。

#CONFIG {MCCP} {ON|OFF} 打开/关闭对MCCP（mud客户端压缩协议）的支持，默认打开。

#CONFIG {LOG LEVEL} {LOW|HIGH} 设置为low时，mud信息将在触发生效前显示，默认为high。

Continue

语法：#continue

#continue命令用于在#foreach、#loop、#parse、#switch、#while命令的循环中跳过一些命令。当执行#continue时，TinTin++直接跳到循环的尾部，并继续执行下去。

例子：#loop 1 10 cnt {#if {$cnt % 2==0} {#continue};say $cnt}

Cr

语法：#cr

#cr命令向mud发送一个回车，但这是一个过时的命令，应当尽可能避免使用。在某些情况下#cr命令依然有点用处，比如当你设置了以enter键来重复执行上一次命令而又想输入一个单纯的回车符时，你就可以使用#cr。另一种替代的办法是使用不带参数的#send命令，或者输入两个分号“;;”来插入一个回车。有一些mud会将多个回车输入当成一个来对待——比如DikuMUD这样的——这时最好的办法是使用#send { \n \n }（这里一共有三个回车）。

例子：#ticker {idle} {#cr} {300}
这条命令将每隔300稍（5分钟）向mud发送一个回车符，这样可以避免你在大多数mud中因发呆而掉线。

Cursor

语法：#cursor {选项}

输入不带选项的#cursor命令可以查看所有的选项，这个命令的主要功能是为输入行编辑操作设置宏键。

例子：#macro {\e\e[3~} {#cursor clear right}
当按下Alt+Del时，光标右侧的文字将被删除，这一功能的默认设置是^K。

Debug

语法：#debug {项目} {参数}

单独的#debug命令将显示所有支持的项目，不带参数的#debug {项目}将切换指定项目的debug状态，或者你也可以指定参数的内容，包括ON、OFF，以及LOG。

迄今为止，仍有部分debug项目尚未生效。

例子：#debug action on
当一个触发启动时，TinTin++将显示被执行的内容。

Default

语法：#default {命令}

#default命令只能用于#switch命令内。当所有#case的条件都不符合时，#default的命令将被执行。

例子：#switch {1d4} {#case 1 hihi;#case 2 hehe;#default grin}

Delay

语法：#delay {秒数} {命令}

语法：#delay {名称} {命令} {秒数}

#delay将一定时间后执行指定的命令，{秒数}支持精确到毫秒级别的浮点数。

#delay命令的工作方式因参数个数的不同而有所差异。当有三个参数时，#delay与#tick的语法相同，允许你对一个延时命名。如果你建立一个带名称的延时，而此时已存在一个同名的延时，那么之前的延时将被删除。使用一个带名称的延时也便于你用#undelay命令进行删除操作。

例子：#delay {840} {#showme 即将更新！}
这个命令将在840秒（14分钟）后提醒你系统即将更新，比如你可以在#act {【江湖传闻】江湖又暂时恢复了表面的宁静}这样的触发中使用。

例子：#delay {renew} {840} {#showme 即将更新！}
与上面的例子相同，只是这次指定了名称。

Echo

语法：#echo {信息格式} {参数}

语法：#echo 信息格式_行号 {参数}

#echo命令将按照符合#format标准的格式在屏幕上显示信息。与#showme不同，#echo显示的信息不会被触发。与#showme相同的是，你可以在{信息格式}后加上{行号}，用以指定显示的位置，这一点与#prompt是相同的。

你可以查看#format与#prompt的帮助文件以了解更多的信息。

例子：#echo {当前时间为：%t.} {%Y-%m-%d %H:%M:%S}

Else

语法：#else {命令}

#else需要在#if或者#elseif命令之后使用，并且只有当#if或#elseif条件判断为假时才被执行。

例子：#if {1d2 ==1} {smile};#else {grin}

Elseif

语法：#elseif {条件} {命令}

#elseif需要在#if或者#elseif命令之后使用，并且只有当之前的#if或#elseif条件判断为假，且自身条件为真时才被执行。

例子：#if {1d3 ==1} {smile};#elseif {1d2 == 1} {grin};#else {laugh}

End

语法：#end

退出TinTin++，你也可以按下^d。

Escape Codes（转义码）

TinTin++的转义符是反斜杠“\”，“\”可以与一些字符组成转义码。

\a   将发送响铃代码。
\b   将发送反斜杠。
\c   将发送一个Ctrl字符，\ca表示^a。
\e   将开始一个转义序列。
\n   将发送一个换行。
\r   将发送一个回车。
\t   将发送一个跳格。
\x   将发送一个十六进制的字符，比如\xFF。
\x7B将发送“{”字符。
\x7D将发送“}”字符。
\0   w将发送一个八进制的字符，比如 \077。

将发送一个单独的“\”号。

在使用#showme、#send或#line命令时，如果在行尾以“\”号结束，TinTin++在输出时将不会自动换行。

在别名中对参数进行转义，需要采用0、1、%%2这样的形式。

Event
（译注：目前本人尚不了解TinTin++中定义的相关事件何时生效，以及如何运用，本章仅尝试按照原文译出，未作相应的测试。其中IAC事件因本人缺少相应的专业知识而存在理解障碍，故附上原文对照，容日后再完善）

语法：#event {事件名} {命令}

#event命令将针对预先定义的事件创建一个触发，不带参数的#event将列出大部分事件及其简要描述，#event %*将显示所有已定义的事件。部分事件将设置参数。

DATE

在指定的日期触发。

DAY

在指定日或每日触发。

END OF PATH

每次使用#path命令行走到一个路径的末尾时都会触发此事件。

HOUR

在指定的小时或每小时触发。

IAC

This event triggers for all telnetnegotiation. Use #config {debug telnet} {on} to see the proper name of telnetevents as they happen. If you create a telnet event for a telnet negotiationthat is normally handled by the mud client, like IAC SB TTYPE, only the eventwill be executed; the automatic response will be blocked.
在进行telnet交互时触发。使用#config {debug telnet} {on}命令后，在telnet事件发生时你可以看到这些事件的正确名称。如果你创建的telnet事件触发针对的是一些正常情况下由mud客户端自动处理的事件——比如IAC SB TTYPE——那么客户端的正常处理机制将会失效，只有你定义的触发会被执行。

IAC SB MSDP

This event triggers on a MSDP (Mud ServerData Protocol) sub negotiation. The %0 argument contains the variable's name,the %1 argument contains the variable's value. If a variable is send as anarray a name/value event is generated for each index.
在telnet交互的MSDP（Mud Server Data Protocol）子过程中触发。参数%0保存变量名，参数%1保存变量的值。如果发送的参数是一个数组，那么数组中的每个数据都会生成一个“变量名/变量值”事件。

IAC SB MSSP

This event triggers on a MSSP (Mud ServerStatus Protocol) sub negotiation. The %0 argument contains the variable's name,the %1 argument contains the variable's value. If a variable is send as anarray a name/value event is generated for each index.
在telnet交互的MSSP（Mud Server Status Protocol）子过程中触发。参数%0保存变量名，参数%1保存变量的值。如果发送的参数是一个数组，那么数组中的每个数据都会生成一个“变量名/变量值”事件。

IAC SB NEW-ENVIRON

This event triggers on a NEW-ENVIRON subnegotiation. Depending on the negotiation type you'll have to append SEND, IS,or INFO to the event name, as shown when using #config {debug telnet} {on}. The%0 argument contains the variable's name, the %1 argument contains thevariable's value.
在telnet交互的NEW-ENVIRON子过程中触发。根据交互类型的不同你需要在事件名后添加SEND、IS或INFO，具体可以打开#config{debug telnet} {on}查看。参数%0保存变量名，参数%1保存变量的值。

IAC SB ZMP

This event triggers on a ZMP subnegotiation. Depending on the ZMP package you'll have to append the package tothe event name, as shown when using #config {debug telnet} {on}. The %0argument contains the ZMP package data.
在telnet交互的ZMP子过程中触发。根据ZMP包的不同你需要在事件名后添加相应的包，具体可以打开#config {debug telnet} {on}查看。参数%0保存ZMP数据包的内容。

IAC SB

This event triggers on any undefined subnegotiation. Some telnet options will be named, others will be a number, asshown when using #config {debug telnet} {on}. The %0 argument will contain thedata inside the sub negotiation.
在telnet交互的其他未定义子过程中触发。一些telnet选项可能被命名，另一些则是数字，具体可以打开#config {debugtelnet} {on}查看。参数%0保存这些子过程中的数据。

MAP ENTER MAP

当进入一张地图时触发。

MAP ENTER ROOM

在自动绘制地图时，每进入一个新的房间，此事件将被触发。参数%0存放房间的标号。

MAP EXIT MAP

离开地图时触发。

MAP EXIT ROOM

在自动绘制地图时，离开当前房间前，此事件将被触发。变量%0存放房间的标号。

MINUTE

在指定分钟或每分钟触发。

MONTH

在指定月或每月触发。

PROGRAM START

在TinTin++完成启动后触发。

PROGRAM TERMINATION

在TinTin++退出时触发。

RECEIVED INPUT

每次输入命令并被执行后触发。变量%0储存输入的内容。

RECEIVED LINE

当接收到从mud服务器发来的完整一行消息时触发，这个事件将在所有其他定义的触发（Action）前发生。变量%0储存消息内容，变量%1储存消息的原始形态（包括颜色代码）。

RECEIVED OUTPUT

当接收到新的输出内容时触发。

SCREEN RESIZE

当改变窗口尺寸时触发。

SECOND

在指定秒或每秒触发。

SEND OUTPUT

当一条命令被发送到mud服务器时触发。变量%0储存发送的内容。

SESSION ACTIVATED

当一个session被激活时触发。

SESSION CONNECTED

当一个session连接到服务器时触发。变量%0储存session名称，%1储存服务器名称，%2储存ip地址，%3储存端口号。

SESSION DEACTIVATED

当一个session进入后台时触发。

SESSION DISCONNECTED

当一个session从服务器断线后触发。变量%0储存session名称，%1储存服务器名称，%2储存ip地址，%3储存端口号。

TIME

在指定时间触发。

WEEK

在指定周或每周触发。

YEAR

在指定年或每年触发。

Forall

语法：#forall {列表} {命令}

{列表}中的元素必须用分号或花括号分隔。

例子：#forall {a;b;c;d} {say &0}
例子：#forall a_b_c_d {say &0}
上面两个例子都等价于：saya;say b;say c;say d

Foreach

语法：#foreach {列表} {变量} {命令}

#foreach命令相当于一个简单的循环，{列表}中的每个元素将被存入{变量}，并在{命令}中使用。

{列表}中的元素必须用分号或花括号分隔。

例子：#foreach {sword;blade;whip}{weapon} {identify $weapon}
例子：#foreach sword_blade_whip{weapon} {identify $weapon}
上面两个例子都等价于：identifysword;identify blade;identify whip

如果要用#foreach遍历一个list变量（或一个嵌套的变量），你需要使用$<list变量名>[%*]的形式。

例子：#foreach {$weapon_list[%*]} {weapon} {identify $weapon}

Format

语法：#format {变量} {格式} {参数1} {参数2}……{参数n}

#format命令用于对字串进行格式化，类似于C语言中的sprintf函数。格式化后的字串将被储存在指定的{变量}中，{格式}部分可以包括固定字串与参数变量，而在{参数}部分你最多可以使用20个参数。

参数          名称          描述
%+9s          字符串        长度为9的字符串，不足的在左侧加空格
%-9s          字符串           长度为9的字符串，不足的在右侧加空格
%.9s          字符串        长度最多为9的字符串
%a            数字          显示相应的ascii字符
%c            颜色          将描述转换为颜色代码，比如你可以用light red
%d            浮点数        显示取整后的数字
%h            页眉          将参数内容转化为页眉格式
%l            小写          将参数内容转化为小写
%m            运算          对参数进行数学运算
%n            姓名          将首字母大写
%p            字符串        去除字符串前后的空格
%r            逆序          将参数内容逆序显示
%s            字符串        正常显示字符串内容
%t            时戳          按照strftime函数的格式显示时间
%u            大写          将参数内容全部大写
%w            自动换行      将参数转换为list
（译注：从输出看是变成了list变量的形式，但不清楚具体用途，原文为wordwrap）
%C            列数          显示屏幕列宽
%G            千分位        以千分位形式显示数字
%L            长度          显示参数的长度
%R            行数          显示屏幕行高
%T            Epoch时间     显示从Epoch开始经过的秒数
%U            Epoch时间     显示从Epoch开始经过的毫秒数
（译注：Epoch指的是一个特定的时间：1970-01-0100:00:00）

例子：
#alias {time}
{

```
#format line {%c当前时间为：%t} {light green} {%Y年%m月%d日 %T};
#showme {$line}
```

}

Function

语法：#function {函数名} {命令}

#function命令将生成一个函数，你可以在函数内部执行一些命令，当函数执行完毕后，调用该函数的语句将得到一个值，这个值由$result变量决定。

由于#echo命令也会使用result变量，因此在一个函数内部使用#echo命令必须十分小心。你可以用@<函数名>{<参数>}这样的形式来调用一个函数，参数被保存在0%到99%的变量中以便在函数中引用，其中%0代表所有的参数，%1代表第1个参数，%2代表第2个，以此类推。参数需要用花括号或分号隔开。

例子：

#function {time}
{

```
#if {"%0" == ""}
{
#format {epoch} {%T}
};
#else
{
#var epoch %0
};
#format {result} {%t} {{%T}{$epoch}}
```

}
这个函数里的#if判断用于检查引用函数时是否设定了参数。如果有，参数将被保存在$epoch变量中；如果没有，#format {epoch} {%T}将把当前的epoch秒数（即从1970年开始至今的秒数）保存到$epoch中。然后$epoch的时间信息将被格式化后保存到$result中。输入#showme @time{}就会显示当前时间。

更多的例子可以浏览本站的script页面。

注：你可以使用#unfunction删除一个函数。

Gag

语法：#gag {内容}

#gag命令相当于#substitute {内容} {.}命令，并将指定的内容加入到替换清单中。被屏蔽的内容将不再被显示。

更多的信息可以查看关于Action的帮助文档。

例子：#gag {%iAlucar}
如果你觉得Alucar这个家伙太话唠了，就可以用这个命令来个眼不见为净。起始处的%i表示不区分大小写，因此不管是Alucar还是ALUCAR都不会再出现在你眼前了。

注：你可以用#ungag命令删除屏蔽。

Greeting

语法：#help greeting

仅仅显示你每次打开TinTin++时的欢迎界面（其中包含版本信息），只有你想看它的时候才有用，而且不计入屏幕缓存。

这其实并不是一个命令，因为你只能通过#help命令来使用它。

Grep

语法：#grep {页数} {关键词}

这个命令将在屏幕缓冲区内查询指定的关键词，并以屏为单位显示包括关键词的行。其中{页数}是可选的，表示显示第几屏查询结果（默认为显示第一屏），这在符合条件的内容较多的时候比较有用。你可以用正则表达式来作为关键词，以获得更好的查询结果。此外，关键词是区分大小写的。

例子：#grep 告诉你
这个命令将把所有别人tell你的内容显示出来。

Help

语法：#help {主题}

#help命令将根据帮助文件的内容显示某个主题的基本帮助信息，不带参数的#help显示所有的帮助主题。

#help命令的内容一般比在线帮助手册更加新一些。

例子：#help alias
显示别名（Alias）的帮助信息。

例子：#help %*
显示所有帮助文件。

Highlight

语法：#highlight{内容} {颜色}

#highlight命令将把指定的内容加入到高亮显示列表，当服务器发来的信息与之匹配时，将以指定的颜色显示。

有关正则表达式的内容可以查看#action命令的帮助，变量%0不应在{内容}中使用。

支持的颜色代码包括：reset、light、faint、underscore、blink、reverse、dim、black、red、green、yellow、blue、magenta、cyan、white、b black、b red、b green、b yellow、b blue、b magenta、b cyan、b white。你也可以使用TinTin++的256色颜色代码。

例子：#highlight {^{你}} {lightcyan}
这条命令将把所有包括“你”的行标为青色粗体，当你在战斗中遇到刷屏的时候，这会有点用处。

例子：#highlight {%*告诉你：%*} {<ace>}
注：你可以使用#unhighlight命令删除高亮。

History

语法：#history {命令} {参数}

#history命令与默认为“!”号的重复字符配合使用。历史命令是一个由所有手工输入过的命令组成的列表，在默认情况下每个session的历史命令包括最近输入的1000条命令，这可以用#config命令进行更改。

#history {delete}

将删除历史命令中的最后一条命令。

#history {insert} {命令}

将把指定的{命令}插入到历史命令的最后。

#history {list}

将显示所有的历史命令。

#history {read} {文件名}

将读入事先保存过的历史命令记录。如果与#event命令配合，可以在打开一个session的时候自动读取。

#history {write} {文件名}

将把历史命令写入一个文件。如果与#event命令配合，可以在关闭一个session的时候自动写入。

If

语法：#if {条件} {true} {false}

{条件}是一个c语言风格的运算式或一个正则表达式。字符串必须加引号。当{条件}的结果为任意非零值时，{true}部分的命令将被执行；当结果为零时，{false}部分的命令被执行。

更多信息可以查询Mathexp（数学表达式）与Regexp（正则表达式）。

例子：#act {%1(%2)告诉你} {#if {“%2”==“icer”} {tell %2 我不是机器人。} {tell%2 我是机器人。}}

Ignore

语法：#ignore {项目} {参数}

不带任何参数的#ignore命令显示所有可选的项目列表，#ignore {项目}将切换指定项目的生效状态，你也可以具体指定{参数}为ON或OFF。

例子：#ignore actions off
令所有触发都暂时失效。

Info

语法：#info

#info命令显示触发、别名、变量等等的基本信息，包括数量、是否生效（#ignore）、是否反馈执行信息（#message、#debug）。

Keypad（小键盘布局）

TinTin++启动时会向终端发送“\e=”以打开终端设备的小键盘模式，你可以用#showme {\e>}关闭该模式。

```
布局 A                      布局 B                      布局 C
+-----+-----+-----+-----+   +-----+-----+-----+-----+   +-----+-----+-----+-----+
|Num  |/    |*    |-    |   |Num  |/    |*    |-    |   |Num  |nkp/ |nkp* |nkp- |
+-----+-----+-----+-----+   +-----+-----+-----+-----+   +-----+-----+-----+-----+
|7    |8    |9    |     |   |Home |Up   |PgUp |     |   |nkp7 |nkp8 |nkp9 |     |
+-----+-----+-----+     |   +-----+-----+-----+     |   +-----+-----+-----+     |
|4    |5    |6    |+    |   |Left |Centr|Right|+    |   |nkp4 |nkp5 |nkp6 |nkp+ |
+-----+-----+-----+-----+   +-----+-----+-----+-----+   +-----+-----+-----+-----+
|1    |2    |3    |     |   |End  |Down |PgDn |     |   |nkp1 |nkp2 |nkp3 |     |
+-----+-----+-----+     |   +-----+-----+-----+     |   +-----+-----+-----+     |
|0          |.    |Enter|   |Ins        |Del  |Enter|   |nkp0       |nkp. |nkpEn|
+-----------+-----+-----+   +-----------+-----+-----+   +-----------+-----+-----+
```

在小键盘模式关闭状态下，锁定numlock将采用布局A，解锁numlock将采用布局B。打开小键盘模式将采用布局C。

支持小键盘模式的终端：

Linux Console, PuTTY, Eterm, aterm.

不支持小键盘模式的终端：

RXVT on Cygwin, Windows Console, GnomeTerminal, Konsole.

特殊终端：

RXVT需要解锁numlock才能启用布局C。

Xterm可能需要禁用Alt/NumLock Modifiers (num-lock)，你可以在Ctrl+鼠标左键的菜单中找到它。或者你也可以修改~/.Xresources并添加XTerm*VT100.numLock:false。

Mac OS X终端需要在菜单中打开“strict vt100 keypad behavior”，你可以在菜单栏的Terminal → Window Settings → Emulation中找到它。

Kill

语法：#kill {类别} {参数}

#kill命令将删除包括别名、触发、变量、定时等在内的各种自定义的东西，甚至包括路径与最基本的config设置。当你想要从头开始的时候这个命令是很有用的。

给定{类别}的#kill将删除指定类别的内容，比如：#killalias将删除所有的别名。

你也可以同时指定{类别}与{参数}，此时只有对应的内容会被删除。，比如：#kill {alias} {%*bla%*}

Line

语法：#line {选项} {参数}

#line命令提供了多种基于行的操作。

#line {gag}

这条命令将屏蔽下一行显示内容。当触发被设定为在被触发语句显示前执行时，将#ling {gag}放在触发命令中可以使触发语句不再显示出来。

#line {log} {<文件名>} {[文本]}

#line {log}将把指定的文本内容存入文件。如果没有给出{文本}参数，下一行显示内容将被存入文件。在{文本}中使用的TinTin++颜色代码将被自动转换为ANSI颜色码。依据#config{LOG}的设置，log文件的格式为HTML、RAW或PLAIN。

#line {logverbatim} {<文件名>} {[文本]}

#line {logverbatim}与#line {log}十分类似，唯一的区别是{文本}中的颜色代码、变量、函数等不会被替换为相应的值。

例子：

#var ignore_list bubba_1_pamela_1;

#act {%1(%2)告诉你：%3}
{

```
#if {&ignore_list[%2]}
{
#line gag
}
{
#line logverbatim tells.log
}
```

}
上面的例子将把所有tell你的消息存入tells.log文件，除非tell你的人位于ignore_list中，而且被忽略的tell消息将被屏蔽。

List

语法：#list {<变量>} {<选项>} {<参数>}

TinTin++中的list变量是一个与序号相关联的数组，#list命令通过自动编号使得对数组的操作更加方便，比如在插入或删除一个数组元素的时候。

当#list命令中的序号是一个在1到list元素总数之间的数，你也可以使用一个负数，此时-1代表list中的最后一个元素，-2代表倒数第2个元素，以此类推。

你可以使用序号来直接显示list中的某个元素，比如$var[1]、$var[2]、$var[-1]等。

如果要遍历list中的所有元素，你可以在#foreach命令中使用$<list>[%*]作为参数。

#list {<list变量>} {add} {<参数1>} {<参数2>} {…}

#lise {add}将把{参数}作为元素添加到{list变量}中。

#list {<list变量>} {clear}

#list {clear}将清空指定的list变量，这个命令相当于#variable{<变量名>} {}

#list {<list变量>} {create} {<参数1>} {<参数2>} {…}

#list {create}将创建一个list变量，并以给定的{参数}作为元素，如果同名的list变量已经存在，该变量将被覆盖。

#list {<list变量>} {delete} {<序号>} {[数量]}

#list {delete}将删除list变量中指定序号的元素，{数量}参数是可选的，表示删除的元素个数，默认只删除一个元素。

#list {<list变量>} {find} {<参数>} {<变量>}

#list {find}用于在list变量中寻找与{参数}内容相匹配的元素，并将该元素的序号保存在{变量}中，如果没有找到，{变量}将赋值0。

#list {<list变量>} {get} {<序号>} {<变量>}

#list {get}用于取出list变量中指定序号的元素并保存在{变量}中，如果给出的{序号}不存在，{变量}将赋值0。你也可以使用$list[<序号>]这样的形式直接从对应的数组中取出指定元素。

#list {<list变量>} {insert} {<序号>} {<参数>}

#list {insert}用于将一个元素插入到list变量的指定位置，如果{序号}为一个正数，插入的元素将位于序号位置，如果{序号}为负数，插入的元素将位于逆序的位置。比如序号-1将把新的元素添加到list变量的最后，序号1将把新的元素添加到list变量的开始。

#list {<list变量>} {set} {<序号>} {<参数>}

#list {set}将改变位于{序号}位置的元素的值，你也可以用#variable {<list变量>[序号]} {内容}这样的命令直接对数组进行操作。

#list {<list变量>} {size} {<变量>}

#list {size}用于获取list变量中元素的总数并保存到指定的变量中。你也可以使用&list[]来直接获得相应的数组的大小。

#list {<list变量>} {sort} {<参数>}

#list {sort}用于将指定内容插入到list变量中，插入的位置由字母顺序决定。（译注：本命令不会对list变量中已有的元素进行排序）

Log

语法：#log {模式} {文件名}

#log命令用于将屏幕缓冲区的内容存入指定文件，{模式}可以为o（overwrite覆盖）或a（append添加）。

通过#config命令你可以指定log文件的保存类别，共有三种，raw（会将转义码原封不动地保存下来）、plain（解释转义码的内容）和html（将转义码转换为html支持的格式）。

例子：#log o mylog.html
假设你已经在#config中设置了html的log文件格式（默认），这个例子将把所有显示内容保存到mylog.html文件中。

Loop

语法：#loop {下限} {上限} {变量} {命令}

#loop命令相当于c语言中循环命令的简化版。{下限}与{上限}必须使用数字。这个命令将按照下限与上限的大小对{变量}采取递增（或递减）方式循环执行{命令}，直到达到 {上限}的数字。{变量}可以在 {命令}部分使用。

例子：#loop 1 10 cnt {say $cnt}
这条命令相当于：say1;say 2;say 3 …say 9;say 10

Macro

Syntax: #macro {按键代码} {命令}

{按键代码}指某个按键被按下时发送到终端的代码，这个代码与操作系统和所采用的终端相关，你可以打开#config中的{CONVERT META}选项来查看按键的具体代码。

如果要为F1键建立一个宏键来执行exert recover命令，你可以输入以下命令：

输入：#macro {(按下F1键)} {exert recover} ——现在宏键F1已经可以使用了。

注：你可以用#unmacro命令删除一个宏键。

Map

语法：#map

#map命令用于自动绘制地图，支持大部分自动绘图功能。更为基本的路径功能请查询#path命令的帮助文件。

输入#map create<房间总数>命令即开始记录地图，同时生成第一个房间，<房间总数>为地图的容量。如果你没有指定<房间总数>，默认的容量是15000个房间。#map goto 1命令将使你进入地图并移动到地图的第一个房间。

你只需要简单地四处移动就可以向地图中添加房间。默认的移动指令包括n、ne、e、se、s、sw、w、nw、u、d，如果你玩的mud包括其他移动指令，你必须用#pathdir命令添加这些指令。

有三种显示地图的方法。一是#mapmap命令，这将显示一张由附近的房间组成的地图。二是用#split命令将屏幕分为三个区域，比如#split 10 1命令中的10就是最上方的窗口的行数，然后再用#map flag vtmap命令，就能在这个窗口显示地图，并在你移动的时候自动更新。三是用#event命令定义一个MAP ENTER ROOM事件，当这个事件发生时执行#map map 80×24 map.txt命令，这将把地图输出到map.txt文件，如果你在另一个终端中执行unix命令tail -fs 0.1 map.txt，你就能在那个终端中看到实时更新的地图。
（译注：第三种方法在unix下可以结合screen实现竖向分屏显示地图，wintin么就只能另求他法了。）

在不少mud里存在位置重叠的地区，甚至在同一个地区内存在位置重叠的房间。对于这种情况，你可以使用#map roomflag void命令制造一个空房间并转换为一种连接，以实现房间的扩展。被标记为void的空房间只能有2个出口，你可以使用#map insert <方向> void命令来插入一个空房间。

与大部分自动地图一样，你可以很容易地实现快速行走。假设你正处于扬州的中央广场（你的map的第一个房间），并用#map name ct命令将这个房间命名为ct，然后你走到曲阜的孔庙并将孔庙这个房间命名为km，再使用#map run ct命令就可以快速返回。当然你也可以使用别名等其他方式返回ct，此时你需要用#map goto ct命令告诉自动绘图程序你已经回到ct。

如果你特别喜欢欣赏vtmap模式下地图的自动更新过程，或者你只是急着想试一下效果，你可以使用#map run {km} 0.75命令来慢速行走到孔庙。

当你完成了上面这些比较困难的工作后，你可以用#map write <文件名>来保存你的地图，以便以后用#mapread <文件名>来读回。读回地图文件后，使用#map return命令可以让你返回到保存地图时你所处的房间。

你可以用#help map命令获得更多有关地图的操作选项及其简要说明。

Math

语法：#math {变量} {数学表达式}

关于运算符的信息可以查询下一节“数学表达式”。

#math命令用于进行数学运算并将运算结果存入给定的变量，#math也可以用于字符串与正则表达式的比较。

例子：#math sumvar {(1 + 1) * 10}
这个基本的运算指令将把计算结果（值为20）存入变量sumvar。

Mathexp（数学表达式）

Mathexp是数学表达式（mathematical expressions）的缩写，用于进行数学与逻辑运算。TinTin++在完整支持c语言运算符的基础上有一些新增的符号。下面是各种运算符的优先级列表：

运算符       优先级                描述
! ~ + -        00                  逻辑否、逐位否、加、减
d              01                  随机整数
% * /          02                  整数取模、乘、除
+ -            03                  整数加、减
«»           04                  逐位左移、右移
< >⇐ >=       05                  逻辑小于、大于、小于等于、大于等于
== !=          06                  逻辑等于、不等于
&              07                  逐位与

|  |
||
|  |

&&             10                  逻辑与

|  |
||
|  |

( )            13                  括号

Message

语法：#message {项目} {参数}

不带{项目}与{参数}的#message命令将显示所有可以进行切换的项目，如果只指定{项目}，将只切换指定项目的message状态。你也可以更加具体地在{参数}中指定ON或OFF。

例子：#message variable off
变量生成或删除时的提示信息将不再被显示。

Name（session名）

语法：#[session名] {命令}

当使用#session命令时你必须指定一个名称，这个名称可用于把相应的session置于前台，格式为#[session名]。如果加上{命令}参数，你可以在不激活那个session的情况下进行后台操作。

例子：#ses one address 23;#ses two address 23;#one;#two idle
上面的命令将创建两个session，后建的那一个（two）将在前台运行。执行#one后，“one”这个session被调到前台；执行#two idle，那么idle这个emote就会在“two”这个session中执行。

Nop

语法：#nop

Nop是“no operation”的综写，当你什么都不想做的时候可以用这条命令。

例子：#act {&} {#nop} {0}
一些mud允许用“&”号来分隔命令，同时也允许玩家在say和tell中使用这个字符。在这种情况下，一些喜欢恶作剧的玩家可能利用这一点来干扰你的触发，所以我们要加个保险。上面的例子使得包括“&”号的信息不会激活一些相对脆弱的触发，因为在同一时刻只有一个触发会启动。

你也可以用#nop在代码中添加注释，此时应当避免使用“{”和“}”号。
（译注：#nop用于注释一行内容时，不会在回车处停止，因此在注释行的最后需要加上分号，否则会将下一行内容一并注释掉。）

Parse

语法：#parse {字符串} {变量} {命令}

#parse命令类似一个简化的循环， {字符串}中的每个字符将被依次存入{变量}，并在 {命令}中使用。

例子：#parse {hello} {character} {say $character!}
上面的例子相当于：say h!;say e!;say l!;say l!;say o!

虽然通常来说#parse是一个比较无用的TinTin++命令，但它在某些情况下也可以有出色的表现，比如下面的例子就能将“.”号作为一个快速行走的快捷命令。
#alias {.%0}
{

```
#var cnt {};
#parse {%0} {char}
{
#if {"$char" >="0" && "$char" <= "9"}
{
#var cnt $cnt$char
};
#elseif {"$cnt" ==""}
{
#send $char
};
#else
{
#loop $cnt 0 cnt
{
#send $char
}
}
}
```

}

Path

语法：#path {del|end|ins|load|map|new|save|run|walk} {参数}

#path命令能够快速方便地记录你的移动路径，并自动建立一个命令列表以实现两地之间的快速往返。如果这还不能满足你，还有更加高端一的地图绘制的功能，具体请查询#map命令的帮助文件。

#path {new}

这条命令将进入路径记录模式，如果你进行了移动（仅针对#pathdir中的移动命令），这个移动命令将被添加到路径中。

#path {end}

当你用#path new开始记录路径后，你可以用#path end来终止记录。#path end不会删除当前记录的路径，但再次输入#path new就会消除记录。

#path {map}

这条命令用于显示到目前为止已经记录的路径。这里的路径只是一个命令清单，并不是图形化的地图。

#path {ins} {前进命令} {后退命令}

在行走的过程中，有时你需要做opendoor之类的动作，用这条命令你就能在记录路径的时候插入其他命令。由于在记录从A地到B地的路径时，从B地返回A地的路径也会同时生成，因此{后退命令}这个参数就用来指定逆向路径的命令。

例子：#path ins {open north} {};n;#path ins {} {open south}

#path {del}

删除路径中的最后一步。

例子：#action {哎哟，你一头撞在墙上，才发现这个方向没有出路。} {#path del}

#path {save} {forward|backward} {变量}

这条命令用于将记录的路径存入变量，你必须指定保存的是正向（forward）还是逆向（backward）路径，并可以使用f和b作为相应的缩写。在用#path save f AtoB保存了一条路径后，你就可以输入$AtoB来使用它。

例子：#path new;n;n;n;e;e;e;#path save backward return;$return

#path {load} {变量}

这条命令将把指定的变量作为路径进行读取，即使变量的内容与行走无关。

#path {run} {延时}

在使用这一命令前，你必须已经记录或读取了一条路径。一旦执行，路径中包含的指令将立即被依次执行并从路径中删除，如果你指定了{延时}，那么路径中的每个指令会依次间隔相应的时间后再执行。{延时}以秒为单位，并支持浮点数。

例子：#path run 0.5

#path {walk} {forward|backward}

在使用这一命令前，你必须已经记录或读取了一条路径。一旦执行，路径中的下一个指令将被执行并从路径中删除，如果已经达到路径的末尾，那么END OF PATH事件将被触发。

例子：#tick {slowwalk} {#walk f} {0.5};#event {END OF PATH} {#untick slowwalk}

Pathdir

语法：#pathdir {前进命令} {后退命令} {coord}

默认情况下TinTin++已经预设了大部分常用的移动指令，因此通常你并不需要用到#pathdir。#pathdir定义的方向主要用于#path和#map命令。

第一个参数是一个方向，第二个参数是相应的相反方向。比如n的反向就是s。

第三个参数是一个空间坐标值。在一般情况下，每个基本方向应当有一个唯一的值，这个值是2的次方（比如1、2、4、8、16、32、64等等）。但复合方向不同，它的值是所包含的基本方向的值的和，比如方向n的值是1，方向e是2，那么ne的值就是3（1+2）。这个值主要用于#map命令的相关功能。

例子：#pathdir {eu} {wd} {18}
注：你可以用#unpathdir删除定义的方向。

Prompt

语法：#prompt {信息} {提示信息} {行号}

这个命令与#substitute很象，但只能在分屏模式下使用。#prompt将替换mud发来的指定信息，如果你没有指定行号，提示信息将在你的分屏栏上显示。

{行号}参数是可选的，它用于在分隔后的屏幕中显示提示信息。正行号表示在屏幕底部向上第n行显示提示信息，负行号表示从屏幕顶部向下第n行显示提示信息。

关于正则表达式匹配的内容请查询 #action命令的帮助文件。

例子：#prompt {【 气血 】%s%1%s/%s%2%s[%d%]} {[<078>气血：%1/%2]}

注：你可以用#unprompt命令删除定义的提示内容。

Read

语法：#read {文件名}

这条命令用于读取一个命令文件。

例子：#read peiyao.tin
假如你已经为平一指配药任务写好了相关的别名、触发、定时器等等，并存放在peiyao.tin文件中，那么这条命令就能读取这些设置，开始自动配药。

Regexp（正则表达式）

语法：#regex {字符串} {正则表达式} {true} {false}

#regex命令（即正则表达式regular expression）用于将给定的字符串与正则表达式进行匹配性比较，通配的变量被保存在&1～&99中，&0代表整个匹配的字串。

以“^”号开头的信息代表一个行首匹配，以“$”号结尾的信息表示一个行尾匹配。

以下内容适用于正则表达式。

{ }内的内容是一个与Perl语言兼容的正则表达式，可用于%n形式的变量，n为上一个变量的序号+1。

```
[ ] . + | ( ) ? * 这些符号将被当作普通文本处理，但在{ }内出现时除外。同时需要注意的是，此时将{ }被( )代替。
```

以下通配符可用于%n形式的变量 ，n为上一个变量的序号+1。

```
%w 匹配0到任意个字母。
%W 匹配0到任意个非字母。
%d 匹配0到任意个数字。
%D 匹配0到任意个非数字。
%s 匹配0到任意个空格。
%S 匹配0到任意个非空格。
```

```
%? 匹配0或1个字符。
%. 匹配1个字符。
%+ 匹配1到任意个字符。
%* 匹配0到任意个字符。
```

```
%i 匹配时不区分大小写。
%I 匹配时区分大小写（默认）。
```

例子：#regex {Hello World} {%* World} {#showme Matched &1 World} {#showme no match :( }

Repeat

语法：#[数字] {命令}

有时你需要重复执行一个命令，那么这就是最好的办法。

例子：#10 eat jinchuang ao
这条命令将使你连续吃10次金创药。

Replace

语法：#replace {变量} {原字串} {新字串}

这个命令将在{变量}中查找{原字串}并用 {新字串}替换。

如果{新字串}为空，那么变量中符合{原字串}的内容将被删除。

例子：#var {test} {bli bla blo};#replace {test} {bl} {tr}
上面的例子将把变量test的内容从“bli bla blo”替换为“tri tra tro”。

Return

语法：#return {内容}

#return可以让你跳出一个正在执行的触发。

你也可以用#return {内容}跳出一个函数，并将result变量的值赋为指定的内容。

Run

语法：#run{session名} {shell命令}

#run命令用于运行一个unix shell命令，当shell命令结束后，相应的session也随之关闭。
（译注：unix专用，在wintin中就不要尝试了，不然会有不可预测的情况发生。）

你可以运行任何shell命令，甚至包括ssh、telnet、python、php、perl、ruby等等。

例子：#run myserver ssh myname@myserver.com
这个例子将建立一个ssh连接，并且支持所有的TinTin++脚本语言。

例子：#run python python;#act {^cmd %1} {%1};print “cmd #showme <118>Hello World!”
这个例子将启动一个python shell，建立一个触发来执行所有以“cmd”开头的本文，并以红色显示“Hello World!”。

注：你也可以使用#script和#system来执行shell命令。

Scan

语法：#scan {文件名}

#scan命令读取一个文件并把文件内容显示出来，它可以用于把ansi文件转换为html，也可以读取log文件。
（译注：使用#scan后需要按page up和page down刷新屏幕才能看到读入的内容。）

Script

语法：#script {变量} {shell命令}

#script命令让你可以在shell中执行命令。命令的输出内容将被以列表形式保存在变量中。这个命令可以用于执行Lua、PHP、Perl、Python、Tcl和Ruby脚本。

例子：#script {result} {lua -e 'print(“Hello TinTin++”)'
例子：#script {result} {ruby -e 'print “Hello TinTin++”'}
例子：#script {result} {python -c 'print “Hello TinTin++”'}
例子：#script {result} {php -r 'echo “Hello TinTin++”'}
例子：#script {result} {tcl -c 'puts “Hello TinTin++”'}
例子：#script {path} {pwd}
如果没有给出{变量}参数，脚本命令的输出内容将被当作TinTin++的输入，并允许你用#showme和#send命令来执行这一脚本输出。当然你也可以执行脚本文件。

如果给定{变量}参数，脚本命令的输出内容将以list变量的形式保存。你可以用$variable[1]、$variable[2]……来读取具体内容。

注：你也可以用#run和#system命令来执行shell命令。

Send

语法：#send {内容}

将{内容}直接发送到mud，如果你想发送一个转义符的话这会比较有用。

Session

语法：#session {session名称} {地址} {端口号}

这条命令将以稳定的名称启动一个session，并连接到给定的服务器。

例子：#ses pkuxkx pkuxkx.net 8080

#session +和#session –用于切换到下一个或上一个session，当然这只针对你打开了多个session的情况。#session <数字>将激活指定序号的session。

Showme

语法：#showme {信息内容} {行号}

用#showme显示的文本可以用于触发其他命令，也可以用于调试#action、#substitute等。#showme中可以用$变量来显示变量信息。

例子：#showme $bla
如果你已经定义了变量“bla”，这条命令将显示bla变量的内容。

{行号}参数是可选的，作用与#prompt命令中的{行号}相同。

Snoop

语法：#snoop {session名称}

如果你有后台运行的session，这条命令能够让你观察到这些session的显示内容。

Speedwalk（快速行走）

快速行走功能让你可以不必输入分号就连续执行移动命令，你也可以在移动命令前加上数字来重复执行一个移动指定。你可以在#config中打开或关闭快速行走功能。

例子：2s5w3s3w2nw
如果没有快速行走功能，你将不得不输入：s;s;w;w;w;w;w;s;s;s;w;w;w;n;n;w

Split

语法：#split

这条命令用于将屏幕分为上下两部分，上方屏幕用于显示从mud服务器接收的信息，下方屏幕用于输入键盘指令。这样就可以避免在你输入文字的时候，由于接收到mud信息而被打断。

语法：#split {下屏行号} {上屏行号}

这是#split命令的一种高级应用，使你能更加精确地分配屏幕空间。

如果你使用了分屏，那我建议你用#prompt命令抓取一些提示信息并放到分屏栏上，否则提示信息可能被新的mud信息刷走。

注：你可以用#unsplit命令取消分屏。

Substitute

语法：#substitute {原信息} {新信息} {优先级}

#substitute命令用于改变mud输出的信息。在{原信息}中可以使用%1～99%的变量并在{新信息}中引用，变量%0不应在{原信息}中使用。“优先级”参数是可选的，它决定了这个替换语句生效的优先权，默认值为5。

更多有关正则表达式的信息请查询Action（触发）的帮助文件。你可以在{新信息}中使用TinTin++的颜色代码来改变信息的颜色，默认情况下{原信息}中不包括颜色信息。更多关于颜色的信息请查询Colors（颜色代码）的帮助文件。

例子：#substitute {你说道：「%*」} {<128>你说道：「<138>%1<128>」}
执行上面的命令并say一句话来看看结果。

注：你可以用#unsubstitute命令删除一个替换。

Suspend

语法：#suspend

这条命令将让TinTin++进入后台运行并返回shell界面，按下^z也能达到同样的效果。如要返回TinTin++，你可以输入fg。
（译注：与其他针对unixshell的命令一样，wintin就不要尝试了，很可能就回不来了。）

Switch

语法：#switch {条件} {语句}

#switch命令与其他语言中的switch语句类似，当执行#switch时，在{语句}部分的#case语句会与逐条与{条件}做比较并判断是否执行，当所有#case都不匹配时，#default语句将被执行。

#break命令可以跳出#switch，但是它并不象在c语言中那样是必须的，因为每个#switch中只有一个#case会被执行。

例子：#switch {1d4} {#case 1 hihi;#case 2 hehe;#default grin}

System

语法：#system {命令}

#system命令用于执行shell指令。

例子：#system ls
如果你正想读取一个机器人文件，却突然想不起文件名的时候，这就很有用了。
（译注：ls是unix shell命令，相当于dos 下的dir，wintin同样不用尝试了。）

注：你也可以用#script和#run命令来执行shell指令。

Tab

语法：#tab {完整语句}

#tab命令将把一个语句增加到你的tab标签列表。当你按下Tab键时，TinTin++将从你的tab标签列表中寻找匹配的语句。这在输入一些比较长的命令时会很方便。

如果你输入的内容没有在tab标签中定义，TinTin++将在屏幕缓冲区中寻找可能匹配的内容。

例子：#tab part_abandon
输入pa然后按下Tab键，整条命令就会出现。

注：你可以用#untab命令来删除tab标签。

Textin

语法：#textin {文件名}

这条命令将读入一个文件，并把文件中的每一行发送到mud。发送的内容不会被TinTin++转换或加以解释，因此可以用来将一个脚本文件发送到mud提供的记事本之类的东西里面。当然如果你一次性输入太多东西的话，大部分mud会把你踢出去的。

例子：#textin desc1.txt
这个例子将把desc1.txt中的数据读入一个olc编辑器或其他类似的东西。

Ticker

语法：#ticker {名称} {命令} {间隔}

{名称}可以是你喜欢起的任何名字，它只在使用#unticker命令时需要。这条命令会按照{间隔}指定的秒数定时执行。

例子：#ticker {autosave} {save} {300}
这个例子将每隔300秒执行一次save命令。

注：你可以使用#unticker命令来删除一个定时器。

Variable

语法：#variable {变量名} {内容}

变量与之前在别名、触发中使用的%0～99的参数变量不同，你可以指定变量的名称，并且只要session没有关闭，定义好的变量会一直存在，除非你改变了它的值。变量可以保存在coms文件中，在不同session中的同名变量是独立的，可以有不同的值。对于每一个session，其中的变量都是全局意义的，你可以在变量前加上“$”号来获得变量值。

例子：#alias {target} {#var target %0}

```
#alias {t} {perform throwing.tan $target}
```

变量名只能由字母和数字组成，这样你才能取到它的值。但如果你办不到这一点，也不必担心，这时你只需要做一件简单的事，把变量名放到括号里：

例子：#variable {cool website} {http://pkuxkx.net}

```
chat 北大侠客行的主页是${cool website}
```

变量可以通过括号进行嵌套使用，以达到类似数组的效果。

例子：#var hp[self] 34;#var hp[target] 46

你可以用$variable[+1]来读取第一个嵌套变量的值，用$variable[-1]读取最后一个。$variable[-2]将返回倒数第二个变量的值，以此类推。如果想查看所有的嵌套标记，可以使用$variable[]。

用&variable可以查看嵌套变量的索引号。

注：使用#if {&{variable}}可以判断一个变量是否存在。

注：一个不存在的嵌套变量与一个存在的根变量将反馈0值。
（译注：此为直译，含义不明，可能是对照上一个#if的例子而言。）

注：你可以用#unvariable命令删除一个变量。

While

语法：#while {条件} {命令}

#while命令与c语言中的while命令类似，当条件为0（假）时，while循环就会终止。

例子：#while {$cnt>0} {#math cnt $cnt-1}

Wildcards（通配符）

通配符用于在正则表达式中匹配字符串。

以“^”号开头的信息代表一个行首匹配，以“$”号结尾的信息表示一个行尾匹配。

以下内容适用于正则表达式。

```
{ }内的内容是一个与Perl语言兼容的正则表达式。
```

[ ] . + | ( ) ? * 这些符号将被当作普通文本处理，但在{ }内出现时除外。同时需要注意的是，此时将{ }被( )代替。

```
%w 匹配0到任意个字母。
%W 匹配0到任意个非字母。
%d 匹配0到任意个数字。
%D 匹配0到任意个非数字。
%s 匹配0到任意个空格。
%S 匹配0到任意个非空格。
```

```
%? 匹配0或1个字符。
%. 匹配1个字符。
%+ 匹配1到任意个字符。
%* 匹配0到任意个字符。
```

```
%i 匹配时不区分大小写。
%I 匹配时区分大小写（默认）。
```

例子：#alias {bla%*}
这将显示所有以“bla”开头的别名。

例子：#if {“$test”==“%*%ibla%*”} {#showme true}
这可以用来检查变量test的内容是否包括“bla”字符串，不区分大小写。

Write

语法：#write {文件名}

这条命令将把所有的设置都存入一个文件。

例子：#write pkuxkx.tin
这个例子将把你的别名、触发、变量等等都写入pkuxkx.tin文件。

Writebuffer

语法：#writebuffer{文件名}

这条命令将把屏幕缓冲区的内容写入指定的文件，数据格式与log文件一样，可以在#config中设置。
（译注：TinTin++2.00.9没有这个命令。）

Zap

语法：#zap

这条命令将关闭当前的session，如果没有活动的session，则关闭TinTin++。

> 来源: https://www.pkuxkx.net/wiki/tintinpp/newmanual
