import platform
import subprocess
from utils.logger import logger

class WindowManager:
    """Manage window arrangement and positioning"""
    
    def __init__(self):
        self.os_type = platform.system()
    
    def get_screen_info(self):
        """Get screen dimensions"""
        try:
            if self.os_type == 'Windows':
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                root.destroy()
                return screen_width, screen_height
            elif self.os_type == 'Darwin':  # macOS
                from AppKit import NSScreen
                screen = NSScreen.mainScreen()
                return int(screen.frame().size.width), int(screen.frame().size.height)
            else:  # Linux
                # Use xrandr for Linux
                result = subprocess.check_output(['xrandr']).decode()
                for line in result.split('\n'):
                    if ' connected primary' in line:
                        parts = line.split()
                        dims = parts[3].split('+')
                        res = dims[0].split('x')
                        return int(res[0]), int(res[1])
        except Exception as e:
            logger.error(f"Failed to get screen info: {e}")
            return 1920, 1080  # Default
    
    def calculate_window_positions(self, window_count):
        """Calculate window positions for tiling"""
        screen_width, screen_height = self.get_screen_info()
        
        # Calculate grid layout
        if window_count == 1:
            cols, rows = 1, 1
        elif window_count == 2:
            cols, rows = 2, 1
        elif window_count <= 4:
            cols, rows = 2, 2
        elif window_count <= 6:
            cols, rows = 3, 2
        elif window_count <= 9:
            cols, rows = 3, 3
        else:
            cols = 4
            rows = (window_count + cols - 1) // cols
        
        # Calculate window dimensions
        window_width = screen_width // cols
        window_height = screen_height // rows
        
        positions = []
        for i in range(window_count):
            row = i // cols
            col = i % cols
            x = col * window_width
            y = row * window_height
            positions.append({
                'x': x,
                'y': y,
                'width': window_width,
                'height': window_height
            })
        
        return positions
    
    def move_window(self, hwnd, position):
        """Move and resize window"""
        try:
            if self.os_type == 'Windows':
                import ctypes
                from ctypes import wintypes
                
                SWP_NOZORDER = 0x0004
                SetWindowPos = ctypes.windll.user32.SetWindowPos
                
                SetWindowPos(
                    hwnd,
                    0,
                    position['x'],
                    position['y'],
                    position['width'],
                    position['height'],
                    SWP_NOZORDER
                )
            else:
                logger.warning("Window positioning not fully supported on this OS")
        except Exception as e:
            logger.error(f"Failed to move window: {e}")

# Global window manager instance
window_manager = WindowManager()
