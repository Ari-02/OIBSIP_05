import socket
import threading

def handle_client(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"{username} has left the chat.")
                break

            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error: {e}")
                clients.remove(client)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)
    print("Server listening on port 5555...")

    while True:
        client_socket, addr = server_socket.accept()
        username = client_socket.recv(1024).decode('utf-8')
        print(f"Connection established with {username} ({addr[0]}:{addr[1]})")
        clients.append(client_socket)
        client_socket.send("Welcome to the chat!".encode('utf-8'))

        client_handler = threading.Thread(target=handle_client, args=(client_socket, username))
        client_handler.start()

clients = []

if __name__ == "__main__":
    start_server()
