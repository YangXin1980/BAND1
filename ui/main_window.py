from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QPushButton, QMenuBar, QMenu, QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from ui.account_manager import AccountManagerWidget
from ui.browser_launcher import BrowserLauncherWidget
from config.settings import settings
from utils.logger import logger
import os

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BAND Browser Manager")
        self.setGeometry(100, 100, 1200, 700)
        
        # Load stylesheet
        self.load_stylesheet()
        
        # Create UI
        self.init_ui()
        self.init_menu()
        
        # Restore window geometry if available
        self.restore_window_geometry()
        
        logger.info("Application started")
    
    def load_stylesheet(self):
        """Load and apply stylesheet"""
        try:
            style_file = os.path.join(os.path.dirname(__file__), 'styles.qss')
            if os.path.exists(style_file):
                with open(style_file, 'r', encoding='utf-8') as f:
                    self.setStyleSheet(f.read())
        except Exception as e:
            logger.error(f"Failed to load stylesheet: {e}")
    
    def init_ui(self):
        """Initialize user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("BAND Browser Manager System")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Tabs
        self.account_widget = AccountManagerWidget()
        self.launcher_widget = BrowserLauncherWidget()
        
        self.tabs.addTab(self.account_widget, "📋 Account Manager")
        self.tabs.addTab(self.launcher_widget, "🚀 Browser Launcher")
        
        layout.addWidget(title_label)
        layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def init_menu(self):
        """Initialize menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        settings_action = edit_menu.addAction("Settings")
        settings_action.triggered.connect(self.show_settings)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
    
    def show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(
            self,
            "Settings",
            "Settings panel coming soon!\n\nCurrent settings can be edited in the application tabs."
        )
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About BAND Browser Manager",
            "BAND Browser Manager System\n\n"
            "Version: 1.0.0\n"
            "A professional multi-account management system for BAND\n\n"
            "Features:\n"
            "• Encrypted account storage (AES-256)\n"
            "• Auto-login with Chrome automation\n"
            "• Batch account operations\n"
            "• Automatic window arrangement\n"
            "• Google Translate support\n\n"
            "© 2026 BAND Browser Manager"
        )
    
    def restore_window_geometry(self):
        """Restore window size and position"""
        try:
            x = settings.get('window_x', 100)
            y = settings.get('window_y', 100)
            width = settings.get('window_width', 1200)
            height = settings.get('window_height', 700)
            self.setGeometry(x, y, width, height)
        except Exception as e:
            logger.error(f"Failed to restore window geometry: {e}")
    
    def closeEvent(self, event):
        """Handle window close event"""
        try:
            # Save window geometry
            settings.set('window_x', self.geometry().x())
            settings.set('window_y', self.geometry().y())
            settings.set('window_width', self.geometry().width())
            settings.set('window_height', self.geometry().height())
            
            logger.info("Application closing")
            event.accept()
        except Exception as e:
            logger.error(f"Error during close: {e}")
            event.accept()
