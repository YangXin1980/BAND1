import json
import os
from datetime import datetime
from core.encryption import encryption
from utils.helpers import get_accounts_db, load_json, save_json
from utils.logger import logger

class AccountStorage:
    """Manage encrypted account storage"""
    
    def __init__(self):
        self.db_file = get_accounts_db()
        self.accounts = self._load_accounts()
    
    def _load_accounts(self):
        """Load accounts from database"""
        try:
            data = load_json(self.db_file, {'accounts': []})
            return data.get('accounts', [])
        except Exception as e:
            logger.error(f"Failed to load accounts: {e}")
            return []
    
    def _save_accounts(self):
        """Save accounts to database"""
        try:
            data = {
                'accounts': self.accounts,
                'last_updated': datetime.now().isoformat()
            }
            save_json(self.db_file, data)
            logger.info("Accounts saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save accounts: {e}")
            return False
    
    def add_account(self, email, password, name=None):
        """Add new account"""
        try:
            # Check if account already exists
            if any(acc['email'] == email for acc in self.accounts):
                logger.warning(f"Account {email} already exists")
                return False, "Account already exists"
            
            account = {
                'id': len(self.accounts) + 1,
                'email': email,
                'password': encryption.encrypt(password),
                'name': name or email.split('@')[0],
                'created_at': datetime.now().isoformat(),
                'enabled': True
            }
            
            self.accounts.append(account)
            self._save_accounts()
            logger.info(f"Account added: {email}")
            return True, "Account added successfully"
        except Exception as e:
            logger.error(f"Failed to add account: {e}")
            return False, str(e)
    
    def get_all_accounts(self):
        """Get all accounts (without passwords)"""
        return [{
            'id': acc['id'],
            'email': acc['email'],
            'name': acc.get('name', ''),
            'enabled': acc.get('enabled', True),
            'created_at': acc.get('created_at', '')
        } for acc in self.accounts]
    
    def get_account_with_password(self, account_id):
        """Get account with decrypted password"""
        try:
            account = next((acc for acc in self.accounts if acc['id'] == account_id), None)
            if account:
                return {
                    'id': account['id'],
                    'email': account['email'],
                    'password': encryption.decrypt(account['password']),
                    'name': account.get('name', ''),
                    'enabled': account.get('enabled', True)
                }
            return None
        except Exception as e:
            logger.error(f"Failed to get account: {e}")
            return None
    
    def update_account(self, account_id, **kwargs):
        """Update account information"""
        try:
            account = next((acc for acc in self.accounts if acc['id'] == account_id), None)
            if not account:
                return False, "Account not found"
            
            if 'password' in kwargs:
                account['password'] = encryption.encrypt(kwargs['password'])
            
            for key in ['email', 'name', 'enabled']:
                if key in kwargs:
                    account[key] = kwargs[key]
            
            self._save_accounts()
            logger.info(f"Account {account_id} updated")
            return True, "Account updated successfully"
        except Exception as e:
            logger.error(f"Failed to update account: {e}")
            return False, str(e)
    
    def delete_account(self, account_id):
        """Delete account"""
        try:
            original_len = len(self.accounts)
            self.accounts = [acc for acc in self.accounts if acc['id'] != account_id]
            
            if len(self.accounts) < original_len:
                self._save_accounts()
                logger.info(f"Account {account_id} deleted")
                return True, "Account deleted successfully"
            else:
                return False, "Account not found"
        except Exception as e:
            logger.error(f"Failed to delete account: {e}")
            return False, str(e)
    
    def export_accounts(self, file_path):
        """Export accounts to JSON file (encrypted)"""
        try:
            export_data = {
                'accounts': self.accounts,
                'exported_at': datetime.now().isoformat()
            }
            save_json(file_path, export_data)
            logger.info(f"Accounts exported to {file_path}")
            return True, "Accounts exported successfully"
        except Exception as e:
            logger.error(f"Failed to export accounts: {e}")
            return False, str(e)
    
    def import_accounts(self, file_path):
        """Import accounts from JSON file"""
        try:
            if not os.path.exists(file_path):
                return False, "File not found"
            
            import_data = load_json(file_path, {'accounts': []})
            imported = import_data.get('accounts', [])
            
            if not imported:
                return False, "No accounts found in file"
            
            # Add imported accounts
            for acc in imported:
                if not any(a['email'] == acc['email'] for a in self.accounts):
                    new_id = max([a['id'] for a in self.accounts], default=0) + 1
                    acc['id'] = new_id
                    self.accounts.append(acc)
            
            self._save_accounts()
            logger.info(f"Imported {len(imported)} accounts from {file_path}")
            return True, f"Imported {len(imported)} accounts successfully"
        except Exception as e:
            logger.error(f"Failed to import accounts: {e}")
            return False, str(e)

# Global account storage instance
account_storage = AccountStorage()
