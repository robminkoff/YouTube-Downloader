#!/usr/bin/env python3
"""
Script to check available quality options for YouTube videos.
"""

import subprocess
import sys
import shutil
import os

def find_yt_dlp():
    """Find the yt-dlp executable path."""
    possible_paths = [
        'yt-dlp',
        '/Users/robminkoff/Library/Python/3.9/bin/yt-dlp',
        '/usr/local/bin/yt-dlp',
        '/opt/homebrew/bin/yt-dlp',
    ]
    
    for path in possible_paths:
        if shutil.which(path) or os.path.exists(path):
            return path
    return None

def check_video_quality(url):
    """Check available quality options for a YouTube video."""
    yt_dlp_path = find_yt_dlp()
    
    if not yt_dlp_path:
        print("❌ yt-dlp not found")
        return
    
    print(f"🔍 Checking quality options for: {url}")
    print("=" * 60)
    
    try:
        # Get available formats
        result = subprocess.run([
            yt_dlp_path, '-F', url
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error checking quality: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 check_quality.py <youtube_url>")
        print("Example: python3 check_quality.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        sys.exit(1)
    
    url = sys.argv[1]
    check_video_quality(url)

if __name__ == "__main__":
    main() 