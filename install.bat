@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo === B站音频提取器安装脚本 (Windows) ===
echo.

REM 检查Python
echo 🔍 检查Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python3
    echo    下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python 已安装: %PYTHON_VERSION%
echo.

REM 检查pip
echo 🔍 检查pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到pip，请重新安装Python并确保包含pip
    pause
    exit /b 1
)
echo ✓ pip 已安装
echo.

REM 检查FFmpeg
echo 🔧 检查FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到FFmpeg
    echo.
    echo 请手动安装FFmpeg:
    echo 1. 访问 https://ffmpeg.org/download.html
    echo 2. 下载Windows版本
    echo 3. 解压到某个目录（如 C:\ffmpeg）
    echo 4. 将 C:\ffmpeg\bin 添加到系统PATH环境变量
    echo 5. 重新打开命令提示符并运行此脚本
    echo.
    pause
    exit /b 1
) else (
    echo ✓ FFmpeg 已安装
)
echo.

REM 安装Python依赖
echo 📦 安装Python依赖...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    pip install yt-dlp requests
)
if %errorlevel% neq 0 (
    echo ❌ Python依赖安装失败
    pause
    exit /b 1
)
echo ✓ Python依赖安装完成
echo.

REM 测试安装
echo 🧪 测试安装...
python -c "import yt_dlp; print('yt-dlp导入成功')" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ yt-dlp 测试失败
    pause
    exit /b 1
)
echo ✓ yt-dlp 测试通过

ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ FFmpeg 测试失败
    pause
    exit /b 1
)
echo ✓ FFmpeg 测试通过
echo.

REM 创建输出目录
echo 📁 创建输出目录...
if not exist "downloads" mkdir downloads
if not exist "audio_output" mkdir audio_output
echo ✓ 输出目录创建完成
echo.

echo 🎉 安装完成！
echo.
echo 使用方法:
echo   完整版: python bilibili_audio_extractor.py
echo   简化版: python simple_extractor.py
echo.
echo 示例:
echo   python simple_extractor.py "https://www.bilibili.com/video/BV1xx411c7mD"
echo.
pause