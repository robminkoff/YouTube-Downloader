# YouTube Video Downloader

A simple Flask web application that allows users to download YouTube videos as MP4 files using yt-dlp.

## Features

- Clean, modern web interface
- Download YouTube videos as MP4 files
- Unique filename generation using UUID
- Basic URL validation
- Error handling for failed downloads
- Automatic file download through browser
- Responsive design with Bootstrap

## Prerequisites

Before running this application, you need to install `yt-dlp`:

```bash
# Install yt-dlp globally
pip install yt-dlp

# Or using pipx (recommended)
pipx install yt-dlp
```

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:

   ```
   http://localhost:8080
   ```

3. Paste a YouTube URL in the text area and click "Download Video"

4. The video will be downloaded as an MP4 file to your browser's default download location

## How it Works

1. **URL Input**: Users paste a YouTube URL into the web form
2. **Validation**: The app validates the URL format
3. **Download**: yt-dlp downloads the video in MP4 format
4. **File Generation**: A unique filename is generated using UUID
5. **Delivery**: The file is served as an attachment for browser download

## Error Handling

The application includes error handling for:

- Invalid YouTube URLs
- Missing yt-dlp installation
- Download timeouts (5 minutes)
- Failed downloads
- File creation issues

## File Structure

```
youtube-downloader/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Web interface template
├── downloads/         # Downloaded videos (auto-created)
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## Configuration

- **Download Timeout**: 5 minutes (configurable in `app.py`)
- **File Format**: MP4 (best available quality)
- **Download Folder**: `downloads/` (auto-created)

## Security Notes

- The application uses a development secret key by default
- For production, set the `SECRET_KEY` environment variable
- Downloaded files are stored locally in the `downloads/` folder
- Consider implementing file cleanup for production use

## Future Improvements

Here are some suggested enhancements for future versions:

### 1. Format Selection

- Add dropdown to select video quality (720p, 1080p, etc.)
- Audio-only download option
- Multiple format support (MP3, WebM, etc.)

### 2. Download Progress

- Real-time progress updates using WebSockets
- Progress bar showing download percentage
- Estimated time remaining

### 3. Enhanced Features

- Playlist support
- Batch download multiple videos
- Video thumbnail preview
- Video information display (duration, size, etc.)
- Download history
- User authentication

### 4. Technical Improvements

- Background task processing with Celery
- Redis for caching
- Database for download history
- File cleanup automation
- Rate limiting
- API endpoints for programmatic access

### 5. UI/UX Enhancements

- Drag and drop URL input
- Mobile-optimized interface
- Dark mode toggle
- Keyboard shortcuts
- Accessibility improvements

## Troubleshooting

### Common Issues

1. **"yt-dlp is not installed" error**

   - Install yt-dlp: `pip install yt-dlp`

2. **Download fails with "Video unavailable"**

   - Check if the video is publicly available
   - Some videos may have download restrictions

3. **Timeout errors**

   - Increase timeout in `app.py` (currently 300 seconds)
   - Check your internet connection

4. **Permission errors**
   - Ensure the `downloads/` folder is writable
   - Check file system permissions

## License

This project is for educational purposes. Please respect YouTube's terms of service and copyright laws when downloading videos.

## Contributing

Feel free to submit issues and enhancement requests!
