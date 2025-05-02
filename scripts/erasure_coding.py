import os
import sys
import subprocess
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from remote.remote_utils import send_fragment

NUM_SHARDS = 5
K_SHARDS = 3
FRAG_DIR = "fragments"
INPUT_FILE = "simple_text.txt"
ENCODED_FILE = "encoded_input.bin"

def encode_file(file_path):
    os.makedirs(FRAG_DIR, exist_ok=True)

    # Write the plaintext directly
    with open(file_path, 'rb') as f:
        data = f.read()
    with open(ENCODED_FILE, 'wb') as f:
        f.write(data)

    print(f"Running command: zfec -k {K_SHARDS} -m {NUM_SHARDS} {ENCODED_FILE}")
    subprocess.run(["zfec", "-k", str(K_SHARDS), "-m", str(NUM_SHARDS), ENCODED_FILE], check=True)
    print(f"📦 File split into {NUM_SHARDS} fragments.")

    pattern = re.compile(rf"{re.escape(ENCODED_FILE)}\.(\d+)_\d+\.fec")
    for filename in os.listdir():
        match = pattern.match(filename)
        if match:
            idx = int(match.group(1))
            new_name = f"fragment_{idx:03d}"
            os.rename(filename, os.path.join(FRAG_DIR, new_name))
            print(f"📦 Moved and renamed {filename} → fragments/{new_name}")

    os.remove(ENCODED_FILE)

    for i in range(NUM_SHARDS):
        frag_path = os.path.join(FRAG_DIR, f"fragment_{i:03d}")
        print(f"🔐 Uploading fragment_{i:03d}...")
        send_fragment(i, frag_path)

    print(f"\n✅ File '{file_path}' split and uploaded to {NUM_SHARDS} nodes.")

if __name__ == "__main__":
    encode_file(INPUT_FILE)