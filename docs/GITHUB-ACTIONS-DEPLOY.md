# 洛克世界频道 - GitHub 自动化部署指南

## 🚀 快速开始

### 第一步：创建 GitHub 仓库

1. 登录 GitHub：https://github.com
2. 点击右上角 **+** → **New repository**
3. 填写仓库信息：
   - **Repository name**: `lok-world-channel`
   - **Description**: 洛克世界频道 - 洛克王国非官方论坛
   - **Private** 或 **Public**: 根据需要选择
   - **勾选** Add a README file
4. 点击 **Create repository**

### 第二步：上传代码

```bash
# 进入项目目录
cd c:/Users/liyanru/WorkBuddy/20260422101304

# 初始化 Git（如果还没初始化）
git init

# 添加所有文件
git add .

# 提交
git commit -m "feat: 初始化洛克世界频道项目

- Vue 3 + Capacitor 前端框架
- FastAPI 后端服务
- GitHub Actions 自动化构建配置
- Android APK 自动打包
- Docker 容器化部署"

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/lok-world-channel.git

# 推送代码
git branch -M main
git push -u origin main
```

### 第三步：配置 GitHub Secrets

为了让 Actions 正常工作，需要配置一些密钥：

1. 进入仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**，添加以下密钥：

| Secret Name | 说明 | 如何获取 |
|------------|------|---------|
| `DOCKERHUB_USERNAME` | Docker Hub 用户名 | Docker Hub 账号 |
| `DOCKERHUB_TOKEN` | Docker Hub 访问令牌 | Docker Hub → Account Settings → Access Tokens |
| `DATABASE_URL` | 数据库连接字符串 | `mysql://user:pass@host:3306/lok_world` |
| `REDIS_URL` | Redis 连接字符串 | `redis://host:6379/0` |
| `SECRET_KEY` | JWT 密钥（随机字符串） | 用 Python: `secrets.token_urlsafe(32)` 生成 |

### 第四步：启用 GitHub Actions

代码推送后，Actions 会自动运行！

1. 进入仓库 → **Actions** 标签页
2. 你会看到两个 workflows：
   - **Build Android APK** - Android 构建
   - **Build Backend Docker Image** - 后端镜像构建
3. 点击任一 workflow 可以查看运行状态

---

## 📱 Android APK 构建

### 构建触发条件

- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request 到 `main` 或 `develop`

### 构建产物

APK 文件会作为 artifact 上传，可以在 Actions 运行日志中下载。

**下载 APK 方法：**
1. 进入仓库 → **Actions** → 选择运行记录
2. 点击 **build-android**
3. 滚动到页面底部，找到 **Artifacts** 部分
4. 点击 **apk-debug** 下载

### 分发 APK

可以通过以下方式分发：
1. 直接分享 APK 文件
2. 使用 [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
3. 使用第三方分发平台（如 Fir.im、蒲公英）

---

## 🐳 后端 Docker 部署

### 自动构建

每次推送到 `main`/`develop` 分支的 `lok-world-backend/` 目录，Docker 镜像会自动构建并推送到 Docker Hub。

### 拉取并运行

```bash
# 拉取最新镜像
docker pull YOUR_USERNAME/lok-world-backend:latest

# 运行容器
docker run -d \
  --name lok-world-backend \
  -p 8000:8000 \
  -e DATABASE_URL=your-database-url \
  -e REDIS_URL=your-redis-url \
  -e SECRET_KEY=your-secret-key \
  YOUR_USERNAME/lok-world-backend:latest
```

---

## 🧪 本地开发

### 使用 Docker Compose（无需安装依赖）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

启动后：
- 前端：http://localhost
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

---

## 🔧 自定义配置

### 修改 Android 配置

编辑 `lok-world-frontend/capacitor.config.ts`：
```typescript
const config: CapacitorConfig = {
  appId: 'com.lokworld.channel',  // 修改包名
  appName: '洛克世界频道',          // 修改应用名
  android: {
    versionCode: 1,               // 每次发布+1
  }
};
```

### 修改 API 地址

编辑 `lok-world-frontend/src/api/request.ts`：
```typescript
const BASE_URL = import.meta.env.VITE_API_URL || 'https://your-api-domain.com';
```

### 修改后端端口

编辑 `lok-world-backend/.env`：
```env
HOST=0.0.0.0
PORT=8000
```

---

## 📊 GitHub Actions 工作流说明

### Android 构建流程

```
1. Checkout code          # 拉取代
2. Setup Node.js          # 安装 Node 20
3. Setup Java JDK         # 安装 JDK 17
4. npm ci                 # 安装依赖
5. npm run build          # 构建前端
6. npx cap sync android   # 同步到 Android
7. ./gradlew assembleDebug # Gradle 构建 APK
8. Upload artifact        # 上传 APK 文件
```

### 后端构建流程

```
1. Checkout code          # 拉取代
2. Setup Docker Buildx    # Docker 构建工具
3. Login to Docker Hub    # 登录镜像仓库
4. Build and push         # 构建并推送镜像
```

---

## ❓ 常见问题

### Q: 构建失败了怎么办？

查看 Actions 日志：
1. 进入 **Actions** 标签页
2. 点击失败的 workflow
3. 点击失败的步骤查看详细错误信息

### Q: 如何添加更多 Secrets？

**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### Q: 如何禁用自动构建？

编辑 `.github/workflows/` 下的 workflow 文件，修改触发条件：
```yaml
on:
  push:
    branches: [main]  # 只在 main 分支触发
  # 或注释掉整个 on 部分
```

### Q: 如何手动触发构建？

进入 **Actions** 标签页，点击左侧 workflow 名称，点击 **Run workflow** 按钮。

---

## 📞 获取帮助

- GitHub Actions 文档：https://docs.github.com/actions
- Capacitor 文档：https://capacitorjs.com/docs
- Docker 文档：https://docs.docker.com
