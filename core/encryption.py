from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
import os
from utils.helpers import get_machine_id

class Encryption:
    """AES-256 encryption for sensitive data"""
    
    def __init__(self):
        self.machine_id = get_machine_id()
        self.cipher_suite = self._generate_cipher()
    
    def _generate_cipher(self):
        """Generate Fernet cipher from machine ID"""
        # Use PBKDF2 to derive a key from machine ID
        machine_id_bytes = self.machine_id.encode()
        salt = b'BAND-Manager-Salt'  # Fixed salt for consistency
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(machine_id_bytes))
        return Fernet(key)
    
    def encrypt(self, data):
        """Encrypt string data"""
        if isinstance(data, str):
            data = data.encode()
        encrypted = self.cipher_suite.encrypt(data)
        return encrypted.decode()
    
    def decrypt(self, encrypted_data):
        """Decrypt string data"""
        try:
            if isinstance(encrypted_data, str):
                encrypted_data = encrypted_data.encode()
            decrypted = self.cipher_suite.decrypt(encrypted_data)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")

# Global encryption instance
encryption = Encryption()
