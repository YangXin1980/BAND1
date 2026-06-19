import os
import json
from utils.helpers import get_config_file, load_json, save_json, get_data_dir

class Settings:
    """Application settings manager"""
    
    DEFAULT_CONFIG = {
        'theme': 'light',
        'language': 'en',
        'auto_login': False,
        'window_width': 1200,
        'window_height': 700,
        'window_x': 100,
        'window_y': 100,
        'chrome_instances': 2,
        'auto_arrange_windows': True,
        'enable_translation': True,
        'log_level': 'INFO',
        'default_timeout': 30,
    }
    
    def __init__(self):
        self.config_file = get_config_file()
        self.config = load_json(self.config_file, self.DEFAULT_CONFIG.copy())
        
        # Ensure all default keys exist
        for key, value in self.DEFAULT_CONFIG.items():
            if key not in self.config:
                self.config[key] = value
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        self.save()
    
    def save(self):
        """Save configuration to file"""
        save_json(self.config_file, self.config)
    
    def reset_to_defaults(self):
        """Reset to default settings"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
    
    def to_dict(self):
        """Get all settings as dictionary"""
        return self.config.copy()

# Global settings instance
settings = Settings()
