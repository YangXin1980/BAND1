#!/usr/bin/env python3
"""
Setup script to prepare the BAND Browser Manager for first run
"""

import os
import sys
import subprocess
from pathlib import Path

def setup():
    """Setup the application"""
    print("="*60)
    print("BAND Browser Manager - Setup Wizard")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"\n✓ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    print("\n[1/3] Installing Python packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Packages installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install packages: {e}")
        sys.exit(1)
    
    # Check Chrome installation
    print("\n[2/3] Checking Chrome installation...")
    from utils.helpers import find_chrome_executable
    chrome_path = find_chrome_executable()
    if chrome_path:
        print(f"✓ Chrome found at: {chrome_path}")
    else:
        print("✗ Chrome not found. Please install Google Chrome.")
        print("  Download from: https://www.google.com/chrome/")
        sys.exit(1)
    
    # Initialize data directories
    print("\n[3/3] Initializing data directories...")
    from utils.helpers import get_data_dir
    from config.settings import settings
    
    data_dir = get_data_dir()
    print(f"✓ Data directory: {data_dir}")
    
    # Load settings
    settings.save()
    print("✓ Settings initialized")
    
    print("\n" + "="*60)
    print("Setup complete! You can now run:")
    print("  python main.py")
    print("="*60)

if __name__ == "__main__":
    setup()
