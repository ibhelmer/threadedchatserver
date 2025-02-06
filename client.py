import socket
import threading

# Definer serverens IP og port
SERVER_IP = "127.0.0.1"  # Ændr dette til serverens IP-adresse
SERVER_PORT = 7913

# Opret en TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Forbind til serveren
client_socket.connect((SERVER_IP, SERVER_PORT))

# Funktion til at modtage beskeder fra serveren
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(f"\n{message}")
        except:
            print("Forbindelsen til serveren blev afbrudt.")
            break

# Start en tråd til at lytte efter beskeder
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Loop til at sende beskeder
while True:
    try:
        message = input("")
        client_socket.send(message.encode())
    except:
        print("Forbindelsen blev afbrudt.")
        client_socket.close()
        break
