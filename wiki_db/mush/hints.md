LUA 的协同程序
协同程序在写mud机器人提供了一种灵活的机制。
local co=nil
co=coroutine.create(function()  –协同程序创建
–todo something
end)
这时候协同程序并没有工作，是挂起状态
coroutine.resume(co)  –协同程序开始运行
在mud编程中，协同在异步处理时候很方便灵活。
我举一个例子让大家理解下
比如 我们在房间A 做一个动作a 在房间B 做一个动作b
我们原来是rbt 做法是
设置A 房间 的触发器，触发逻辑a
设置B房间 的触发器，触发逻辑b
然后look ，触发器获得触发，机器人工作正常，一切ok。
但是有一天你想修改下机器人
在特殊条件下，你想在B房间 触发动作c，为了使机器人正常工作
你在动作b之前加了if 判断语句。然后写了一个分支c过程
机器人通过测试，工作正常。
现在又有新特殊条件，B房间又要做一个新触发逻辑d
结果你几次修改后，B 触发器里面的逻辑会变成这样
if condition1 then a.
if condition2 then b.
if condtion3 then c.
…..
逻辑判断语句一大堆。

现在来看看怎么用lua协同来写机器人的
co=coroutine.create(function()  –协同程序创建
–todo something
Send(“look”)  – look命令
AddTriggerEx (“roomA”, “A房间触发语句”, “coroutine.resume(co)”, trigger_flag.RegularExpression + trigger_flag.Enabled + trigger_flag.Replace,custom_colour.NoChange, 0, “”, “”, 12, 99)
coroutine.yield()  –挂起 等待抓取房间描述结束
–处理 逻辑 a  b
a()
end)
coroutine.resume(co) –启动协同程序
你比较下是否简洁很多。
触发器作用只是把刚才没有执行完的中断逻辑继续执行下去。没有大量逻辑判断写在触发器中。
这样写还会带来另一个额外的好处。
如果你的程序中有个A房间触发器没有关闭，这时候有条屏幕上语句正好触发了它，结果会发生什么事情？
结果就是你会屁颠屁颠跑去执行这个逻辑，最后机器人出错。
要是用协同程序写会怎么样呢？
A触发器coroutine.resume(co) 让co继续运行，协同程序状态已经dead，结果什么也没有发生，程序可靠性提高很多

> 来源: https://www.pkuxkx.net/wiki/mush/hints
