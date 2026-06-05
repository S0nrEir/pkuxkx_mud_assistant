PaoTin++：北侠最火爆的新生代客户端

快速前往：
官网主页 ※ 亮点功能 ※  特性介绍

- 1-下载安装

- 2-截图预览

- 3-新手上路

- 4-完全手册

- 5-通关秘籍

- 6-贝海拾珠

加载中...>>前往此页面

如何安装 PaoTin++

几乎所有的操作系统都可以一键安装 PaoTin++，不同的操作系统之间机器可以通用。请选择你的操作系统以查看具体步骤：

Windows

第一步，到 Windows 商店里寻找安装一个 Windows Terminal（简称 WT）。如果你没有 Windows 商店，那么也可以从这里下载 WT。

下载后解压，其中的 `wt.exe` 就是主程序。但是，**先不要双击**，因为还有第二步。

第二步，到这里选择一个较新的安装包并下载安装 PaoTin++ for Windows。

第三步，打开第一步安装好的 WT，并从下拉列表里寻找「北大侠客行」即可开始游戏。

如果你是个好奇宝宝，第一步就已经双击过 `wt.exe` 了的话，要先关掉窗口重新双击打开。

更详细的安装说明请阅读米娃的《PaoTin++ for Windows 开箱教程》。其中也包含了安装后如何自动登录。

使用过程中如果遇到问题也可以查阅 PaoTin++ for Windows 常见问题（FAQ）。

Android

第一步，先到你的应用商店下载一个 Termux，如果应用商店里找不到，可以从官网下载。如果官网无法访问，可以从这里下载。

第二步，打开 Termux，在其中以复制粘贴方式执行下面的命令：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/termux-install | bash
```

如果全部正常的话安装就算是完成了。

第三步，杀掉 Termux 进程，重启。输入 `pt` 然后回车就可以进入 PaoTin++ 了。以后每次进入也都只需要输入 `pt` 即可，不需要再做第一步和第二步。

iOS

第一步，先到你的应用商店里下载一个 iSH Shell。

第二步，打开 iSH Shell，在其中以复制粘贴方式执行下面的命令：

```
wget -qO - https://chat.unix5.com/mudclient/paotin/raw/install/ish-install | sh
```

如果全部正常的话安装就算是完成了。

第三步，杀掉 iSH 进程，重启。输入 `pt` 然后回车就可以进入 PaoTin++ 了。以后每次进入也都只需要输入 `pt` 即可，不需要再做第一步和第二步。

macOS

第一步，安装依赖。（没用过 brew 的同学请看这里，需要先安装 brew）

```
brew update && brew install gcc make gnutls pcre zlib git bash tmux curl neovim
```

第二步，安装完依赖之后，统一用下面的命令就可以安装：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/unix-install | bash
```

第三步，如果上面全部正常的话安装就算是完成了。然后输入 `cd ~/paotin && ./paotin-start` 就可以开始游戏。

聪明的人肯定知道可以将它做成别名以节省输入。

Ubuntu

第一步，安装依赖。

```
sudo apt update && sudo apt-get install -y build-essential zlib1g-dev libpcre3-dev git bash tmux curl neovim
```

第二步，安装完依赖之后，统一用下面的命令就可以安装：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/unix-install | bash
```

第三步，如果上面全部正常的话安装就算是完成了。然后输入 `cd ~/paotin && ./paotin-start` 就可以开始游戏。

聪明的人肯定知道可以将它做成别名以节省输入。

Debian

第一步，安装依赖。

```
sudo apt update && sudo apt-get install -y build-essential zlib1g-dev libpcre3-dev git bash tmux curl neovim
```

第二步，安装完依赖之后，统一用下面的命令就可以安装：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/unix-install | bash
```

第三步，如果上面全部正常的话安装就算是完成了。然后输入 `cd ~/paotin && ./paotin-start` 就可以开始游戏。

聪明的人肯定知道可以将它做成别名以节省输入。

Fedora

第一步，安装依赖。

```
sudo yum install -y which make gcc zlib-devel pcre-devel git bash tmux curl neovim
```

第二步，安装完依赖之后，统一用下面的命令就可以安装：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/unix-install | bash
```

第三步，如果上面全部正常的话安装就算是完成了。然后输入 `cd ~/paotin && ./paotin-start` 就可以开始游戏。

聪明的人肯定知道可以将它做成别名以节省输入。

CentOS

第一步，安装依赖。

```
sudo yum install -y which make gcc zlib-devel pcre-devel git bash tmux curl
```

第二步，安装完依赖之后，统一用下面的命令就可以安装：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/unix-install | bash
```

第三步，如果上面全部正常的话安装就算是完成了。然后输入 `cd ~/paotin && ./paotin-start` 就可以开始游戏。

聪明的人肯定知道可以将它做成别名以节省输入。

已知问题： CentOS 7 及以前的版本中，tmux 的版本太低，建议手动升级至 3.X 版本。

openSUSE

第一步，安装依赖。

```
sudo zypper update -y && sudo zypper install -y git bash tmux gcc make pcre-devel zlib-devel curl neovim
```

第二步，安装完依赖之后，统一用下面的命令就可以安装：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/unix-install | bash
```

第三步，如果上面全部正常的话安装就算是完成了。然后输入 `cd ~/paotin && ./paotin-start` 就可以开始游戏。

聪明的人肯定知道可以将它做成别名以节省输入。

Alpine

第一步，安装依赖。

```
sudo sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
sudo apk update
sudo apk add --no-cache git gcc libc-dev zlib-dev zlib-static pcre-dev make curl
sudo apk add --no-cache tmux bash ncurses less neovim nano
```

第二步，安装完依赖之后，统一用下面的命令就可以安装：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/unix-install | bash
```

第三步，如果上面全部正常的话安装就算是完成了。然后输入 `cd ~/paotin && ./paotin-start` 就可以开始游戏。

聪明的人肯定知道可以将它做成别名以节省输入。

Docker on Linux

如果你本地已经安装好了 Docker 环境，使用下面命令就可以立即开始**体验 PaoTin++**：

```
docker run --rm -it --name pt-taste --hostname pt-taste mudclient/paotin
```

上面的命令会自动下载 Docker 镜像，创建 Docker 容器，然后启动游戏界面，开始体验。

如果一切正常，你将会看到一个带有蓝色状态栏的 tmux 界面。和一个简单的游戏指引。

如果想要结束体验，可以按 `<ctrl+a> d` 组合键，就会退出游戏，并自动删除刚刚创建的 Docker 容器。

但是！！！ **上面的方法只是让你用来体验 PaoTin++，并不能用来长期挂机**。

如果你想要长期挂机，则要使用下面的命令：

```
# 创建游戏目录结构
mkdir -p $HOME/my-paotin/{ids,ids,data,log,plugins}

docker run -d -it --name pt --hostname pt -v $HOME/my-paotin:/paotin/var mudclient/paotin:beta daemon
```

以后每次上线的时候，只需要用下面的命令就可以连接到 UI：

```
docker exec -it pt start-ui
```

同样可以用 `<ctrl+a> d` 组合键退出游戏。但这并不会终止 PaoTin++ 挂机，下次用上面的命令可以继续游戏。

Docker on Windows

进入 cmd.exe，依次输入以下命令，以建立游戏目录：

```
mkdir $HOME/my-paotin/
mkdir $HOME/my-paotin/ids
mkdir $HOME/my-paotin/etc
mkdir $HOME/my-paotin/data
mkdir $HOME/my-paotin/log
mkdir $HOME/my-paotin/plugins

docker run -d -it --name pt --hostname pt -v $HOME/my-paotin:/paotin/var mudclient/paotin:beta daemon
```

以后每次上线的时候，只需要用下面的命令就可以连接到 UI：

```
docker exec -it pt start-ui
```

同样可以用 `<ctrl+a> d` 组合键退出游戏。但这并不会终止 PaoTin++ 挂机，下次用上面的命令可以继续游戏。

FreeBSD

第一步，安装依赖。

```
sudo pkg update && sudo pkg install -y gcc make++ pcre zlib-ng git bash tmux curl neovim
```

第二步，安装完依赖之后，统一用下面的命令就可以安装：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/unix-install | bash
```

第三步，如果上面全部正常的话安装就算是完成了。然后输入 `cd ~/paotin && ./paotin-start` 就可以开始游戏。

聪明的人肯定知道可以将它做成别名以节省输入。

OpenBSD

第一步，安装依赖。

```
sudo pkg_add -u && sudo pkg_add pcre git bash curl neovim
```

第二步，安装完依赖之后，统一用下面的命令就可以安装：

```
curl -sL https://chat.unix5.com/mudclient/paotin/raw/install/unix-install | bash
```

第三步，如果上面全部正常的话安装就算是完成了。然后输入 `cd ~/paotin && ./paotin-start` 就可以开始游戏。

聪明的人肯定知道可以将它做成别名以节省输入。

新用户安装好之后强烈推荐阅读本教程：本雪的《新手向炮艇驾驶手册》

>>前往此页面

> 来源: https://www.pkuxkx.net/wiki/tools/paotin
