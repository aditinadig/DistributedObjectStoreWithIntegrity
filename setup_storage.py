import os
import shutil

# Configuration: Define the number of storage nodes
NUM_NODES = 3  # You can increase this later if needed
DATA_DIR = "distributed_storage"  # The main directory where nodes will be created

def setup_storage():
    """Creates storage node directories, ensuring a clean setup each time."""
    # Delete existing storage if it exists
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)  # Remove old storage folders

    os.makedirs(DATA_DIR)  # Create main storage directory

    # Create individual storage nodes (folders)
    for i in range(NUM_NODES):
        os.makedirs(f"{DATA_DIR}/node_{i}")

    print(f"Successfully set up {NUM_NODES} storage nodes in '{DATA_DIR}'.")

# Run the setup when executing this script
if __name__ == "__main__":
    setup_storage()