import os
import uuid
import subprocess
import shutil
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Ensure downloads directory exists
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Find yt-dlp executable
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

YT_DLP_PATH = find_yt_dlp()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url', '').strip()
        
        if not youtube_url:
            flash('Please enter a YouTube URL', 'error')
            return render_template('index.html')
        
        # Validate URL (basic check)
        if 'youtube.com' not in youtube_url and 'youtu.be' not in youtube_url:
            flash('Please enter a valid YouTube URL', 'error')
            return render_template('index.html')
        
        try:
            print(f"Starting download for URL: {youtube_url}")
            
            # Check if yt-dlp is available
            if not YT_DLP_PATH:
                print("yt-dlp not found")
                flash('yt-dlp is not installed or not found. Please install it first: pip install yt-dlp', 'error')
                return render_template('index.html')
            
            # Generate unique filename
            unique_id = str(uuid.uuid4())
            output_filename = f"{unique_id}.mp4"
            output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)
            
            # First, get format info to determine quality
            format_cmd = [
                YT_DLP_PATH,
                '--cookies-from-browser', 'chrome',
                '-f', 'best[height>=1080][ext=mp4]/best[height>=720][ext=mp4]/best[ext=mp4]/best',
                '--print', 'format_id,height,width,ext',
                '--no-playlist',
                youtube_url
            ]
            
            print(f"Getting format info: {' '.join(format_cmd)}")
            format_result = subprocess.run(format_cmd, capture_output=True, text=True, timeout=30)
            
            quality_info = "unknown"
            if format_result.returncode == 0 and format_result.stdout.strip():
                lines = format_result.stdout.strip().split('\n')
                # Look for the height line (should be a number)
                for line in lines:
                    if line.isdigit() and 100 <= int(line) <= 4320:  # Valid height range
                        quality_info = line + 'p'
                        break
            
            print(f"Quality detected: {quality_info}")
            
            # Now run the actual download command
            download_cmd = [
                YT_DLP_PATH,
                '--cookies-from-browser', 'chrome',
                '-f', 'best[height>=1080][ext=mp4]/best[height>=720][ext=mp4]/best[ext=mp4]/best',
                '-o', output_path,
                '--no-playlist',
                '--merge-output-format', 'mp4',
                youtube_url
            ]
            
            print(f"Running download command: {' '.join(download_cmd)}")
            
            result = subprocess.run(
                download_cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            print(f"Download command completed with return code: {result.returncode}")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            
            if result.returncode != 0:
                error_msg = f'Download failed: {result.stderr}'
                if result.stdout:
                    error_msg += f'\nOutput: {result.stdout}'
                print(f"Download failed with return code {result.returncode}")
                print(f"Error: {result.stderr}")
                print(f"Output: {result.stdout}")
                flash(error_msg, 'error')
                return render_template('index.html')
            
            # Check if file was actually created
            if not os.path.exists(output_path):
                print(f"Download failed: File not created at {output_path}")
                flash('Download failed: File not created', 'error')
                return render_template('index.html')
            
            # Get file size for display
            file_size = os.path.getsize(output_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # Debug: Print to console for troubleshooting
            print(f"Download completed: Quality={quality_info}, Size={file_size_mb:.1f}MB, File={output_filename}")
            
            # Show success message and return the file directly
            flash(f'Download successful! Quality: {quality_info}, File size: {file_size_mb:.1f} MB', 'success')
            
            # Return the file as attachment
            return send_file(
                output_path,
                as_attachment=True,
                download_name=f"youtube_video_{unique_id}.mp4",
                mimetype='video/mp4'
            )
            
        except subprocess.TimeoutExpired:
            print("Download timed out")
            flash('Download timed out. Please try again.', 'error')
        except FileNotFoundError:
            print("yt-dlp not found in exception handler")
            flash('yt-dlp is not installed. Please install it first: pip install yt-dlp', 'error')
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            flash(f'An error occurred: {str(e)}', 'error')
        
        return render_template('index.html')
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    """Download a specific file."""
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"youtube_video_{filename}",
            mimetype='video/mp4'
        )
    else:
        flash('File not found', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port) 