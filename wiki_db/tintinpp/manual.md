- 命令参考手册

- 命令：#

- 語法

- 說明

- 举例

- 命令：Action

- 语法

- 說明

- 举例

- 命令： All

- 语法

- 說明

- 举例

- 命令：AntiSubstitute

- 语法

- 說明

- 举例

- 命令: Alias

- 語法

- 說明

- 举例

- 命令: Bell

- 語法

- 說明

- 举例

- 命令: Boss

- 語法

- 說明

- 举例

- 命令: Char

- 語法

- 說明

- 举例

- 命令: CR

- 語法

- 說明

- 举例

- 命令: End

- 語法

- 說明

- 命令: Echo

- 語法

- 說明

- 举例

- 命令: IF

- 語法

- 說明

- 命令: INFO

- 語法

- 說明

- 举例

- 命令: IGNORE

- 語法

- 說明

- 举例

- 命令: KILLALL

- 語法

- 說明

- 命令: LOOP

- 語法

- 說明

- 命令: LOG

- 語法

- 說明

- 举例

- 命令: MESSAGE

- 語法

- 說明

- 命令: MARK

- 語法

- 說明

- 命令: Map

- 語法

- 說明

- 举例

- 命令: MATH

- 語法

- 說明

- 命令: # NAME

- 語法

- 說明

- 举例

- 命令: NOP

- 語法

- 說明

- 举例

- 命令: PATH

- 語法

- 說明

- 命令: PathDir

- 語法

- 說明

- 举例

- 命令: PRESUB

- 語法

- 說明

- 举例

- 命令: RETURN

- 語法

- 說明

- 举例

- 命令: REDRAW

- 語法

- 說明

- 命令: READ

- 語法

- 說明

- 举例

- 命令: SAVEPATH

- 語法

- 說明

- 举例

- 命令: SNOOP

- 語法

- 說明

- 举例

- 命令: SHOWME

- 語法

- 說明

- 举例

- 命令: Session

- 語法

- 說明

- 举例

- 命令: Speedwalk

- 語法

- 說明

- 举例

- 命令: Split

- 語法

- 說明

- 举例

- 命令: Substitute

- 語法

- 說明

- 命令: Suspend

- 語法

- 說明

- 命令: System

- 語法

- 說明

- 举例

- 命令：TabAdd

- 語法

- 說明

- 举例

- 命令：tabdelete

- 語法

- 說明

- 命令：tablist

- 語法

- 說明

- 命令：textin

- 語法

- 說明

- 命令：tick

- 語法

- 說明

- 命令：tickon tickoff

- 語法

- 說明

- 举例

- 命令：tickset

- 語法

- 說明

- 命令：ticksize

- 語法

- 說明

- 举例

- 命令：togglesubs

- 語法

- 說明

- 命令：unaction

- 語法

- 說明

- 举例

- 命令：unalias

- 語法

- 說明

- 举例

- 命令：unantisub

- 語法

- 說明

- 举例

- 命令：ungag

- 語法

- 說明

- 举例

- 命令：unhighlight

- 語法

- 說明

- 命令：unpath

- 語法

- 說明

- 举例

- 命令：unsplit

- 語法

- 說明

- 命令：unsubs

- 語法

- 說明

- 举例

- 命令：UnVariable

- 語法

- 說明

- 举例

- 命令：variable

- 語法

- 說明

- 举例

- 命令：verbatim

- 語法

- 說明

- 命令：version

- 語法

- 說明

- 命令：wizlist

- 語法

- 說明

- 命令：write

- 語法

- 說明

- 命令：zap

- 語法

- 說明

命令参考手册

-  **来源：** pwpw 收集自cc.fjtc.edu.tw（台湾和春技術學院）(貌似学校现在的域名改成了http://www.fotech.edu.tw/)的繁体中文手册 ,相对比较旧，当写作得比较生动，对新手而言，比译自官网手册的要有趣得多，适合入门时查阅浏览。1)

-  **注意：** 该手册基于 tintin++ 较早的版本，目前很多命令已经不再使用，或者用法已经变更。本手册为尊重原作者劳动，没有删除，只是简单地标注了 。

命令：#

語法

```
# {命令}
```

說明

-  普通列表项目重覆的執行 {命令}  所指定的次數.

举例

```
#7 drink skin
```

*連續喝七次水.*

```
#7 kiss muyi
```

*連續 kiss muyi 七次. *^^**

```
#7 buy orange
```

*連續買七個小橘子..:p*

命令：Action

语法

```
#action {觸發文字} {反應命令} {優先權}
```

說明

-  當 tintin++ 接收到 {觸發文字} 中的內容時, tintin 便會自動的去執行反應命令中所列的命令字串.

-  在 {觸發文字} 中, 可使用 %0-9 可以代替所接收到的字串, 並且在{反應命令} 中對應使用.

-  優先權的等級: 0 是最重要, 9 是最不重要, 假如您沒指定優先權的初值, 預設值是 5.

-  假如您在 {觸發文字} 中以 '^' 開頭, 則 tintin++ 會只找每行訊息的開頭.

举例

假如 tintin 接收到以下的訊息:

```
Muyi kisses you.
```

則

```
#action {kisses} {blush}
```

將會動作,
而

```
#action {^kisses} {blush}
```

將不會動作,
因為 kisses 並不在字串的開頭.

只鍵入 #action 的話, 將會把您所定義的所有 action 都列出來.

再來我們舉幾個例子: (註: 範例因太長而換行, 實際寫作請勿換行..)

```
#action {Alycia has arrived} {pat alycia;smile alycia} {0}
```

*假使 alycia (兔兔) 進入這間房間, 您將會自動拍她的頭, 並對她微笑.*

```
#action {生命值 %1/%2 , 法力點數 %3/%4 , 移動點數 %5/%6 }
{
say my hp: %1, mana: %3, mv: %5
}
```

*則當 tintin 抓到對應 message 時, 您會自動說出:*

```
"my hp: xx, mana: xx, mv: xx"
```

假如您鍵入 #action {觸發文字}, 則您將會看到您所定義要做的事. 萬用字元'*' 在此狀況下是可以使用的.

```
#action
```

*列出所有 action*

```
#action *tell*
```

*列出所有包含 tell 這個字的 action*

命令： All

语法

```
#all  {您想送去所有 session 的命令}
```

說明

-  #all 會把您所指定的命令送去所有目前存在的 session。這個命令在您同時開兩個以上的 session 在玩 mud 時可以用得著..

举例

```
#all {chat bye bye ^_^}
```

*則同時間, tintin++ 會對所有的 session 送出 “chat bye bye ”*

命令：AntiSubstitute

语法

```
#antisubstitute {文字}
```

說明

-  這個命令會讓您所指定的 {文字} 將不會被 #substitute 置換調,或被 #gag 刪除掉.

举例

```
#antisubstitute {RECALL}
```

-  則所有包含 'RECALL' 文字的那一行, 將不會被 #substitute 置換調,或被 #gag 刪除掉.

命令: Alias

語法

```
#alias {alias name} {這個alias將執行的命令}
```

說明

-  #alias 可以講大量的命令或是過長的命令置換成一個短短的 alias.

-  #alias 題供 10 個變數給我們使用, 分別為 %0 ～ %9

-  變數 %0-9 的用法如下:

-  %0 所有的參數.

-  %1 參數的第一個.

-  …

-  %9 參數的第九個.

举例

例一

```
#alias {hiya} {say hiya %0}
```

則當您輸入

```
hiya cute Alycia
```

tintin++ 將赋值

```
%0 = cute Alycia
%1 = cute
%2 = Alycia
```

因此, 這個 Alias 將被展開為:

```
say hiya cute Alycia
```

後送出.

如果您寫:

```
#alias {hiya} {say hiya %1}
```

而輸入同為

```
hiya cute Alycia
```

, 則 tintin++ 將會把這個 alias 展開成為:

```
say hiya cute
```

後送出.

而當您若您未加變數, 則 tintin++ 預設值為 %0.

```
#alias {hiya} {say hiya}
```

會變成:

```
#alias {hiya} {say hiya %0}
```

例二

alias 也可以設成一次執行多個命令唷, 命令和命令中間只要用分號分開就好了.

```
#alias {kissmuyi} {hug muyi;kiss muyi;lick muyi;blush}
```

而 alias 也可以叫用其它的 alias :

例三

```
#alias {7drs} {#7 drs}
#alias {cw} {cast 'create water' buffalo}
#alias {full} {wake;7drs;cw;rest}
```

當您輸入 full 後, tintin++ 會先送出 wake 使您站起來,然後喝 water skin 中的水七次, 再施造水術把 water skinc填滿水, 然後再坐下..

這裡要注意的是, tintin 並不作同名 alias 的檢查, 也就是說,當您作了一個類似以下的 alias :

```
#alias {catch} {catch}
```

而當您輸入 catch 後, tintin++ 將陷入無窮回路.

其它例子

```
#alias {cw} {cast 'create water' buffalo}  設定 alias.
#alias {cw}                                顯示您 alias 的內容.
#alias                                     將您所有的 alias 列出.
#alias {*eb*}                              列出所有包含 eb 這兩個字的 alias.
#alias {eb*}                               列出所有以 eb 開頭的alias.
```

命令: Bell

語法

```
#bell
```

說明

-  這個命令可以使您聽到一聲 beep.

-  基本上是所有的終端機或終端機模擬程式都可以辦到.

举例

```
#alias {6beep} {#6 #bell}
```

當您輸入 6beep 後, 將會聽到六聲 beep 響聲.

命令: Boss

語法

```
#boss
```

說明

有點類似一般 PC game 上提供的 boss key 的功能.

```
當您輸入 #boss 後, 您將會看到一個類似樹狀結構排序的畫面,
而讓人不知道你在玩 Mud.. (打死我也不相信..:P)
```

举例

```
當您的叫獸..呃?! 鍵盤短路了.. 教授從您背後走近時, 您便可以輸入
#boss , 讓他看看 tree sorting 的程式執行..
```

```
呃?! 啥..您不是相關科系的.. wuwu..
啊!? 被教授看破了, 還被 shouts 'that is a poor program...'
嗯啊..
```

命令: Char

語法

```
#char {新的命令起始字元}
```

說明

這個命令可以讓您改變 tintin++ 內建的命令起始字元.

tintin++ 預設命令起始字元是 '#', 這個是定義在原始程式碼的 tintin.h
含括檔中, 假如您不喜歡, 您便可以用這個命令把它換掉.

举例

```
#char {/}
#char {@}
```

命令: CR

語法

```
#cr
```

說明

送出一個 enter 換行碼到 session. 這在 alias 或 action 中須要按

```
enter 鍵時可以使用.
```

举例

```
#action {^Reconnect} {#cr;#cr}
```

命令: End

語法

```
#end
```

說明

當下達這個命令後, tintin++ 將會結束而跳回 UNIX. (呵..差點打成跳回 DOS..)

不過要注意的是, #end 這個命令並不會幫您把所有的角色(character) quit.

命令: Echo

語法

```
#echo
```

說明

如果您把 echo 設為 on, 則 #action 在作所有動作前都會先告知.

举例

假設您設了一個 #action 如下:

```
#action {^[%1hp %2m %3mv]} {#var hp %1;#var mp %2;#var mv %3}
```

則當 tintin 抓到 {^[%1hp %2m %3mv]} 這個 message 後, 將會顯示:

[ACTION: #var hp %1;#var mp %2;#var mv %3]
當 echo 為 on 時, 您可以再輸入一次 #echo 把它 off 掉.

那鍋同學, 你還沒教學費說.. 學費是啥!? 前面有 post.. ^Q^
求青天乎?? 求水戶黃門乎?? 真正的真理在個人心中. *-
好像和 mud 無關的句子..:p

命令: IF

語法

```
#if {條件判斷式} {條件成立所要執行的命令}
```

說明

#if 命令的用法和一般程式語言 'if' 的用法很類似, 在處裡條件式的判斷

```
時, 是以 c 語言的楚裡方法為其基礎.
當 tintin++ 碰到一個 #if 命令時, tintin++ 將會開始判斷條件判斷式,
假如結果是為真值 (True, 也就是成立), 則指定的命令將會被送出執行,
#if 的敘述句只有 tintin++ 碰到時才會開始處理並進行判斷, 所以, 您必
須將 #if 命令放在其他命令下. (for example: #action, #alias 命令).
```

```
有關判斷式所使用的運算符號, 請參考命令 #math.
```

```
不過要注意的是, #if 目前只能用來比較數目字, 還無法用來比對字串.
```

for examples:

```
#action {%0 give you %1 coins} {#if {%%1>5000} {thank %%0}}
```

這個行命令的意思是, 當發現到某人給你的錢大於 5000 coins 時, 您將會
自動的謝謝他/她.

而 %0, %1 是源自 #action 所送來的變數, 但由於此為巢狀命令列, 所以, 您
在使用時必須再加上一個 '%', 變為 0, 1.

```
#action {^[hp:%0 } {#if {%%0
```

命令: INFO

語法

```
#info
```

說明

將目前這個 session 所定義的 #action, #alias, #variables,

```
#substitues, #antisubstitutes, 以及 #highlights 的數目列
出來.
```

```
如果沒有開啟任何的 session, 則列出預設的總數.
```

举例

```
#info
```

```
You have defined the following:
Actions : 94
Aliases : 245
Substitutes : 176
Antisubstitutes : 10
Variables : 39
Highlights : 176
Echo : 0 (1 - on, 0 - off)    Speedwalking : 1   Redraw: 0
Toggle Subs: 0   Ignore Actions : 1   PreSub-ing: 1
```

命令: IGNORE

語法

```
#ignore
```

說明

#ignore 簡單的說就是 #action 的開關. 假如說 #ignore 設為開啟

```
(on), 那所有的 #action 就會動作, 如果設為關閉 (off), 則所有
的 #action 將不會動作.
```

```
#ignore 預設值為開啟, 輸入 #ignore 後為關閉, 再輸入一次又會
再度開啟.
```

举例

假設有這樣一個 #action :

```
#action {^%0 kisses you.} {blush}
```

(預設值為開啟..)
Muyi kisses you.
Your cheeks are burning.  =⇒ #action 的反應.
Cuteals giggles.

(現在把 #ignore 關閉)

```
#ignore
```

```
#ACTIONS ARE IGNORED FROM NOW ON.
```

Muyi kisses you.

```
==> #action 的反應被關閉了.
```

(再開啟)

```
#ignore
```

```
#ACTIONS ARE NO LONGER IGNORED.
```

Muyi kisses you.
Your cheeks are burning.  =⇒ #action 的反應又出現了.

命令: KILLALL

語法

```
#killall
```

說明

#killall 將會刪除掉所有已讀入記憶體中的 #aliases, #actions, #subs, #antisubs, #highlights 和 #variables.

常用在當你需要讀另一個 tintin++ 的檔案進來時, 你可以不用離開 tintin++ , 直接載入新的檔案.

命令: LOOP

語法

```
#loop {起始值,終止值} {命令}
```

說明

如同一般程式語言的 for-next 迴路, #loop 命令會從啟始值一直加一

```
或減一到終止值為止. 而迴路計數器的值可以在命令中以 %0 去取用.
```

```
如果起始值大於終止值, 計數將會以加一的形式直到終止值;
如果起始值小於終止值, 計數將會以減一的形式直到終止值;
```

for examples:

```
#loop {1,3} {get all %0.corpse}
```

這一行命令可以展開成為:

```
get all 1.corpse;get all 2.corpse;get all 3.corpse
```

```
#loop {3,1} {drop %0.key}
```

這一行命令可以展開成為:

```
drop 3.key;drop 2.key;drop 1.key
```

再也沒有其它的科學, 能像電腦科學一樣, 擁有這麼多豐富動人的言詞了.
當您走入一塵不染的電腦室中, 仔細的將溫度控制在 25 度, 所要面對的,
居然是一堆病毒 (Virus 醫學類)、特洛伊木馬 (Trojan Horse 神話類)、
臭蟲 (bugs 生物類)、蠕蟲 (worm 生物類)、墜機 (crash 生活用語)、炸
彈 (bomb 武器類)、變性人 (sex changer)、致命的錯誤 (fatal error 像
電影片名吧)…其它還有許多特殊名詞, 都成為電腦人口中的慣用詞句.. ^.^

命令: LOG

語法

```
#log {檔案名稱}
```

說明

把這個 session 所有輸入和輸出的訊習存入 {檔案名稱} 中.

举例

```
#log Miyu.log   ==> 開始記錄
```

```
:
:         ==> 開始玩..^.^
:
```

```
#log Miyu.log   ==> 結束記錄
```

命令: MESSAGE

語法

#message {型別}

說明

當 tintin++ 的內部命令作業時, 是否要將 tintin++

```
所作的事顯示出來.
可以看到的訊息選項有:
alias, action, substitute, antisubstitute, highligh, variable.
一般說來, 當你在對 action 和 variable 的設定除錯時, 開啟 #message
可以看到 動作結果和您所設計的是否一樣.
```

命令: MARK

語法

```
#mark
```

說明

將上一個 path 清除, 並重新開始一個 path 存放您現在的位置.

命令: Map

語法

```
#map {方向}
```

說明

-  當您使用了 #map {方向} 後, {方向} 將會被加到目前的 path 尾端.

-  這個命令常在跟隨某人時使用.

举例

```
#action {$leader leaves %0.} {#map {%%0}}
```

假如說, 變數 #leader 中所設的領隊往某個方向離去, 這個方向將被加到path 的尾端.

譯注: 不過在原說明書中的範例, 在中文化的 Mud 上沒法子用了 (像 Dr 這種能切換中英文的是例外).

理由如下:

這個範例是英文, 抓不到同樣的訊息不能用呀..所以我們要改成中文…

```
#action {$leader 往%0離去} {#map {%%0}}
```

假設變數 leader = Laser, 訊息為: Laser 往東離去

這個 #action 就可以展開成為:

```
#action {Laser 往東離去} {#map {東}}
```

命令: MATH

語法

```
#math {變數名稱} {運算式}
```

說明

將 {運算式} 中的計算結果放入 {變數名稱} 中. #math 命令的運算式

```
和運算子的用法, 有點像 c 語言, 排列在下表的運算子, 越上面的運
算子, 具有越高的優先權.
```

運算子                       函式

---

!                            邏輯反運算 (logical not)
*                            數值乘法運算 (integer multiply)
/                            數值除法運算 (integer divide)
+                            數值加法運算 (integer addition)
-                            數值減法運算 (integer subtraction)
2m>                            大於 (傳回零或非零值)

=                           大於等於 (傳回零或非零值)

0m<                            小於 (傳回零或非零值)
⇐                           小於等於 (傳回零或非零值)
= or ==                      等於 (傳回零或非零值)
!=                           不等於 (傳回零或非零值)
& or &&                      邏輯及運算 (logical and) (傳回零或非零值)

| or |
|---|

比較的運算子 (如 >, >=, <, ⇐..etc), 當比較成立時會傳回真值 (True),
真值為任一不為零的數目字; 不成立則傳回假值 (Flase), 假值為零.
在運算式中, 你可以使用 T 和 F 表示真值或假值.
括號 () 在所有運算子中具有最高優先權, 所以, 在括號中的算式將最先被計算.

for examples:

```
#math {heals} {$mana/40}
```

假設說, 唸一次 heal 的法術要 mana 40 點, 這個算式就是用來計算您可以唸幾
次 heal 法術.

首先, 將變數 mana 除以 40, 然後放到 heals 這個變數中. heals 中的數值就
是您可以唸 heal 法術的次數.

以 basic 來寫就像這樣: heals = mana/40

```
#action {^你得到 %0 點經驗} {updatexp %0}
```

```
#alias updatexp {#math {xpneed} {$xpneed-%%0}
```

Hxpneed 是一個變數, 所代表的意思是升級尚需多少點經驗值.

當 #action 抓到 {^你得到 %0 點經驗} 的訊息時, 就會去把 %0 (得到的 exp)
傳給 alias “updatexp”, updatexp 這個 alias 就會把 xpneed 減掉 %0 (傳入
的所得 exp), 這樣就可以計算升級尚須多少 exp 了.

命令: # NAME

語法

```
#{session_name} {cmd}
```

說明

對  送出命令.

举例

假設我同時玩三個 Mud: Dr, Casamia, Arion.
這三個 Mud 的 session_name 分別為: dr, ca, ar.

目前我在的 session 為 dr, 假設我要在 Arion chat 'hiya OD'
就可以這樣子下命令:

```
#ar chat hiya OD
```

要在 Casamia 問 laser 事情,
就可以這樣子下命令:

```
#ca tell laser have u see my muyi? :
```

如果說, 只有打 #, 則會把主 session 切換到

假設主 session 現在是 dr,
輸入: #ar
這樣主 session 就切換到 Arion 去了.

命令: NOP

語法

```
#nop [字串]
```

說明

一個空命令. 在 #nop 之後的文字將不被 tintin++ 作任何用途,一般常可以用在作註解時用到.

举例

```
#nop --------------------------------------------------------------------------
#nop                              scoial alias
#nop --------------------------------------------------------------------------
#alias {cpat} {emote 輕輕拍拍 %0 的頭}
#alias {cthink} {emote 雙頰羞紅, 呆呆的正不知道在想什麼.;blush}
#alias {cplay} {emote 不知所措的玩弄著自己的長髮;blush}
#alias {cnod} {emote 雙頰羞紅, 輕輕的低下了頭;blush}
#alias {clag} {emote 因吃驚而呆住了..}
#alias {ccatch} {emote 露出依依不捨的表情, 雙手緊緊抓著 %0 的衣袖}
```

命令: PATH

語法

```
#path
```

說明

將目前的 path 內容顯示出來.

命令: PathDir

語法

```
#pathdir {單個方向} {使用 speedwalk 的解釋}
```

說明

設定當 #mark 後儲存的 path, 當使用 #return 命令時的對應.

举例

```
#pathdir {n} {u}
```

假設 path : n n n

您輸入: #return
如此, 將往上走, path: n n
所以, 一般都是設反方向: #pathdir {n} {s}
這樣回頭才會走對路. ^.^
不過, 某些特別設計的..呃..我啥都沒講唷..:p

命令: PRESUB

語法

```
#presub
```

說明

設定 #action 會不會被 #sub 所置換的訊息觸發動作.

举例

假設今天我們設一個 #sub 替換訊息:

```
#sub {%0 瀕臨死亡邊緣} {%0 瀕臨死亡邊緣...............  5% more.}
```

然後, 設一個 #action 如下:

```
#action {%0 瀕臨死亡邊緣...............  5% more.} {say poor mobile}
```

假如 #presub 設為 off, 範例中所設的 #action 就不會動作.

命令: RETURN

語法

```
#return
```

說明

將 path 中最後所存的方向取出, 並退回相反方向.

举例

假設 path 中現在內容為 : e s s w
#return 一次會將 w 取出, 並往 e 退回去一步.
path : e s s
再 #return : 往 n 退一步.
path : e s

命令: REDRAW

語法

```
#redraw
```

說明

假如您把 #redraw 設為開啟, 又沒有使用 #split 切割螢幕, 則您的

```
輸入字串會在 Mud 或 tintin++ 的訊息打斷後重新顯示出來.
```

命令: READ

語法

```
#read {檔名} or #read 檔名
```

說明

讀進另一個 tintin++ 命令檔到記憶體中. 假如這個命令檔中的命令之

```
前並未設定, 它將被載入記憶體中, 如果有重覆的命令名, 則新的命令
將覆蓋前面的就命令.
```

举例

```
#read miyu.tt
```

命令: SAVEPATH

語法

```
#savepath {alias name}
```

說明

將目前 path 中的內容存到一個 alias 中.

举例

設 path 內容為 : n n n w

```
#savepath {goprac}
```

則會多出一個 alias 叫 goprac, 內容為 {nnnw}

嗯..現在要講的命令是..史奴比!? :pp
the cute snoopy dog..
oh..是 snoop, not snoopy.. ccc :p

命令: SNOOP

語法

```
#snoop {session name}
```

說明

假如您用 tintin++ 同時開啟多個 session, 您可以用這個命令指定您要看

```
主 session 外的 session name 的訊息.
```

举例

假設我在 dr, casamia, arion 的 session name 分別為 : dr, ca, ar.
主 session 為 dr, 我想看 arion 發生的事.

```
#snoop ar
```

畫面就像這樣:
月野ちび兔閒聊說 'poor haska..'  =⇒ 這是主 session (dr) 的訊息

%ar 橘夢閒聊說 '呵呵呵..'        =⇒ 這是 arion (session ar) 的訊息.

命令: SHOWME

語法

```
#showme {字串}
```

說明

將 {字串} 送到終端機, 但不送到 mud 去. 常用在警告, 或給自己的特定訊息.

举例

```
#action {Laser has enter the game.} {#showme {Miyu, Laser login lo ^.^}}
```

當出現訊息 : Laser has enter the game, 你將看到..

Miyu, Laser login lo ^.^
Laser has enter the game.

命令: Session

語法

```
#session {session name} { }
```

說明

用來開啟一個 session, 其名稱為 {session name}, 連線的位址為

```
{ }
```

举例

```
#session {miyu} {drake.ntu.edu.tw 3000}
```

開啟一個進入 dr 的 session, session name 為 miyu

命令: Speedwalk

語法

```
#speedwalk
```

說明

設定 speedwalking 模式是開 (on) 或是關 (off)
什麼是 Speedwalking 呢? 簡單的說就是把你要走的路一次打出來, 重覆
的部份可以用數字取代次數.

举例

```
#speedwalk       ==> 設定 speedwalk mode on/off
```

假設現在為 on:
您要從 oz 的入口直奔去咬猴子, 要往西走 22 步, 您可以一次打 22 個 w,
tintin++ 就會把這 22 個 w 解釋成往 w 走 22 步, 而一次送出一個 w, 循
環 22 次.
您也可以改打成 : 22w , 這樣更省事. ^.^

命令: Split

語法

```
#split {訊息視窗行數}
```

說明

-  普通列表项目當您使用 vt100 或是 ANSI 終端機時, 您便可以設定 split screen.設定後, 您的鍵盤輸入將會在訊息視窗的下一行被顯示出來, 而輸入的訊息直到您按了 enter 鍵後才被送出.

-  這個模式的好處是, 可以使您的輸入不被 mud 或是 tintin++ 的訊息打斷. 不過如果您用 Ncsa telnet, 捲回去看 screen buffer 時, 卻看不到東西..

举例

```
#split 23      <= 把畫面從第 23 行切開.
```

命令: Substitute

語法

```
#substitute {要置換的訊息} {置換後的輸出}
```

說明

將從 mud server 送來的訊息改成您想要置換的訊息.
for examples:

```
#sub {%0 瀕臨死亡邊緣} {%0 瀕臨死亡邊緣...............  0% more.}
```

```
#sub {%0 快不行了.} {%0 快不行了................... 10% more.}
```

比如您打 mobile 時, 打到一半去看 mobile, 可以看到類似 xxx 快不行了..
這一類訊息, 現在, 可以加上明確的註解.
比如說, mud server 傳來 “a small puppet快不行了.”, 就會被替換成
“a small puppet 快不行了………………. 10% more.”

命令: Suspend

語法

```
#suspend
```

說明

```
暫時停止 tintin++ 的運作, 會到 unix shell 提示符號下.
這和您按下 control-z (^z) 的作用是一樣的. 您可以按 "fg"
回到 tintin++.
```

命令: System

語法

```
#system
```

說明

送一個 unix shell 的命令給 unix shell.
如同前面提過的, 可以用 chat 害您刪除您帳號下所有檔案 (rm -r * 那個 sample),
您可以試著把這個命令的名字換掉, 它被定義在 tintin.h 中.

举例

```
#system who
```

=⇒ 如同您在 unix shell 提示符號下鍵入 who 一樣的用途.可以看到有誰 login 到這台工作站上.

命令：TabAdd

** 注意：** 该命令已经由 #tab 命令取代

語法

```
#tabadd {word}
```

說明

增加一個給 tab 完成輸入功能用的單字.

举例

今天多了一隻叫 OrangeDream 的 imm, 我想 pk 她, 可是, 名字太長了,
但是她的 ID 沒在 tab.txt 中, 於是:

```
#tabadd {OrangeDream}
```

然後您就可以只打前幾個字, 再按 tab 鍵替您補完整了. ^.^
像這樣: k ora, 就變成: k orangedream  ^.*
(ah.. od..妳..妳不要..ah….hh..)

命令：tabdelete

語法

```
#tabdelete {word}
```

說明

刪除一個在 tab 輸入列表中的字.

命令：tablist

語法

```
#tablist
```

說明

列出所有在 tab 輸入列表中的字.

命令：textin

語法

```
#textin {檔名}
```

說明

#textin 可以讓您讀進一個檔案, 然後將這個檔案的內容送到 mud 去.

```
一般可以用在 imm 的線上創造(OnLine Create. OLC), 或寫長篇的 note
時, 非常方便..
```

命令：tick

語法

```
#tick
```

說明

顯示出離下一個 tick 到來的時間還有幾秒.

命令：tickon tickoff

語法

```
#tickon/#tickoff
```

說明

設定 Tintin++ 的 tick 計數器開 (on) 或是關 (off)
H

举例

#tickon   ⇐ 將 Tintin++ 的 tick 計數器開啟, 並重設 tick 計數時間.

```
您可以用 #ticksize 設定 tick 長度, 預設值為 75 秒
```

#tickoff  ⇐ 關閉 Tintin++ 的 tick 計數器.

命令：tickset

語法

```
#tickset
```

說明

將 Tintin++ 的 tick 記數器開啟, 並重設計數器的 tick 長度.

命令：ticksize

語法

```
#ticksize
```

說明

設定 tick 長度.

举例

#ticksize 30   ⇐ 將 tick 長度設為 30 秒.

命令：togglesubs

語法

```
#togglesubs
```

說明

就像 #ignore, #togglesubs 是 #sub 將置換訊息或否的開關.

命令：unaction

語法

```
#unaction {}
```

說明

取消一個 action.
H

举例

假設現在有一個 action: #action {Dragons has enter the game.} {smile Dragons}
現在要將它取消, 您可輸入: #unaction {Dragons has enter the game.}
而輸入:
#unaction {*has*}  , 則所有含有 “has” 這個字的 #action 都將被取消.
#unaction {has*}   , 則所有以 “has” 這個字開始的 #action 都將被取消.

命令：unalias

語法

```
#unalias {}
```

說明

取消一個 alias

举例

```
#unalias {*has*}  , 所有含有 "has" 這個字的 #alias 都將被取消.
```

```
#unalias {has*}   , 所有以 "has" 這個字開始的 #alias 都將被取消.
```

命令：unantisub

語法

```
#unantisub {}
```

說明

取消一個 antisub.

举例

參考 #unaction, #unalias.

命令：ungag

語法

```
#ungag {}
```

說明

取消一個 gag

举例

參考 #unaction, #unalias.

命令：unhighlight

語法

```
#unhighlight {}
```

說明

取消一個 highlights.
for example
參考 #unaction, #unalias.

命令：unpath

語法

```
#unpath
```

說明

將最後一個移動記陸從 path 中去掉.

举例

假設 path: e e e s u d

```
#unpath
```

變成 path: e e e s u

命令：unsplit

語法

```
#unsplit
```

說明

取消 split-screen 模式, 回到 full-screen 模式.

命令：unsubs

語法

```
#unsubs {}
```

說明

取消一個 sub.

举例

參考 #unaction, #unalias.

命令：UnVariable

語法

```
#unvariable {}
```

說明

取消一個 variable.

举例

參考 #unaction, #unalias.
命令: Variable

命令：variable

語法

```
#variable {變數名稱} {變數內容}
```

說明

這裡的變數和 %0-%9 的變數不同唷, 這裡的變數可以給你用一個你想要

```
用的字去命名.
而同名的變數在不同的 session 是分開的, 且不同的 session 改變變數
並不會互相干擾.
不過, 必需注意的是, 您不能使用類似像 miyu1, miyu2 這種類型的變項
, 這將在 Tintin 2.0 時支援..(天知道幾時出..:)
```

举例

```
#action {^[%1hp %2m %3mv]} {#var nhp %1;#var nmp %2;#var nmv %3}
```

這樣就可以把您的 hp/mana/mv 的現值存到自定的變數中.
嗯, robot 的基本..呃? 啊..沒事沒事..:p

命令：verbatim

語法

```
#verbatim
```

說明

設定 verbatim 模示的開啟或關閉. 當處於 verbatim 模示下, 所有

```
的文字將不被檢查, 且會對 Mud 送出 'as is' 字串.
以 tab 鍵完成輸入和 #history 兩項命令在 verbatim 模式下仍然
可以工作. 這將有益於撰寫訊息, 線上創作 (OLC)..等.
```

譯注: 這個功能人家到現在都不懂..以上大概的翻一下, 原文如下.

```
請知道的人告訴我好嗎..:p
```

Description:  Toggle  verbatim mode on and off.  When in verbatim
mode,  text will not be  parsed, and will be  sent 'as is' to the
mud.  Tab completion and history scrolling are still available in
verbatim mode.  It is  helpful for writing messages, doing online
creation, and the like.

命令：version

語法

```
#version
```

說明

```
顯式您目前用的 Tintin++ 的版本.
```

命令：wizlist

語法

```
#wizlist
```

說明

顯示出 Tintin++ 的作者群.

命令：write

語法

```
#write {}
```

說明

將您記憶體中的 alias, action, subs..等等內容回存到 {}中.

命令：zap

語法

```
#zap
```

說明

將所有在動作中的 sssion 關閉. 但是這個命令並不會將您的 characters

```
quit, 所以, 您的 characters 等於處於 lost link 的狀態.
```

1)
pwpw 收集自cc.fjtc.edu.tw的繁体中文手册

> 来源: https://www.pkuxkx.net/wiki/tintinpp/manual
