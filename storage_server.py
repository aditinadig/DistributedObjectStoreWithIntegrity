import os
import socket
import threading
import json
import subprocess

# Configuration
HOST = "127.0.0.1"
PORT = 5001

def handle_client(conn):
    """Handles client requests and executes corresponding commands."""
    try:
        request = conn.recv(1024).decode()
        print(f"📥 Received request: {request}")

        if request == "ENCODE":
            output = subprocess.run(["python", "erasure_coding.py"], capture_output=True, text=True)
        elif request == "VERIFY":
            output = subprocess.run(["python", "verify_fragments.py"], capture_output=True, text=True)
        elif request == "RECONSTRUCT":
            output = subprocess.run(["python", "reconstruct_file.py"], capture_output=True, text=True)
        else:
            output = "❌ Unknown command!"

        conn.send(output.stdout.encode())  # Send response to client
    except Exception as e:
        conn.send(f"❌ Server error: {str(e)}".encode())
    finally:
        conn.close()

def start_server():
    """Starts the storage management server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"🚀 Storage server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"🔗 Connected to client: {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    start_server()