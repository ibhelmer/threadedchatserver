import socket
import threading

# Definer serverens IP og port
SERVER_IP = "0.0.0.0"  # Tillader forbindelser fra alle enheder på netværket
SERVER_PORT = 7913

# Opret en liste til at gemme klientforbindelser
clients = []

# Opret en TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind serveren til IP og port
server_socket.bind((SERVER_IP, SERVER_PORT))

# Lyt efter forbindelser (maks 30 klienter i kø)
server_socket.listen(30)
print(f"Server kører på {SERVER_IP}:{SERVER_PORT}")

# Funktion til at sende beskeder til alle klienter
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Send ikke beskeden til afsenderen selv
            try:
                client.send(message)
            except:
                # Fjern klienten, hvis den ikke længere er tilsluttet
                clients.remove(client)

# Funktion til at håndtere hver klient
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Besked modtaget: {message.decode()}")
            broadcast(message, client_socket)
        except:
            break

    # Fjern klienten, hvis den afbryder forbindelsen
    clients.remove(client_socket)
    client_socket.close()
def main():
    # Hovedloop til at acceptere klientforbindelser
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Ny klient tilsluttet: {client_address}")

        # Tilføj klient til listen
        clients.append(client_socket)

        # Start en tråd til at håndtere klienten
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
if __name__ == "__main__":
    main()