# crypto_utils.py

from cryptography.fernet import Fernet
import os

KEY_PATH = "secret.key"

def generate_and_store_key():
    """Generates a new Fernet key and stores it in a file."""
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
    print("🔐 New Fernet key generated and saved to secret.key")

def load_key():
    """Loads the Fernet key from file, generates if missing."""
    if not os.path.exists(KEY_PATH):
        print("⚠️ Key not found. Generating a new one...")
        generate_and_store_key()
    with open(KEY_PATH, "rb") as key_file:
        return key_file.read()