import socket
import pickle

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_peer(self, peer_host, peer_port):
        """Connects to the peer (another player)."""
        self.socket.connect((peer_host, peer_port))
        print("Connected to peer:", peer_host, peer_port)

    def accept_peer_connection(self):
        """Accept an incoming peer connection."""
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.connection, addr = self.socket.accept()
        print("Accepted connection from:", addr)

    def send_message(self, message):
        """Sends a message (move or game state) to the peer."""
        serialized_msg = pickle.dumps(message)
        self.connection.send(serialized_msg)
        print("Sent message:", message)

    def receive_message(self):
        """Receives a message (move or game state) from the peer."""
        serialized_msg = self.connection.recv(1024)
        message = pickle.loads(serialized_msg)
        print("Received message:", message)
        return message

    def close_connection(self):
        """Closes the socket connection."""
        self.connection.close()
        self.socket.close()
        print("Connection closed.")
