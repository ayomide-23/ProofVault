import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
#the purpose of this encryption key is to turn the raw private key into an encrypted private key that will be sored to the database
encryption_key = os.getenv("ENCRYPTION_KEY")
if not encryption_key: 
    raise ValueError("Encryption key not found")

fernet = Fernet(encryption_key.encode())

#function to encrypt the raw private key
def encrypt_key(raw_key: str) -> str: 
    """Encrypts the raw private key using Fernet and gets stored to the database"""
    return fernet.encrypt(raw_key.encode()).decode()

#function to decrypt the encrypted private key
def decrypt_key(encrypted_key: str) -> str:
    """Decrypts the encrypted private key from the database using fernet"""
    return fernet.decrypt(encrypted_key.encode()).decode() 