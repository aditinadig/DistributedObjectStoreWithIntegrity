# remote_utils.py

import subprocess
from remote.remote_config import REMOTE_IPS, KEY_PATH


def send_fragment(node_id, local_file):
    remote = REMOTE_IPS[node_id]

    if "fingerprint" in local_file:
        subdir = "fingerprints"
    elif "fragment" in local_file:
        subdir = "fragments"
    else:
        subdir = ""

    setup_cmd = f"mkdir -p ~/storage_node/{subdir}"
    print(f"[DEBUG] Creating remote dir: {setup_cmd} on node {node_id}")
    subprocess.run(["ssh", "-i", KEY_PATH, remote, setup_cmd], check=True)

    remote_path = f"{remote}:~/storage_node/{subdir}/"
    print(f"[DEBUG] Uploading {local_file} to {remote_path}")
    subprocess.run(["scp", "-i", KEY_PATH, local_file, remote_path], check=True)