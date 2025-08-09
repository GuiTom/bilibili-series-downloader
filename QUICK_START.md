# 🚀 快速开始指南

## 📋 准备工作

### 1. 安装依赖

**macOS/Linux 用户：**
```bash
./install.sh
```

**Windows 用户：**
```cmd
install.bat
```

**手动安装：**
```bash
# 安装 Python 依赖
pip3 install yt-dlp requests

# 安装 FFmpeg (macOS)
brew install ffmpeg

# 安装 FFmpeg (Ubuntu/Debian)
sudo apt install ffmpeg
```

## 🎵 使用方法

### 🚀 最简单的方式（推荐）

```bash
# 一键启动（交互式）
./run.sh

# 直接下载
./run.sh "https://www.bilibili.com/video/BV1xx411c7mD"
```

### 方式一：简化版（手动激活虚拟环境）

```bash
# 激活虚拟环境
source venv/bin/activate

# 下载单个视频音频
python simple_extractor.py "https://www.bilibili.com/video/BV1xx411c7mD"

# 下载播放列表音频
python simple_extractor.py "https://www.bilibili.com/video/BV1LJ411t7VS"
```

### 方式二：完整版（更多功能）

```bash
# 激活虚拟环境
source venv/bin/activate

# 交互式使用
python bilibili_audio_extractor.py

# 命令行使用
python bilibili_audio_extractor.py "https://www.bilibili.com/video/BV1xx411c7mD"
```

### 方式三：高级版（并发下载）

```bash
# 激活虚拟环境
source venv/bin/activate

# 使用默认配置
python advanced_extractor.py "https://www.bilibili.com/video/BV1xx411c7mD"

# 自定义参数
python advanced_extractor.py "URL" -q 320 -f mp3 --concurrent 5
```

## 📁 输出文件

- **简化版**：保存在 `downloads/` 目录
- **完整版**：保存在 `audio_output/` 目录
- **高级版**：可在 `config.json` 中自定义

## 🔧 配置文件

编辑 `config.json` 来自定义下载设置：

```json
{
  "output_directory": "./downloads",
  "audio_format": "mp3",
  "audio_quality": "192",
  "max_concurrent_downloads": 3
}
```

## 📝 支持的URL格式

- 单个视频：`https://www.bilibili.com/video/BVxxxxxxx`
- 播放列表：`https://www.bilibili.com/video/BVxxxxxxx?p=1`
- 合集：`https://space.bilibili.com/xxx/channel/collectiondetail?sid=xxx`
- 用户投稿：`https://space.bilibili.com/xxx/video`

## ❓ 常见问题

**Q: 下载失败怎么办？**
A: 检查网络连接，确保URL正确，尝试使用代理

**Q: 音质如何调整？**
A: 修改配置文件中的 `audio_quality` 参数（如：128, 192, 320）

**Q: 如何批量下载？**
A: 使用高级版的并发下载功能，或者准备URL列表文件

## 🎯 快速测试

```bash
# 最简单的测试方式
./run.sh "https://www.bilibili.com/video/BV1LJ411t7VS"

# 或者手动激活虚拟环境
source venv/bin/activate
python simple_extractor.py "https://www.bilibili.com/video/BV1LJ411t7VS"
```

### MP3格式说明

如果下载的音频是M4A格式，可以使用内置的转换工具：

```bash
# 方法1: 使用启动脚本
./run.sh
# 然后选择 "4. 转换M4A为MP3"

# 方法2: 直接运行转换脚本
source venv/bin/activate
python convert_to_mp3.py
```

转换器会自动：
- 检测audio_output目录中的所有M4A文件
- 转换为高质量MP3格式（192kbps）
- 删除原始M4A文件
- 显示转换进度和结果

### MP3文件重命名

下载的音频文件名通常包含很多无关信息，可以使用重命名工具清理：

```bash
# 方法1: 使用启动脚本
./run.sh
# 然后选择 "5. 重命名MP3文件"

# 方法2: 直接运行重命名脚本
source venv/bin/activate
python rename_mp3.py

# 方法3: 指定目录
python rename_mp3.py /path/to/your/mp3/files
```

重命名工具会自动：
- 从复杂的文件名中提取歌曲名称
- 去掉序号、合集信息、电影名、年份等无关内容
- 清理不合法的文件名字符
- 生成简洁的"歌曲名.mp3"格式

## 📞 获取帮助

- 查看详细文档：`README.md`
- 检查程序版本：`python3 simple_extractor.py --version`
- 遇到问题请检查终端输出的错误信息