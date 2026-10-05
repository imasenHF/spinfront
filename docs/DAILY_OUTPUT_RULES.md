# 每日输出分类规则（词表1.2.0）

正式标签使用taxonomy/taxonomy.json中的标准ID。direction_ids仅允许nmr、epr，不能为空；同时涉及两者时写["nmr", "epr"]。不再生成nmr_epr、mrs或mrv方向ID。

活体磁共振波谱使用nmr方向与in_vivo_mrs实验类型；磁共振测速使用nmr方向与mr_velocimetry实验类型。单独的医学MRI及磁共振静脉成像不据此标注为测速。

每期taxonomy_version为1.2.0。sample_systems保留无法可靠映射的样品概念。UI方法组不生成正式ID，原有父子方法标签规则继续使用。

摘要、具体意义、发布时间和来源依照既有日报规则生成。tag_review_status与来源及日期复核状态分别记录；词表迁移不改变来源核验结论。屏幕正文、HTML和JSON保持一致，所有内容记录均无图片字段。
