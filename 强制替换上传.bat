@echo off
chcp 65001 >nul
echo ========================================
echo 强制替换上传到 system-Webpage 仓库
echo 警告：这将覆盖仓库中的所有现有文件！
echo ========================================
echo.

echo [检查] Git是否已安装...
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Git未安装！
    echo.
    echo 请先安装Git:
    echo 1. 访问: https://git-scm.com/download/win
    echo 2. 或使用: winget install Git.Git
    echo.
    pause
    exit /b 1
)
echo [成功] Git已安装
echo.

echo [1/7] 初始化Git仓库...
if not exist .git (
    git init
    echo [成功] Git仓库已初始化
) else (
    echo [跳过] Git仓库已存在
)
echo.

echo [2/7] 配置远程仓库...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/q379078150-netizen/system-Webpage.git
echo [成功] 远程仓库已配置
echo.

echo [3/7] 配置Git用户信息...
git config user.name "q379078150-netizen" >nul 2>&1
git config user.email "q379078150-netizen@users.noreply.github.com" >nul 2>&1
echo [成功] 用户信息已配置
echo.

echo [4/7] 添加所有文件...
git add .
if errorlevel 1 (
    echo [错误] 添加文件失败
    pause
    exit /b 1
)
echo [成功] 所有文件已添加
echo.

echo [5/7] 提交更改...
git commit -m "Release v1.0.0: 情报推送系统 - 强制替换所有文件" --allow-empty
if errorlevel 1 (
    echo [警告] 提交可能失败，继续执行...
)
echo [成功] 更改已提交
echo.

echo [6/7] 设置主分支...
git branch -M main 2>nul
echo [成功] 分支已设置
echo.

echo [7/7] 强制推送到GitHub（覆盖现有文件）...
echo [警告] 这将覆盖仓库中的所有现有文件！
echo [提示] 如果要求输入密码，请使用Personal Access Token
echo [提示] 生成Token: https://github.com/settings/tokens
echo.
pause
echo.
git push -u origin main --force
if errorlevel 1 (
    echo.
    echo [错误] 推送失败
    echo.
    echo 可能的原因:
    echo 1. 认证失败 - 请使用Personal Access Token
    echo 2. 网络问题 - 请检查网络连接
    echo 3. 权限问题 - 请确认有仓库访问权限
    echo.
    echo 如果仍然失败，请尝试手动执行:
    echo git push -u origin main --force
    echo.
    pause
    exit /b 1
)
echo.
echo [成功] 所有文件已强制推送到GitHub
echo.

echo [8/8] 创建版本标签...
git tag -d v1.0.0 >nul 2>&1
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0 --force
if errorlevel 1 (
    echo [警告] 标签推送失败
) else (
    echo [成功] 版本标签v1.0.0已创建
)
echo.

echo ========================================
echo 强制替换上传完成！
echo ========================================
echo.
echo 仓库地址: https://github.com/q379078150-netizen/system-Webpage
echo.
echo 所有现有文件已被替换为新版本！
echo.
echo 下一步:
echo 1. 访问仓库查看: https://github.com/q379078150-netizen/system-Webpage
echo 2. 刷新页面确认文件已更新
echo 3. 在GitHub上创建Release（可选）
echo    - 访问: https://github.com/q379078150-netizen/system-Webpage/releases/new
echo    - Tag: v1.0.0
echo    - Title: v1.0.0 - 情报推送系统首次发布
echo.
pause
