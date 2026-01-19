@echo off
chcp 65001 >nul
echo ========================================
echo 创建 v1.0.0 版本标签
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

echo [1/5] 检查Git仓库状态...
if not exist .git (
    echo [执行] 初始化Git仓库...
    git init
)
git status
echo.

echo [2/5] 检查是否有未提交的更改...
git diff --quiet
if errorlevel 1 (
    echo [提示] 发现未提交的更改
    echo [执行] 添加所有文件...
    git add .
    echo.
    set /p commit_msg="请输入提交信息（直接回车使用默认）: "
    if "!commit_msg!"=="" set commit_msg=Release v1.0.0: 完整功能版本
    git commit -m "!commit_msg!"
    echo [成功] 更改已提交
) else (
    echo [跳过] 没有未提交的更改
)
echo.

echo [3/5] 检查v1.0.0标签是否已存在...
git tag -l v1.0.0 >nul 2>&1
if not errorlevel 1 (
    echo [警告] v1.0.0标签已存在
    set /p overwrite="是否删除并重新创建? (y/n): "
    if /i "!overwrite!"=="y" (
        git tag -d v1.0.0
        echo [成功] 旧标签已删除
    ) else (
        echo [取消] 操作已取消
        pause
        exit /b 0
    )
)
echo.

echo [4/5] 创建v1.0.0版本标签...
git tag -a v1.0.0 -m "Release version 1.0.0

功能特性:
- 实时快讯推送系统
- 多渠道推送支持（Ghost/Telegram/Discord）
- 每日简报生成
- The Block Beats风格三栏布局
- 暗色主题界面
- 完整API和文档

发布日期: 2025-01-19"
if errorlevel 1 (
    echo [错误] 标签创建失败
    pause
    exit /b 1
)
echo [成功] 版本标签v1.0.0已创建
echo.

echo [5/5] 检查远程仓库配置...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [警告] 未配置远程仓库
    echo [提示] 标签已创建在本地，但无法推送到远程
    echo [提示] 如需推送，请先配置: git remote add origin YOUR_REPO_URL
) else (
    echo [执行] 推送标签到GitHub...
    git push origin v1.0.0
    if errorlevel 1 (
        echo [警告] 标签推送失败（可能需要认证）
        echo [提示] 请手动执行: git push origin v1.0.0
    ) else (
        echo [成功] 标签已推送到GitHub
    )
)
echo.

echo ========================================
echo v1.0.0 版本标签创建完成！
echo ========================================
echo.
echo 版本信息:
echo - 标签名: v1.0.0
echo - 当前提交: 
git rev-parse HEAD
echo.
echo 回退方法:
echo 1. 查看标签: git show v1.0.0
echo 2. 切换到标签: git checkout v1.0.0
echo 3. 创建回退分支: git checkout -b rollback-v1.0.0 v1.0.0
echo.
echo 下一步:
echo 1. 在GitHub上创建Release（可选）
echo    - 访问: https://github.com/q379078150-netizen/system-Webpage/releases/new
echo    - Tag: v1.0.0
echo    - Title: v1.0.0 - 情报推送系统首个稳定版本
echo.
pause
