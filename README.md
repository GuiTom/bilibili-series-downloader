# B站视频音频提取器

一个用于从B站视频和合集中提取音频并保存为MP3文件的Python工具。

## 功能特性

- ✅ 支持单个B站视频音频提取
- ✅ 支持B站合集视频批量音频提取
- ✅ 自动转换为MP3格式（192kbps）
- ✅ 智能文件命名（合集视频按序号命名）
- ✅ 支持短链接（b23.tv）
- ✅ 错误处理和进度显示

## 系统要求

- Python 3.7+
- FFmpeg（用于音频转换）

## 安装步骤

### 1. 安装FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
- 从 [FFmpeg官网](https://ffmpeg.org/download.html) 下载
- 解压并添加到系统PATH

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

或者手动安装：
```bash
pip install yt-dlp requests
```

## 使用方法

### 命令行使用

```bash
# 交互式输入URL
python bilibili_audio_extractor.py

# 直接指定URL
python bilibili_audio_extractor.py "https://www.bilibili.com/video/BV1xx411c7mD"
```

### 支持的URL格式

- 标准视频链接：`https://www.bilibili.com/video/BV1xx411c7mD`
- 合集链接：`https://www.bilibili.com/video/BV1xx411c7mD?p=1`
- 短链接：`https://b23.tv/xxxxxx`
- 播放列表：自动检测并批量下载

### 输出文件

- **单个视频**：`视频标题.mp3`
- **合集视频**：`01_第一集标题.mp3`, `02_第二集标题.mp3` ...
- **保存位置**：`./downloads/` 目录

## 使用示例

### 示例1：下载单个视频音频
```bash
python bilibili_audio_extractor.py "https://www.bilibili.com/video/BV1xx411c7mD"
```

### 示例2：下载合集音频
```bash
python bilibili_audio_extractor.py "https://www.bilibili.com/video/BV1xx411c7mD?p=1"
```

### 示例3：交互式使用
```bash
python bilibili_audio_extractor.py
# 然后输入URL
```

## 程序输出示例

```
=== B站视频音频提取器 ===
支持单个视频和合集视频的音频提取

请输入B站视频URL: https://www.bilibili.com/video/BV1xx411c7mD
开始处理: https://www.bilibili.com/video/BV1xx411c7mD
✓ FFmpeg 已安装
正在分析合集: https://www.bilibili.com/video/BV1xx411c7mD
发现合集，共 10 个视频

[1/10] 正在处理: 第一集标题
✓ 音频提取完成: 01_第一集标题

[2/10] 正在处理: 第二集标题
✓ 音频提取完成: 02_第二集标题

...

合集处理完成！成功提取 10/10 个音频文件

✓ 所有音频文件已保存到: /path/to/downloads
```

## 注意事项

1. **网络连接**：确保网络连接稳定，某些视频可能需要较长下载时间
2. **存储空间**：确保有足够的磁盘空间存储音频文件
3. **版权声明**：请遵守相关版权法律，仅用于个人学习和研究
4. **文件命名**：程序会自动处理文件名中的特殊字符

## 故障排除

### 常见问题

**Q: 提示"未找到 FFmpeg"**
A: 请按照上述步骤安装FFmpeg并确保添加到系统PATH

**Q: 下载失败或速度很慢**
A: 可能是网络问题，请检查网络连接或稍后重试

**Q: 某些视频无法下载**
A: 可能是视频有访问限制或需要登录，程序会跳过这些视频

**Q: 文件名包含乱码**
A: 程序会自动处理特殊字符，如果仍有问题请检查系统编码设置

## 技术细节

- 使用 `yt-dlp` 作为下载引擎
- 使用 `FFmpeg` 进行音频格式转换
- 支持自动重试和错误恢复
- 音频质量：192kbps MP3格式

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规。