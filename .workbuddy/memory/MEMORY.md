# 洛克世界频道 - 长期记忆

## 项目概况
- 项目名：洛克世界频道（洛克王国非官方论坛）
- 项目路径：c:/Users/liyanru/WorkBuddy/20260422101304
- 技术栈：Vue 3 + TypeScript + Tauri（PC端EXE）+ Tauri Mobile/Capacitor（移动端APK）
- 后端：FastAPI + MySQL + Redis + JWT

## 前端团队分工（2026-04-22 确认）
| 开发者 | 负责模块 |
|--------|----------|
| frontend-dev-1 | 宠物查询模块 |
| frontend-dev-2 | 用户中心 + 全局基础设施（axios、Pinia、路由守卫、Token管理） |
| frontend-dev-3 | 论坛模块（帖子列表、详情、版块、评论、点赞收藏） |

## frontend-dev-3 关键依赖（由 dev-2 提供）
- `useUserStore`：用户信息、登录态（isLoggedIn）、用户ID
- `useAuthStore`：登录/登出、Token刷新、OAuth状态
- `request`：封装好的axios实例
- 路由守卫：需登录页面自动拦截
- `useRequireAuth()`：登录检查组合式函数

## 团队角色（2026-04-22 更新）
| 角色 | 成员名 | 状态 |
|------|--------|------|
| 资深产品经理 | product-manager | 待汇报 |
| 资深项目经理 | project-manager | 待汇报 |
| 资深前端主程 | frontend-lead | ✅ 方案完成 |
| 资深前端开发 ×3 | frontend-dev-1/2/3 | 待分配 |
| 资深后端主程 | backend-lead | 待汇报 |
| 运维工程师 | devops | 待汇报 |
| 运营负责人 | operations | 待汇报 |
| 数据工程师 | data-engineer | 待汇报 |
| 游戏体验专家 | game-expert | 待汇报 |
| 测试工程师 | qa | 待汇报 |
| **资深交互设计师** | interaction-designer | **新增** |

## 开发节奏
- dev-2 先搭基础设施（1-2天），我并行搭建论坛UI骨架
- 基础设施就绪后我接入数据层
