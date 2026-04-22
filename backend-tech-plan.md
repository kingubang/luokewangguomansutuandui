# 洛克世界频道 - 后端技术方案

**版本**: v1.0  
**作者**: backend-lead  
**日期**: 2026-04-22

---

## 一、技术栈选型

### 1.1 语言与框架

| 层级 | 技术选型 | 理由 |
|------|----------|------|
| **主语言** | Python 3.11+ | 生态丰富、开发效率高、异步支持优秀 |
| **Web框架** | FastAPI | 高性能、自动API文档、类型安全、异步支持 |
| **ORM** | SQLAlchemy 2.0 | 成熟稳定、类型提示完善、异步支持 |
| **数据库** | MySQL 8.0 | 项目成熟方案、社区广泛、兼容性好 |
| **缓存层** | Redis 7.0 | 高性能、支持多种数据结构、会话存储 |
| **认证** | JWT + Refresh Token | 无状态认证、支持Token续期 |

### 1.2 核心技术组件

| 组件 | 选型 | 用途 |
|------|------|------|
| API文档 | Swagger/OpenAPI (自动生成) | 接口文档、调试 |
| 异步任务 | Celery + Redis | 邮件发送、数据同步等异步任务 |
| 文件存储 | 本地存储 + CDN | 头像、宠物图片、帖子图片 |
| 日志 | loguru | 结构化日志、异步支持 |
| 验证 | Pydantic v2 | 请求/响应数据验证 |

### 1.3 技术栈全景图

```
┌─────────────────────────────────────────────────────────┐
│                    客户端层                              │
│         (PC EXE / Mobile APK / Web)                     │
└─────────────────┬─────────────────────────────────────┘
                  │ HTTPS + JWT
┌─────────────────▼─────────────────────────────────────┐
│                   API Gateway                            │
│              (Nginx / 负载均衡)                         │
└─────────────────┬─────────────────────────────────────┘
                  │
┌─────────────────▼─────────────────────────────────────┐
│               FastAPI 应用集群                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ API Node1│  │ API Node2│  │ API Node3│           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
└───────┼─────────────┼─────────────┼───────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼───────────────────┐
│              Redis 集群 (会话/缓存)                     │
└───────────────────────┬───────────────────────────────┘
                        │
┌───────────────────────▼───────────────────────────────┐
│              MySQL 主从集群                             │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│   │Master RW│──│Slave RO │  │Slave RO │                │
│   └─────────┘  └─────────┘  └─────────┘                │
└────────────────────────────────────────────────────────┘
```

---

## 二、项目目录结构设计

```
lok_world_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # 应用入口
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── redis.py                # Redis连接
│   │
│   ├── api/                    # API路由层
│   │   ├── __init__.py
│   │   ├── deps.py             # 依赖注入
│   │   │
│   │   ├── v1/                 # API v1版本
│   │   │   ├── __init__.py
│   │   │   ├── router.py       # 路由汇总
│   │   │   │
│   │   │   ├── auth/           # 认证模块
│   │   │   │   ├── __init__.py
│   │   │   │   ├── wechat.py    # 微信登录
│   │   │   │   ├── qq.py        # QQ登录
│   │   │   │   └── jwt.py       # JWT工具
│   │   │   │
│   │   │   ├── user/           # 用户模块
│   │   │   │   ├── __init__.py
│   │   │   │   ├── crud.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── routes.py
│   │   │   │
│   │   │   ├── pet/            # 宠物模块
│   │   │   │   ├── __init__.py
│   │   │   │   ├── crud.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── routes.py
│   │   │   │
│   │   │   ├── forum/          # 论坛模块
│   │   │   │   ├── __init__.py
│   │   │   │   ├── post.py      # 帖子
│   │   │   │   ├── comment.py   # 评论
│   │   │   │   └── like.py      # 点赞
│   │   │   │
│   │   │   └── admin/          # 管理后台
│   │   │       ├── __init__.py
│   │   │       ├── crud.py
│   │   │       ├── schemas.py
│   │   │       └── routes.py
│   │
│   ├── models/                 # 数据库模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── pet.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   ├── like.py
│   │   └── admin.py
│   │
│   ├── schemas/                # Pydantic模型
│   │   ├── __init__.py
│   │   ├── base.py            # 基础模型
│   │   ├── user.py
│   │   ├── pet.py
│   │   ├── post.py
│   │   └── response.py        # 统一响应格式
│   │
│   ├── services/              # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── pet_service.py
│   │   └── forum_service.py
│   │
│   ├── utils/                 # 工具函数
│   │   ├── __init__.py
│   │   ├── security.py        # 安全工具
│   │   ├── file_upload.py     # 文件上传
│   │   └── cache.py           # 缓存工具
│   │
│   └── middleware/            # 中间件
│       ├── __init__.py
│       ├── cors.py
│       ├── logging.py
│       └── rate_limit.py      # 限流
│
├── scripts/                   # 脚本
│   ├── init_db.py             # 数据库初始化
│   ├── create_admin.py        # 创建管理员
│   └── seed_data.py           # 种子数据
│
├── tests/                     # 测试
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth/
│   ├── test_user/
│   ├── test_pet/
│   └── test_forum/
│
├── logs/                      # 日志目录
├── uploads/                   # 上传文件目录
├── .env.example               # 环境变量示例
├── requirements.txt           # 依赖
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 三、数据库表结构设计

### 3.1 用户表 (users)

```sql
CREATE TABLE users (
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username        VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    email           VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
    password_hash   VARCHAR(255) NOT NULL COMMENT '密码哈希',
    nickname        VARCHAR(50) COMMENT '昵称',
    avatar_url      VARCHAR(500) DEFAULT '' COMMENT '头像URL',
    phone           VARCHAR(20) DEFAULT '' COMMENT '手机号',
    
    -- 第三方登录
    wechat_openid   VARCHAR(100) UNIQUE COMMENT '微信OpenID',
    wechat_unionid  VARCHAR(100) COMMENT '微信UnionID',
    qq_openid        VARCHAR(100) UNIQUE COMMENT 'QQ OpenID',
    
    -- 账户状态
    status          TINYINT DEFAULT 1 COMMENT '状态: 0禁用 1正常 2待验证',
    role            TINYINT DEFAULT 1 COMMENT '角色: 1普通用户 2版主 3管理员',
    
    -- 时间戳
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at   DATETIME COMMENT '最后登录时间',
    
    -- 索引
    INDEX idx_wechat (wechat_openid),
    INDEX idx_qq (qq_openid),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

### 3.2 宠物表 (pets)

```sql
CREATE TABLE pets (
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '宠物ID',
    pet_no          VARCHAR(20) UNIQUE NOT NULL COMMENT '宠物编号',
    name            VARCHAR(50) NOT NULL COMMENT '宠物名称',
    type_id         INT UNSIGNED COMMENT '宠物类型ID',
    type_name       VARCHAR(30) COMMENT '宠物类型名称',
    level           INT UNSIGNED DEFAULT 1 COMMENT '等级',
    evolution_stage INT UNSIGNED DEFAULT 1 COMMENT '进化阶段',
    element_type    VARCHAR(20) COMMENT '元素属性',
    
    -- 基础属性
    hp              INT UNSIGNED DEFAULT 0 COMMENT '生命值',
    attack          INT UNSIGNED DEFAULT 0 COMMENT '攻击',
    defense         INT UNSIGNED DEFAULT 0 COMMENT '防御',
    speed           INT UNSIGNED DEFAULT 0 COMMENT '速度',
    magic           INT UNSIGNED DEFAULT 0 COMMENT '魔攻',
    
    -- 外观
    image_url       VARCHAR(500) COMMENT '图片URL',
    icon_url        VARCHAR(500) COMMENT '图标URL',
    
    -- 描述
    description     TEXT COMMENT '宠物描述',
    skills          JSON COMMENT '技能列表 JSON',
    
    -- 稀有度
    rarity          TINYINT DEFAULT 1 COMMENT '稀有度: 1普通 2稀有 3史诗 4传说',
    
    -- 状态
    is_active       TINYINT DEFAULT 1 COMMENT '是否启用',
    
    -- 时间戳
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- 索引
    INDEX idx_type (type_id),
    INDEX idx_rarity (rarity),
    INDEX idx_name (name),
    FULLTEXT idx_search (name, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='宠物表';
```

### 3.3 宠物收藏表 (user_pet_favorites)

```sql
CREATE TABLE user_pet_favorites (
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id         BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    pet_id          BIGINT UNSIGNED NOT NULL COMMENT '宠物ID',
    note            VARCHAR(255) DEFAULT '' COMMENT '备注',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_pet (user_id, pet_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户宠物收藏';
```

### 3.4 帖子表 (posts)

```sql
CREATE TABLE posts (
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id         BIGINT UNSIGNED NOT NULL COMMENT '作者ID',
    category_id     INT UNSIGNED DEFAULT 1 COMMENT '分类ID',
    title           VARCHAR(200) NOT NULL COMMENT '标题',
    content         TEXT NOT NULL COMMENT '正文',
    images          JSON DEFAULT NULL COMMENT '图片列表JSON',
    
    -- 统计数据
    view_count      INT UNSIGNED DEFAULT 0 COMMENT '浏览数',
    like_count      INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    comment_count   INT UNSIGNED DEFAULT 0 COMMENT '评论数',
    collect_count   INT UNSIGNED DEFAULT 0 COMMENT '收藏数',
    
    -- 状态
    status          TINYINT DEFAULT 1 COMMENT '状态: 0草稿 1已发布 2已删除 3已锁定',
    is_top          TINYINT DEFAULT 0 COMMENT '是否置顶',
    is_essence      TINYINT DEFAULT 0 COMMENT '是否精华',
    
    -- 审核
    audit_status    TINYINT DEFAULT 1 COMMENT '审核状态: 0待审核 1通过 2拒绝',
    audit_remark    VARCHAR(255) DEFAULT '' COMMENT '审核备注',
    
    -- 时间戳
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published_at    DATETIME COMMENT '发布时间',
    
    -- 索引
    INDEX idx_user (user_id),
    INDEX idx_category (category_id),
    INDEX idx_status (status),
    INDEX idx_created (created_at),
    FULLTEXT idx_search (title, content),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='帖子表';
```

### 3.5 评论表 (comments)

```sql
CREATE TABLE comments (
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    post_id         BIGINT UNSIGNED NOT NULL COMMENT '帖子ID',
    user_id         BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    parent_id       BIGINT UNSIGNED DEFAULT 0 COMMENT '父评论ID(0为顶层)',
    reply_to_id     BIGINT UNSIGNED DEFAULT 0 COMMENT '回复目标评论ID',
    content         TEXT NOT NULL COMMENT '评论内容',
    
    -- 层级
    level           TINYINT DEFAULT 1 COMMENT '评论层级',
    path            VARCHAR(255) DEFAULT '' COMMENT '评论路径',
    
    -- 状态
    status          TINYINT DEFAULT 1 COMMENT '状态: 0删除 1正常',
    like_count      INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    
    -- 时间戳
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- 索引
    INDEX idx_post (post_id),
    INDEX idx_user (user_id),
    INDEX idx_parent (parent_id),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';
```

### 3.6 点赞表 (likes)

```sql
CREATE TABLE likes (
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id         BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    target_type     VARCHAR(20) NOT NULL COMMENT '目标类型: post/comment',
    target_id       BIGINT UNSIGNED NOT NULL COMMENT '目标ID',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_target (user_id, target_type, target_id),
    INDEX idx_target (target_type, target_id),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='点赞表';
```

### 3.7 帖子收藏表 (user_collections)

```sql
CREATE TABLE user_collections (
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id         BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    post_id         BIGINT UNSIGNED NOT NULL COMMENT '帖子ID',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_post (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='帖子收藏表';
```

### 3.8 帖子分类表 (post_categories)

```sql
CREATE TABLE post_categories (
    id              INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(50) NOT NULL COMMENT '分类名称',
    description     VARCHAR(255) DEFAULT '' COMMENT '分类描述',
    icon            VARCHAR(100) DEFAULT '' COMMENT '图标',
    sort_order      INT UNSIGNED DEFAULT 0 COMMENT '排序',
    parent_id       INT UNSIGNED DEFAULT 0 COMMENT '父分类ID',
    post_count      INT UNSIGNED DEFAULT 0 COMMENT '帖子数量',
    status          TINYINT DEFAULT 1 COMMENT '状态',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='帖子分类表';

-- 初始数据
INSERT INTO post_categories (name, description, sort_order) VALUES
('综合讨论', '综合讨论区', 1),
('宠物交流', '宠物相关讨论', 2),
('攻略心得', '游戏攻略分享', 3),
('交易买卖', '宠物/道具交易', 4),
('问答互助', '问题求助区', 5);
```

### 3.9 附件表 (attachments)

```sql
CREATE TABLE attachments (
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id         BIGINT UNSIGNED NOT NULL COMMENT '上传用户ID',
    file_name       VARCHAR(255) NOT NULL COMMENT '原始文件名',
    file_path       VARCHAR(500) NOT NULL COMMENT '存储路径',
    file_size       BIGINT UNSIGNED COMMENT '文件大小',
    mime_type       VARCHAR(100) COMMENT 'MIME类型',
    file_type       VARCHAR(20) COMMENT '文件类型: image/video/audio/doc',
    
    -- 关联
    target_type     VARCHAR(20) DEFAULT '' COMMENT '关联类型',
    target_id       BIGINT UNSIGNED DEFAULT 0 COMMENT '关联ID',
    
    -- 状态
    status          TINYINT DEFAULT 1 COMMENT '状态: 0禁用 1正常',
    uploaded_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user (user_id),
    INDEX idx_target (target_type, target_id),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='附件表';
```

---

## 四、API接口设计规范

### 4.1 URL规范

```
协议://域名/api/v1/{模块}/{操作}

示例:
POST   /api/v1/auth/login              # 登录
POST   /api/v1/auth/wechat/callback     # 微信回调
GET    /api/v1/users/me                 # 获取当前用户
GET    /api/v1/pets?keyword=火神       # 搜索宠物
GET    /api/v1/posts/{id}               # 获取帖子详情
POST   /api/v1/posts/{id}/comments      # 发表回复
```

### 4.2 认证方式

#### JWT Token 方案

```
访问令牌 (Access Token)
- 有效期: 24小时
- 携带方式: Authorization: Bearer <token>
- 用途: API访问鉴权

刷新令牌 (Refresh Token)  
- 有效期: 7天
- 携带方式: 请求体或专用接口
- 用途: 续期Access Token

令牌结构:
{
  "sub": "user_id",
  "username": "xxx",
  "role": 1,
  "exp": 1713xxxxxx,  # 过期时间
  "iat": 1712xxxxxx   # 签发时间
}
```

#### 第三方登录Token

```
微信: code换openid → openid换用户
QQ:   openid换用户
```

### 4.3 统一响应格式

```json
{
  "code": 200,           // 状态码 (见4.4)
  "message": "success",  // 消息
  "data": {},            // 数据体
  "timestamp": 1713xxxx  // 时间戳
}

// 分页响应
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "pages": 5
  },
  "timestamp": 1713xxxx
}

// 错误响应
{
  "code": 401,
  "message": "Token已过期",
  "data": null,
  "timestamp": 1713xxxx
}
```

### 4.4 状态码定义

| 区间 | 含义 | 说明 |
|------|------|------|
| 200-299 | 成功 | 业务成功 |
| 400-499 | 客户端错误 | 参数错误、权限不足等 |
| 500-599 | 服务端错误 | 服务器异常 |
| 1000-1099 | 认证模块 | 登录、注册、Token相关 |
| 1100-1199 | 用户模块 | 用户信息相关 |
| 1200-1299 | 宠物模块 | 宠物查询相关 |
| 1300-1399 | 论坛模块 | 帖子、评论相关 |
| 1400-1499 | 管理模块 | 后台管理相关 |

### 4.5 API列表

#### 认证模块 /api/v1/auth

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /register | 用户注册 | 否 |
| POST | /login | 账号密码登录 | 否 |
| POST | /logout | 登出 | 是 |
| POST | /refresh | 刷新Token | 是 |
| GET | /wechat/qrcode | 获取微信登录二维码 | 否 |
| POST | /wechat/callback | 微信登录回调 | 否 |
| GET | /qq/qrcode | 获取QQ登录二维码 | 否 |
| POST | /qq/callback | QQ登录回调 | 否 |

#### 用户模块 /api/v1/users

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /me | 获取当前用户信息 | 是 |
| PUT | /me | 更新个人信息 | 是 |
| PUT | /me/avatar | 上传头像 | 是 |
| PUT | /me/password | 修改密码 | 是 |
| GET | /{id} | 获取用户公开信息 | 否 |
| POST | /{id}/follow | 关注用户 | 是 |
| DELETE | /{id}/follow | 取消关注 | 是 |
| GET | /{id}/followers | 获取粉丝列表 | 否 |
| GET | /{id}/following | 获取关注列表 | 否 |

#### 宠物模块 /api/v1/pets

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | / | 宠物列表(分页+搜索) | 否 |
| GET | /{id} | 宠物详情 | 否 |
| GET | /{id}/skills | 宠物技能列表 | 否 |
| GET | /types | 宠物类型列表 | 否 |
| GET | /{id}/evolution | 进化链 | 否 |
| GET | /{id}/comments | 相关评论 | 否 |
| POST | /{id}/favorite | 收藏宠物 | 是 |
| DELETE | /{id}/favorite | 取消收藏 | 是 |
| GET | /favorites | 我的收藏列表 | 是 |

#### 论坛模块 /api/v1/forum

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /posts | 帖子列表 | 否 |
| POST | /posts | 发布帖子 | 是 |
| GET | /posts/{id} | 帖子详情 | 否 |
| PUT | /posts/{id} | 编辑帖子 | 是 |
| DELETE | /posts/{id} | 删除帖子 | 是 |
| POST | /posts/{id}/like | 点赞帖子 | 是 |
| DELETE | /posts/{id}/like | 取消点赞 | 是 |
| POST | /posts/{id}/collect | 收藏帖子 | 是 |
| DELETE | /posts/{id}/collect | 取消收藏 | 是 |
| GET | /posts/{id}/comments | 评论列表 | 否 |
| POST | /posts/{id}/comments | 发表回复 | 是 |
| PUT | /comments/{id} | 编辑评论 | 是 |
| DELETE | /comments/{id} | 删除评论 | 是 |
| POST | /comments/{id}/like | 点赞评论 | 是 |
| GET | /categories | 分类列表 | 否 |
| GET | /users/{id}/posts | 用户帖子列表 | 否 |
| GET | /users/{id}/collections | 用户收藏列表 | 否 |

#### 后台管理 /api/v1/admin

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /login | 管理员登录 | 否 |
| GET | /users | 用户列表 | 是 |
| PUT | /users/{id}/status | 修改用户状态 | 是 |
| PUT | /users/{id}/role | 修改用户角色 | 是 |
| GET | /posts | 所有帖子列表 | 是 |
| PUT | /posts/{id}/audit | 审核帖子 | 是 |
| PUT | /posts/{id}/top | 置顶/精华 | 是 |
| GET | /pets | 宠物列表管理 | 是 |
| POST | /pets | 添加宠物 | 是 |
| PUT | /pets/{id} | 编辑宠物 | 是 |
| GET | /stats | 数据统计 | 是 |
| GET | /logs | 操作日志 | 是 |

---

## 五、第三方登录流程设计

### 5.1 微信登录流程

```
┌──────────────────────────────────────────────────────────────┐
│                        微信OAuth2.0登录流程                    │
└──────────────────────────────────────────────────────────────┘

1. 前端请求登录二维码
   前端 → GET /api/v1/auth/wechat/qrcode
   后端 → 返回微信授权URL + state参数

2. 用户扫码授权
   用户在微信客户端确认授权

3. 微信回调
   微信 → POST /api/v1/auth/wechat/callback
   参数: code + state

4. 后端换取access_token
   后端 → 微信API: https://api.weixin.qq.com/sns/oauth2/access_token
   获取: openid, access_token, unionid

5. 获取用户信息
   后端 → 微信API: https://api.weixin.qq.com/sns/userinfo
   获取: nickname, headimgurl等

6. 业务处理
   - 检查openid是否已绑定用户
   - 已绑定: 直接登录，返回JWT
   - 未绑定: 返回绑定页面，引导完善信息或关联已有账号

7. 返回前端
   成功 → { token, refresh_token, user }
```

#### 微信登录代码示例

```python
# app/api/v1/auth/wechat.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

router = APIRouter(prefix="/wechat", tags=["微信登录"])

WECHAT_APPID = "your_appid"
WECHAT_SECRET = "your_secret"
WECHAT_TOKEN_URL = "https://api.weixin.qq.com/sns/oauth2/access_token"
WECHAT_USERINFO_URL = "https://api.weixin.qq.com/sns/userinfo"

@router.get("/qrcode")
async def get_wechat_qrcode_url():
    """获取微信登录授权URL"""
    redirect_uri = "https://api.lokworld.com/api/v1/auth/wechat/callback"
    state = generate_random_state()
    auth_url = (
        f"https://open.weixin.qq.com/connect/qrconnect"
        f"?appid={WECHAT_APPID}"
        f"&redirect_uri={quote(redirect_uri)}"
        f"&response_type=code"
        f"&scope=snsapi_login"
        f"&state={state}"
    )
    return {"auth_url": auth_url, "state": state}

@router.post("/callback")
async def wechat_callback(code: str, state: str):
    """微信登录回调"""
    # 1. 用code换取access_token
    async with httpx.AsyncClient() as client:
        resp = await client.get(WECHAT_TOKEN_URL, params={
            "appid": WECHAT_APPID,
            "secret": WECHAT_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        })
        token_data = resp.json()
        
        if "errcode" in token_data:
            raise HTTPException(status_code=400, detail="微信授权失败")
        
        openid = token_data["openid"]
        unionid = token_data.get("unionid")
        
        # 2. 获取用户信息
        user_resp = await client.get(WECHAT_USERINFO_URL, params={
            "access_token": token_data["access_token"],
            "openid": openid
        })
        wx_user = user_resp.json()
    
    # 3. 业务处理
    user = await get_user_by_wechat_openid(openid)
    if user:
        # 已绑定用户，直接登录
        return await create_login_response(user)
    else:
        # 新用户，返回绑定提示
        return {
            "need_bind": True,
            "openid": openid,
            "unionid": unionid,
            "nickname": wx_user.get("nickname"),
            "avatar": wx_user.get("headimgurl")
        }
```

### 5.2 QQ登录流程

```
┌──────────────────────────────────────────────────────────────┐
│                         QQ OAuth2.0登录流程                   │
└──────────────────────────────────────────────────────────────┘

1. 前端请求登录二维码
   前端 → GET /api/v1/auth/qq/qrcode
   后端 → 返回QQ授权URL

2. 用户扫码授权
   用户在QQ客户端确认授权

3. QQ回调
   QQ → POST /api/v1/auth/qq/callback  
   参数: code + state

4. 后端换取access_token
   后端 → QQ API换取access_token

5. 获取openid (QQ特有，需要用access_token换取)
   后端 → QQ API: https://graph.qq.com/oauth2.0/me
   获取: openid

6. 获取用户信息
   后端 → QQ API: https://graph.qq.com/user/get_user_info
   获取: nickname, figureurl等

7. 业务处理 (同微信)
```

#### QQ登录代码示例

```python
# app/api/v1/auth/qq.py
from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/qq", tags=["QQ登录"])

QQ_APPID = "your_appid"
QQ_APPKEY = "your_appkey"
QQ_TOKEN_URL = "https://graph.qq.com/oauth2.0/token"
QQ_OPENID_URL = "https://graph.qq.com/oauth2.0/me"
QQ_USERINFO_URL = "https://graph.qq.com/user/get_user_info"

@router.get("/qrcode")
async def get_qq_login_url():
    """获取QQ登录授权URL"""
    redirect_uri = "https://api.lokworld.com/api/v1/auth/qq/callback"
    state = generate_random_state()
    auth_url = (
        f"https://graph.qq.com/oauth2.0/authorize"
        f"?response_type=code"
        f"&client_id={QQ_APPID}"
        f"&redirect_uri={quote(redirect_uri)}"
        f"&state={state}"
    )
    return {"auth_url": auth_url, "state": state}

@router.post("/callback")
async def qq_callback(code: str, state: str):
    """QQ登录回调"""
    # 1. 用code换取access_token
    async with httpx.AsyncClient() as client:
        token_resp = await client.get(QQ_TOKEN_URL, params={
            "grant_type": "authorization_code",
            "client_id": QQ_APPID,
            "client_secret": QQ_APPKEY,
            "code": code,
            "redirect_uri": "https://api.lokworld.com/api/v1/auth/qq/callback"
        })
        # 解析: access_token=xxx&expires_in=xxx&refresh_token=xxx
        token_params = parse_qs(token_resp.text)
        access_token = token_params["access_token"][0]
        
        # 2. 获取openid
        me_resp = await client.get(QQ_OPENID_URL, params={
            "access_token": access_token
        })
        # 解析: callback({"openid": "xxx"}); 
        openid_data = json.loads(me_resp.text[10:-2])
        openid = openid_data["openid"]
        
        # 3. 获取用户信息
        user_resp = await client.get(QQ_USERINFO_URL, params={
            "access_token": access_token,
            "oauth_consumer_key": QQ_APPID,
            "openid": openid
        })
        qq_user = user_resp.json()
    
    # 4. 业务处理
    user = await get_user_by_qq_openid(openid)
    if user:
        return await create_login_response(user)
    else:
        return {
            "need_bind": True,
            "openid": openid,
            "nickname": qq_user.get("nickname"),
            "avatar": qq_user.get("figureurl_qq_2") or qq_user.get("figureurl_qq_1")
        }
```

### 5.3 账号绑定/注册接口

```python
# 第三方登录后绑定或创建账号
@router.post("/bind")
async def bind_account(
    openid: str,
    openid_type: str,  # "wechat" or "qq"
    unionid: str = None,
    username: str = None,
    password: str = None,
    action: str = "register"  # "register" or "bind_exists"
):
    """
    绑定账号
    - action=register: 创建新账号并绑定
    - action=bind_exists: 绑定到已有账号(需提供username+password验证)
    """
    if action == "register":
        # 创建新用户
        user = await create_user(
            username=generate_unique_username(),
            password=password or generate_random_password(),
            wechat_openid=openid if openid_type == "wechat" else None,
            wechat_unionid=unionid,
            qq_openid=openid if openid_type == "qq" else None
        )
    else:
        # 绑定已有账号
        user = await authenticate(username, password)
        if not user:
            raise HTTPException(status_code=401, detail="账号或密码错误")
        
        # 更新第三方绑定信息
        await bind_third_party(user.id, openid_type, openid, unionid)
    
    return await create_login_response(user)
```

---

## 六、部署架构建议

### 6.1 开发环境

```
本地开发:
- Python 3.11+
- MySQL 8.0 (Docker)
- Redis 7.0 (Docker)
- VSCode + Pylance
```

### 6.2 测试环境

```
单节点部署:
┌─────────────────────────────────────┐
│          Docker Compose             │
│  ┌─────────┐  ┌─────────┐          │
│  │  API    │  │ MySQL   │          │
│  │ (8000)  │  │ (3306)  │          │
│  ├─────────┤  └─────────┘          │
│  │  Redis  │                       │
│  │ (6379)  │                       │
│  └─────────┘                       │
└─────────────────────────────────────┘
```

### 6.3 生产环境

```
高可用集群:
┌─────────────────────────────────────────────────────────────┐
│                      SLB (负载均衡)                          │
│                   健康检查 + SSL卸载                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   API Node 1   │  │   API Node 2   │  │   API Node 3   │
│   (Docker)     │  │   (Docker)     │  │   (Docker)     │
│   :8000        │  │   :8000        │  │   :8000        │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
────────┴──────────────────┴──────────────────┴───────────────
        │                  │                  │
        ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                        Redis Cluster                         │
│                   (Session + Cache + 队列)                    │
└─────────────────────────────────────────────────────────────┘
        │                  │                  │
        ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      MySQL 主从集群                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │  Master  │◄─│ Slave1  │◄─│ Slave2  │◄─│ Slave3  │        │
│  │   (RW)   │  │   (RO)  │  │   (RO)  │  │   (RO)  │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### 6.4 Docker Compose 配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+aiomysql://user:pass@mysql:3306/lokworld
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mysql
      - redis
    restart: unless-stopped
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 2G

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: lokworld
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api

volumes:
  mysql_data:
  redis_data:
```

### 6.5 Nginx 配置

```nginx
# nginx.conf
upstream api_backend {
    least_conn;
    server api:8000 weight=5;
}

server {
    listen 80;
    server_name api.lokworld.com;
    
    # SSL配置
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # API代理
    location /api/ {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时配置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # 限流
        limit_req zone=api_limit burst=20 nodelay;
    }
    
    # 静态文件
    location /uploads/ {
        alias /var/www/uploads/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 6.6 环境变量配置

```bash
# .env.example

# 应用配置
APP_ENV=production
APP_DEBUG=false
APP_SECRET_KEY=your-super-secret-key-change-in-production

# 数据库
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/lokworld
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=7

# 微信登录
WECHAT_APPID=wx_xxxxx
WECHAT_SECRET=xxxxx

# QQ登录
QQ_APPID=10xxxxxx
QQ_APPKEY=xxxxx

# 文件上传
UPLOAD_DIR=/var/www/uploads
MAX_UPLOAD_SIZE=10485760

# CORS
CORS_ORIGINS=https://lokworld.com,https://www.lokworld.com
```

---

## 七、安全考虑

### 7.1 认证安全

- [x] 密码使用 bcrypt 加密存储
- [x] JWT Token 设置合理过期时间
- [x] Refresh Token 仅使用一次（使用后立即失效）
- [x] 敏感操作要求重新验证密码

### 7.2 输入验证

- [x] 所有输入使用 Pydantic 严格验证
- [x] SQL参数化查询防注入
- [x] XSS过滤（富文本内容需HTML净化）
- [x] 请求频率限制防滥用

### 7.3 权限控制

```python
# 权限装饰器示例
from functools import wraps
from fastapi import HTTPException

def require_role(*roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(current_user: User, *args, **kwargs):
            if current_user.role not in roles:
                raise HTTPException(status_code=403, detail="权限不足")
            return await func(current_user, *args, **kwargs)
        return wrapper
    return decorator

# 使用
@router.delete("/posts/{id}")
@require_login
@require_role(Role.ADMIN, Role.MOD)
async def delete_post(id: int, current_user: User):
    ...
```

---

## 八、里程碑计划

| 阶段 | 功能 | 预计工时 |
|------|------|----------|
| **Sprint 1** | 项目初始化、数据库设计、用户认证 | 20人日 |
| **Sprint 2** | 宠物查询API、收藏功能 | 15人日 |
| **Sprint 3** | 论坛帖子/评论/点赞API | 20人日 |
| **Sprint 4** | 第三方登录（微信/QQ）集成 | 15人日 |
| **Sprint 5** | 管理后台API | 15人日 |
| **Sprint 6** | 部署、测试、文档 | 15人日 |
| **总计** | | **100人日** |

---

*文档版本: v1.0 | 最后更新: 2026-04-22*
