#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版B站音频提取器
更轻量级的实现，减少依赖
"""

import os
import sys
import re
import subprocess
from pathlib import Path

class SimpleBilibiliExtractor:
    def __init__(self, output_dir="./audio_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def check_yt_dlp(self):
        """检查yt-dlp是否可用"""
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ yt-dlp 版本: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            pass
        
        print("❌ 未找到 yt-dlp")
        print("安装方法:")
        print("  pip install yt-dlp")
        print("  或者: brew install yt-dlp (macOS)")
        return False
    
    def extract_audio_simple(self, url):
        """使用yt-dlp直接提取音频"""
        if not self.check_yt_dlp():
            return False
        
        print(f"\n开始提取音频: {url}")
        
        # 构建yt-dlp命令
        cmd = [
            'yt-dlp',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--audio-quality', '192K',
            '--output', str(self.output_dir / '%(playlist_index)02d_%(title)s.%(ext)s'),
            '--postprocessor-args', 'ffmpeg:-c:a libmp3lame -b:a 192k',
            '--ignore-errors',
            '--no-warnings',
            url
        ]
        
        try:
            print("正在下载和转换音频...")
            result = subprocess.run(cmd, check=True, text=True)
            print("✓ 音频提取完成！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 提取失败: {e}")
            return False
    
    def list_output_files(self):
        """列出输出的音频文件"""
        audio_files = list(self.output_dir.glob('*.mp3'))
        if audio_files:
            print(f"\n📁 输出目录: {self.output_dir.absolute()}")
            print(f"📄 共生成 {len(audio_files)} 个音频文件:")
            for i, file in enumerate(sorted(audio_files), 1):
                print(f"  {i}. {file.name}")
        else:
            print("\n❌ 未找到生成的音频文件")

def main():
    print("=== 简化版B站音频提取器 ===")
    print("快速提取B站视频音频为MP3格式\n")
    
    # 获取URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("请输入B站视频URL: ").strip()
    
    if not url:
        print("❌ 请提供有效的URL")
        return
    
    # 验证URL
    if 'bilibili.com' not in url and 'b23.tv' not in url:
        print("❌ 请提供有效的B站视频URL")
        return
    
    # 创建提取器并开始工作
    extractor = SimpleBilibiliExtractor()
    
    if extractor.extract_audio_simple(url):
        extractor.list_output_files()
    else:
        print("\n❌ 音频提取失败，请检查URL和网络连接")

if __name__ == "__main__":
    main()