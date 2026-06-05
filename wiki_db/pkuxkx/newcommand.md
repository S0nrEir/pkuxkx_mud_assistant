近期命令

---

- 前言：北侠的输入命令和set太多太杂了，这里的目的是跟以前的普通指令区分开来主要记录着WIZ近期新增的一些命令和set。

| 指令或set | 指令或set的作用详解 |
|---|---|
| set death_report | 设定为1的时候，死亡时会显示损失信息，就是即时生成的一份简报。不设定也会自动附加在death_log，不影响提交bug，设定了就是可以实时通知一下损失。 |
| death_log persist | death_log 增加 persist参数，比如death_log persist 1就会保存第一条死亡记录，不会被后续死亡顶掉，但是每个人只能保存一条这种永久记录（之后再次death_log persist 2会被第二条记录顶掉），应用场景，报告自己的bug导致死亡。有了这条命令之后不再接受不能提供系统log的申诉。 |
| trait reset | 大宗师级别会随机替换掉不喜欢的特征到同级别的其他特征。自在境可以指定trait reset with本月内有效，注意这里的有效并不是28天，30天或者31天。比如你在6月1日或者6月29日替换都只能用到6月底7月就会重置回老特征以及重新获得重置机会。主动替换之后trait和score都会看到新的列表，系统重置会老的特征，trait是立刻体现，score会因为有cache延迟。 |
| set feilong | 可设置为1或者0（默认），默认状况下是一招晕飞龙，保留原来设定，可以无激发使用，无需气势，600秒cd设置为1的情况下是化学攻击，需要激发使用,需要16点气势（消耗6点），8秒cd化学基础算法一样，攻击威力提升和内功境界相关。 |
| sm last_death | 复盘上次死亡时候战斗细节。和combat_brief相比更注重对手的细节。分解到每个pfm对手使用了多少次，方便分析自身弱点。 |
| zhuan zhu | 专注(zhuanzhu)为公共职业特技，但非朱雀（含凤凰）职业使用专注会有伤害惩罚，白虎击中专注对象，消减15%，青龙和玄武消减20%，无职业玩家使用专注消减50%。举例：战斗中对手是甲乙丙低，你是青龙，专注了甲，打中甲正常伤害1000，消减到800，打中乙、丙、丁，伤害还是1000不会被消弱。 |
| realm | 查看内功境界，realm next看自己内功境界以及到下一个内功境界程度，而who -l -realm这个指令是查看所有玩家内功达到内功境界的状况 |
| score -growth | 可以获取自己最多最近12个月的历史记录，比较自己的成长曲线。 |
| duihuan 1.2M | 浑天仪兑换经验支持额外格式,duihuan 1.2m就是1200000。 |
| who -year | 比较伤感的一个指令，看到同期生还有谁在，没想到08年的就我一个号还在，yearbook命令作为who -year的补充，yearbook -l 同年玩家的详细信息（彩色是100天之内登陆过的，灰色是超过100天没有登陆的）yearbook id 类似who id，不过过滤到你的同年玩家。 |
| stat lethal_pfms | 统计从上周开始玩家真死前中的pfm，斗转yyds |
| set refuse_family_rescue | 假死不被同门救走，依然是以前进鬼门关的假死 |
| enable 命令增加save/restore选项 | enable save会保存你当前enable和prepare的内容，restore会尝试把它们激发，bei回去 |
| set 增加-share 功能 | 获得一个字符窜，可以把自己的环境变量共享给任何人，其他玩家输入set -share 将尝试设定和提供共享玩家一样的环境变量设定，取消共享的命令是set -unshare。 |
| stat命令增加analyze_family 和analyze_pro 参数 | 比如stat analyze_family 武当派或者stat analyze_pro zhuque。里面提供阶段玩家的平均增长率（fullme下的经验增长和时间比值)，因为用中位数和fullme次数限制，过滤掉基本不动的样本。高端和中位数差值越大说明玩的好和玩的差的区别越大。参数可以带冒号，比如stat analyze_pro zhuque:xuanwu 比较2个职业不同阶段玩家的成长效率。方便萌新结合who 的门派人数,who -pro的职业人数来判断到底什么样的组合成长最快。 |
| 增加calibrate命令 | toggle 2个状态，针对gbk下黑体部分人物眼睛显示对不齐的情况。 |
| 百晓生提供注音服务，命令是zhuyin | 比如zhuyin 冄，如果是汉字，百晓生会告诉你所有读法（拼音）。如果玩家名字是多音字，而字本身不是生僻字，比如王 可以读wang或者yu，系统就没法知道该读哪一个。现在可以用typo my name命令一个交互过程指导系统你的姓名读音。 |

> 来源: https://www.pkuxkx.net/wiki/pkuxkx/newcommand
