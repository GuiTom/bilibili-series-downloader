#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站视频音频提取器
支持单个视频和合集视频的音频提取，输出为MP3格式
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs

try:
    import yt_dlp
except ImportError:
    print("错误：未安装 yt-dlp，请运行: pip install yt-dlp")
    sys.exit(1)

class BilibiliAudioExtractor:
    def __init__(self, output_dir="./downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # yt-dlp 配置
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '192',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'writeinfojson': True,
            'ignoreerrors': True,
        }
    
    def check_dependencies(self):
        """检查必要的依赖是否安装"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
            print("✓ FFmpeg 已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ 错误：未找到 FFmpeg")
            print("请安装 FFmpeg:")
            print("  macOS: brew install ffmpeg")
            print("  Ubuntu: sudo apt install ffmpeg")
            print("  Windows: 从 https://ffmpeg.org/download.html 下载")
            return False
        return True
    
    def extract_video_id(self, url):
        """从B站URL中提取视频ID"""
        patterns = [
            r'bilibili\.com/video/([^/?]+)',
            r'b23\.tv/([^/?]+)',
            r'BV([A-Za-z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                if not video_id.startswith('BV'):
                    video_id = 'BV' + video_id
                return video_id
        return None
    
    def get_video_info(self, url):
        """获取视频信息"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            print(f"获取视频信息失败: {e}")
            return None
    
    def download_audio(self, url, custom_title=None):
        """下载单个视频的音频"""
        try:
            opts = self.ydl_opts.copy()
            if custom_title:
                # 清理文件名中的非法字符
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', custom_title)
                opts['outtmpl'] = str(self.output_dir / f'{safe_title}.%(ext)s')
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                print(f"✓ 音频提取完成: {custom_title or url}")
                return True
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return False
    
    def extract_from_collection(self, url):
        """从合集中提取所有视频的音频"""
        print(f"正在分析合集: {url}")
        
        # 获取合集信息
        info = self.get_video_info(url)
        if not info:
            return False
        
        # 检查是否为合集
        if 'entries' in info:
            print(f"发现合集，共 {len(info['entries'])} 个视频")
            
            success_count = 0
            for i, entry in enumerate(info['entries'], 1):
                if entry is None:
                    continue
                    
                title = entry.get('title', f'Video_{i}')
                video_url = entry.get('webpage_url') or entry.get('url')
                
                print(f"\n[{i}/{len(info['entries'])}] 正在处理: {title}")
                
                if self.download_audio(video_url, f"{i:02d}_{title}"):
                    success_count += 1
            
            print(f"\n合集处理完成！成功提取 {success_count}/{len(info['entries'])} 个音频文件")
            return success_count > 0
        else:
            # 单个视频
            print("这是单个视频，正在提取音频...")
            title = info.get('title', 'Unknown')
            return self.download_audio(url, title)
    
    def extract_audio_from_url(self, url):
        """主要的音频提取方法"""
        if not self.check_dependencies():
            return False
        
        print(f"开始处理: {url}")
        
        # 标准化URL
        if 'b23.tv' in url:
            # 处理短链接
            try:
                import requests
                response = requests.head(url, allow_redirects=True)
                url = response.url
            except:
                pass
        
        return self.extract_from_collection(url)

def main():
    print("=== B站视频音频提取器 ===")
    print("支持单个视频和合集视频的音频提取")
    print()
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("请输入B站视频URL: ").strip()
    
    if not url:
        print("错误：请提供有效的URL")
        return
    
    # 创建提取器实例
    extractor = BilibiliAudioExtractor()
    
    # 开始提取
    success = extractor.extract_audio_from_url(url)
    
    if success:
        print(f"\n✓ 所有音频文件已保存到: {extractor.output_dir.absolute()}")
    else:
        print("\n❌ 提取过程中出现错误")

if __name__ == "__main__":
    main()