#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M4A到MP3转换器
将audio_output目录中的m4a文件转换为mp3格式
"""

import os
import sys
import subprocess
from pathlib import Path

def check_ffmpeg():
    """检查FFmpeg是否可用"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, check=True)
        print("✓ FFmpeg 可用")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未找到 FFmpeg")
        print("请安装 FFmpeg:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu: sudo apt install ffmpeg")
        return False

def convert_m4a_to_mp3(input_file, output_file, quality="192k"):
    """将m4a文件转换为mp3"""
    cmd = [
        'ffmpeg',
        '-i', str(input_file),
        '-c:a', 'libmp3lame',
        '-b:a', quality,
        '-y',  # 覆盖输出文件
        str(output_file)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e}")
        return False

def main():
    print("=== M4A到MP3转换器 ===")
    print("将audio_output目录中的m4a文件转换为mp3格式\n")
    
    if not check_ffmpeg():
        return
    
    # 设置目录
    audio_dir = Path("./audio_output")
    if not audio_dir.exists():
        print(f"❌ 目录不存在: {audio_dir}")
        return
    
    # 查找m4a文件
    m4a_files = list(audio_dir.glob("*.m4a"))
    if not m4a_files:
        print("❌ 未找到m4a文件")
        return
    
    print(f"📁 找到 {len(m4a_files)} 个m4a文件")
    
    success_count = 0
    for i, m4a_file in enumerate(m4a_files, 1):
        # 生成mp3文件名
        mp3_file = m4a_file.with_suffix('.mp3')
        
        print(f"[{i}/{len(m4a_files)}] 转换: {m4a_file.name} -> {mp3_file.name}")
        
        if convert_m4a_to_mp3(m4a_file, mp3_file):
            print(f"  ✓ 转换成功")
            # 删除原始m4a文件
            try:
                m4a_file.unlink()
                print(f"  ✓ 已删除原文件")
            except Exception as e:
                print(f"  ⚠️ 删除原文件失败: {e}")
            success_count += 1
        else:
            print(f"  ❌ 转换失败")
    
    print(f"\n🎉 转换完成！")
    print(f"📊 成功转换: {success_count}/{len(m4a_files)} 个文件")
    
    # 列出最终的mp3文件
    mp3_files = list(audio_dir.glob("*.mp3"))
    if mp3_files:
        print(f"\n📁 MP3文件列表 ({len(mp3_files)} 个):")
        for i, file in enumerate(sorted(mp3_files), 1):
            file_size = file.stat().st_size / (1024 * 1024)  # MB
            print(f"  {i:2d}. {file.name} ({file_size:.1f} MB)")

if __name__ == "__main__":
    main()