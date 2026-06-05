- Lordstar的常用函数

- %abs(n)

- %a2u(string)

- %u2a(string)

- %delitem(value,list)

- %alias(string)

- %arbnum(string)

- %begins(string a,string b)

- %ends(string a,string b)

- %case(n,a,b,c,d,e,..)

- %char(n)

- %chnnum(number)

- %concat(a,b,c,d,..)

- %copy(string,n,m)

- %right(string,n)

- %rightback(string,n)

- %diffcolor()

- %dirfiles(path)

- %dumps(list)

- %eval()

- %float()

- %file(n)

- %gamescount()

- %gamebytes()

- %setglobal(key,value)

- %getglobal(key)

- %include(list a,list b)

- %isint(n)

- %isconnect()

- %label(n)

- %len(string)

- %xlen(string)

- %line(n,windows)

- %rawline(n,windows)

- %lower(string)

- %upper(string)

- %match(string,match,var)

- %regex(string,match,var)

- %max(m,n)

- %mim(m,n)

- %random(m,n)

- %null(var)

- %word(string,n,word)

- %numwords(string,word)

- %syspath()

- %sort(string)

- %trim(string)

- %tick()

- %time()

- %var(string)

Lordstar的常用函数

Lua脚本访问lordstar函数的方法是函数Result()

一个例子：local test = Result(“%syspath()”)

%abs(n)

说明：数字n的绝对值
举例:

```
#var a %abs(5)  -- 结果5
#var a %abs(-5) -- 结果5
#var a %abs(0)  -- 结果0

```

%a2u(string)

说明：也可写作%ansitoutf8(),ansi码转为utf8
举例:

```
#var a %a2u(哈哈)
```

%u2a(string)

说明：也可写作%utf8toansi(),utf8码转为ansi
举例:

```
#var a %u2a(哈哈)
```

%delitem(value,list)

说明：删除集合型变量的某个元素，比如a=5|1|2|3|1|a|4|1  重复的元素只删除第一个
举例:

```
a=a=5|1|2|3|1|a|4|1;#var b %delitem(1,@a)
```

%alias(string)

说明：显示一个alias的内容
举例:

```
#alias aa {haha};
#var a %alias(aa)
```

%arbnum(string)

说明：把字符串中的中文数字转换为阿拉伯数字。中文数字应当是包含百、千、万分位的标准描述，
比如：一亿零二十三万四千零六十七。

```
a=%arbnum(一亿零二十三万四千零六十七)
```

%begins(string a,string b)

说明：检查string a 是否以 string b开头
举例:

```
%begins(aabbcc,aa)  -- 1
%begins(aabbcc,kk)  -- 0

```

%ends(string a,string b)

说明：检查string a 是否以 string b结尾
举例:

```
%begins(aabbcc,cc)  -- 1
%begins(aabbcc,kk)  -- 0
```

%case(n,a,b,c,d,e,..)

说明：返回数字n后，第n个元素
举例:

```
%case(1,aa,bb,cc)  -- aa
%case(3,aa,bb,cc)  -- cc
%case(0,aa,bb,cc)  -- 空
%case(4,aa,bb,cc)  -- 空
%case(m,aa,bb,cc)  -- 空

```

%char(n)

说明：返回数字n代表的ascii码字符
举例:

```
%case(100)  -- d
```

%chnnum(number)

说明：把阿拉伯数字变中文数字

```
%chnnum(123456) -- 一十二万三千四百五十六
```

%concat(a,b,c,d,..)

说明：连接字符，解析变量

```
a=哈哈,
%concat("你好",@a,是吗)
```

很多时候某个命令无法解析变量的时候，可以用来解析。比如#xxxx @a @b

可以写成%concat(“#xxxx ”,@a,“ ”,@b)

%copy(string,n,m)

说明：复制字符,第n个字后，长度m
举例:

```
%copy(aabbccdd,3,3) -- bbc
```

%right(string,n)

说明：复制字符,第n个字后的字串
举例:

```
%right(aabbccdd,3) -- ccd
```

%rightback(string,n)

说明：复制字符,第n个字后的字串
举例:

```
%right(aabbccdd,3) -- ccd
```

%diffcolor()

说明：触发中本行不同颜色字符，结果是一个集合型变量aa|bb|cc,字数最少的字排在前面
举例:

```
触发:^(*)$
#var a %diffcolor()
```

%dirfiles(path)

说明：返回某个文件夹下的所有文件名字，以集合型变量排练，排列不分先后
举例:

```
#var a %dirfiles(c:\baigonggong\avi)
```

%dumps(list)

说明：删除一个集合型list变量中重复的元素
举例:

```
#var a aa|bb|aa|cc;#var b %dumps(@a)  -- 结果aa|bb|cc
```

%eval()

说明：数学计算
举例:

```
a=%eval(12*5/6*3+6/2)
```

%float()

说明：数学计算,浮点运算，有小数点的
举例:

```
a=%float(12*5/6*3+6/2)

```

%file(n)

说明：检查文件编号是否被#file 打开着
举例:

```
#file aa 1.txt;
#say 开着 %file(aa);
#close aa;
#say 关着 %file(aa)
```

%gamescount()

说明：一共打开多少个窗口–含#cap #sendto 的聊天窗口
举例:

```
#say %gamescount()
```

%gamebytes()

说明：所有服务器发送的总字节数,不含机器人#show #say Print Echo出的信息
举例:

```
a=%gamebytes()
```

%setglobal(key,value)

说明：设置一个全局变量
举例:

```
#if %setglobal(aa,哈哈哈) {}
```

:!:zmud好像就是个函数不是命令

%getglobal(key)

说明：获得一个全局变量的数值
举例:

```
#var a %getglobal(aa)
```

%include(list a,list b)

说明：如果list a中包含所有list b的元素，则返回1
举例:

```
a=aa|bb|cc|aa|ee;
b=aa|ee;
#say %include(@a,@c)

```

%isint(n)

说明：是否是整形数字
举例:

```
%isint(5)    -- 1
%isint(1.2)  -- 0
%isint(abc)  -- 0

```

%isconnect()

说明：是否连线中，连线中返回1，断线返回0

%label(n)

说明：返回第n个窗口的标签name名称

```
#say %label()   -- 当前窗口
#say %label(2)  -- 第二个窗口
```

%len(string)

说明：返回一个字符串的长度，英文1，中文2

```
%len(abc你好)   -- 7

```

%xlen(string)

说明：返回一个字符串的长度，英文1，中文也是1

```
%xlen(abc你好)  -- 5
```

%line(n,windows)

说明：返回第几行信息

```
%line(1)      -- 当前行，触发行，最后一行
%line(2)      -- 倒数第二行
%line(1,chat) -- chat窗口的倒数第一行

```

%rawline(n,windows)

说明：返回第几行信息，含有颜色字符信息

```
%rawline(1)      -- 当前行，触发行，最后一行
%rawline(2)      -- 倒数第二行
%rawline(1,chat) -- chat窗口的倒数第一行
```

%lower(string)

说明：大写字母变小写

```
#var a %lower(AAAbc)

```

%upper(string)

说明：小写字母变大写

```
#var a %upper(hi)
```

字符串的匹配

%match(string,match,var)

说明：用match格式匹配字符string,返回到变量var中,zmud触发规则

```
%match(aabbcc123kk,"^%x%dkk$") -- 1 匹配成功
%match(aabbcc123kk,"^(%d)")    -- 1 匹配成功
%match(aabbcc123kk,"%s")       -- 0 匹配失败
```

%regex(string,match,var)

说明：用match格式匹配字符string,返回到变量var中,正则PCRE规则

```
%match(aabbcc123kk,"^.*\$")          -- -1 匹配成功,但是没有用括号抓取
%match(aabbcc123kk,"(\d+)")          --  1 匹配成功
%match(aabbcc123kk,"\s+")            --  0 匹配失败
%match(aabbcc123kk,"(\d+)(\S+)",aa)  --  2 匹配成功,匹配值抓取到aa这个集合型变量,@aa.1 @aa.2
```

专题结束

%max(m,n)

说明：最大值

%mim(m,n)

说明：最小值

%random(m,n)

说明：m之n之间取随机数

%null(var)

说明：判断变量是否为空

```
#var a "";%null(@a)    -- 1
#unvar a;%null(@a)     -- 1
#var a {};%null(@a)    -- 1
#var a 10;%null(@a)    -- 0

```

%word(string,n,word)

说明:字符串string，以word分割，的第n个字符分隔符默认空格

```
%word(aa bb cc,2)      -- bb
%word(aa|bb|cc,3,|)    -- cc
%word(你去扬州北大街找张三,1,北大街)              -- 你去扬州
%word(%word(去扬州北大街找张三,1,北大街),2,你去)  -- 扬州
```

%numwords(string,word)

说明：一个字串含有多个单词，默认以空格分割

```
%numwords(aa bb cc)        -- 3
%numwords(aa|bb|cc|dd,|)   -- 4
%numwords(aa|bb|cc|dd)     -- 1
```

%syspath()

说明：返回lordstar所在目录非常重要，经常用到

```
#say %dirfiles(%syspath())
```

%sort(string)

说明：把一个集合型变量排序

```
%sort(kk|1g|22|k8|你好)  --  1g|22|k8|kk|你好
```

%trim(string)

说明：去除string前后的空白

%tick()

说明：操作系统从启动到当前所经过的总毫秒数。不是ls软件开启后的计时

%time()

说明：按照参数指定格式输出系统当前时间。

默认格式为“yyyy-mm-dd hh:nn:ss”。

```
#var aa %time(szzz)
```

%var(string)

说明：获取一个变量值

```
#var b %var(aa)      -- 获取变量aa的值
#var b %var(aa,chat) -- 获取chat窗口变量aa的值

```

变量可以只用当命令输入

例如：#var aa {haha;#alias bb {xixi};bb};@aa

lordstar界面访问lua脚本函数使用%%luafunction()

> 来源: https://www.pkuxkx.net/wiki/lordstar/functions
