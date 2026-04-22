# 洛克世界频道

洛克王国非官方论坛 Android 客户端

## 项目介绍

洛克世界频道是一个专为洛克王国玩家打造的社区论坛应用，提供宠物查询和社区交流两大核心功能。

## 功能特性

### 🐾 宠物查询
- [x] 宠物列表浏览（分类筛选、搜索）
- [x] 宠物详情查看（基础信息、培养推荐、捕获信息、进阶信息）
- [x] 宠物对比工具（双宠资质对比）
- [x] 异色宠物展示

### 📝 论坛社区
- [x] 发帖/评论/点赞/收藏
- [x] 楼中楼回复
- [x] 版块分类
- [x] VIP功能（特殊标识）
- [x] 阵容推荐（发帖时可添加宠物阵容）

### 💬 世界频道
- [x] 公共实时聊天
- [x] 发言频率限制

### 👤 用户系统
- [x] 账号密码登录/注册
- [x] 微信第三方登录
- [x] QQ第三方登录
- [x] JWT Token认证
- [x] 用户资料编辑

### 📱 悬浮窗功能
- [x] 悬浮窗入口按钮
- [x] 横屏显示适配

## 技术栈

### 前端
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite 5
- **跨平台**: Capacitor 6
- **UI组件库**: Vant 4
- **状态管理**: Pinia
- **CSS**: UnoCSS

### 后端
- **框架**: FastAPI (Python)
- **数据库**: MySQL
- **缓存**: Redis
- **认证**: JWT

## 项目结构

```
lok-world-channel/
├── lok-world-frontend/     # 前端项目
│   ├── src/
│   │   ├── api/           # API接口封装
│   │   ├── components/    # 公共组件
│   │   ├── stores/        # Pinia状态管理
│   │   ├── views/         # 页面组件
│   │   ├── router/        # 路由配置
│   │   └── assets/        # 静态资源
│   └── package.json
│
├── lok-world-backend/      # 后端项目
│   ├── app/
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据库模型
│   │   ├── routers/       # API路由
│   │   ├── schemas/       # Pydantic模型
│   │   └── services/      # 业务逻辑
│   └── requirements.txt
│
└── 需求文档/               # 需求文档
```

## 快速开始

### 前端开发

```bash
cd lok-world-frontend

# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build
```

### 后端开发

```bash
cd lok-world-backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制配置
cp .env.example .env
# 编辑 .env 配置数据库等信息

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Android 构建

```bash
cd lok-world-frontend

# 初始化 Capacitor
npm run cap:init

# 添加 Android 平台
npm run cap:add

# 同步到 Android 项目
npm run cap:sync

# 打开 Android Studio
npm run cap:open
```

## API 文档

启动后端服务后，访问: http://localhost:8000/docs

## 数据库

### 核心表结构

- `users` - 用户表
- `pets` - 宠物表
- `boards` - 版块表
- `posts` - 帖子表
- `comments` - 评论表
- `teams` - 阵容表
- `channel_messages` - 世界频道消息表

## 团队成员

| 角色 | 职责 |
|------|------|
| 产品经理 | 产品规划、需求分析 |
| 项目经理 | 项目管理、进度把控 |
| 前端主程 | 前端架构、技术选型 |
| 前端开发 | 页面开发、功能实现 |
| 后端主程 | 后端架构、API设计 |
| 运维工程师 | 部署、监控、安全 |
| 运营负责人 | 内容运营、用户增长 |
| 数据工程师 | 数据采集、清洗、存储 |
| 游戏体验专家 | 游戏属性把控、用户体验 |
| 测试工程师 | 测试策略、缺陷跟踪 |
| 交互设计师 | 交互设计、用户体验 |

## 许可证

MIT License
