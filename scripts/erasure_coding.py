import os
import math
import sys
from crypto_utils import load_key
from cryptography.fernet import Fernet

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from remote.remote_config import REMOTE_IPS, KEY_PATH
from remote.remote_utils import send_fragment

NUM_NODES = 3

def encode_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    os.makedirs("fragments", exist_ok=True)

    chunk_size = math.ceil(len(data) / NUM_NODES)
    fragments = [data[i * chunk_size: (i + 1) * chunk_size] for i in range(NUM_NODES)]

    key = load_key()
    fernet = Fernet(key)

    for i, fragment in enumerate(fragments):
        encrypted_fragment = fernet.encrypt(fragment)
        fragment_filename = f"fragments/fragment_{i}.bin"
        with open(fragment_filename, 'wb') as f:
            f.write(encrypted_fragment)
        print(f"📦 Created {fragment_filename}, sending to node {i}...")
        send_fragment(i, fragment_filename)

    print(f"\n✅ File '{file_path}' split, encrypted, and uploaded to 3 remote storage nodes.")

if __name__ == "__main__":
    encode_file("simple_text.txt")