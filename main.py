#!/usr/bin/env python3
"""
BAND Browser Manager System - Main Application Entry Point

A professional Python-based multi-account management system for BAND
with Chrome automation, account encryption, and batch operations.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow
from utils.logger import logger
from config.settings import settings

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import PyQt5
        import selenium
        import cryptography
        return True, "All requirements satisfied"
    except ImportError as e:
        return False, f"Missing required package: {e}"

def init_application():
    """Initialize application"""
    logger.info("Initializing BAND Browser Manager System")
    
    # Check requirements
    ok, message = check_requirements()
    if not ok:
        logger.error(message)
        print(f"ERROR: {message}")
        print("\nPlease install required packages:")
        print("pip install -r requirements.txt")
        return False
    
    logger.info("Application initialization complete")
    return True

def main():
    """Main application entry point"""
    
    # Initialize
    if not init_application():
        sys.exit(1)
    
    try:
        # Create application
        app = QApplication(sys.argv)
        
        # Set application style
        app.setStyle('Fusion')
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Main window displayed")
        
        # Run application
        sys.exit(app.exec_())
    
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print(f"FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
