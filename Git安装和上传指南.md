# 📤 Git安装和GitHub上传完整指南

## 第一步：安装Git（如果还没有安装）

### Windows系统

1. **下载Git**
   - 访问：https://git-scm.com/download/win
   - 下载最新版本的Git for Windows
   - 或者使用包管理器：
     ```powershell
     winget install Git.Git
     ```

2. **安装Git**
   - 运行下载的安装程序
   - 使用默认设置即可
   - 安装完成后重启终端

3. **验证安装**
   打开新的PowerShell或CMD窗口，执行：
   ```bash
   git --version
   ```
   如果显示版本号，说明安装成功。

### 如果不想安装Git（使用GitHub Desktop）

1. 下载GitHub Desktop：https://desktop.github.com/
2. 安装并登录GitHub账号
3. 使用图形界面操作（更简单）

---

## 第二步：准备上传到GitHub

### 方法一：使用命令行（推荐）

#### 1. 初始化Git仓库

在项目根目录（`C:\Users\86138\.config\clash\profiles`）打开PowerShell，执行：

```powershell
git init
```

#### 2. 配置Git用户信息（首次使用需要）

```powershell
git config --global user.name "您的名字"
git config --global user.email "您的邮箱"
```

#### 3. 添加所有文件

```powershell
git add .
```

#### 4. 提交到本地仓库

```powershell
git commit -m "Release v1.0.0: 情报推送系统首次发布"
```

#### 5. 在GitHub上创建仓库

1. 访问 https://github.com 并登录
2. 点击右上角的 **"+"** → **"New repository"**
3. 填写信息：
   - **Repository name**: `intelligence-push-system`
   - **Description**: `智能情报推送系统 v1.0.0`
   - **Visibility**: Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
4. 点击 **"Create repository"**

#### 6. 连接本地仓库到GitHub

GitHub会显示仓库地址，类似：
```
https://github.com/your-username/intelligence-push-system.git
```

在本地执行（替换为您的实际地址）：

```powershell
git remote add origin https://github.com/your-username/intelligence-push-system.git
```

#### 7. 推送到GitHub

```powershell
git branch -M main
git push -u origin main
```

**如果遇到认证问题**：
- 使用Personal Access Token作为密码
- 生成Token：https://github.com/settings/tokens
- 权限至少选择 `repo`

#### 8. 创建版本标签

```powershell
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

---

### 方法二：使用GitHub Desktop（更简单）

1. **安装GitHub Desktop**
   - 下载：https://desktop.github.com/
   - 安装并登录GitHub账号

2. **添加仓库**
   - 打开GitHub Desktop
   - 点击 **"File"** → **"Add Local Repository"**
   - 选择项目目录：`C:\Users\86138\.config\clash\profiles`

3. **提交更改**
   - 在GitHub Desktop中会看到所有文件
   - 在左下角填写提交信息：`Release v1.0.0: 情报推送系统首次发布`
   - 点击 **"Commit to main"**

4. **发布到GitHub**
   - 点击 **"Publish repository"**
   - 填写仓库名称和描述
   - 选择Public或Private
   - 点击 **"Publish repository"**

5. **创建Release**
   - 在GitHub网站上访问您的仓库
   - 点击 **"Releases"** → **"Create a new release"**
   - Tag: `v1.0.0`
   - Title: `v1.0.0 - 首次发布`
   - 描述：可以复制 `CHANGELOG.md` 的内容
   - 点击 **"Publish release"**

---

## 第三步：使用自动化脚本（Windows）

我已经为您创建了自动化脚本，可以直接使用：

### 使用 upload_to_github.bat

1. **先配置远程仓库**（只需一次）：
   ```powershell
   git remote add origin https://github.com/your-username/intelligence-push-system.git
   ```

2. **运行脚本**：
   ```powershell
   .\upload_to_github.bat
   ```

脚本会自动执行：
- 检查Git初始化
- 添加所有文件
- 提交更改
- 推送到GitHub
- 创建版本标签

---

## 快速命令总结

```powershell
# 1. 初始化Git（如果还没有）
git init

# 2. 配置用户信息（首次使用）
git config --global user.name "您的名字"
git config --global user.email "您的邮箱"

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Release v1.0.0: 情报推送系统首次发布"

# 5. 添加远程仓库（替换为您的地址）
git remote add origin https://github.com/your-username/intelligence-push-system.git

# 6. 推送到GitHub
git branch -M main
git push -u origin main

# 7. 创建版本标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

---

## 常见问题

### Q1: 提示"git不是内部或外部命令"

**解决**：需要安装Git，参考第一步。

### Q2: 认证失败

**解决**：
1. 使用Personal Access Token代替密码
2. 生成Token：https://github.com/settings/tokens
3. 权限选择：`repo`（完整仓库访问权限）

### Q3: 分支名称不匹配

**解决**：
```powershell
git branch -M main
```

### Q4: 想更新代码

**解决**：
```powershell
git add .
git commit -m "更新描述"
git push
```

---

## 重要提示

⚠️ **安全提示**：
- `.env` 文件已添加到 `.gitignore`，不会被上传
- 确保敏感信息（API密钥等）不会提交到GitHub
- 如果误提交了敏感信息，立即在GitHub上删除并重新生成密钥

✅ **已准备的文件**：
- ✅ `VERSION` - 版本号文件
- ✅ `CHANGELOG.md` - 更新日志
- ✅ `.gitignore` - Git忽略文件
- ✅ `README.md` - 已更新版本信息

---

## 完成后的检查清单

- [ ] Git已安装并配置
- [ ] GitHub仓库已创建
- [ ] 本地代码已提交
- [ ] 代码已推送到GitHub
- [ ] 版本标签v1.0.0已创建
- [ ] GitHub Release已创建（可选）

---

**完成！** 您的代码现在已经安全地保存在GitHub上了！🎉

访问您的仓库：`https://github.com/your-username/intelligence-push-system`
