import PyInstaller.__main__
import os
import shutil

def build_exe():
    # Copy necessary files
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Build using PyInstaller
    PyInstaller.__main__.run([
        'mmac.spec',
        '--clean',
        '--noconfirm'
    ])
    
    print("Build completed!")

if __name__ == "__main__":
    build_exe()
