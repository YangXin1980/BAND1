#!/usr/bin/env python3
"""
Build script to create standalone executable using PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

def build():
    """Build standalone executable"""
    print("="*60)
    print("BAND Browser Manager - Build Script")
    print("="*60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("\nInstalling PyInstaller...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "pyinstaller"
        ])
    
    # Build command
    build_dir = Path("dist")
    build_dir.mkdir(exist_ok=True)
    
    print("\nBuilding executable...")
    print(f"Output directory: {build_dir.absolute()}")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=BAND-Browser-Manager",
        "--icon=ui/icon.ico" if Path("ui/icon.ico").exists() else "",
        "--add-data=ui/styles.qss:ui",
        "--distpath=dist",
        "--buildpath=build",
        "--specpath=.",
        "main.py"
    ]
    
    # Remove empty strings
    cmd = [c for c in cmd if c]
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Build successful!")
        print(f"\nExecutable location:")
        print(f"  {build_dir.absolute() / 'BAND-Browser-Manager.exe'}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
