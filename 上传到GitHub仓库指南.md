# 📤 上传到GitHub仓库指南

## 您的GitHub仓库

**仓库地址**: https://github.com/q379078150-netizen/li  
**仓库名称**: li  
**当前状态**: 空仓库

---

## 方法一：使用GitHub Desktop（最简单，推荐）

### 步骤1：安装GitHub Desktop

1. 访问：https://desktop.github.com/
2. 下载并安装GitHub Desktop
3. 使用您的GitHub账号登录

### 步骤2：克隆或添加仓库

#### 选项A：克隆空仓库（推荐）

1. 在GitHub Desktop中，点击 **"File"** → **"Clone repository"**
2. 选择 **"URL"** 标签
3. 输入仓库地址：`https://github.com/q379078150-netizen/li.git`
4. 选择本地保存位置（建议选择其他位置，不要覆盖当前项目）
5. 点击 **"Clone"**

#### 选项B：添加现有项目

1. 在GitHub Desktop中，点击 **"File"** → **"Add Local Repository"**
2. 浏览到项目目录：`C:\Users\86138\.config\clash\profiles`
3. 点击 **"Add repository"**

### 步骤3：发布到GitHub

1. 在GitHub Desktop中，点击 **"Publish repository"** 按钮
2. 确保仓库名称是：`li`
3. 选择 **"Keep this code private"** 或取消勾选（公开）
4. 点击 **"Publish repository"**

### 步骤4：提交所有文件

1. 在左侧会看到所有更改的文件
2. 在左下角填写提交信息：
   ```
   Release v1.0.0: 情报推送系统首次发布
   ```
3. 点击 **"Commit to main"**
4. 点击 **"Push origin"** 上传到GitHub

### 步骤5：创建Release标签

1. 访问：https://github.com/q379078150-netizen/li
2. 点击右侧的 **"Releases"**
3. 点击 **"Create a new release"**
4. 填写信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - 情报推送系统首次发布`
   - **Description**: 可以复制 `CHANGELOG.md` 的内容
5. 点击 **"Publish release"**

---

## 方法二：使用命令行（需要先安装Git）

### 步骤1：安装Git

1. 访问：https://git-scm.com/download/win
2. 下载并安装Git for Windows
3. 安装完成后，重启PowerShell

### 步骤2：验证安装

打开新的PowerShell窗口，执行：

```powershell
git --version
```

如果显示版本号，说明安装成功。

### 步骤3：初始化Git仓库

在项目目录下执行：

```powershell
cd C:\Users\86138\.config\clash\profiles
git init
```

### 步骤4：配置Git用户信息（首次使用）

```powershell
git config --global user.name "q379078150-netizen"
git config --global user.email "您的GitHub邮箱"
```

### 步骤5：添加所有文件

```powershell
git add .
```

### 步骤6：提交到本地仓库

```powershell
git commit -m "Release v1.0.0: 情报推送系统首次发布"
```

### 步骤7：连接到GitHub仓库

```powershell
git remote add origin https://github.com/q379078150-netizen/li.git
```

### 步骤8：推送到GitHub

```powershell
git branch -M main
git push -u origin main
```

**如果遇到认证问题**：
- 使用Personal Access Token代替密码
- 生成Token：https://github.com/settings/tokens
- 权限选择：`repo`

### 步骤9：创建版本标签

```powershell
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

---

## 方法三：使用自动化脚本

我已经为您创建了自动化脚本，但需要先安装Git。

### 使用步骤：

1. **先安装Git**（参考方法二的步骤1）

2. **配置远程仓库**（只需一次）：
   ```powershell
   git remote add origin https://github.com/q379078150-netizen/li.git
   ```

3. **运行脚本**：
   ```powershell
   .\upload_to_github.bat
   ```

---

## 快速命令总结（命令行方法）

```powershell
# 1. 初始化Git
git init

# 2. 配置用户信息（首次使用）
git config --global user.name "q379078150-netizen"
git config --global user.email "您的邮箱"

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Release v1.0.0: 情报推送系统首次发布"

# 5. 连接GitHub仓库
git remote add origin https://github.com/q379078150-netizen/li.git

# 6. 推送到GitHub
git branch -M main
git push -u origin main

# 7. 创建版本标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

---

## 重要提示

### ⚠️ 安全提示

1. **`.env` 文件已保护**：已添加到 `.gitignore`，不会被上传
2. **敏感信息**：确保API密钥等敏感信息不会提交
3. **如果误提交**：立即在GitHub上删除并重新生成密钥

### ✅ 已准备的文件

- ✅ `VERSION` - 版本号（1.0.0）
- ✅ `CHANGELOG.md` - 更新日志
- ✅ `.gitignore` - Git忽略文件
- ✅ `README.md` - 项目说明（已更新版本信息）

### 📝 认证问题解决

如果推送时要求密码：

1. **使用Personal Access Token**：
   - 访问：https://github.com/settings/tokens
   - 点击 **"Generate new token (classic)"**
   - 权限选择：`repo`（完整仓库访问权限）
   - 生成并复制Token
   - 推送时使用Token作为密码

2. **或者使用SSH**：
   - 生成SSH密钥
   - 添加到GitHub账户
   - 使用SSH地址：`git@github.com:q379078150-netizen/li.git`

---

## 上传后的检查

上传完成后，访问您的仓库：

**仓库地址**: https://github.com/q379078150-netizen/li

检查以下内容：

- [ ] 所有文件都已上传
- [ ] README.md显示正确
- [ ] 版本号显示为1.0.0
- [ ] Release标签v1.0.0已创建
- [ ] `.env`文件没有被上传（安全）

---

## 后续更新代码

当您修改代码后，使用以下命令更新：

```powershell
git add .
git commit -m "更新描述"
git push
```

或者在GitHub Desktop中：
1. 查看更改
2. 填写提交信息
3. 点击"Commit to main"
4. 点击"Push origin"

---

## 推荐方案

**如果您是第一次使用Git**：
👉 **推荐使用方法一（GitHub Desktop）**，图形界面更简单直观。

**如果您熟悉命令行**：
👉 **推荐使用方法二（命令行）**，更灵活高效。

---

**完成上传后，您的代码将安全地保存在GitHub上！** 🎉

访问查看：https://github.com/q379078150-netizen/li
