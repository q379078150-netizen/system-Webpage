@echo off
echo ========================================
echo 情报推送系统 - GitHub上传脚本
echo ========================================
echo.

echo [1/6] 检查Git是否已初始化...
if not exist .git (
    echo 初始化Git仓库...
    git init
) else (
    echo Git仓库已存在
)
echo.

echo [2/6] 检查远程仓库...
git remote -v
if errorlevel 1 (
    echo 警告: 未找到远程仓库
    echo 请先执行: git remote add origin YOUR_GITHUB_URL
    pause
    exit /b 1
)
echo.

echo [3/6] 添加所有文件到Git...
git add .
echo.

echo [4/6] 提交更改...
git commit -m "Release v1.0.0: 情报推送系统首次发布"
echo.

echo [5/6] 推送到GitHub...
git push -u origin main
if errorlevel 1 (
    echo 尝试推送到master分支...
    git push -u origin master
)
echo.

echo [6/6] 创建版本标签...
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
echo.

echo ========================================
echo 上传完成！
echo ========================================
echo.
echo 如果遇到认证问题，请使用Personal Access Token
echo 访问: https://github.com/settings/tokens
echo.
pause
