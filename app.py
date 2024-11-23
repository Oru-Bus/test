import os
import socket
import threading

clients = {}  # Dictionnaire pour associer pseudo à l'adresse du client

def handle_client(client_socket, addr):
    global clients
    try:
        pseudo = client_socket.recv(1024).decode('utf-8')  # Le pseudo est la première chose reçue
        clients[pseudo] = client_socket
        print(f"{pseudo} ({addr}) connecté.")
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            recipient, message = data.split("|", 1)
            if recipient in clients:
                clients[recipient].send(f"Message de {pseudo}: {message}".encode('utf-8'))
            else:
                client_socket.send(f"{recipient} n'est pas connecté.".encode('utf-8'))
    except ConnectionResetError:
        print(f"{addr} déconnecté.")
    finally:
        if pseudo in clients:
            del clients[pseudo]
        client_socket.close()

def start_server(host='0.0.0.0', default_port=12345):
    # Récupère le port dynamique fourni par Railway ou utilise 12345 par défaut
    port = int(os.getenv("PORT", default_port))  
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Serveur démarré sur {host}:{port}")
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
