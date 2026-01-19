@echo off
chcp 65001 >nul
echo ========================================
echo 上传到GitHub仓库: q379078150-netizen/system-Webpage
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

echo [1/8] 检查Git是否已初始化...
if not exist .git (
    echo [执行] 初始化Git仓库...
    git init
) else (
    echo [跳过] Git仓库已存在
)
echo.

echo [2/8] 检查远程仓库配置...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [执行] 添加远程仓库...
    git remote add origin https://github.com/q379078150-netizen/system-Webpage.git
    echo [成功] 远程仓库已添加
) else (
    echo [检查] 当前远程仓库:
    git remote -v
    echo.
    set /p confirm="是否要更新远程仓库地址? (y/n): "
    if /i "%confirm%"=="y" (
        git remote set-url origin https://github.com/q379078150-netizen/system-Webpage.git
        echo [成功] 远程仓库地址已更新
    )
)
echo.

echo [3/8] 拉取现有内容（处理可能的冲突）...
git fetch origin >nul 2>&1
if not errorlevel 1 (
    echo [执行] 拉取远程内容...
    git pull origin main --allow-unrelated-histories >nul 2>&1
    if not errorlevel 1 (
        echo [成功] 远程内容已拉取
        echo [处理] 如果有README.md冲突，保留新版本...
        git checkout --ours README.md >nul 2>&1
    ) else (
        echo [跳过] 无法拉取（可能是空仓库或网络问题）
    )
) else (
    echo [跳过] 无法连接远程仓库（首次推送）
)
echo.

echo [4/8] 添加所有文件到Git...
git add .
if errorlevel 1 (
    echo [错误] 添加文件失败
    pause
    exit /b 1
)
echo [成功] 文件已添加
echo.

echo [5/8] 提交更改...
git commit -m "Release v1.0.0: 情报推送系统首次发布" >nul 2>&1
if errorlevel 1 (
    echo [警告] 提交失败，可能没有更改或已提交
    echo [提示] 尝试强制提交...
    git commit -m "Release v1.0.0: 情报推送系统首次发布" --allow-empty
) else (
    echo [成功] 更改已提交
)
echo.

echo [6/8] 设置主分支...
git branch -M main 2>nul
echo [成功] 分支已设置
echo.

echo [7/8] 推送到GitHub...
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
    echo 4. 冲突问题 - 可能需要先拉取: git pull origin main --rebase
    echo.
    pause
    exit /b 1
)
echo [成功] 代码已推送到GitHub
echo.

echo [8/8] 创建版本标签...
git tag -a v1.0.0 -m "Release version 1.0.0" 2>nul
if errorlevel 1 (
    echo [警告] 标签可能已存在，尝试删除后重新创建...
    git tag -d v1.0.0 2>nul
    git tag -a v1.0.0 -m "Release version 1.0.0"
)
git push origin v1.0.0 2>nul
if errorlevel 1 (
    echo [警告] 标签推送失败（可能已存在）
) else (
    echo [成功] 版本标签v1.0.0已创建
)
echo.

echo ========================================
echo 上传完成！
echo ========================================
echo.
echo 仓库地址: https://github.com/q379078150-netizen/system-Webpage
echo.
echo 下一步:
echo 1. 访问仓库查看上传的文件
echo 2. 在GitHub上创建Release（可选）
echo    - 访问: https://github.com/q379078150-netizen/system-Webpage/releases/new
echo    - Tag: v1.0.0
echo    - Title: v1.0.0 - 情报推送系统首次发布
echo    - Description: 可以复制 CHANGELOG.md 的内容
echo.
pause
