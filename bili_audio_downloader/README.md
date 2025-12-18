# Bili Audio Downloader

A Flutter application to download audio from Bilibili videos and convert them to MP3.

## Features

- Extract audio from Bilibili videos (BV/b23.tv links)
- Convert to MP3 format automatically
- Supports Android and iOS

## Requirements

### Android
- Android SDK.
- Min SDK 24 (likely required by ffmpeg_kit).

### iOS
- CocoaPods is required (`sudo gem install cocoapods`).
- iOS 12.1+ (ffmpeg_kit requirement).

## Getting Started

1. **Install Dependencies**:
   ```bash
   flutter pub get
   ```

2. **Run the App**:
   ```bash
   flutter run
   ```

## Architecture

- **lib/api**: Handles Bilibili API requests to get video metadata and stream URLs.
- **lib/service**: Manages file downloading and FFmpeg conversion.
- **lib/provider**: State management using `Provider`.
- **lib/ui**: User Interface.

## Note on Bilibili API
This app uses a direct extraction method. Bilibili APIs change frequently, so if extraction fails, the API logic in `lib/api/bilibili_api.dart` might need updates.
