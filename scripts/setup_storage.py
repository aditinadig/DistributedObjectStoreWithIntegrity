import os
import shutil

# Configuration: Define the number of storage nodes
NUM_NODES = 3
PARITY_SHARDS = 0
DATA_DIR = "distributed_storage"

def setup_storage():
    """Creates storage node directories, ensuring a clean setup each time."""
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)  # Remove old storage folders

    os.makedirs(DATA_DIR)  # Create main storage directory

    for i in range(NUM_NODES):
        os.makedirs(f"{DATA_DIR}/node_{i}")

    print(f"✅ Using {NUM_NODES} main storage nodes.")  # since PARITY_SHARDS = 0
    print(f"Successfully set up {NUM_NODES} storage nodes in '{DATA_DIR}'.")

if __name__ == "__main__":
    setup_storage()