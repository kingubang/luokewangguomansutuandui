# 洛克世界频道 - 宠物数据采集与存储方案

**项目：** 洛克世界频道  
**角色：** 数据工程师  
**创建时间：** 2026-04-22  
**版本：** v1.0

---

## 一、数据采集渠道分析

### 1.1 主要数据来源

| 来源渠道 | 数据完整性 | 更新频率 | 访问难度 | 推荐程度 |
|---------|-----------|---------|---------|---------|
| 洛克王国官网/百科 | ★★★★★ | 低 | 低 | ⭐⭐⭐⭐⭐ |
| 洛克王国玩家论坛 | ★★★★ | 中 | 中 | ⭐⭐⭐⭐ |
| 百度百科/搜狗百科 | ★★★ | 低 | 低 | ⭐⭐⭐ |
| 洛克王国Wiki | ★★★★ | 中 | 中 | ⭐⭐⭐⭐ |
| 游戏内数据抓包 | ★★★★★ | 高 | 高 | ⭐⭐⭐ |

### 1.2 推荐主要渠道

#### 1.2.1 洛克王国官方网站
- **地址**：洛克王国官网（根据实际域名）
- **数据类型**：宠物图鉴、技能列表、种族值
- **优点**：官方数据，权威准确
- **缺点**：可能没有详细的进化路线和培养攻略

#### 1.2.2 玩家社区/Wiki
- **地址**：洛克王国相关Wiki站点
- **数据类型**：玩家整理的详细数据，包括进化路线、技能搭配
- **优点**：数据详细，有玩家经验
- **缺点**：可能存在玩家错误，需交叉验证

#### 1.2.3 现有公开API
- 部分游戏数据网站提供现成API
- 优点：接入简单
- 缺点：数据可能过时

---

## 二、数据字段设计

### 2.1 宠物基础信息表 (pet_basic)

| 字段名 | 类型 | 描述 | 示例 |
|-------|------|-----|-----|
| pet_id | VARCHAR(20) | 宠物唯一标识 | "10001" |
| pet_name | VARCHAR(50) | 宠物名称 | "火花鹤" |
| pet_nickname | VARCHAR(50) | 宠物别名/简称 | "小火鹤" |
| element_type | VARCHAR(20) | 主属性 | "火" |
| element_type2 | VARCHAR(20) | 副属性(可空) | "飞行" |
| level_limit | INT | 等级上限 | 100 |
| evolve_level | INT | 进化等级(可空) | 32 |
| is_final_form | TINYINT | 是否为最终形态 | 1 |
| description | TEXT | 宠物描述 | "洛克王国火系宠物..." |
| image_url | VARCHAR(255) | 宠物图片URL | "https://..." |
| is_legendary | TINYINT | 是否为传说宠物 | 0 |

### 2.2 宠物种族值表 (pet_stats)

| 字段名 | 类型 | 描述 | 示例 |
|-------|------|-----|-----|
| pet_id | VARCHAR(20) | 宠物ID(外键) | "10001" |
| hp | INT | 生命值 | 75 |
| attack | INT | 攻击 | 70 |
| defense | INT | 防御 | 65 |
| speed | INT | 速度 | 80 |
| magic | INT | 魔攻 | 85 |
| magic_defense | INT | 魔抗 | 70 |

### 2.3 宠物技能表 (pet_skills)

| 字段名 | 类型 | 描述 | 示例 |
|-------|------|-----|-----|
| skill_id | VARCHAR(20) | 技能唯一标识 | "S001" |
| skill_name | VARCHAR(50) | 技能名称 | "火花" |
| skill_type | VARCHAR(20) | 技能属性 | "火" |
| pp | INT | PP值 | 25 |
| power | INT | 威力(可空) | 40 |
| accuracy | INT | 命中率 | 100 |
| effect | TEXT | 技能效果描述 | "发射火球攻击..." |
| is_special | TINYINT | 是否为特殊技能 | 0 |

### 2.4 宠物-技能关联表 (pet_skill_relation)

| 字段名 | 类型 | 描述 | 示例 |
|-------|------|-----|-----|
| pet_id | VARCHAR(20) | 宠物ID | "10001" |
| skill_id | VARCHAR(20) | 技能ID | "S001" |
| learn_level | INT | 学习等级 | 1 |
| skill_slot | VARCHAR(10) | 技能槽位 | "遗传" |

### 2.5 宠物进化链表 (pet_evolution)

| 字段名 | 类型 | 描述 | 示例 |
|-------|------|-----|-----|
| pet_id | VARCHAR(20) | 宠物ID | "10001" |
| evolve_to_id | VARCHAR(20) | 进化目标ID | "10002" |
| evolve_level | INT | 进化等级 | 32 |
| evolve_type | VARCHAR(20) | 进化类型 | "等级" |
| evolve_condition | TEXT | 特殊进化条件 | "需要特定道具" |

### 2.6 宠物获取方式表 (pet_acquisition)

| 字段名 | 类型 | 描述 | 示例 |
|-------|------|-----|-----|
| pet_id | VARCHAR(20) | 宠物ID | "10001" |
| location | VARCHAR(100) | 获取地点 | "洛克王国-宠物园" |
| method | VARCHAR(50) | 获取方式 | "野生捕捉" |
| probability | FLOAT | 概率(可空) | 5.5 |
| notes | TEXT | 备注说明 | "仅在特定时间出现" |

---

## 三、数据采集方案

### 3.1 技术栈选型

```
┌─────────────────────────────────────────────────────────────┐
│                      数据采集层                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Python     │  │   Scrapy     │  │   Selenium   │      │
│  │   requests   │  │   分布式爬虫  │  │   动态渲染    │      │
│  │   + Beautiful│  │   + Splash   │  │   + Chrome   │      │
│  │   Soup       │  │   集群        │  │   Headless   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│                      数据处理层                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Pandas     │  │   正则表达式  │  │   NLP        │      │
│  │   数据清洗    │  │   文本提取    │  │   实体识别    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 技术选型理由

| 工具 | 用途 | 优势 | 适用场景 |
|-----|-----|-----|---------|
| requests + BeautifulSoup | 静态页面抓取 | 轻量、快速 | 官网百科页面 |
| Scrapy | 大规模爬虫 | 异步、分布式、自动去重 | 多站点数据采集 |
| Selenium/Playwright | 动态渲染页面 | 支持JS渲染 | 需要登录的页面 |
| Pandas | 数据清洗处理 | 强大数据处理能力 | 数据清洗和转换 |

### 3.3 采集频率设计

| 数据类型 | 更新频率 | 采集策略 |
|---------|---------|---------|
| 宠物基础信息 | 季度更新 | 全量采集 |
| 宠物种族值 | 季度更新 | 全量采集 |
| 技能信息 | 季度更新 | 增量采集 |
| 新增宠物 | 实时监控 | 增量采集 |
| 攻略数据 | 月度更新 | 增量采集 |

### 3.4 爬虫架构设计

```
                    ┌─────────────────┐
                    │   Scheduler     │
                    │   任务调度器     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Spider 1  │  │ Spider 2  │  │ Spider 3  │
        │ 官网采集  │  │ Wiki采集  │  │ 论坛采集  │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    ┌─────────────────┐
                    │   Pipeline      │
                    │   数据处理管道   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Validation│  │ Transform │  │ Storage   │
        │ 数据验证  │  │ 数据转换  │  │ 存储入库  │
        └──────────┘  └──────────┘  └──────────┘
```

---

## 四、数据清洗流程

### 4.1 清洗流程图

```
原始数据 ──▶ 去重 ──▶ 格式标准化 ──▶ 缺失值处理 ──▶ 异常值检测 ──▶ 关联校验 ──▶ 入库
```

### 4.2 清洗规则

#### 4.2.1 去重规则
- 宠物ID唯一性校验
- 技能ID唯一性校验
- 图片URL去重

#### 4.2.2 格式标准化
| 字段 | 原始格式 | 标准格式 |
|-----|---------|---------|
| 等级 | "Lv.100" / "100级" | 100 |
| 概率 | "5.5%" / "5.5" | 5.5 |
| 属性 | "火系" / "火" | "火" |
| 种族值 | "HP:75" | 75 |

#### 4.2.3 缺失值处理策略
| 缺失字段 | 处理策略 |
|---------|---------|
| 副属性 | 设为NULL |
| 进化等级 | 通过进化链推断 |
| 技能威力 | 设为0或"N/A" |
| 图片URL | 使用占位图或标记 |

#### 4.2.4 异常值检测
- 种族值范围校验（0-200）
- 技能PP值范围校验（0-99）
- 命中率范围校验（0-100）
- 属性值枚举校验

### 4.3 质量检查点

```python
# 数据质量检查伪代码
def validate_pet_data(pet):
    errors = []
    
    # 必填字段检查
    if not pet.pet_id:
        errors.append("缺少宠物ID")
    
    if not pet.pet_name:
        errors.append("缺少宠物名称")
    
    # 数值范围检查
    if pet.hp and not 0 <= pet.hp <= 200:
        errors.append(f"HP值异常: {pet.hp}")
    
    # 关联完整性检查
    if pet.evolve_level and pet.evolve_to_id:
        if not check_evolution_valid(pet):
            errors.append("进化关系异常")
    
    return errors
```

---

## 五、数据存储方案

### 5.1 数据库选型

| 场景 | 推荐数据库 | 理由 |
|-----|----------|-----|
| 核心业务数据 | MySQL 8.0 | 成熟稳定，支持事务，运维成本低 |
| 全文检索 | Elasticsearch | 支持模糊搜索，高性能 |
| 缓存层 | Redis | 热点数据缓存，加快查询 |
| 数据仓库 | MySQL | 数据量可控，简化架构 |

**架构决策：MySQL单库方案**
- 理由：宠物数据量预估在5000-10000条，MySQL完全满足
- 避免过度设计，优先保证稳定可靠

### 5.2 表结构设计

```sql
-- 宠物基础信息表
CREATE TABLE pet_basic (
    pet_id VARCHAR(20) PRIMARY KEY COMMENT '宠物ID',
    pet_name VARCHAR(50) NOT NULL COMMENT '宠物名称',
    pet_nickname VARCHAR(50) COMMENT '宠物别名',
    element_type VARCHAR(20) NOT NULL COMMENT '主属性',
    element_type2 VARCHAR(20) COMMENT '副属性',
    level_limit INT DEFAULT 100 COMMENT '等级上限',
    evolve_level INT COMMENT '进化等级',
    is_final_form TINYINT DEFAULT 1 COMMENT '是否为最终形态',
    description TEXT COMMENT '宠物描述',
    image_url VARCHAR(255) COMMENT '图片URL',
    is_legendary TINYINT DEFAULT 0 COMMENT '是否传说宠物',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (pet_name),
    INDEX idx_element (element_type, element_type2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 宠物种族值表
CREATE TABLE pet_stats (
    pet_id VARCHAR(20) PRIMARY KEY,
    hp INT DEFAULT 0,
    attack INT DEFAULT 0,
    defense INT DEFAULT 0,
    speed INT DEFAULT 0,
    magic INT DEFAULT 0,
    magic_defense INT DEFAULT 0,
    total_stats INT GENERATED ALWAYS AS (hp + attack + defense + speed + magic + magic_defense) STORED,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pet_basic(pet_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 技能表
CREATE TABLE skills (
    skill_id VARCHAR(20) PRIMARY KEY,
    skill_name VARCHAR(50) NOT NULL,
    skill_type VARCHAR(20) NOT NULL,
    pp INT DEFAULT 0,
    power INT DEFAULT 0,
    accuracy INT DEFAULT 100,
    effect TEXT,
    is_special TINYINT DEFAULT 0,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 宠物技能关联表
CREATE TABLE pet_skill_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id VARCHAR(20) NOT NULL,
    skill_id VARCHAR(20) NOT NULL,
    learn_level INT DEFAULT 1,
    skill_slot VARCHAR(20) DEFAULT '普通',
    FOREIGN KEY (pet_id) REFERENCES pet_basic(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE,
    UNIQUE KEY uk_pet_skill (pet_id, skill_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 宠物进化链表
CREATE TABLE pet_evolution (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id VARCHAR(20) NOT NULL,
    evolve_to_id VARCHAR(20),
    evolve_level INT,
    evolve_type VARCHAR(20) DEFAULT '等级',
    evolve_condition TEXT,
    FOREIGN KEY (pet_id) REFERENCES pet_basic(pet_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 宠物获取方式表
CREATE TABLE pet_acquisition (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id VARCHAR(20) NOT NULL,
    location VARCHAR(100),
    method VARCHAR(50),
    probability FLOAT,
    notes TEXT,
    FOREIGN KEY (pet_id) REFERENCES pet_basic(pet_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 数据更新日志表
CREATE TABLE data_update_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50),
    update_type VARCHAR(20),
    record_count INT,
    start_time DATETIME,
    end_time DATETIME,
    status VARCHAR(20),
    error_msg TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 5.3 ER图

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  pet_basic  │──────▶│  pet_stats   │◀──────│   skills    │
│  基础信息    │  1:1  │   种族值     │       │    技能     │
└──────┬──────┘       └─────────────┘       └──────┬──────┘
       │                                            │
       │ 1:N         ┌─────────────┐                │
       └────────────▶│pet_skill_   │◀───────────────┘
                     │relation     │
                     │ 宠物-技能   │
                     └─────────────┘
       │
       │ 1:N         ┌─────────────┐
       └────────────▶│pet_evolution│
                     │   进化链    │
                     └─────────────┘
       │
       │ 1:N         ┌─────────────┐
       └────────────▶│pet_acqui-   │
                     │sition       │
                     │  获取方式   │
                     └─────────────┘
```

---

## 六、数据更新机制

### 6.1 更新策略

| 更新类型 | 策略 | 触发条件 | 频率 |
|---------|-----|---------|-----|
| 全量更新 | 重建表 | 大版本更新 | 季度/半年 |
| 增量更新 | INSERT/UPDATE/DELETE | 发现新数据 | 实时/每日 |
| 修复更新 | UPDATE特定记录 | 数据错误报告 | 按需 |

### 6.2 增量更新流程

```
┌────────────────┐
│  定时任务触发   │
│  (每日凌晨2点)  │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  获取目标站点   │
│  最新数据列表   │
└───────┬────────┘
        │
        ▼
┌────────────────┐     ┌────────────────┐
│  与数据库对比   │────▶│  识别新增/变更  │
│               │     │     记录       │
└───────┬────────┘     └────────────────┘
        │
        ▼
┌────────────────┐
│  执行增量写入   │
│  INSERT/UPDATE │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  记录更新日志   │
│  发送告警通知   │
└────────────────┘
```

### 6.3 版本控制

```python
# 版本标记示例
class DataVersion:
    def __init__(self, version, timestamp, source):
        self.version = version  # "v2026.04"
        self.timestamp = timestamp
        self.source = source
        self.change_log = []
```

---

## 七、反爬应对策略

### 7.1 反爬机制分析

| 反爬类型 | 特征 | 应对策略 |
|---------|-----|---------|
| IP限流 | 访问频率限制 | 代理IP池、延迟请求 |
| UA检测 | 识别非浏览器 | 随机User-Agent |
| Cookie/Session | 追踪会话 | 定期更换Cookie |
| 验证码 | 人机验证 | 图像识别、人工介入 |
| JS加密 | 数据动态加载 | Selenium渲染、API分析 |
| 蜜罐 | 陷阱链接 | 智能URL过滤 |

### 7.2 应对方案

#### 7.2.1 代理IP池
```python
# 代理池配置示例
proxy_pool = {
    "http": [
        "http://user:pass@proxy1.com:8080",
        "http://user:pass@proxy2.com:8080",
        # ...更多代理
    ],
    "rotation": "random"
}
```

#### 7.2.2 请求策略
```python
# 智能延迟配置
class RequestStrategy:
    # 基础延迟
    base_delay = 2  # 秒
    # 随机抖动
    jitter = (0.5, 1.5)  # 秒
    # 失败重试
    max_retries = 3
    retry_delay = 5  # 秒
    # 夜间低频
    night_ratio = 0.3
```

#### 7.2.3 浏览器指纹
```python
# 随机指纹配置
fingerprint = {
    "user_agent": random.choice(UA_LIST),
    "accept_language": "zh-CN,zh;q=0.9",
    "accept_encoding": "gzip, deflate, br",
    "sec_ch_ua": '"Not_A Brand";v="8"',
}
```

### 7.3 合规建议

⚠️ **重要提醒**：
1. 遵守目标网站的robots.txt协议
2. 控制请求频率，避免影响网站正常运营
3. 获取的数据仅用于个人/项目学习
4. 如有条件，优先联系官方获取数据授权

---

## 八、数据质量监控方案

### 8.1 监控指标体系

| 指标类别 | 指标名称 | 计算方式 | 告警阈值 |
|---------|---------|---------|---------|
| 完整性 | 字段完整率 | 非空字段/总字段 | < 95% |
| 准确性 | 数值越限率 | 异常值数/总数 | > 2% |
| 一致性 | 关联失效率 | 失效外键/总数 | > 1% |
| 时效性 | 更新延迟 | 当前时间-更新时间 | > 7天 |
| 唯一性 | 重复记录率 | 重复数/总数 | > 0.5% |

### 8.2 监控实现

```python
# 数据质量检查类
class DataQualityChecker:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def check_completeness(self):
        """检查数据完整性"""
        sql = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN pet_name IS NOT NULL THEN 1 ELSE 0 END) as named
        FROM pet_basic
        """
        # 计算完整率
    
    def check_consistency(self):
        """检查关联一致性"""
        sql = """
        SELECT COUNT(*) as orphan_count
        FROM pet_stats ps
        LEFT JOIN pet_basic pb ON ps.pet_id = pb.pet_id
        WHERE pb.pet_id IS NULL
        """
        # 检查外键完整性
    
    def check_timeliness(self):
        """检查数据时效性"""
        sql = """
        SELECT MAX(update_time) as last_update
        FROM pet_basic
        """
        # 检查更新延迟
```

### 8.3 告警机制

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  定时检查   │────▶│  阈值判断   │────▶│  触发告警   │
│  (每日一次) │     │  (指标超限) │     │  (微信/邮件) │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 8.4 质量报告模板

```markdown
# 数据质量日报 - 2026-04-22

## 概览
- 宠物总数: 5,432
- 数据完整率: 98.5% ✅
- 昨日新增: 3
- 告警数量: 1

## 详细指标
| 指标 | 当前值 | 阈值 | 状态 |
|-----|-------|-----|-----|
| 字段完整率 | 98.5% | >95% | ✅ |
| 关联一致性 | 99.9% | >99% | ✅ |
| 更新时效性 | 2天 | <7天 | ✅ |

## 告警详情
- ⚠️ 技能表存在5条重复记录待处理

## 改进建议
1. 补充宠物"星光狮"的进化链数据
2. 更新"冰晶凤凰"的图片URL
```

---

## 九、实施计划

### 9.1 阶段规划

| 阶段 | 时间 | 任务 | 交付物 |
|-----|-----|-----|-------|
| **Phase 1** | 第1周 | 搭建采集环境，确定数据源 | 数据源清单 |
| **Phase 2** | 第2周 | 开发爬虫，完成基础数据采集 | 首批数据集 |
| **Phase 3** | 第3周 | 数据清洗，入库存储 | 清洗后数据集 |
| **Phase 4** | 第4周 | 搭建监控告警体系 | 监控系统 |
| **Phase 5** | 持续 | 增量更新机制运行 | 自动更新流程 |

### 9.2 资源需求

| 资源类型 | 需求 | 备注 |
|---------|-----|-----|
| 服务器 | 1台 2核4G | 爬虫+数据库 |
| 代理IP | 100+ IP池 | 应对反爬 |
| 人力 | 0.5人/月 | 数据工程师 |

---

## 十、风险与应对

| 风险 | 影响 | 概率 | 应对措施 |
|-----|-----|-----|---------|
| 数据源不可用 | 高 | 中 | 多数据源备份 |
| 反爬加强 | 中 | 高 | 储备更多代理IP |
| 数据质量差 | 中 | 低 | 强化清洗流程 |
| 存储容量不足 | 低 | 低 | 定期归档历史数据 |

---

**文档状态：** 初稿完成  
**下一步行动：** 确认数据源后启动爬虫开发
