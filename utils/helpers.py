import os
import json
import uuid
import platform
from pathlib import Path

def get_data_dir():
    """Get application data directory"""
    if platform.system() == 'Windows':
        data_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'BAND-Manager')
    elif platform.system() == 'Darwin':  # macOS
        data_dir = os.path.expanduser('~/.band-manager')
    else:  # Linux
        data_dir = os.path.expanduser('~/.band-manager')
    
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_config_file():
    """Get config file path"""
    return os.path.join(get_data_dir(), 'config.json')

def get_accounts_db():
    """Get accounts database path"""
    return os.path.join(get_data_dir(), 'accounts.db')

def get_machine_id():
    """Get unique machine identifier"""
    machine_id_file = os.path.join(get_data_dir(), '.machine_id')
    
    if os.path.exists(machine_id_file):
        with open(machine_id_file, 'r') as f:
            return f.read().strip()
    else:
        machine_id = str(uuid.uuid4())
        with open(machine_id_file, 'w') as f:
            f.write(machine_id)
        return machine_id

def load_json(file_path, default=None):
    """Load JSON file safely"""
    if default is None:
        default = {}
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
    
    return default

def save_json(file_path, data):
    """Save JSON file safely"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def find_chrome_executable():
    """Find Chrome executable path"""
    if platform.system() == 'Windows':
        possible_paths = [
            os.path.join(os.getenv('ProgramFiles'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            os.path.join(os.getenv('ProgramFiles(x86)'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            os.path.join(os.getenv('LocalAppData'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
        ]
    elif platform.system() == 'Darwin':
        possible_paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        ]
    else:  # Linux
        possible_paths = [
            '/usr/bin/google-chrome',
            '/usr/bin/chromium',
        ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None
