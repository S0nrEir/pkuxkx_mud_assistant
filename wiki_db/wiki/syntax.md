- 格式规则

- 文档基础格式

- 链接

- 外部链接

- 内部链接

- 跨Wiki链接

- 共享

- 图片链接

- 脚注

- 小节

- 三级标题

- 图片和其他文件

- 列表

- 表情

- 样式

- 应用

- 表格

- 无编译区块

- 高亮格式

- HTML与PHP代码嵌入

- 格式插件

格式规则

DokuWiki 支持一些能尽量地使资料具有较强的可读性的简单的标记语言。这个页面归纳了在你编辑页面时可能使用的所有格式。只要点击页顶或页底的 *编辑本页* 按钮，就可以查看本页的源代码。如果你想尝试编写一些东西，请到 playground 页面。这种简易的标记语言也可通过 quickbuttons 查看。

**请注意：北侠WIKI支持MARKDOWN语法扩展，请使用<markdown> </markdown>标记将markdown语法内容嵌入wiki网页中即可。如：

<markdown>

# Header

</markdown>**

与wiki相关的markdown语法请参照：[markdown插件语法说明](https://www.dokuwiki.org/plugin:mdpage)

也可以在编辑页面采用支持所见即所得的在线markdown语法编辑器插件来进行编辑，只要在编辑器中点击箭头所指位置即可（第一次加载可能要等待一会儿）：

效果如下图所示：

**但是别忘了编辑完回到wiki编辑器时将所编辑的内容用<markdown> </markdown>标记包含。**

小幅或零散编辑已有内容时不建议混合使用wiki与markdown语法，可能引起显示混乱，也增加其他人修改的难度。

---

文档基础格式

DokuWiki 支持 **加粗**, *斜体*, *下划线* 和 `加宽` 的文本。当然你也可以 ****`综合使用`**** 这些格式

```
DokuWiki 支持 **加粗**, //斜体//, __下划线__ 和 ''加宽'' 的文本。
当然你也可以 **__//''综合使用''//__** 这些格式。
```

你也可以使用 下标 和 上标。

```
你也可以使用 <sub>下标</sub> 和 <sup>上标</sup>。
```

你也可以用 删除号 进行标记。

```
你也可以用 <del>删除号</del> 进行标记。
```

**段落** 从空白行开始。如果你想不回车便 **另起一行** ，你可以在句末使用两个反斜杠，后面加上一个空格。

这是有换行的一段话

请注意，两个反斜杠只是被认为是一行的结束

后面要有

一个空格 \\没有空格就会这样

```
这是有换行的一段话\\ 请注意，
两个反斜杠只是被认为是一行的结束\\
后面要有\\ 一个空格 \\没有空格就会这样。
```

如果真的需要的话，你可以这样强制换行。

链接

DokuWiki 支持许多创建链接的方法。

外部链接

外部链接可以被自动识别： http://www.google.com 或者仅仅是 www.google.com —— 你也可以设置链接名： 这个链接指向google。像这样的Email地址： andi@splitbrain.org 也能被识别。

```
DokuWiki 支持许多创建链接的方法。外部链接可以被
自动识别： http://www.google.com 或者仅仅是 www.google.com —— 你也可以
设置链接名: [[http://www.google.com|这个链接指向google]]。像这样的
Email地址： <andi@splitbrain.org> 也能被识别。
```

内部链接

内部链接用方括号创建。你可以使用 wiki:页面名 或者使用 页面标题。Wiki的页面名称会自动转为小写体，但不支持特殊字符。

```
内部链接用方括号创建。你可以使用
[[doku>wiki:页面名]] 或者使用 [[doku>wiki:页面名|页面标题]]。Wiki的页面名称
会自动转为小写提，但不支持特殊字符
```

你可以在这个页面使用一个冒号表示 命名空间 。

```
你可以在这个页面使用一个冒号表示 [[wiki:命名空间]] 。
```

命名空间的详细说明请看 wiki:namespaces。

也可以创建指向某一小节的链接。只需如HTML语言一样在#号后面写上小节名称。这个链接指向 这一小节。

```
这个链接指向 [[syntax#内部链接|这一小节]].
```

注意：

-  指向 存在的页面 的链接与 不存在的页面 的表现方式不同。

-  DokuWiki 不使用 骆驼拼写法 来创建链接，但是可以通过 config 来启用这种拼写方式。注意：如果 DokuWiki 是一个链接，那么这是允许的。

-  当一个小节的标题改变时，它的书签也需要改变。所以不能太过于依赖书签。

跨Wiki链接

DokuWiki支持 跨Wiki链接 。这些链接可以迅速的连向其它的Wiki。比如，这是一个连向 Wikipedia's 的关于Wiki的链接： Wiki。

```
DokuWiki支持 [[doku>wiki:interwiki|跨Wiki链接]] 。这些链接可以迅速的连向其它的Wiki。
比如，这是一个连向 Wikipedia 的关于Wiki的链接： [[wp>Wiki]]。
```

共享

像 这样 的共享也能被识别。请注意，这只在像公司的 Intranet 这样的同性质用户组里才能生效。

```
像 [[\\server\share|这样]] 的共享也能被识别。
```

注意：

-  因为安全原因，对共享的直接浏览只能通过Microsoft Internet Explorer进行（仅在“本地区域”）。

-  对于Mozilla和Firefox浏览器，可以通过 security.checkloaduri 的设置开启，不过不建议这样做。

-  点击 151 查看更多信息。

图片链接

你也可以通过综合运用常规链接和 片句法 规则来建立通往内部或者外部页面的图片链接（如下）：

```
[[http://www.php.net|{{wiki:dokuwiki-128.png}}]]
```

请注意：图片句法是链接名中唯一允许的句法格式。

DokuWiki支持 图片句法 和 链接 格式（包括图片大小调整，内部和外部图片，超链接以及跨Wiki链接）。

脚注

你可以通过双括号加入脚注 1) 。

```
你可以通过双括号加入脚注 ((这是脚注)) 。
```

小节

你可以使用五种不同级别的标题来构建你的文章。如果你有三个以上的标题，就会自动生成列表——这可以通过在文档种加入 `~~NOTOC~~` 字符串来取消。

三级标题

四级标题

五级标题

```
==== 三级标题 ====
=== 四级标题 ===
== 五级标题 ==
```

使用四个以上的破折号，你可以创建一条分割线：

---

图片和其他文件

你可以通过花括号显示 images 。你还可以设定图片的尺寸。

实际尺寸：

重设宽度：

重设宽度和高度：

重设尺寸的外部图片：

```
实际尺寸：                        {{wiki:dokuwiki-128.png}}
重设宽度：                        {{wiki:dokuwiki-128.png?50}}
重设宽度和高度：                  {{wiki:dokuwiki-128.png?200x50}}
重设尺寸的外部图片：              {{http://de3.php.net/images/php.gif?200x50}}
```

通过左右空格，你可以设置对齐方式

```
{{ wiki:dokuwiki-128.png}}
{{wiki:dokuwiki-128.png }}
{{ wiki:dokuwiki-128.png }}
```

当然，你也可以加入说明文字（作为给浏览者提供的提示）。

```
{{ wiki:dokuwiki-128.png |这是说明文字}}
```

如果你使用的是非图片（`gif,jpeg,png`）的文件名（外部或者内部）那么它会被作为一个链接。

对于把图片链接向另外一个页面的运用，请见上面的 图片链接 。

列表

Dokuwiki支持有序和无序列表。为了创建一个列表条目，你需要在文本前面加入两个空格和一个`*`来表示无序列表，或者用`-`表示有序列表。

-  这是个列表

-  第二条

-  可以设置不同的级别

-  另外一条

-  同样的列表，有序的

-  第二条

-  使用缩进表示深层级别

-  这就是了

```
* 这是个列表
* 第二条
* 可以设置不同的级别
* 另外一条

- 同样的列表，有序的
- 第二条
- 使用缩进表示深层级别
- 这就是了
```

表情

DokuWiki包含了常用的表情（emoticon）。可以在`smiley`文件夹里添加更多表情并在`conf/smileys.conf`文件中进行配置。这是DokuWiki的表情综览。

-     8-)

-     8-O

-     :-(

-     :-)

-      =)

-     :-/

-     :-\

-     :-?

-     :-D

-     :-P

-     :-O

-     :-X

-     :-|

-     ;-)

-     ^_^

-     :?:

-     :!:

-     LOL

-     FIXME

-    DELETEME

样式

DokuWiki可以通过简单的文本符号来表示特殊符号。这是能够被识别的符号的例子。

→ ← ↔ ⇒ ⇐ ⇔ » « – — 640×480 © ™ ®
“他想道'这是人类的世界'…”

```
-> <- <-> => <= <=> >> << -- --- 640x480 (c) (tm) (r)
"他想道'这是人类的世界'..."
```

请注意：这些变化可以通过 配置选项和 模式文件关闭。

应用

有时你想表明一些话是回答或者评论，你可以使用这样的格式：

```
I think we should do it

> No we shouldn't

>> Well, I say we should
```

```
> Really?

>> Yes!

>>> Then lets do it!
```

I think we should do it

No we shouldn't

Well, I say we should

Really?

Yes!

Then lets do it!

表格

DokuWiki支持简易制表。

| 标题 1 | 标题 2 | 标题 3 |
|---|---|---|
| 1 行 1 列 | 1 行 2 列 | 1 行 3 列 |
| 2 行 1 列 | 单元格合并（注意双分隔符） |
| 3 行 1 列 | 3 行 2 列 | 3 行 3 列 |

表格的标题行通过`^`来做首尾，普通行通过`|` 来做首尾。

```
^ 标题 1      ^ 标题 2       ^ 标题 3          ^
| 1 行 1 列   | 1 行 2 列    | 1 行 3 列       |
| 2 行 1 列   | 列合并（注意双分隔符）        ||
| 3 行 1 列   | 3 行 2 列    | 3 行 3 列       |
```

如果要进行行合并，只需像上面那样，让下一单元格留空。确认每一行有相同数量的单元格分隔号！

纵向表头也能设置

|  | 标题 1 | 标题 2 |
|---|---|---|
| 标题 3 | 1 行 2 列 | 1 行 3 列 |
| 标题 4 | 这次不进行列合并 |  |
| 标题 5 | 3 行 2 列 | 3 行 3 列 |

正如你所见，单元格的格式由它前面的单元格分隔号决定：

```
|          ^ 标题 1          ^ 标题 2      ^
^ 标题 3   | 1 行 2 列       | 1 行 3 列   |
^ 标题 4   | 这次不进行列合并|             |
^ 标题 5   | 3 行 2 列       | 3 行 3 列   |
```

注意：不支持行合并

你也可以设置对其方式，只要在文本的两面加入两个以上的空格：左面加入两个空格进行右对齐，右面加入两个空格进行右对齐，两边至少两个空格进行居中。

| 表格对齐方式 |
|---|
| 右对齐 | 居中 | 左对齐 |
| 左对齐 | 右对齐 | 居中 |
| xxxxxxxxxxxx | xxxxxxxxxxxx | xxxxxxxxxxxx |

这是源代码的表示：

```
^           表格对齐方式                   ^^^
|        右对齐|     居中     |左对齐        |
|左对齐        |        右对齐|     居中     |
| xxxxxxxxxxxx | xxxxxxxxxxxx | xxxxxxxxxxxx |
```

无编译区块

你可以通过在行首加入两个以上的空格（就像上面的例子）或者使用`code`或`file`的标签来表示无编译区块。

```
这是所有内容都保留的代码：就像              <-这样
```

```
这个非常类似，但是你可以用它来表示你引用了一个文件
```

为了让解析器完全忽略一块区域（也就是说不对其进行编译），可以附上`nowiki`的标签，或者更简单的是，使用两个百分号`%%`。

这是一段包含这样的地址的文字：：http://www.splitbrain.org 和 **编译**，但是它们没被编译。

请查看这段内容的源代码来查看如何使用这些手段。

高亮格式

DokuWiki可以将一段代码高亮，使它更易阅读。这是使用 GeSHi 通用格式高亮器——支持GeSHi的语言都支持它。这个格式和前面一小节的代码区段很像，但是这次使用的语言标志是插入到标签内，比如`<code java>`。

```
/**
* The HelloWorldApp class implements an application that
* simply displays "Hello World!" to the standard output.
*/
class HelloWorldApp {
public static void main(String[] args) {
System.out.println("Hello World!"); //Display the string.
}
}
```

以下字符串都能被正确识别：*actionscript, actionscript-french, ada, apache, applescript, asm, asp, autoit, bash, blitzbasic, caddcl, cadlisp, c, c_mac, cfm, cpp, csharp, css, delphi, diff, d, div, dos, eiffel, freebasic, gml, html4strict, ini, inno, java, java5, javascript, lisp, lua, matlab, mpasm, mysql, nsis, objc, ocaml, ocaml-brief, oobas, oracle8, pascal, perl, php-brief, php, python, qbasic, scheme, sdlbasic, smarty, sql, tsql, robots, ruby, vb, vbnet, vhdl, visualfoxpro, xml*

HTML与PHP代码嵌入

你可以通过使用`html` or `php`标签来向文档内嵌入HTML或PHP代码：

```
<html>
This is some <font color="red" size="+1">HTML</font>
</html>
```

`This is some <font color="red" size="+1">HTML</font>`

```
<php>
echo 'A logo generated by PHP:';
echo '<img src="' . $_SERVER['PHP_SELF'] . '?=' . php_logo_guid() . '" alt="PHP Logo !" />';
</php>
```

`echo 'A logo generated by PHP:';
echo '<img src="' . $_SERVER['PHP_SELF'] . '?=' . php_logo_guid() . '" alt="PHP Logo !" />';`

**请注意**：HTML和PHP嵌入在配置里面默认关闭。如果关闭，代码会被显示而不是被编译。

格式插件

DokuWiki的格式可以通过 插件 扩展。使用说明里有如何使用已安装的插件的描述。以下格式插件在这个版本的DokuWiki上是可用的：

~~INFO:syntaxplugins~~

1)
这是脚注

> 来源: https://www.pkuxkx.net/wiki/wiki/syntax
