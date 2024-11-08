import PyInstaller.__main__
import os
import sys
import shutil

def build_exe():
    # Create necessary directories
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    if not os.path.exists('dist'):
        os.makedirs('dist')

    # Build command with cross-platform compatibility options
    build_args = [
        'mmac.spec',
        '--clean',
        '--noconfirm',
        '--distpath', './dist',
        '--workpath', './build'
    ]
    
    try:
        PyInstaller.__main__.run(build_args)
        print("Build completed successfully!")
        
        # Create a zip file of the dist directory for distribution
        if os.path.exists('dist/MMAC'):
            shutil.make_archive('dist/MMAC-Windows', 'zip', 'dist/MMAC')
            print("Created distribution zip file: MMAC-Windows.zip")
    except Exception as e:
        print(f"Build failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
