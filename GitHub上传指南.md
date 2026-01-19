# 📤 GitHub上传指南

## 步骤一：准备Git仓库

### 1. 初始化Git仓库（如果还没有）

在项目根目录下打开终端，执行：

```bash
git init
```

### 2. 检查当前状态

```bash
git status
```

## 步骤二：添加文件到Git

### 1. 添加所有文件

```bash
git add .
```

### 2. 提交到本地仓库

```bash
git commit -m "Release v1.0.0: 情报推送系统首次发布

- 实时快讯推送系统
- 多渠道推送支持（Ghost/Telegram/Discord）
- 每日简报生成
- 现代化Web界面（同花顺风格）
- 完整的API和文档"
```

## 步骤三：创建GitHub仓库

### 1. 登录GitHub

访问 https://github.com 并登录您的账号

### 2. 创建新仓库

1. 点击右上角的 **"+"** 按钮
2. 选择 **"New repository"**
3. 填写仓库信息：
   - **Repository name**: `intelligence-push-system` (或您喜欢的名称)
   - **Description**: `智能情报推送系统 - 支持实时快讯推送和每日简报生成`
   - **Visibility**: 选择 Public（公开）或 Private（私有）
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）
4. 点击 **"Create repository"**

## 步骤四：连接本地仓库到GitHub

### 1. 添加远程仓库

GitHub创建仓库后，会显示仓库地址，类似：
```
https://github.com/your-username/intelligence-push-system.git
```

在本地终端执行：

```bash
git remote add origin https://github.com/your-username/intelligence-push-system.git
```

**注意**：将 `your-username` 替换为您的GitHub用户名，`intelligence-push-system` 替换为您创建的仓库名。

### 2. 验证远程仓库

```bash
git remote -v
```

应该显示您添加的远程仓库地址。

## 步骤五：推送到GitHub

### 1. 推送到GitHub

```bash
git push -u origin main
```

如果您的默认分支是 `master`，使用：

```bash
git push -u origin master
```

### 2. 输入认证信息

- 如果使用HTTPS，需要输入GitHub用户名和密码（或Personal Access Token）
- 如果使用SSH，需要配置SSH密钥

## 步骤六：创建Release标签（可选但推荐）

### 1. 创建v1.0.0标签

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
```

### 2. 推送标签到GitHub

```bash
git push origin v1.0.0
```

### 3. 在GitHub上创建Release

1. 访问您的仓库页面
2. 点击右侧的 **"Releases"**
3. 点击 **"Create a new release"**
4. 填写信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - 首次发布`
   - **Description**: 可以复制 `CHANGELOG.md` 的内容
5. 点击 **"Publish release"**

## 常见问题解决

### 问题1：认证失败

**解决方案**：使用Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 选择权限：至少勾选 `repo`
4. 生成token并复制
5. 推送时使用token作为密码

### 问题2：分支名称不匹配

如果GitHub默认分支是 `main`，但本地是 `master`：

```bash
git branch -M main
git push -u origin main
```

### 问题3：需要强制推送（谨慎使用）

```bash
git push -u origin main --force
```

**注意**：强制推送会覆盖远程仓库，请谨慎使用！

## 快速命令总结

```bash
# 1. 初始化（如果还没有）
git init

# 2. 添加文件
git add .

# 3. 提交
git commit -m "Release v1.0.0"

# 4. 添加远程仓库（替换为您的仓库地址）
git remote add origin https://github.com/your-username/intelligence-push-system.git

# 5. 推送到GitHub
git push -u origin main

# 6. 创建标签（可选）
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## 后续更新

当您修改代码后，使用以下命令更新GitHub：

```bash
# 1. 查看更改
git status

# 2. 添加更改的文件
git add .

# 3. 提交更改
git commit -m "描述您的更改"

# 4. 推送到GitHub
git push
```

## 仓库结构建议

您的GitHub仓库应该包含：

```
intelligence-push-system/
├── app.py                      # Flask应用入口
├── config.py                   # 配置文件
├── requirements.txt            # Python依赖
├── README.md                   # 项目说明
├── CHANGELOG.md                # 更新日志
├── VERSION                     # 版本号
├── .gitignore                  # Git忽略文件
├── .env.example                # 环境变量示例
├── backend/                    # 后端代码
├── frontend/                   # 前端代码
├── database/                   # 数据库（已忽略）
└── logs/                       # 日志（已忽略）
```

## 安全提示

⚠️ **重要**：确保 `.env` 文件已添加到 `.gitignore`，不要将敏感信息（API密钥等）提交到GitHub！

---

**完成！** 您的代码现在已经上传到GitHub了！🎉

访问您的仓库地址查看：`https://github.com/your-username/intelligence-push-system`
