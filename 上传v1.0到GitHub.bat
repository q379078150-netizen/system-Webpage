@echo off
chcp 65001 >nul
echo ========================================
echo 上传 v1.0.0 版本到 GitHub
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
    echo 3. 安装完成后，重新打开此脚本
    echo.
    pause
    exit /b 1
)
echo [成功] Git已安装
git --version
echo.

echo [1/8] 检查Git仓库状态...
if not exist .git (
    echo [执行] 初始化Git仓库...
    git init
    echo [成功] Git仓库已初始化
) else (
    echo [跳过] Git仓库已存在
)
echo.

echo [2/8] 配置远程仓库...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [执行] 添加远程仓库...
    git remote add origin https://github.com/q379078150-netizen/system-Webpage.git
    echo [成功] 远程仓库已添加
) else (
    echo [检查] 当前远程仓库...
    git remote get-url origin
    set /p update_remote="是否更新远程仓库地址? (y/n): "
    if /i "!update_remote!"=="y" (
        git remote set-url origin https://github.com/q379078150-netizen/system-Webpage.git
        echo [成功] 远程仓库地址已更新
    )
)
echo.

echo [3/8] 检查未提交的更改...
git add .
git status --short
if errorlevel 1 (
    echo [提示] 没有需要提交的文件
) else (
    echo [执行] 提交所有更改...
    git commit -m "Release v1.0.0: 情报推送系统首个稳定版本

功能特性:
- 实时快讯推送系统
- 多渠道推送支持（Ghost/Telegram/Discord）
- 每日简报生成
- The Block Beats风格三栏布局
- 暗色主题界面
- 完整API和文档

发布日期: 2025-01-19"
    echo [成功] 更改已提交
)
echo.

echo [4/8] 检查v1.0.0标签是否已存在...
git tag -l v1.0.0 >nul 2>&1
if not errorlevel 1 (
    echo [警告] v1.0.0标签已存在
    set /p overwrite="是否删除并重新创建? (y/n): "
    if /i "!overwrite!"=="y" (
        git tag -d v1.0.0
        echo [成功] 旧标签已删除
    ) else (
        echo [跳过] 保留现有标签
        goto :push
    )
)
echo.

echo [5/8] 创建v1.0.0版本标签...
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

:push
echo [6/8] 推送到GitHub...
echo [提示] 如果这是首次推送，可能需要输入GitHub用户名和密码
echo [提示] 建议使用Personal Access Token作为密码
echo.
set /p push_code="是否推送代码到main分支? (y/n): "
if /i "!push_code!"=="y" (
    git push -u origin main
    if errorlevel 1 (
        echo [警告] 代码推送失败，可能需要认证
        echo [提示] 请手动执行: git push -u origin main
    ) else (
        echo [成功] 代码已推送到GitHub
    )
) else (
    echo [跳过] 代码推送已取消
)
echo.

echo [7/8] 推送v1.0.0标签...
set /p push_tag="是否推送v1.0.0标签? (y/n): "
if /i "!push_tag!"=="y" (
    git push origin v1.0.0
    if errorlevel 1 (
        echo [警告] 标签推送失败，可能需要认证
        echo [提示] 请手动执行: git push origin v1.0.0
    ) else (
        echo [成功] 标签已推送到GitHub
    )
) else (
    echo [跳过] 标签推送已取消
)
echo.

echo [8/8] 验证上传结果...
echo [提示] 请访问以下链接查看:
echo https://github.com/q379078150-netizen/system-Webpage
echo.
echo [提示] 创建Release:
echo 1. 访问: https://github.com/q379078150-netizen/system-Webpage/releases/new
echo 2. Tag: v1.0.0
echo 3. Title: v1.0.0 - 情报推送系统首个稳定版本
echo 4. 填写描述并发布
echo.

echo ========================================
echo v1.0.0 版本上传完成！
echo ========================================
echo.
echo 版本信息:
echo - 标签名: v1.0.0
echo - 远程仓库: https://github.com/q379078150-netizen/system-Webpage
echo - 当前提交: 
git rev-parse HEAD
echo.
echo 下一步:
echo 1. 在GitHub上创建Release（可选）
echo 2. 查看代码: https://github.com/q379078150-netizen/system-Webpage
echo 3. 查看标签: git show v1.0.0
echo.
pause
