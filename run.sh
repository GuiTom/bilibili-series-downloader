#!/bin/bash

# B站音频提取器启动脚本
# 自动激活虚拟环境并运行程序

set -e

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 ./install.sh"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

echo "=== B站音频提取器 ==="
echo "🐍 虚拟环境已激活"
echo

# 检查参数
if [ $# -eq 0 ]; then
    echo "请选择要使用的程序:"
    echo "1. 简化版 (推荐)"
    echo "2. 完整版"
    echo "3. 高级版 (并发下载)"
    echo "4. 转换M4A为MP3"
    echo "5. 重命名MP3文件"
    echo
    read -p "请输入选择 (1-5): " choice
    echo
    
    case $choice in
        1)
            read -p "请输入B站视频URL: " url
            python simple_extractor.py "$url"
            ;;
        2)
            read -p "请输入B站视频URL: " url
            python bilibili_audio_extractor.py "$url"
            ;;
        3)
            read -p "请输入B站视频URL: " url
            python advanced_extractor.py "$url"
            ;;
        4)
            echo "启动M4A到MP3转换器..."
            python convert_to_mp3.py
            ;;
        5)
            echo "启动MP3文件重命名工具..."
            python rename_mp3.py
            ;;
        *)
            echo "❌ 无效选择"
            exit 1
            ;;
    esac
else
    # 如果提供了URL参数，使用简化版
    python simple_extractor.py "$1"
fi

echo
echo "🎉 程序执行完成！"
echo "📁 请检查输出目录中的音频文件"