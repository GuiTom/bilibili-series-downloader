#!/bin/bash

# B站音频提取器安装脚本
# 适用于 macOS 和 Linux

set -e

echo "=== B站音频提取器安装脚本 ==="
echo

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    echo "❌ 不支持的操作系统: $OSTYPE"
    exit 1
fi

echo "检测到操作系统: $OS"
echo

# 检查Python
echo "🔍 检查Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo "✓ Python3 已安装: $PYTHON_VERSION"
else
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi
echo

# 检查pip
echo "🔍 检查pip..."
if command -v pip3 &> /dev/null; then
    echo "✓ pip3 已安装"
else
    echo "❌ 未找到pip3，请先安装pip"
    exit 1
fi
echo

# 安装FFmpeg
echo "🔧 安装FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg 已安装"
else
    echo "正在安装FFmpeg..."
    if [[ "$OS" == "macOS" ]]; then
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "❌ 未找到Homebrew，请手动安装FFmpeg"
            echo "   安装Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            echo "   然后运行: brew install ffmpeg"
            exit 1
        fi
    elif [[ "$OS" == "Linux" ]]; then
        if command -v apt &> /dev/null; then
            sudo apt update
            sudo apt install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        elif command -v pacman &> /dev/null; then
            sudo pacman -S ffmpeg
        else
            echo "❌ 无法自动安装FFmpeg，请手动安装"
            exit 1
        fi
    fi
    echo "✓ FFmpeg 安装完成"
fi
echo

# 创建虚拟环境
echo "🐍 创建Python虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 虚拟环境创建完成"
else
    echo "✓ 虚拟环境已存在"
fi
echo

# 激活虚拟环境并安装依赖
echo "📦 安装Python依赖..."
source venv/bin/activate
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install yt-dlp requests
fi
echo "✓ Python依赖安装完成"
echo

# 测试安装
echo "🧪 测试安装..."
source venv/bin/activate
if python -c "import yt_dlp; print('yt-dlp导入成功')" 2>/dev/null; then
    echo "✓ yt-dlp 测试通过"
else
    echo "❌ yt-dlp 测试失败"
    exit 1
fi

if ffmpeg -version &> /dev/null; then
    echo "✓ FFmpeg 测试通过"
else
    echo "❌ FFmpeg 测试失败"
    exit 1
fi
echo

# 创建输出目录
echo "📁 创建输出目录..."
mkdir -p downloads audio_output
echo "✓ 输出目录创建完成"
echo

echo "🎉 安装完成！"
echo
echo "使用方法 (记得先激活虚拟环境):"
echo "  source venv/bin/activate"
echo "  python bilibili_audio_extractor.py"
echo "  python simple_extractor.py"
echo
echo "示例:"
echo "  source venv/bin/activate"
echo "  python simple_extractor.py 'https://www.bilibili.com/video/BV1xx411c7mD'"
echo