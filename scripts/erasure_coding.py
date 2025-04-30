# erasure_coding.py
import os
import math
import sys

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from remote.remote_config import REMOTE_IPS, KEY_PATH
from remote.remote_utils import send_fragment

NUM_NODES = 3
DATA_DIR = "distributed_storage"



def encode_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    os.makedirs("fragments", exist_ok=True)

    chunk_size = math.ceil(len(data) / NUM_NODES)
    fragments = [data[i * chunk_size: (i + 1) * chunk_size] for i in range(NUM_NODES)]

    for i, fragment in enumerate(fragments):
        fragment_filename = f"fragments/fragment_{i}.bin"
        with open(fragment_filename, 'wb') as f:
            f.write(fragment)
        print(f"📦 Created {fragment_filename}, sending to node {i}...")
        send_fragment(i, fragment_filename)

    print(f"\n✅ File '{file_path}' split and uploaded to 3 remote storage nodes.")

if __name__ == "__main__":
    encode_file("simple_text.txt")