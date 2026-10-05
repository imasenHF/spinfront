# SpinFront每日任务完整要求

执行SpinFront每日检索、分类审阅、文件生成和GitHub发布。先读取imasenHF/spinfront仓库main最新内容：docs/MAINTENANCE.md、docs/DAILY_OUTPUT_RULES.md、taxonomy/taxonomy.json、templates/issue.html、assets/style.css、scripts/build.py，以及完整历史data索引。以仓库当前受控词表与渲染程序为准；不要凭旧对话重新设计样式。仓库地址：https://github.com/imasenHF/spinfront。报告日期与24小时窗口按Asia/Shanghai确定，并记录检索截止时刻。

检索并发送一份每日NMR/EPR新闻简报。每日精选10条与核磁共振波谱（NMR）、电子顺磁共振波谱（EPR）、磁共振仪器或其具体应用高度相关的信息。不要单独收录泛AI工具、泛化学或泛材料内容；AI、计算化学、化学、材料、生命科学、量子科技、政策、采购及行业市场信息，只有在核心内容直接涉及NMR/EPR方法、谱图分析、脉冲序列、硬件部件、软件算法、样品体系、应用方案或仪器采购时才可入选。

不设置EPR与NMR的固定条数或主题顺序，按当日信息价值动态分配；允许当日内容主要或全部属于NMR或EPR。混合编排学术进展、仪器产品与技术、应用案例、行业市场、政策及采购动态，兼顾中国与海外来源，采用中英混合表达。

优先检索过去24小时。若不足10条，可扩展至过去7天，并在对应条目中标注“近7天扩展”及准确发布日期；仍不足时只发送符合质量要求的实际条目，不用低相关性内容补足。核对页面发布时间与事件发生时间，避免重复上一期已经发送的内容。优先使用论文原文、期刊、机构官网、公司公告和政府采购等一手来源。

晨报品牌固定采用三行：
自旋前沿｜SpinFront
NMR / EPR Daily Brief
追踪自旋、谱学与应用进展

聊天屏幕版标题使用“自旋前沿｜SpinFront｜YYYY-MM-DD”，并保留“NMR / EPR Daily Brief”和“追踪自旋、谱学与应用进展”。随后提供范围说明，再逐条排列“编号＋简洁标题—分类标签—约100–150字中文摘要—具体意义—发布日期—原始来源链接”，条目之间使用分隔线。具体意义需面向NMR/EPR应用研发、仪器配置、方案交流或客户工作，给出明确的实验条件、部件、脉冲序列、数据处理或样品要求。屏幕版采用纯文本内容，不显示图片、图片占位区域或图片检索关键词。

发送屏幕版完整正文的同时，生成可下载的单文件HTML，文件名固定为SpinFront_YYYY-MM-DD.html，例如SpinFront_2026-08-26.html。HTML内容和条目顺序与屏幕版一致，采用UTF-8、响应式单栏排版，优先适配手机阅读。HTML页首同样使用三行品牌信息。正文最大宽度约720px；每条使用独立卡片，标题、分类标签、摘要、具体意义、日期和来源集中在同一卡片内。控制信息密度，使每条在常见6–7英寸手机上约占一屏。

纯文本规则：后续日报不检索、不下载、不嵌入任何图片；不生成Base64数据、图片占位图、自制摘要图或图片检索关键词。HTML、屏幕正文和结构化记录均不保留图片字段。

版权信息规则：聊天屏幕版和HTML均在全部条目之后、页面最下方显示以下三行页脚信息：
SpinFront · NMR / EPR Daily Brief · YYYY-MM-DD
© 当年 wuhaifeng@ustc.edu.cn. All rights reserved.
本报告版权归作者所有，未经许可不得复制、转载或用于商业用途。
日期使用当期晨报日期。邮箱仅显示为纯文本，不设置mailto或其他超链接。页脚使用低干扰、居中、小字号样式，并与正文保持适当间距。

结构化输出规则：除屏幕正文和SpinFront_YYYY-MM-DD.html外，同时生成SpinFront_YYYY-MM-DD.json，作为SpinFront_Project的单期数据。JSON顶层固定包含schema_version、report_date、scope_note和items。每条items记录必须包含item_id、report_date、item_no、title_cn、direction_ids、experiment_type_ids、method_ids、application_ids、sample_systems、instrument_component_ids、information_type、summary_cn、meaning_cn、publication_date、time_scope、source、url、doi、alternative_sources、related_to、review_status、first_seen、last_updated和report_file。item_id格式为SF-YYYYMMDD-NN；time_scope只允许24h或7d_extension；review_status默认unreviewed。JSON与HTML的条目数量、顺序、标题、摘要、具体意义、日期和来源必须一致。

标准标签规则：正式标签、版本、定义和父子关系以仓库当前taxonomy/taxonomy.json为唯一依据，输出前读取并验证。谱学方向只使用nmr、epr；同时涉及两者时使用两个ID。活体波谱使用nmr与in_vivo_mrs；磁共振测速使用nmr与mr_velocimetry，排除将医学静脉成像误标为测速。顶层taxonomy_version与仓库版本一致。UI展示分组不作为正式ID。无法可靠映射的概念保留在sample_systems或正文，并在范围说明后列出待复核标签。

查重输出规则：生成当期JSON前，优先依据历史日报与可访问的项目索引，按标准化DOI、去除跟踪参数后的URL和标准化标题检查重复。DOI完全一致的既有论文不作为新条目；同一活动页面承载多个独立议程时允许保留不同条目；正式出版替代Early Access时更新说明，不重复收录。

增强搜索触发与执行规则：
1. 先完成常规检索并去重。若过去24小时内合格条目少于5条，或扩展至近7天后合格条目仍少于8条，必须自动启动增强搜索；无需等待用户确认。
2. 增强搜索采用分层而非仅增加宽泛关键词。至少覆盖以下五条路线：
   - 专业期刊与论文：Journal of Magnetic Resonance、Journal of Magnetic Resonance Open、Magnetic Resonance、Journal of Biomolecular NMR、Solid State Nuclear Magnetic Resonance、Magnetic Resonance in Chemistry、Applied Magnetic Resonance，以及ACS、RSC、Wiley、Springer Nature、Elsevier、AIP等平台中直接以NMR/EPR方法为核心的论文；
   - 预印本与机构：arXiv、ChemRxiv、PubMed、科研机构及高校官方新闻；
   - 仪器与软件：Bruker、JEOL、Oxford Instruments、Magritek、Nanalysis、SpinSolve相关厂商、CIQTEK/国仪量子及其他NMR/EPR厂商的产品、软件、附件、应用说明和技术活动；
   - 会议与培训：ENC、EUROMAR、ICMRBS、EFEPR、APES、ISMAR及专业Workshop的新增独立议程；
   - 采购与政策：中国政府采购网、全国公共资源交易平台、高校招标网站、SAM.gov及其他可核验的政府或高校采购公告。
3. 方法词必须扩展检索，不得只搜索NMR或EPR全称。至少轮换使用：MAS、fast MAS、DNP、TD-NMR、benchtop NMR、low-field NMR、qNMR、NUS、pure shift、DOSY、CEST、DEST、reaction monitoring、paramagnetic NMR、CW-EPR、pulsed EPR、DEER/PELDOR、ENDOR、ESEEM、HYSCORE、TREPR、spin trapping、spin labeling、operando EPR、EC-EPR、rapid-scan EPR、resonator、probe、magnet、console、autosampler和spectral processing。
4. 中国与海外来源分别检索；学术、仪器软件、应用案例、会议、采购五类分别检索。不能用单次综合搜索无结果代替某一类别的专项搜索。
5. 对每个候选核验页面实际发布日期、事件日期及刊期日期。仅有“最近抓取”“页面更新”或期刊卷期日期而无新增事件证据的，不作为新条目。
6. 增强搜索仍不得降低相关性标准，不得用常规辅助表征论文、医学MRI泛内容或旧页面补足数量。
7. 在当期范围说明中明确写出“已启动增强搜索”，说明触发原因、覆盖范围、排除的重复数量和最终实际条目数。若增强搜索后仍少于目标条数，保留实际高质量条目，并说明不足原因。
8. JSON生成前须将最近至少7期已发送正文与可访问项目索引共同用于查重；项目索引缺期时，以近期对话中的日报条目补足查重，不得仅依赖不完整索引。

深度增强检索规则：
1. 若完成上述增强搜索后最终合格条目仍少于8条，必须继续启动第二级“深度增强检索”，不得仅凭通用搜索引擎结果结束检索。
2. 深度增强必须完整回扫报告日前7个自然日，不得只搜索当天或前一日；逐日检查尚未收录的候选，并以实际在线发布日期或明确事件日期归入24h或7d_extension。
3. 专业期刊路线必须逐站点核查Latest Articles、Articles in Press、Early View、ASAP或Online First页面，至少包括Journal of Magnetic Resonance、Journal of Magnetic Resonance Open、Magnetic Resonance、Journal of Biomolecular NMR、Solid State Nuclear Magnetic Resonance、Magnetic Resonance in Chemistry、Applied Magnetic Resonance及ACS、RSC、Wiley、Springer Nature、Elsevier、AIP相关期刊。不得用一次综合检索代替逐站核查。
4. 预印本与文献数据库路线必须分别检查arXiv、ChemRxiv、PubMed/Crossref或等效的一手元数据来源；对预印本转正式出版的同一工作，按DOI、标题和作者核对后只保留一次。
5. 厂商路线必须分别检查Bruker、JEOL、Oxford Instruments、Magritek、Nanalysis、CIQTEK/国仪量子及其他相关厂商的新闻、产品、应用说明、软件更新和技术活动页面；没有实际新增日期的常驻产品页不得收录。
6. 会议路线必须检查ENC、EUROMAR、ICMRBS、EFEPR、APES、ISMAR及专业Workshop的日程、摘要册和会后材料；同一会议页面只有在承载独立且技术内容不同的报告时才可拆分条目，闭幕或页面更新本身不得重复收录。
7. 采购路线必须分别检查中国政府采购网、全国公共资源交易平台、高校采购网站、仪器采购聚合页、SAM.gov及可核验海外政府或高校公告；按公告发布日期而非开标日期判断新旧，医学MRI采购排除。
8. 方法词按主题簇分轮检索：高分辨液体NMR、固体NMR/MAS/DNP、低场与TD-NMR、NMR软件与谱图处理、CW/rapid-scan EPR、脉冲EPR/DEER/ENDOR/ESEEM/HYSCORE、TREPR与光照、operando/EC-EPR、探头/谐振器/磁体/控制台/自动进样。每个主题簇至少执行一次独立检索。
9. 日期核验必须区分网页发布时间、论文online publication、卷期日期、会议发生日期和搜索引擎抓取时间。缺少精确时刻时，不得仅凭日期边界标为24h；无法证明处于过去24小时的条目统一标为7d_extension。
10. 深度增强过程应形成内部候选清单，记录标题、来源、DOI或规范化URL、实际日期、相关性判断、重复键和排除原因。范围说明必须报告常规、增强及深度增强的触发原因、覆盖路线、排除重复数、日期不明排除数和最终条目数。
11. 深度增强仍不得降低质量门槛。最终不足10条时保留实际合格数量，但只有完成全部路线和主题簇后才能结束，并明确不足来自周末低产出、索引延迟、重复或日期不可核验中的哪些原因。
12. 输出前再次审计：HTML、JSON和屏幕正文数量与顺序一致；所有URL可访问或至少可由权威元数据确认；DOI标准化；最近至少7期查重完成；任何图片字段均不存在。

学术条目相关性门槛：必须判定NMR/EPR在论文中的实际作用。只接收以下三种情况：（1）method_core：研究直接提出或验证NMR/EPR方法、脉冲序列、采样、谱图处理、硬件或定量性能；（2）key_evidence：NMR/EPR结果直接决定主要结构、活性物种、自旋态、交换耦合、距离、动力学或机制结论；（3）application_core：研究围绕NMR/EPR的应用、定量方法或实际分析流程展开。routine_characterization：仅用常规1H/13C确认合成产物，或仅凭一张未分析的EPR图泛称自由基存在，不入选。unverified：实际作用无法从可访问原文、补充材料或明确摘要确认，不入选。期刊名气、关键词出现频次、摘要中出现NMR/EPR均不单独构成入选理由。论文主角可以是催化、结构或物理问题，但须指出具体哪项结论依赖磁共振数据。预印本执行相同门槛并明确其出版状态。只看得到摘要时，摘要需明确满足上述作用判定，正文分析限于摘要可确认范围，不补写图号、序列或实验参数。仪器、软件、会议、采购与政策按对象直接涉及NMR/EPR及新增技术信息判定，不套用论文结构结论门槛。常驻产品页、会议召开/闭幕及无技术增量的宣传不入选。

期刊检索优先级（属于本项目检索安排，不代表统一学术排名）：每轮常规检索同时覆盖高影响研究与磁共振专业期刊，两条路线均为必查。高影响优先：Nature、Science、Nature Materials、Nature Chemistry、Nature Catalysis、Nature Physics、Nature Methods、JACS、Angewandte Chemie International Edition、PNAS；Science Advances为重点补充，Science Translational Medicine、Science Immunology等按直接磁共振相关性专项检查；Nature Communications排在上述Nature重点刊之后，不设收录配额。物理重点补充Physical Review Letters、Physical Review X；PRX Quantum、Physical Review B、Physical Review Applied、Physical Review A、Reviews of Modern Physics按自旋、凝聚态、量子传感或方法内容检索。专业必查Journal of Magnetic Resonance（JMR）、Journal of Magnetic Resonance Open、Magnetic Resonance（Copernicus）、Journal of Biomolecular NMR、Solid State Nuclear Magnetic Resonance、Magnetic Resonance in Chemistry、Applied Magnetic Resonance。方法综述补充Progress in Nuclear Magnetic Resonance Spectroscopy、Annual Reports on NMR Spectroscopy；活体波谱补充NMR in Biomedicine、Magnetic Resonance in Medicine、Magnetic Resonance Materials in Physics Biology and Medicine，排除泛MRI内容；EPR相关物理化学补充PCCP、The Journal of Physical Chemistry A/B/C、The Journal of Chemical Physics。所有期刊执行相同作用门槛；专业刊中的具体方法进展可优先于高影响刊中的常规辅助表征。JMR不能等到条目不足时才检查。

具体意义写作：读者为对信息感兴趣的科研和相关行业人员，中文克制、中立、客观，不使用自称、营销判断或日报内部工作流程措辞。每条用约80–150字，允许按信息复杂度调整；围绕该条独有内容写出实验或分析对象、获得的可测信息、适用条件与一项关键限制。优先提取可确认的核种/微波频段、场强、温度、脉冲序列、采样方式、浓度/标记/氘代要求、耦合常数、距离分布、时间窗口、信噪比、误差或对照结果，不要求凑齐所有参数。论文原文结论与分析推断明确区分；推断写成条件句，不将可能性表述为既定事实。上传教材仅在当前执行能实际读取时用于原理解释；记录书名、章节和定位信息，不依赖记忆补写教材内容，不复制长段教材。材料不可访问时依照论文原文分析并记录限制。不得用“为仪器选型提供参考”“有助于方案交流”等可复制到任意条目的通用句结束。执行可替换性检查：删掉文献名后仍可用于不相干文献的句子须改写。不能推导到仪器配置或实验决策时，客观说明该研究的机制或方法意义，不强行给出配置建议。

自动Review：由执行者逐条完成，不将常规审阅转交用户。生成docs/reviews/YYYY-MM-DD.json，包含报告日期、检索截止时刻、查重使用的最近至少7期日期和全库索引版本、各检索路线执行/访问失败状态，以及候选标题、来源、规范化DOI/URL、实际在线日期、出版状态、磁共振作用类别、判定依据及来源定位、入选或排除理由、重复键、标签及每个标签的短理由。审阅正式标签的ID、维度、父子关系和正文依据；存储最具体且有依据的ID，不因一般关联添加仪器部件或应用。direction_ids仅允许nmr、epr，两者都是主要内容时才同时标记。MRS与磁共振测速按现有词表实验类型记录。应用标签依据实际用途，不把方法名、样品名、采购或会议性质强行映射为科学应用。无法映射的概念放sample_systems和候选日志，不自动扩展词表。tag_review_status在完成分类审阅后记approved，分类理由保存在审阅日志。来源、日期、重复和科学解释分别记录状态；不得用tag_review_status=approved代替事实复核。原始来源无法确认、日期超窗或不明、主要作用不明的候选不能发布。候选不足保留实际数量；访问失败或执行资源限制如实写入范围说明，不能声称未执行的路线已完成。

模板、数据与发布：先生成唯一当期JSON作为内容源，顶层包含schema_version、taxonomy_version、report_date、scope_note、items，taxonomy_version使用仓库当前版本。按仓库既有字段规则生成items，不携带图片字段。由同一JSON输出屏幕正文、网页与可下载HTML；使用templates/issue.html、assets/style.css和scripts/build.py，禁止每期重新写CSS或独立设计卡片。可下载HTML取构建产物_site/downloads/SpinFront_YYYY-MM-DD.html，其中CSS内嵌；JSON取data/YYYY/SpinFront_YYYY-MM-DD.json。网页日报由构建生成YYYY-MM-DD/index.html，主页日历、搜索索引及归档随构建自动更新。

用户已授权此每日任务自动向公开仓库imasenHF/spinfront提交合格日报JSON和当期Review日志，并触发GitHub Pages发布，无需每天再次确认。每次先用GitHub只读工具验证当前运行具备仓库读写能力并读取main最新HEAD。只提交data/YYYY/当期JSON与docs/reviews/当期日志；正常日报运行不得修改模板、样式、词表、工作流、历史记录或主站仓库。不得提交凭证、私人教材、客户材料、下载的第三方全文或本地生成的_site目录。运行python scripts/build.py --check、python scripts/build.py、node tests/search.test.cjs，并核对屏幕/HTML/JSON数量、顺序、正文、日期、来源相同，单文件HTML不依赖外部CSS。检查全库DOI/URL/标题查重及至少7期近期发送内容后再提交。提交信息为Publish SpinFront YYYY-MM-DD (N items)。使用已授权GitHub连接的写入能力，原子提交两个文件，以最新HEAD为父提交，禁止force push。已有同日文件先比较内容；相同不重复提交，不同作为明确修订保留既有item_id并记录日志，不能无依据覆盖。冲突时重读最新HEAD和当日数据重新校验，不能覆盖并发修改。

提交后检查该commit对应Actions构建及Pages部署状态，访问并验证当期公开页面与索引中实际有新日期和正确条目数。最终在版权页脚之后另附简短执行状态，注明报告/标签审阅完成情况、提交SHA、部署状态及公开链接；发布状态不写入学术条目正文。只有提交和部署核实成功才写已发布。GitHub写入工具不可用、连接过期或权限不足时，继续完成正文与HTML/JSON并保留Review日志，明确写未提交及具体原因；自动化执行上下文的工具与授权可能不同于当前对话，不得把提示词写入视作未来成功发布的保证。部署仍进行中写待部署确认；失败报告日志中的原因与已保存结果，不声称主页已更新。
