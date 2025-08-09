#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MP3文件重命名工具
去掉文件名中与歌曲名无关的部分，只保留歌曲名称和扩展名
"""

import os
import re
from pathlib import Path

def extract_song_name(filename):
    """从文件名中提取歌曲名称"""
    # 去掉扩展名
    name_without_ext = filename.rsplit('.', 1)[0]
    
    # 最新格式：序号_【合集标题】 p序号 歌曲名-歌手-立体声伴奏
    # 例如：01_【合集11首】周华健-经典歌曲高品质立体声伴奏合集-精品伴奏馆 p01 爱相随-周华健-立体声伴奏
    pattern_latest = r'^\d+_.*?\sp\d+\s+(.+?)(?:-.*?-.*?)?$'
    match = re.search(pattern_latest, name_without_ext)
    if match:
        song_name = match.group(1).strip()
        # 如果歌曲名中还有-，取第一个-之前的部分
        if '-' in song_name:
            song_name = song_name.split('-')[0].strip()
        return song_name
    
    # 王杰格式：序号_【Hi-Res无损音质】2025年王杰100首精选歌曲合集...p序号 序号.歌曲名
    # 例如：01_【Hi-Res无损音质】2025年王杰100首精选歌曲合集（只选播放量最高的）值得单曲循环的歌单！ p01 1.谁明浪子心
    pattern_new = r'^\d+_.*?\sp\d+\s+\d+\.(.+)$'
    match = re.search(pattern_new, name_without_ext)
    if match:
        song_name = match.group(1).strip()
        return song_name
    
    # 旧格式1：序号_长标题 p序号 歌曲名-电影名-年份
    # 例如：01_70后 80后 90后 欧美奥斯卡电影金曲精选合集（1940-2015）珍藏版 值得回味收藏！ p01 【开头王炸】My heart will go on-泰坦尼克号-1997
    pattern1 = r'^\d+_.*?\sp\d+\s+(?:【.*?】)?(.+?)(?:-.*?-\d{4})?$'
    match = re.search(pattern1, name_without_ext)
    if match:
        song_name = match.group(1).strip()
        return song_name
    
    # 旧格式2：NA_开头的格式
    # 例如：NA_奥斯卡百年金曲《Say You, Say Me》，歌声飘过36年，永恒的经典
    pattern2 = r'^NA_.*?《(.+?)》.*$'
    match = re.search(pattern2, name_without_ext)
    if match:
        song_name = match.group(1).strip()
        return song_name
    
    # 如果都不匹配，尝试提取最后一个-之前的部分作为歌曲名
    pattern3 = r'^.*?\s+(.+?)(?:-.*?-\d{4})?$'
    match = re.search(pattern3, name_without_ext)
    if match:
        song_name = match.group(1).strip()
        return song_name
    
    # 如果都不匹配，返回原文件名（去掉扩展名）
    return name_without_ext

def clean_filename(filename):
    """清理文件名，去掉不合法字符"""
    # 替换不合法的文件名字符
    illegal_chars = r'[<>:"/\\|?*]'
    cleaned = re.sub(illegal_chars, '_', filename)
    
    # 去掉多余的空格和点
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    cleaned = cleaned.strip('.')
    
    return cleaned

def rename_mp3_files(directory="./downloads"):
    """重命名指定目录中的MP3文件"""
    print("=== MP3文件重命名工具 ===")
    print("去掉文件名中与歌曲名无关的部分，只保留歌曲名称\n")
    
    # 检查目录是否存在
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"❌ 目录不存在: {directory}")
        return
    
    # 查找MP3文件
    mp3_files = list(dir_path.glob("*.mp3"))
    if not mp3_files:
        print(f"❌ 在 {directory} 目录中未找到MP3文件")
        return
    
    print(f"📁 找到 {len(mp3_files)} 个MP3文件")
    print("\n开始重命名...\n")
    
    success_count = 0
    for i, mp3_file in enumerate(mp3_files, 1):
        old_name = mp3_file.name
        
        # 提取歌曲名称
        song_name = extract_song_name(old_name)
        
        # 清理文件名
        clean_song_name = clean_filename(song_name)
        
        # 生成新文件名
        new_name = f"{clean_song_name}.mp3"
        new_path = mp3_file.parent / new_name
        
        print(f"[{i:2d}/{len(mp3_files)}] {old_name}")
        print(f"     -> {new_name}")
        
        # 检查新文件名是否已存在
        if new_path.exists() and new_path != mp3_file:
            print(f"     ⚠️ 目标文件已存在，跳过")
            continue
        
        # 如果新旧文件名相同，跳过
        if old_name == new_name:
            print(f"     ✓ 文件名已是最佳格式，无需修改")
            success_count += 1
            continue
        
        try:
            # 重命名文件
            mp3_file.rename(new_path)
            print(f"     ✓ 重命名成功")
            success_count += 1
        except Exception as e:
            print(f"     ❌ 重命名失败: {e}")
        
        print()
    
    print(f"🎉 重命名完成！")
    print(f"📊 成功处理: {success_count}/{len(mp3_files)} 个文件")
    
    # 显示重命名后的文件列表
    updated_files = list(dir_path.glob("*.mp3"))
    if updated_files:
        print(f"\n📁 重命名后的MP3文件列表 ({len(updated_files)} 个):")
        for i, file in enumerate(sorted(updated_files), 1):
            file_size = file.stat().st_size / (1024 * 1024)  # MB
            print(f"  {i:2d}. {file.name} ({file_size:.1f} MB)")

def main():
    """主函数"""
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "./downloads"
    
    rename_mp3_files(directory)

if __name__ == "__main__":
    main()