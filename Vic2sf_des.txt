区域数据（区域数据里有区域内的pop数据）居然是以1={...} 2={... } 这样的形式直接记录在顶层的，还以为要放到zone{}块里什么的，P社就是任性。

顺便记录一下存档结构，既然区域数组放到顶层了当然主要内容也就是这些

date 当前日期
player 当前玩家，当然实际上任何存档可以随时切换玩家，这个可能只是显示旗帜提醒你用的
government 政府类型？为什么这个要专门标出来？可能前面的要显示存档时快速读取用
automate_trade 自动贸易？。。是继承HOI没删掉的属性？。。
automate_sliders  what fuck..
rebel ???叛军的专用id吗
unit ???1939?
state ???
flags 貌似是玩家吃的那些值为yes的flag，如自由主义革命
gameplaysetting 不知道什么鬼
start_date 游戏开始日期
start_pop_index 初始pop的index？链表？
worldmarket 由 worldmarket_pool price_pool last_price_history supply_pool last_supply_pool 各一个以及一堆price_history组成。每个元素都是每个商品的一个数值（价格/需求量/生产量）映射 price_history_last_update price_change discovered_goods actual_sold actual_sold_world real_demand demand player_balance 还有一堆不完全的cache标记
#总的来说worldmarket是用来形成贸易那个界面用的。另外这似乎反映了存档文件的惰性保存风格，它们全是以每个记录都会造成有意义的改变——换而言之，如果没有改变，仍为默认值的话就不保存为思想记录的。虽然这显得保存的结构参差不齐，但并没有什么问题。
great_wars_enabled 
world_wars_enabled
overseas_penelty
unit_cost 单位开销，弹药那些
budget_balance 一组值，不知道什么预算
player_monthly_pop_growth 可能是用来形成历史序列用的
player_monthly_pop_grouwth_tag 
player_monthly_pop_growth_date 应该和上面那个市场价格一样是用来反应人口变化的截断日期，不过并没有发现在VIC2里哪里可以查看这一数值。
fascist 法西斯事件？下同
socialist
communist
anarcho_liberal
canals 运河。这个要用专门的标记吗
id 什么鬼。。
fired_events  已发生事件？由一系列id={id=31300 type=39}之类的记录组成
1={...} 2={...} 区域大数组，下面详述
大数组下面有一些貌似是海域的记录，其虽然属于大数组，但是内容都很简单，{name="coast of Britanny" garrison=100.000}之类的东西。
REB={...}国家大数组（这尼玛怎么都放在顶层。。）
一堆rebel_faction 反向标记哪些pop是叛党等
diplomacy 这个似乎不是真外交，而是一些真实历史信息，比如1822.1.1到1847.7.26（这档是1842的，也有到1949的）的盟友。可能是反映传统关系之类的数据
combat 这里貌似是一系列正在进行的战斗的记录，理所当然主要由攻城战组成
一系列active_war 正在发生的战争，和下面那个一起可能是那个java存档解析器主要的解析目标
一系列previous_war 还有独立战争。。什么鬼

invention
great_nations 列强id
outliner
news_collector 新闻信息
crisis_manager 危机？
region 不知道在记录什么。。貌似就是危机区域，你这个完全依据顺序来记录真的好吗

一个没有相应的 } 宣告存档文件eof了

pop标记
pop都是用
类型={...} 出现在区域描述段里的
类型
aristocrats 贵族
artisans 可能是手工业者，也可能是劳工或者技工
bureaucrats 官僚
clergymen 牧师
labourers劳工
officers军官
soldiers士兵
字段:
id pop id
size 人数
native_american_minor=animist 这种形式 民族=宗教 秘制语法
money 不知道是哪种钱
ideology 意识形态占比，里面是{1=12.8 3=64.3}这样的记法
issues 主要政见 就是需要集会自由，需要自由贸易那种，记法类似上面
con 什么鬼
mil 什么鬼
literacy 识字率？
bank 存款？
con_factor ?
everyday_needs 日常品需求满足度？
luxury_needs 奢侈品需求满足度？
random ?

rgo感觉只有一些废话信息

国家大数组
tax_base 税基，这个专门拉出来是什么鬼。。
flags
variables 
capital 首都
technology 块，科技一些条目，按照默认+修改原则，这里实际记录的都是已经研发完的
research 块，正在研发科技的一些情况
last_reform 应该是上一次议会改革事件
last_election 上一次选举时间
一堆社会政策=XX状况。。
upper_house 块，各意识形态所占比
ruling_party 执政党，不过不知道这个id到底指什么，也许是国家的政党文件里的政党id
active_party 已经激活但没有执政的党
naval_need 块，就是运输损耗（维护）那个
land_supply_cost 陆军补给消耗
naval_supply_cost 海军补给消耗
diplomatic_points 外交点数
religion 官方宗教（原来有吗。。从没注意到）
government 政府类型
plurality 多元化
revanchism 复仇主义
rich_tax 块，富裕阶级税收。记录了比例，当前收入，效率，最大最小区间等
middle_tax 同上
poor_tax 同上
education_spending 教育开支，这些由与上面的类似，主要反映你看到的界面的状态
crime_fighting 同上（犯罪斗争开支。。行政开支）
social_spending 同上
military_spending 同上
overseas_penalty ?也许是殖民那个数值
leadership 领导力
auto_assign_leaders 
auto_create_leaders
leader 一堆leader={}的块，
army 一堆army={}的块，注意army里持有了reginment块是陆军单位。类似的还有navy-ship
国家大数组，每个项是块，映射关系值与上一次外交时间，势力范围那一套
active_inventions 已激活发明
illegal_inventions 不可激活发明？
government_flag
last_mission_cancel
ai_hard_strategy
ai 一堆征服省份的指令、、
foreign_investment
schools 科技组
primary_culture 主体文化圈
culture 可接受？
prestige 声望
bank
money
last_bankrupt 
movement 社会运动
stockpile 库存
nationalvalue 平等自由秩序那个
buy_domestic
trade
civilized 开化
last_greatness_date
state 一堆state={}块，这个很重要，工厂就在这，下面展开讲

state:
id
provinces id数组,貌似是对该国而言的state包括的区域
savings 储蓄？国家银行显示的那个？
interest 利息？怎么利息比储蓄还多。。
popproject 什么鬼。。有点像工厂
state_buildings 工厂记录

state_buildings:
building 工厂类型
level 等级，0是在建
stockpile 库存,商品映射
employment 是一些匿名块组成的序列，记录了雇佣情况。包括该state的该building的雇佣人来自state中的哪个province(id)，雇佣类型是哪个（type），应该是用index区分该province的不同同类pop的。不过还没发现证据
money 资金？在游戏里也没发现是干吗用的，破产也不是看这个
last_spending 最近支出
last_income 最近收入
pops_paychecks 薪水
last_investment 最后投资，什么鬼？
unprofitable_days 破产时间？
subsidised 是否被补贴
leftover 剩下的？没卖出去的还是没用完的
injected_money 注入资金？
injected_days 注入天？
produces 生产了多少产品
profit_history_days 连续取得利润天数？
profit_history_current 当前连续获利天数？
profit_history_entry 数组，貌似是过去7天的获利天数
