#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级B站音频提取器
支持配置文件、并发下载、进度显示等高级功能
"""

import os
import sys
import json
import asyncio
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yt_dlp
except ImportError:
    print("错误：未安装 yt-dlp，请运行: pip install yt-dlp")
    sys.exit(1)

class AdvancedBilibiliExtractor:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.output_dir = Path(self.config['output_directory'])
        self.output_dir.mkdir(exist_ok=True)
        
        # 设置yt-dlp选项
        self.setup_ydl_options()
    
    def load_config(self, config_file: str) -> Dict:
        """加载配置文件"""
        config_path = Path(config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"✓ 已加载配置文件: {config_file}")
                return config
            except Exception as e:
                print(f"⚠️ 配置文件加载失败: {e}，使用默认配置")
        
        # 默认配置
        return {
            "output_directory": "./downloads",
            "audio_format": "mp3",
            "audio_quality": "192",
            "filename_template": "%(playlist_index)02d_%(title)s.%(ext)s",
            "max_concurrent_downloads": 3,
            "retry_attempts": 3,
            "download_options": {
                "writeinfojson": True,
                "writethumbnail": False
            },
            "postprocessor_options": {
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        }
    
    def setup_ydl_options(self):
        """设置yt-dlp选项"""
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(self.output_dir / self.config['filename_template']),
            'extractaudio': True,
            'audioformat': self.config['audio_format'],
            'audioquality': self.config['audio_quality'],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                **self.config['postprocessor_options']
            }],
            'ignoreerrors': True,
            'retries': self.config.get('retry_attempts', 3),
            **self.config.get('download_options', {})
        }
        
        # 添加代理设置
        if self.config.get('proxy', {}).get('enabled'):
            proxy_config = self.config['proxy']
            if proxy_config.get('http_proxy'):
                self.ydl_opts['proxy'] = proxy_config['http_proxy']
        
        # 添加用户代理和头部
        if self.config.get('user_agent'):
            self.ydl_opts['user_agent'] = self.config['user_agent']
        
        if self.config.get('headers'):
            self.ydl_opts['http_headers'] = self.config['headers']
    
    def progress_hook(self, d):
        """下载进度回调"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                print(f"\r下载进度: {percent:.1f}% ({d['downloaded_bytes']}/{d['total_bytes']} bytes)", end='')
            elif '_percent_str' in d:
                print(f"\r下载进度: {d['_percent_str']}", end='')
        elif d['status'] == 'finished':
            print(f"\n✓ 下载完成: {d['filename']}")
    
    def download_single_video(self, url: str, title: str = None) -> bool:
        """下载单个视频的音频"""
        try:
            opts = self.ydl_opts.copy()
            opts['progress_hooks'] = [self.progress_hook]
            
            if title:
                print(f"\n🎵 正在处理: {title}")
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                return True
        except Exception as e:
            print(f"\n❌ 下载失败: {e}")
            return False
    
    def get_playlist_info(self, url: str) -> Optional[Dict]:
        """获取播放列表信息"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            print(f"获取视频信息失败: {e}")
            return None
    
    def download_playlist_concurrent(self, url: str) -> bool:
        """并发下载播放列表"""
        print(f"🔍 正在分析播放列表: {url}")
        
        info = self.get_playlist_info(url)
        if not info:
            return False
        
        if 'entries' not in info:
            # 单个视频
            title = info.get('title', 'Unknown')
            print(f"📹 检测到单个视频: {title}")
            return self.download_single_video(url, title)
        
        # 播放列表
        entries = [entry for entry in info['entries'] if entry is not None]
        total_videos = len(entries)
        
        print(f"📋 检测到播放列表，共 {total_videos} 个视频")
        print(f"🔧 使用 {self.config['max_concurrent_downloads']} 个并发下载")
        
        success_count = 0
        
        # 使用线程池进行并发下载
        max_workers = min(self.config['max_concurrent_downloads'], total_videos)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有下载任务
            future_to_video = {}
            for i, entry in enumerate(entries, 1):
                if entry is None:
                    continue
                
                title = entry.get('title', f'Video_{i}')
                video_url = entry.get('webpage_url') or entry.get('url')
                
                future = executor.submit(self.download_single_video, video_url, f"[{i}/{total_videos}] {title}")
                future_to_video[future] = (i, title)
            
            # 等待所有任务完成
            for future in concurrent.futures.as_completed(future_to_video):
                video_num, title = future_to_video[future]
                try:
                    if future.result():
                        success_count += 1
                        print(f"✅ [{video_num}/{total_videos}] 完成: {title}")
                    else:
                        print(f"❌ [{video_num}/{total_videos}] 失败: {title}")
                except Exception as e:
                    print(f"❌ [{video_num}/{total_videos}] 异常: {title} - {e}")
        
        print(f"\n🎉 播放列表处理完成！")
        print(f"📊 成功: {success_count}/{total_videos} 个视频")
        print(f"📁 文件保存在: {self.output_dir.absolute()}")
        
        return success_count > 0
    
    def list_downloaded_files(self):
        """列出已下载的文件"""
        audio_files = list(self.output_dir.glob(f'*.{self.config["audio_format"]}'))
        if audio_files:
            print(f"\n📁 输出目录: {self.output_dir.absolute()}")
            print(f"🎵 音频文件 ({len(audio_files)} 个):")
            for i, file in enumerate(sorted(audio_files), 1):
                file_size = file.stat().st_size / (1024 * 1024)  # MB
                print(f"  {i:2d}. {file.name} ({file_size:.1f} MB)")
        else:
            print("\n❌ 未找到音频文件")
    
    def extract_audio(self, url: str) -> bool:
        """主要的音频提取方法"""
        print("=== 高级B站音频提取器 ===")
        print(f"📋 配置: {self.config['audio_format'].upper()} @ {self.config['audio_quality']}kbps")
        print(f"📁 输出目录: {self.output_dir.absolute()}")
        print(f"🔧 最大并发: {self.config['max_concurrent_downloads']}")
        print()
        
        success = self.download_playlist_concurrent(url)
        
        if success:
            self.list_downloaded_files()
        
        return success

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='高级B站音频提取器')
    parser.add_argument('url', nargs='?', help='B站视频URL')
    parser.add_argument('-c', '--config', default='config.json', help='配置文件路径')
    parser.add_argument('-o', '--output', help='输出目录')
    parser.add_argument('-q', '--quality', help='音频质量 (如: 192, 320)')
    parser.add_argument('-f', '--format', help='音频格式 (如: mp3, m4a)')
    parser.add_argument('--concurrent', type=int, help='并发下载数')
    
    args = parser.parse_args()
    
    # 获取URL
    url = args.url
    if not url:
        url = input("请输入B站视频URL: ").strip()
    
    if not url:
        print("❌ 请提供有效的URL")
        return
    
    # 创建提取器
    extractor = AdvancedBilibiliExtractor(args.config)
    
    # 覆盖配置文件中的设置（如果提供了命令行参数）
    if args.output:
        extractor.config['output_directory'] = args.output
        extractor.output_dir = Path(args.output)
        extractor.output_dir.mkdir(exist_ok=True)
    
    if args.quality:
        extractor.config['audio_quality'] = args.quality
    
    if args.format:
        extractor.config['audio_format'] = args.format
    
    if args.concurrent:
        extractor.config['max_concurrent_downloads'] = args.concurrent
    
    # 重新设置yt-dlp选项
    extractor.setup_ydl_options()
    
    # 开始提取
    success = extractor.extract_audio(url)
    
    if not success:
        print("\n❌ 音频提取失败")
        sys.exit(1)

if __name__ == "__main__":
    main()