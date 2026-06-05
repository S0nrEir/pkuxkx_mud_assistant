- MushClient3.78中文版

- MushClient4.12中文版

- MushClient4.18中文版(英简繁)

- MushClient4.43北侠集成版补丁

- MushClient版北侠路径

- MUSHclient中文手册

- Mud客户端下载

- 【MUSHClient】北侠集成版补丁2.0

下载方式：到QQ群152814678的群共享里面搜索下载“神灯教新手套装1.4”。

注意：mushclient499+504(含汉化常用插件) 里面499和504版本任选一个即可，注意安装目录不要有中文。

MushClient3.78中文版

优点：迄今为止最为强大的Mud客户端，功能及其强大，支持代理，对脚本语言的支持无比强大，最中文支持很好，稳定性完美

缺点：自身函数功能差，需要编程基础

下载页面

---

MushClient4.12中文版

优点：迄今为止最为强大的Mud客户端，功能及其强大，支持代理，对脚本语言的支持无比强大，最中文支持很好，稳定性完美

缺点：自身函数功能差，需要编程基础

汉化说明：文件里有个“MUSHclient412_Locale_ch.rar”，把里面两个汉化文件解压到mush安装目录下面的locale文件夹；打开mush，file—global preferences—general，在locale那里填入ch，确定，再重启mush就变成中文了。
如果用比4.12高的版本这两个汉化文件还是可以用的，不过global preferences会出问题。

下载页面

---

MushClient4.18中文版(英简繁)

优点：MUSHclient 是一个功能极其强大的 MUD/MUSH 客户端，支持压缩协议，MUD 扩展协议，速度比同类的软件要快很多。支持各种脚本语言，如 Lua、JavaScript 和 VBScript，你可以做出功能非常完善的机器人，实在是挖泥利器，比 zMUD 毫不逊色，相信你会喜欢它。另外，它对中文的支持非常好。

缺点：喜欢就好，因人而异＾＿＾这只是一个格式。

p.s.以下下载页面是“MUSHclient 爱好者网站”的下载页，喜欢的朋友不妨关注一下。

下载页面

---

MushClient4.43北侠集成版补丁

【MUSHClient】4.43北侠集成版，集成了汉化补丁，fullme插件，北侠路径插件，mush运行环境配置，共四部分内容，欢迎下载使用。

下载安装使用说明及原帖地址：
【MUSHClient】4.43北侠集成版

---

MushClient版北侠路径

由Muxiao提议，Duno、Ddid大力修改而成

下载页面

---

注意：MUSH的显示混乱问题（如：使用命令 “i” 查看装备，发现界面混论）通常而言都是设置问题，可以通过设置解决。以Mush499中文版为例：成功连接游戏后，在mush中点击 “文件 → 游戏属性 → Appearance → output”中，找到“输出窗口中自动换行的列号”，把前面的勾去掉，或者在后面输入框中输入一个较大的数（如500），点击“确定”，基本可以解决显示混乱的问题。

北侠yhzzyahoo出品的入门教材：粗学mush----mush简单教程

推荐一个专业性很强的mush教材，北侠lzkd出品，必属精品：

-  初级篇：MUSHclient实用型教程（北侠版mush实用教程）

-  还有中级篇：【MUSHClient】中级教程（完）（北侠版）

-  最后是这个：【MUSHclient】教程中文手册1.1

MUSHclient中文手册

出品人：小刀（Lzkd）

内容部分来自北侠mush技术高手原创，部分来自一个MUSHclient中文网站，地址手册上有。模板来自MUSHclient官网。内部图片采用侠logo。支持全文搜索功能，可以在Big5环境正常使用

内容列表：

-  MUSHclient的安装及汉化

-  MUSHclient的配置（按照Zmud习惯进行配置）

-  MUSHclient的简单应用（其中正则相关部分花了我许多心血）

-  MUSHclient的服本环境配置(for Lua)

-  MUSHclient所有函数介绍

-  闲来添杯酒－－北侠玩家文选－北侠给人很放松的感觉，就象闲时喝一杯淡淡的酒

-  淡笑看红尘－－北侠巫师文选－巫师是远远的在天上看着我们这些红尘中人的

手册文件为2.14M的chm附件

【MUSHclient】中文手册

---

Mud客户端下载

【MUSHClient】北侠集成版补丁2.0

```
欢迎来到北大侠客行。
您现在使用的是北侠MUSHClient 集成版2.0，该版本已经集成了北侠路径插件
及北侠fullme插件。关于fullme，请参考http://www.pkuxkx.net/forum/thread-9706-1-5.html，
关于北侠资料，请参考http://www.pkuxkx.net/wiki/。

您需要下载并用安装最新的MUSHClient，很抱歉，因为能力原因，无法做到直接安装。将原版和集成包
都安装完毕后，运行 MUSHclient，按 Ctrl+Alt+G，在“General（常规）”对话框的右下角把语言代码改
成 CH，保存后退出 MUSHclient，下次运行就可以看到效果了。
如果想使用北侠fullme插件，还需要允许载入dll文件，及打开沙箱。具体做法是：点击文件－－全局属性
－－Lua－－选中“允许载入dll文件”。
然后再点编辑，找到package.loadlib = ReportDisabled  ("package", "loadlib") -- disable loadlib function这一行，在前面加上“--”，就可以了。

MUSHclient的所有设置都已经按照Zmud的习惯设置好了，只要您使用worlds目录下的pkuxkx_link.MCL
进行连接就可以。如果您觉得这些设置还不能令您满意，请参考http://www.pkuxkx.net/forum/thread-9546-1-1.html，
如果您觉得这个教程已经不能令您满足，请参考北侠版MUSHclient中文手册http://pkuxkx.net/wiki/course/mushclient，
如果您还有什么疑问，请到论坛提问，相信北侠的玩家会热情回答您的问题http://www.pkuxkx.net/forum/。
路径文件的使用请看http://www.pkuxkx.net/forum/thread-17542-1-1.html。（感谢littleknife提供路径文件）

如果有什么问题和建议，请在北侠论坛PM lzkd。
希望您在北侠游戏愉快。

by 小刀(lzkd)

2011.1.9

版本更新说明

2011.1.9 因北侠地图大变动，重新更新路径文件，升级到2.0版本，感谢littleknife提供路径文件。
2010.1.16 完成1.0版。
```

原帖地址

---

> 来源: https://www.pkuxkx.net/wiki/mush/all
