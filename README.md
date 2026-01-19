# 情报推送系统 v1.0.0

一个智能的情报推送系统，支持实时快讯推送和每日简报生成。

**版本**: 1.0.0  
**发布日期**: 2025-01-19

## 功能特性

- ✅ **实时快讯**: 4-5星级情报秒级推送至全渠道
- ✅ **多渠道推送**: 支持Ghost官网、Telegram Bot、Discord Webhook
- ✅ **每日简报**: 3星以上情报自动生成深度简报
- ✅ **跨平台适配**: 自动格式化内容以适应不同平台
- ✅ **安全隔离**: 多渠道账号安全隔离机制

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的配置信息。

#### 管理员删除权限（可选）

如需启用“仅管理员可删除情报”，在 `.env` 增加：

```bash
ADMIN_TOKEN=请替换为一段足够长的随机字符串
```

- 前端右上角点击“盾牌”按钮，输入该 Token 后进入管理员模式，此时会显示“删除”按钮
- 后端删除接口会校验请求头 `X-Admin-Token`，未配置或不匹配会返回 403

### 3. 初始化数据库

```bash
python app.py
```

首次运行会自动创建数据库表。

### 4. 启动服务

```bash
python app.py
```

服务将在 `http://0.0.0.0:8080` 启动。

## API文档

### 创建情报

```bash
POST /api/intelligence
Content-Type: application/json

{
  "title": "情报标题",
  "content": "情报内容",
  "source": "来源",
  "rating": 5
}
```

### 获取情报列表

```bash
GET /api/intelligence?rating=5&status=published
```

### 手动触发推送

```bash
POST /api/push/<intelligence_id>
```

### 生成每日简报

```bash
POST /api/digest/generate
Content-Type: application/json

{
  "date": "2024-01-01"
}
```

## 配置说明

### Ghost配置

1. 登录Ghost管理后台
2. 进入 Settings > Integrations
3. 创建新的Custom Integration
4. 复制Admin API Key和Content API Key

### Telegram配置

1. 在Telegram中搜索 @BotFather
2. 创建新Bot，获取Token
3. 获取Chat ID（可以使用 @userinfobot）

### Discord配置

1. 进入Discord服务器设置
2. 进入Integrations > Webhooks
3. 创建新Webhook，复制URL

## 项目结构

```
intelligence_push_system/
├── app.py                      # Flask应用入口
├── config.py                   # 配置文件
├── requirements.txt             # Python依赖
├── .env                        # 环境变量（不提交到Git）
├── backend/                    # 后端核心代码
│   ├── intelligence/          # 情报处理模块
│   ├── publishers/            # 推送模块
│   ├── digest/                # 简报生成模块
│   └── scheduler.py           # 任务调度
└── database/                   # 数据库文件
```

## 版本信息

- **当前版本**: 1.0.0
- **发布日期**: 2025-01-19
- **查看更新日志**: [CHANGELOG.md](CHANGELOG.md)

## GitHub仓库

如果这个项目对您有帮助，欢迎Star和Fork！

## 开发计划

- [x] 基础架构搭建
- [x] 情报分级系统
- [x] Ghost API集成
- [x] Telegram Bot集成
- [x] Discord Webhook集成
- [x] 内容格式化系统
- [x] 实时推送功能
- [x] 每日简报生成
- [x] 任务调度系统
- [x] 前端管理界面（同花顺风格）
- [ ] 安全隔离优化
- [ ] 性能监控

## 许可证

MIT License
