@echo off
chcp 65001 >nul
echo ========================================
echo 上传到GitHub仓库: q379078150-netizen/li
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
    echo 或者使用GitHub Desktop（更简单）:
    echo 访问: https://desktop.github.com/
    echo.
    pause
    exit /b 1
)
echo [成功] Git已安装
echo.

echo [1/7] 检查Git是否已初始化...
if not exist .git (
    echo [执行] 初始化Git仓库...
    git init
) else (
    echo [跳过] Git仓库已存在
)
echo.

echo [2/7] 检查远程仓库配置...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [执行] 添加远程仓库...
    git remote add origin https://github.com/q379078150-netizen/li.git
    echo [成功] 远程仓库已添加
) else (
    echo [检查] 当前远程仓库:
    git remote -v
    echo.
    set /p confirm="是否要更新远程仓库地址? (y/n): "
    if /i "%confirm%"=="y" (
        git remote set-url origin https://github.com/q379078150-netizen/li.git
        echo [成功] 远程仓库地址已更新
    )
)
echo.

echo [3/7] 添加所有文件到Git...
git add .
if errorlevel 1 (
    echo [错误] 添加文件失败
    pause
    exit /b 1
)
echo [成功] 文件已添加
echo.

echo [4/7] 提交更改...
git commit -m "Release v1.0.0: 情报推送系统首次发布" >nul 2>&1
if errorlevel 1 (
    echo [警告] 提交失败，可能没有更改或已提交
) else (
    echo [成功] 更改已提交
)
echo.

echo [5/7] 设置主分支...
git branch -M main 2>nul
echo [成功] 分支已设置
echo.

echo [6/7] 推送到GitHub...
echo [提示] 如果要求输入密码，请使用Personal Access Token
echo [提示] 生成Token: https://github.com/settings/tokens
echo.
git push -u origin main
if errorlevel 1 (
    echo [错误] 推送失败
    echo.
    echo 可能的原因:
    echo 1. 认证失败 - 请使用Personal Access Token
    echo 2. 网络问题 - 请检查网络连接
    echo 3. 权限问题 - 请确认有仓库访问权限
    echo.
    pause
    exit /b 1
)
echo [成功] 代码已推送到GitHub
echo.

echo [7/7] 创建版本标签...
git tag -a v1.0.0 -m "Release version 1.0.0" 2>nul
git push origin v1.0.0 2>nul
if errorlevel 1 (
    echo [警告] 标签创建失败（可能已存在）
) else (
    echo [成功] 版本标签v1.0.0已创建
)
echo.

echo ========================================
echo 上传完成！
echo ========================================
echo.
echo 仓库地址: https://github.com/q379078150-netizen/li
echo.
echo 下一步:
echo 1. 访问仓库查看上传的文件
echo 2. 在GitHub上创建Release（可选）
echo    - 访问: https://github.com/q379078150-netizen/li/releases/new
echo    - Tag: v1.0.0
echo    - Title: v1.0.0 - 情报推送系统首次发布
echo.
pause
