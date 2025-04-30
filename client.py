import socket

# Configuration
HOST = "127.0.0.1"
PORT = 5001  # Ensure this matches the server port

def send_request(command):
    """Sends a request to the storage server and prints debug messages."""
    try:
        print(f"🔗 Connecting to {HOST}:{PORT}...")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)  # Prevent infinite waiting
        client.connect((HOST, PORT))
        print("✅ Connected to server!")

        print(f"📤 Sending request: {command}")
        client.send(command.encode())

        response = client.recv(4096).decode()
        print(f"\n📥 Response from server:\n{response}")

    except socket.timeout:
        print("❌ Connection timed out. Server may not be responding.")
    except ConnectionRefusedError:
        print("❌ Connection refused. Ensure the server is running.")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    while True:
        print("\n📌 Available commands: ENCODE, VERIFY, RECONSTRUCT, EXIT")
        command = input("Enter command: ").strip().upper()

        if command == "EXIT":
            print("🚪 Exiting client.")
            break

        send_request(command)