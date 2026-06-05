- Lordstar的常用命令

- #abort

- #add

- #additem

- %additem(list,value)

- #delitem

- %delitem(value,list)

- #delnitem

- %dumps(list)

- %include(list a,list b)

- %numitems(list)

- %item(list,n)

- %ismember(value,list)

- #alias

- #alarm

- #delalarm

- #buff

- #cap

- #case

- #close

- #color

- #cls

- #connect

- #disconnect

- #trigger

- #deltrigger

- #t+

- #t-

- #show #echo

- #say

- #echop

- #file

- %read(file,n)

- #write

- %grep(file,string)

- #close

- #erase

- #forall

- #exe

- #gag

- #getdiffcolor

- #getdiffcolorset

- #if

- #ignore

- #load

- #label

- #logfile

- #longmess

- #mess

- #math

- #mxp

- #prompt

- #pick

- #reloadlua

- #run

- #send

- #sendto

- #timer

- #deltimer

- #ts

- #tz

- #unalias

- #wait

- #unwait

- #var

- #unvar

- #while

- #until

- #yesno

Lordstar的常用命令

#abort

说明：可以简写为#ab,一般用于一个循环中断跳出,如#while #forall
举例:

```
#forall {1|2|3|4} {#say %i;#if %i>2 {#abort}}

```

#add

说明：原有变量数值增加
举例:

```
#var a 5;#add a 3
```

以下集合变量item的操作

#additem

说明：集合型变量增加元素，比如a=你好|kk   元素加在list后面
举例:

```
#var a 你好|kk;#additem a 杀了黑猫
```

%additem(list,value)

说明：集合型变量增加元素，比如a=你好|kk   元素加在list前面
举例:

```
#var a 你好|kk;a=%additem(@a,杀了黑猫)
```

#delitem

说明：删除集合型变量的某个元素，比如a=你好|kk|12|kk|哈  重复的元素会全部被删除
举例:

```
a=你好|kk|12|kk|哈;#delitem a kk
```

%delitem(value,list)

说明：删除集合型变量的某个元素，比如a=5|1|2|3|1|a|4|1  重复的元素只删除第一个
举例:

```
a=a=5|1|2|3|1|a|4|1;#var b %delitem(1,@a)
```

#delnitem

说明：删除型集合型变量的第几个元素，比如a=你好|kk|12|kk|哈
举例:

```
a=你好|kk|12|kk|哈;#delnitem a 2
```

%dumps(list)

说明：删除一个集合型list变量中重复的元素
举例:

```
#var a aa|bb|aa|cc;#var b %dumps(@a)  -- 结果aa|bb|cc

```

%include(list a,list b)

说明：如果list a包含所有list b的元素，则返回1
举例:

```
a=aa|bb|cc|aa|ee;
b=aa|ee;
#say %include(@a,@c)

```

%numitems(list)

说明：集合型变量值的个数，比如a=你好|kk
举例:

```
#var a 你好|kk;#say %numitems(@a)
```

%item(list,n)

说明：集合型变量第n个项的值，比如a=你好|kk
举例:

```
#var a 你好|kk;#say %item(@a,2)
```

%ismember(value,list)

说明：集合型变量list中是否含有value
举例:

```
#var a 你好|kk;#say %ismember(kk,@a)
```

专题结束

#alias

说明：可以简写为#al,创建一个别名#alias aa {haha},空的alias可以用#alias aa {},删除alias用#unalias aa
举例:

```
#alias aa {haha}
```

```
#alias aa {say 1--%1;say 2--%2}
```

```
#alias aa {say %*}
```

```
#alias aa {#alias bb {say "%1"}}
```

#alarm

说明：闹钟，好像比较复杂，以下只举几个例子 – 注意具体id可以不写
举例:

```
#alarm +600 {haha} idxxxx 建立一个600秒的一次性闹钟，执行haha，名称为idxxxx
#alarm *1 {haha} idxxxx   建立每秒的闹钟，执行haha，名称为idxxxx
#alarm *:55:01 {#say haha} 建立一个闹钟在每个小时55分01秒的时候执行

```

#delalarm

说明：删除创建的#alarm，–只能删除带id的闹铃，举例

```
#alarm +60 {haha} idxxxx;
#delalarm idxxxx;
```

#buff

说明：显示一个buff图标，倒计时n秒后执行一个指令
举例:

```
#buff 1 60 {say 强发结束} 倒计时60秒后说出一句话

```

#cap

说明：#capture 抓当前触发行到一个窗口 – 注意只能用在触发中
举例:

```
#cap chat
```

#case

说明：#case 数值 {1} {2} {3} ..
举例:

```
#case %eval(1+2) {#say 11} {#say 2} {#say 3} {#say 4} 这是3第四个大括号所以#say 3

```

#close

说明：见#file

#color

说明：修改为触发行的颜色。只能在触发器中使用。可同时设置文字颜色和背景色，中间用逗号隔开。

```
文字颜色：black黑/red红/green绿/yellow黄/blue蓝/fuchsia紫/teal青/white白
背景颜色：bblack黑/bred红/bgreen绿/byellow黄/bblue蓝/bfuchsia紫/bteal青/bwhite白
```

举例:

```
#color green,bteal
```

#cls

说明：清除屏幕内容

#connect

说明：简写#con;连接服务器，举例

```
#connect mud.pkuxkx.net 8080

```

#disconnect

说明：断开连接服务器，举例

以下触发器的操作

#trigger

说明：简写#tr;新建一条触发器。

1.不支持新建颜色触发，颜色触发必须手动添加。

2.同一ID只能存在一条触发器，重复ID时新建的将覆盖原有的。不指定ID（即ID为空）不影响触发器的使用。

3.ID为空的触发器不受数量限制。

4.没有写ID的触发无法用指令精确操作该条触发器。 只能删除有ID的触发。

参数介绍:#trigger {哈哈-#1} {xixi;faint-#2} {测试目录-#3} 0-#4 1-#5 0-#6 测试id-#7

参数1:触发匹配语句，可以使用通配符;

参数2:触发成功后的命令;

参数3:触发器的目录Class，可以使用#t+ 打开一个目录或使用#t- 关闭一个目录;

参数4:触发语句冷却时间,触发一次以后n秒内不会再被触发;

参数5:触发器是否开启，1表示开启，0表示关闭，一般都是1;

参数6:触发器参数

.     1,是不等待换行符直接当行触发

.     2,是正则触发

.     3,3=1+2当行触发且正则触发

参数7:触发器的具体ID，有ID的触发方便删除;

```
测试1:
#trigger {哈哈} {hehe} {} 0 1
测试2:
#trigger {^你对着(*)$} {#alias aa {smash};aa} {测试} 0 1 0 test
自己感受一下区别吧
```

通配符

* 匹配任何数量的字符或空格ls中是最短匹配!!!

? 匹配一个字符

%d 匹配任何数量的数字（0－9）

%w 匹配任何数量的字母（a-z）

%a 匹配任何数量的字母或数字（0－9，a-z）

%s 匹配任何数量的空格（spaces, tabs)

%x 匹配任何数量的非空格

^ 强制从一行的开始进行匹配

$ 强制匹配到一行的结束

(pattern) 保存匹配的式样到参数％1～％99

~ 包括其中的字符不会被解释为特殊字符

{val1|val2|val3|…} 匹配其中列出的任何特殊的串

#deltrigger

说明：删除指定id的触发

```
#deltrigger test
```

#t+

说明：打开指定目录

```
#t+ 打坐

```

#t-

说明：关闭指定目录

```
#t- 打坐
```

专题结束

#show #echo

说明：简写#sh,显示一行字到屏幕

```
#echo hello 木木
```

#say

说明：显示一行字到屏幕，无法触发

```
#say 1+1= %eval(1+1)

```

#echop

说明：和#echo差不多，只是行尾没有换行符，只能自己体会了

以下#File文件的操作

#file

说明：打开一个txt文件

```
#file 1 hongdou.txt;
#say %read(1,1);
#var a %read(1,5);
#say %grep(1,孟子);
#close 1
```

%read(file,n)

说明：获取#file打开文件的某一行

```
#file test hongdou.txt;
kkk=%read(test,12);
#say @kkk;
#close test
```

#write

说明：#write file string n,在#file打开文件中写入一行

```
#file 2 aa.txt;
#write 2 这是个写入最后一行测试;
#write 2 {这是个写入第一行测试 aa} 0;
#write 2 这是个写入第五行测试 4;
#close 2
```

%grep(file,string)

说明：搜索文件file中含有string的所有行信息，以|分隔

```
#file 2 hongdou.txt;
test=%greap(2,孟子);
#close 2
```

#close

说明：关闭一个txt文件，随时关闭文件是个好习惯

```
#file 1 hongdou.txt;
#say %read(1,1);
#close 1
```

#erase

说明：删除一个文件

```
#erase hongdou.txt
#erase %syspath()/MXP/123456.jpg
```

专题结束

#forall

说明：遍历整个集合型变量

```
#var a {1|2|3|5|4};#forall @a {#say %i}
#forall {a|b|c} {#var kk.%i %i}

```

#exe

说明：打开一个windows的执行程序

```
#exe c:\windows\notepad.exe %syspath()\hongdou.txt
```

#gag

说明：屏蔽一段信息

```
触发：本尊拿了大砍刀走了过来。
#gag
```

#getdiffcolor

说明：将触发行中的文字按照其字体颜色的不同进行排类，返回字数最少的那一类，将其文字存放在变量中。
只能在触发器中使用该命令，无需开启颜色触发。

```
触发：(*)
#getdiffcolor test
#getdiffcolor test 2
```

#getdiffcolorset

说明：将触发行中的文字按照其字体颜色的不同进行排类，把排类结果依据其字数从少到多的顺序排列，
以集合型的方式存放在指定变量中。只能在触发器中使用该命令，无需开启颜色触发。

```
触发：(*)
#getdiffcolor alltest
```

#if

说明：逻辑判断

```
#if 1 {#say 真的是1} {#say 假的是0}
#if %null(@a) {#say 真的是1} {#say 假的是0}
#if @a=ok {#say 真的是1} {#say 假的是0}
#if (@a=ok & @b=ok) {#say 真的是1} {#say 假的是0}
#if (@a=ok | @b=ok) {#say 真的是1} {#say 假的是0}
#if @a=ok {testa;} {
#if @b=ok {testb;} {
testc;
}
}
```

#ignore

说明：简写#ig,临时打开关闭所有触发和闹铃
举例:

```
#ig
```

#load

说明：加载机器人
举例:

```
#load save/job.xml
```

#label

说明：给当窗口改个下标
举例:

```
#label man
```

#logfile

说明：将当前窗口内容log记录到一个文件
举例:

```
#logfile 1.txt;
#logfile off;
```

#longmess

说明：比较长的消息弹窗可以\n分行
举例:

```
#longmess hi\n这是个测试

```

#mess

说明：一个消息弹窗
举例:

```
#mess hi
```

#math

说明：数学运算
举例:

```
#math a {10*24+9/4}
相当于a=%eval(10*24+9/4)
```

#mxp

说明：下载一张图片
举例:

```
#mxp http://pkuxkx.net/antirobot/robot.php?filename=1542814021336932
```

#prompt

说明：让用户输入一个变量的值
举例:

```
#pr id man
```

#pick

说明：让用户选择一个内容并执行
举例:

```
#pick O:1 {测试1:aa} {测试2:bb}

```

#reloadlua

说明：从新加载lua脚本
举例:

```
#reloadlua

```

#run

说明：解析内容发送，相当于输入栏输入内容
举例:

```
#run "#t+ aa;#alias aa {haha};aa"

```

#send

说明：不解析直接发送给服务器
举例:

```
#alias aa {say %*};
#run aa haha;
#send aa haha;
```

#sendto

说明：发送给别的窗口
举例:

```
#sendto chat #sh 显示一下信息
#sendto man "#alias aa {haha};aa"
```

以下定时器timer的操作

#timer

说明：创建一个定时器
举例:

```
#timer {say test} 60
```

#deltimer

说明：删除一个指定id的定时器

```
#deltimer timerid

```

#ts

说明：修改定时器的时间

```
#ts 0    --所有没有id的定时器改为0秒，关闭的意思
#ts 60   --所有没有id的定时器改为60秒
#ts 5 id --一个叫id的定时器，时间改为5秒
```

#tz

说明：恢复定时器的初始时间

```
#tz      --恢复所有没有id的定时器为初始时间
#tz aa   --恢复aa这个定时器为初始时间
```

专题结束

#unalias

说明：删除一个alias

```
#unalias yq
```

#wait

说明：简写#wa，等待多少毫秒

```
#5 e;#wa 2000;#4 s
```

#unwait

说明：删除所有wait，wait之后的命令不在执行

```
#unwait
```

#var

说明：给变量命名

```
#var a 10;
a=10
```

数组型变量介绍

```
#var test.10 你好;
#var test.aa 多嘛;
#say @test.1 @test.aa
```

#unvar

说明：删除变量

```
#unvar a;
```

#while

说明：循环

```
#var a 10;
#while @a>0 {
#if @a>5 {#say hi};
#add a -1;
}
```

#until

说明：循环,直到条件是真

```
#var a 10;
#until @a<1 {
#if @a>5 {#say hi};
#add a -1;
}
```

#yesno

说明:让用户判断选择

```
#yesno 是否需要买长剑？ 是:changjian=1 否:changjian=0;
```

还有一些命令比如数据库#sql 等我没用过，暂不更新。

如果出现一些命令不解析后面的变量，比如#exe @a.mp3

请使用%concat解析一下，比如%concat(“#exe ”,@a,“.mp3;”)

Lua脚本访问lordstar命令的方法是函数Run()

一个例子：Run(“haha;#wa 2000;xixi”)

> 来源: https://www.pkuxkx.net/wiki/lordstar/commands
