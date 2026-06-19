# BAND Browser Manager System

A professional Python-based multi-account management system for BAND with Chrome automation, account encryption, and batch operations.

## Features

✨ **Account Management**
- Encrypted account storage (AES-256)
- Import/Export accounts
- Support for multiple accounts
- Quick account switching

🌐 **Chrome Automation**
- Auto-login with saved credentials
- Multiple browser instances
- Isolated browser profiles
- Google Translate support preserved
- Automatic window arrangement

📊 **Batch Operations**
- Launch multiple browsers at once
- Manage multiple accounts simultaneously
- Batch account import/export

🔧 **Advanced Features**
- User-configurable instance count
- Real-time browser status monitoring
- Secure password encryption
- Professional PyQt5 UI
- Comprehensive logging system

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

```
BAND-Browser-Manager/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration management
├── ui/
│   ├── __init__.py
│   ├── main_window.py        # Main application window
│   ├── account_manager.py    # Account management UI
│   ├── browser_launcher.py   # Browser launcher UI
│   └── styles.qss            # PyQt5 stylesheet
├── core/
│   ├── __init__.py
│   ├── encryption.py         # AES-256 encryption
│   ├── account_storage.py    # Account database operations
│   ├── browser_manager.py    # Chrome browser management
│   ├── chrome_automation.py  # Selenium automation
│   └── window_manager.py     # Window arrangement
├── utils/
│   ├── __init__.py
│   ├── logger.py             # Logging system
│   └── helpers.py            # Utility functions
└── data/
    └── .gitkeep
```

## Usage

### Add Account
1. Click "Add Account" button
2. Enter email and password
3. Account is automatically encrypted and saved

### Launch Browsers
1. Select accounts from the list
2. Configure number of instances
3. Click "Launch Selected" or "Launch All"
4. Browsers will auto-arrange on screen

### Import/Export
- Use "Import Accounts" to load accounts from file
- Use "Export Accounts" to save accounts as backup
- All data remains encrypted during export/import

## Security

- All passwords encrypted with AES-256
- Encryption key derived from machine ID
- No plaintext storage
- Secure credential handling

## License

MIT License
