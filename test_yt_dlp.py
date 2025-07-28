#!/usr/bin/env python3
"""
Test script to verify yt-dlp installation and basic functionality.
"""

import subprocess
import sys
import shutil
import os

def find_yt_dlp():
    """Find the yt-dlp executable path."""
    # Try common locations
    possible_paths = [
        'yt-dlp',  # If it's in PATH
        '/Users/robminkoff/Library/Python/3.9/bin/yt-dlp',  # macOS user install
        '/usr/local/bin/yt-dlp',  # System install
        '/opt/homebrew/bin/yt-dlp',  # Homebrew on Apple Silicon
    ]
    
    for path in possible_paths:
        if shutil.which(path) or os.path.exists(path):
            return path
    
    return None

def test_yt_dlp_installation():
    """Test if yt-dlp is properly installed and accessible."""
    yt_dlp_path = find_yt_dlp()
    
    if not yt_dlp_path:
        print("❌ yt-dlp not found. Please install it with: pip install yt-dlp")
        return False
    
    try:
        result = subprocess.run([yt_dlp_path, '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ yt-dlp is installed: {result.stdout.strip()}")
            print(f"   Location: {yt_dlp_path}")
            return True
        else:
            print(f"❌ yt-dlp installation test failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ yt-dlp test timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing yt-dlp: {e}")
        return False

def test_flask_installation():
    """Test if Flask is properly installed."""
    try:
        import flask
        import importlib.metadata
        version = importlib.metadata.version("flask")
        print(f"✅ Flask is installed: {version}")
        return True
    except ImportError:
        print("❌ Flask not found. Please install it with: pip install -r requirements.txt")
        return False

def main():
    print("🧪 Testing YouTube Downloader Setup...\n")
    
    # Test yt-dlp
    yt_dlp_ok = test_yt_dlp_installation()
    
    # Test Flask
    flask_ok = test_flask_installation()
    
    print("\n" + "="*50)
    if yt_dlp_ok and flask_ok:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nTo start the application:")
        print("  python3 app.py")
        print("\nThen open: http://localhost:8080")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 