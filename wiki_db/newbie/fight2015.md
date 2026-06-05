newbie:fight2015

技能CD绑定

化学伤害将增加关于加力效果的标准调整，主要是追加伤害和追加内力消耗，效果和该化学伤害所使用的兵器有关系，轻重兵器效果较差，空手较好，暗器无加力效果，如果内力不足以扣除加力消耗，将按照剩余内力按比例缩减效果，以下已开放功能中涉及此功能调整的将会附加说明“化学功能标准调整”

红花会将会择期纳入随机npc范围，大家将会体会修改后的红花会功夫效果。加入CD捆绑的概念。所谓CD捆绑就是多个动作共用一个CD，比如慕容剑法项下三个动作将会CD捆绑。比如流星快剑3秒cd，七剑连环指8秒cd，满天星斗10秒cd，如果你先用流星快剑，那么3秒后可以用慕容剑法下面的动作，如果你先用七剑连环指，则要8秒后才能用慕容剑法下面的动作。

下面只列标准化列表，有备注表示功能受影响部分。

(大轮寺的火焰刀，华山的独孤九剑，将会在重构此代码同时进行优化）

| 招式ID | 招式名称 | 变化 |  |
|---|---|---|---|
| 武当派功夫 |  |
| taiji-jian.lian | 太极剑·连 | 6秒CD，CD捆绑（捆绑ID：taiji-jian） |  |
| taiji-jian.chan | 太极剑·缠 |  |  |
| taiji-jian.sanhuan | 三环套月 | 极大提高普攻命中，一剑比一剑命中高。4秒cd，CD捆绑（捆绑ID：taiji-jian） |  |
| taiji-jian.sui | 太极剑·随 |  |  |
| taiji-jian.tongshou | 天地同寿 | 15秒CD，CD捆绑（捆绑ID：taiji-jian） |  |
| 红花会功夫 |  |
| baihua-cuoquan.cuoluan | 百花错乱 | 5秒CD，化学攻击标准调整 |  |
| benlei-tiezhang.benlei | 奔雷 |  |  |
| mantian-xingyu.sanhua | 天女散花 |  |  |
| zhuangzi-mengwu.hua | 化蝶 |  |  |
| zhuangzi-mengwu.rao | 绕蝶 |  |  |
| zhuihun-jian.duoming | 夺命 | 5秒CD，BUSY 2秒，化学攻击标准调整 |  |
| zhuihun-jian.zhuihun | 追魂快剑 | 5秒CD，BUSY 2秒 |  |
| 少林寺功夫 |  |
| banruo-zhang.san | 一拍两散 | 大幅提升命中，5秒 CD |  |
| damo-jian.sanjue | 达摩三绝剑 | 提高命中，去除busy，3秒 CD |  |
| daweituo-chu.rulai | 我佛如来 | 5秒CD，1秒-1.5秒busy，内力消耗封顶500，150级易筋经，CD绑定（绑定ID：daweituo-chu），排斥绑定ID为ranmu-daofa，riyue-bian对应的CD |  |
| daweituo-chu.wuxiang | 无相无我 | 8秒CD，第三招busy降低为1s，化学伤害标准化调整，CD绑定（绑定ID：daweituo-chu），排斥绑定ID为ranmu-daofa，riyue-bian对应的CD |  |
| fengyun-shou.foguang | 佛光普照 | 5秒CD，2秒busy，伤害上限提高，化学伤害标准化调整 |  |
| ranmu-daofa.fentian | 举火焚天 | 成功6秒CD失败2秒CD，1秒 busy，化学伤害标准化调整，伤害上限调高，CD绑定（绑定ID：ranmu-daofa） |  |
| ranmu-daofa.fenwo | 焚我 | 3秒 CD，1秒 busy，CD绑定（绑定ID：ranmu-daofa） |  |
| ranmu-daofa.fenxin | 焚心 | 140级混元一气，CD绑定（绑定ID：ranmu-daofa） |  |
| riyue-bian.chan | 日月鞭•缠 |  |  |
| riyue-bian.fumoquan | 金刚伏魔圈 | 修正CD绑定bug |  |
| zui-gun.zuida | 八仙醉打 |  |  |
| 姑苏慕容功夫 |  |
| canhe-zhi.canshang | 参商指 | 降低内力消耗，当捆绑ID：murong-jianfa的动作处于CD中时无法执行动作 |  |
| canhe-zhi.dianxue | 拈花点穴 |  |  |
| murong-jianfa.liuxing | 流星快剑 | 3秒cd，去除自身busy，大幅提高伤害和命中，CD捆绑（捆绑ID：murong-jianfa） |  |
| murong-jianfa.lianhuan | 七剑连环指 | 8秒cd，去除自身busy，CD捆绑（捆绑ID：murong-jianfa） |  |
| murong-jianfa.xingdou | 满天星斗 | 10秒CD，1s busy，CD捆绑（捆绑ID：murong-jianfa） |  |
| douzhuan-xingyi.xingyi | 星移斗转 | 5秒CD，成功率略有提升，去除成功busy，失败busy降低为1s，化学伤害部分调高并进行标准化调整，CD捆绑（捆绑ID：douzhuan-xingyi） |  |
| douzhuan-xingyi.yihua | 移花接木 | 5秒CD，1s busy，修改消耗算法，化学伤害计算略有修改并进行标准化调整，CD捆绑（捆绑ID：douzhuan-xingyi） |  |
| 古墓派功夫 |  |
| changhen-bian.chan | 长恨鞭•缠 |  |  |
| chilian-shenzhang.wudu | 五毒神掌 | 5秒CD，去除自身busy，化学伤害标准化调整 |  |
| 丐帮功夫 |  |
| dagou-bang.chan | 打狗棒•缠 |  |  |
| dagou-bang.chuo | 打狗棒•戳 | 提高伤害，化学伤害标准化调整 |  |
| dagou-bang.tiao | 打狗棒•挑 |  |  |
| dagou-bang.zhuan | 打狗棒•转 |  |  |
| 天地会功夫 |  |
| danxin-jian.feihua | 雨打飞花剑 | 8秒CD，去除busy，群攻，最多3人，CD捆绑（捆绑ID：danxin-jian） |  |
| danxin-jian.sancai | 剑出三才 | 4秒CD，1秒busy，化学伤害标准化调整，CD捆绑（捆绑ID：danxin-jian） |  |
| fulong-shou.an | 逆鳞按穴 | 命中提升5%，取消叫杀，修改成不能偷袭 |  |
| houquan.pofuchenzhou | 破釜沉舟 | 6秒CD，2秒busy |  |
| 大轮寺功夫 |  |
| dashou-yin.tianyin | 阿修罗天印 | 5秒CD，1秒busy，化学伤害标准化调整，大幅提高伤害上限，设定内力不足强行使用会降低效果。 |  |
| 明教功夫 |  |
| datengnuo-bufa.tisha | 万里黄沙 |  |  |
| feihua-shou.tan | 漫天金花 | 5秒CD，1秒busy，偷袭状态下伤害增加50%，化学伤害标准化调整。 |  |
| hanbing-zhang.shixue | 天蝠嗜血 | 化学伤害标准化调整 |  |
| 天龙寺功夫 |  |
| duanjia-jian.ailao | 哀牢山剑意 | 段家剑法为大理段家和天龙寺共用武功 |  |
| feihua-zhuyue.feihua | 飞花逐月 | 6秒CD，2秒busy |  |
| 朝廷功夫 |  |
| duanyun-bian.duanyun | 断云 |  |  |
| gehu-ji.zhentian | 雷霆震天 | 6秒CD，群攻，朝廷5人，非朝廷3人，朝廷额外增加一招，增加伤害，要求先天膂力25，内力消耗提高。 |  |
| 华山派功夫 |  |
| dugu-jiujian.po | 独孤九剑•总诀式 | 6s CD，化学伤害标准化调整，debuff增加破绽效果破绽效果说明：相比原先debuff效果翻倍，并在原先基础上增加普通伤害抗性减少，招架命中和躲闪命中减少等debuff。破绽效果请到cjg兑换，第三层兑换积分3万分。非华山派弟子无法拥有破绽效果，取消总决式之前的debuffer效果该效果合并到破绽效果中，未开放破绽效果将无debuffer效果 |  |
| dugu-jiujian.pobing | 独孤九剑•破兵式 | 4秒CD，1秒busy（失败2秒），1000级独孤九剑以后不判定其他兵器基本攻击级别，CD绑定（绑定ID：dugu-jiujian） |  |
| dugu-jiujian.kuangfeng | 狂风卷地 | 4秒CD，化学伤害标准化调整（去除CD绑定） |  |
| dugu-jiujian.poqi | 独孤九剑•破气式 | 4秒CD，命中上调5%，化学伤害标准化调整，CD绑定（绑定ID：dugu-jiujian） |  |
| dugu-jiujian.pozhang | 独孤九剑•破掌式 | 4秒CD，1秒busy（失败2秒），化学伤害标准化调整，CD绑定（绑定ID：dugu-jiujian） |  |
| hunyuan-zhang.wuji | 混元无极 | 剑宗5秒CD，气宗3秒CD，气宗伤害更高，物理伤害修改成化学伤害，化学伤害标准化调整，成功无busy失败双方各1秒，命中判定B |  |
| huashan-jianfa.feijian | 紫霞飞剑 | 5秒CD，可以剑气共用，化学伤害上限提高一倍，化学伤害标准化调整，CD绑定（绑定ID：huashan-jianfa） |  |
| huashan-jianfa.jianyi | 华山剑意 |  |  |
| huashan-jianfa.jianzhang | 剑掌五连环 | 5秒CD，1秒busy，第二招和第四招修改成化学伤害，化学伤害标准化调整，命中判定B-，CD绑定（绑定ID：huashan-jianfa） |  |
| kuangfeng-kuaijian.lianhuan | 夺命连环三仙剑 | 5秒CD，1秒busy，化学伤害标准化调整，对方处于破绽效果下，伤害提高25%，CD绑定（绑定ID：kuangfeng-kuaijian） |  |
| kuangfeng-kuaijian.kuangfeng | 狂风连环剑 | 5秒CD，1秒busy，CD绑定（绑定ID：kuangfeng-kuaijian） |  |
| kuangfeng-kuaijian.feilong | 天外飞龙 | 6秒CD，化学伤害不做标准化调整请注意，对方处于破绽效果下，成功率提升一个大级别，CD绑定（绑定ID：kuangfeng-kuaijian） |  |
| yangwu-jian.yangwu | 养吾剑 | 成功1秒busy，失败1-3秒，化学伤害和自身恢复限定仅对方处于破绽效果下才生效，最长busy时间30秒，化学伤害标准化调整 |  |
| yunushijiu-jian.sanqingfeng | 太岳三青峰 | 5秒CD，1秒busy，化学伤害标准化调整，对方处于破绽效果下，伤害提高25%，CD绑定（绑定ID：yunushijiu-jian） |  |
| yunushijiu-jian.shijiu | 玉女十九式 | 12秒CD，缩短每次发招自身busy，缩短发招频率间隔，化学伤害标准化调整，降低内力使用门槛，CD绑定（绑定ID：yunushijiu-jian） |  |
| yunushijiu-jian.wushuang | 无双无对，宁氏一剑 | busy模式无CD其他5秒CD，其他模式1秒busy，化学伤害标准化调整 |  |
| 神龙岛功夫 |  |
| dulong-bi.meiren | 美人三招 | 5秒CD，1秒busy，内力消耗提升到每次200，CD捆绑（捆绑ID：dulong-bi） |  |
| dulong-bi.yingxiong | 英雄三招 | 3秒CD，1秒busy，化学伤害标准化调整，CD捆绑（捆绑ID：dulong-bi） |  |
| dulong-bi.zhi | 孤注一掷 | 6秒CD，1秒busy，化学伤害标准化调整 |  |
| huagu-mianzhang.bujue | 绵绵不绝 | 5秒CD，发招间隔降低到1-2秒，“疯魔”状态适用性更广泛，每次发招将会重新获得5秒CD |  |
| huagu-mianzhang.hua | 辣手化骨 | 10秒CD，可以偷袭（效果可能需要等整个技能优化完毕才能生效），debuff持续时间60s，失败自身busy修改为2秒 |  |
| 峨嵋派武功 |  |
| fuliu-jian.fuliu | 拂柳 | 3秒CD，1秒busy |  |
| fuliu-jian.huifeng | 回风诀 | 3-4秒CD，1秒busy，峨嵋弟子根据敌人所受伤害恢复一定量自身气血 |  |
| fuliu-jian.juejian | 绝剑 | 取消自身busy |  |
| fuliu-jian.miejian | 灭剑 | 成功6秒CD |  |
| 桃花岛武功 |  |
| fuxue-shou.fuxue | 兰花拂穴 | 取消叫杀 |  |
| 白驼山武功 |  |
| shentuo-zhang.puji | 扑击 | 去除精神方面的消耗，30秒CD，招式正常结束后自动消除CD |  |
| shentuo-zhang.shentuo | 神驼夺魄 | 4秒CD，命中提高10%，伤害上限提高，化学伤害标准化调整 |  |
| shexing-diaoshou.chanwan | 金丝缠腕 | 命中提升5% |  |
| 灵鹫宫武功 |  |
| zhemei-shou.duo | 空手入白刃 | 6秒CD |  |
| zhemei-shou.tanmei | 弹梅.落雪.散花香 | 5秒CD，1秒busy，CD捆绑(捆绑ID：zhemei-shou） |  |
| zhemei-shou.zhemei | 折梅 | 4秒CD，1秒busy，伤害略有提升，化学伤害标准化调整，CD捆绑(捆绑ID：zhemei-shou） |  |
| 公共武学 |  |
| bizhen-qingzhang.qingxiao | 碧针清啸 |  |  |
| fengyun-jian.biri | 风云蔽日 | 成功刺目则8秒CD否则无CD，原东厂武功，化学伤害标准化调整 |  |
| flatter.qiurao | 求饶 | 15秒CD，1秒busy，负神最多降低到-500万。 |  |
| guihun-jian.wuyong | 天地无用 | 8秒CD，2秒busy，化学伤害标准化调整 |  |
| hero-jianfa.xiyang | 夕阳残照 |  |  |
| zui-quan.gfzj | 贵妃醉酒 | 化学伤害标准化调整 |  |
| zui-quan.l | 罗汉醉拳 |  |  |
| zui-quan.lingwu | 领悟醉拳 |  |  |
| zui-quan.sqzh | 杀气纵横 | 10秒CD，1秒busy，化学伤害标准化调整 |  |
| zui-quan.zsms | 醉生梦死 | 12秒CD，化学伤害标准化调整 |  |
| zui-quan.zxhc | 醉笑红尘 | 8秒CD，化学伤害标准化调整 |  |

> 来源: https://www.pkuxkx.net/wiki/newbie/fight2015
