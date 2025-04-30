# tc_utils.py
import os
import subprocess
import sys

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from remote.remote_config import REMOTE_IPS, KEY_PATH

def run_remote_command(node_id, command):
    """Runs a shell command via SSH on a remote node."""
    remote = REMOTE_IPS[node_id]
    ssh_cmd = ["ssh", "-i", KEY_PATH, remote, command]
    result = subprocess.run(ssh_cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def resolve_remote_path(filename):
    """Adds the correct subdirectory prefix based on file type."""
    if filename.startswith("fragment"):
        return f"fragments/{filename}"
    elif filename.startswith("fingerprint"):
        return f"fingerprints/{filename}"
    else:
        return filename

def delete_file(node_id, filename):
    """Deletes a specific file from a node."""
    remote_path = resolve_remote_path(filename)
    cmd = f"rm ~/storage_node/{remote_path}"
    out, err = run_remote_command(node_id, cmd)
    print(f"🗑️ Deleted {filename} from node {node_id}: {err or 'OK'}")

def overwrite_file(node_id, filename, content="CORRUPTED\n"):
    """Overwrites a file on a node with fake content (to simulate corruption)."""
    remote_path = resolve_remote_path(filename)
    cmd = f"printf '{content}' > ~/storage_node/{remote_path}"
    out, err = run_remote_command(node_id, cmd)
    print(f"⚠️ Overwrote {filename} on node {node_id}: {err or 'OK'}")

def reset_remote_storage(node_id):
    """Deletes all files from a node’s storage_node folders."""
    cmd = "rm -rf ~/storage_node/fragments/* ~/storage_node/fingerprints/*"
    out, err = run_remote_command(node_id, cmd)
    print(f"🔁 Reset node {node_id}: {err or 'OK'}")

def reset_all_nodes():
    """Resets all nodes by clearing their storage_node directories."""
    for i in REMOTE_IPS:
        reset_remote_storage(i)