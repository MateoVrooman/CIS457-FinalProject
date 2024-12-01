import argparse
import pygame
from chess import Board, GameState # Assuming ChessBoard and pieces are imported from chess.py
from network import Peer  # Import Peer class from network.py
import pickle

class Game:
    def __init__(self, is_host, host, port, peer_host=None, peer_port=None):
        pygame.init()
        self.is_host = is_host
        self.host = host
        self.port = port
        self.peer_host = peer_host
        self.peer_port = peer_port
        self.game_state = GameState()
        self.board = Board(self.game_state)  # Assuming Board handles the chess board setup and game logic
        self.peer = Peer(host, port)

        if is_host:
            self.peer.accept_peer_connection()  # Wait for the second player to connect
        else:
            self.peer.connect_to_peer(peer_host, peer_port)  # Connect to the host

        self.game_over = False

    def game_loop(self):
        """Main game loop."""
        while not self.game_over:
            self.handle_events()  # Event handling (user input, etc.)
            self.update_display()  # Redraw board and pieces
            self.check_for_game_over()  # Check if the game is over

            if self.turn == "white" and self.is_host or self.turn == "black" and not self.is_host:
                # The player whose turn it is should make a move
                self.handle_player_move()
                self.turn = "black" if self.turn == "white" else "white"  # Toggle turn
            else:
                # Wait for the opponent's move
                self.handle_opponent_move()

    def handle_events(self):
        """Handle user input and events (e.g., mouse clicks)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle piece selection and move logic
                pass

    def update_display(self):
        """Update the display (redraw the board, pieces, etc.)."""
        self.board.draw_board()  # Draw the chess board
        self.board.draw_pieces()  # Draw all pieces on the board

    def handle_player_move(self):
        """Let the player make a move and send it to the opponent."""
        # Example: You would need to capture a piece move using mouse clicks, etc.
        # For now, assume the player makes a valid move represented by `move`
        move = self.board.get_player_move()

        # Serialize the move and send it to the opponent
        self.peer.send_message(move)

        # Make the move locally
        self.board.make_move(move)

    def handle_opponent_move(self):
        """Receive the opponent's move and apply it to the game."""
        move = self.peer.receive_message()  # Receive move from the opponent

        # Apply the opponent's move
        self.board.make_move(move)

    def check_for_game_over(self):
        """Check if the game has ended (checkmate, stalemate, etc.)."""
        if self.board.is_checkmate("white") or self.board.is_checkmate("black"):
            self.game_over = True
            print(f"Game Over! {self.turn} wins!")
        elif self.board.is_stalemate("white") or self.board.is_stalemate("black"):
            self.game_over = True
            print("Game Over! It's a stalemate.")

# Start the game
if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Chess game with peer-to-peer architecture")
    parser.add_argument('role', choices=['host', 'client'], help="Specify whether this instance is a 'host' or 'client'")
    parser.add_argument('--address', type=str, default="localhost", help="Address for connecting to the peer (only used if client)")
    parser.add_argument('--port', type=int, default=5555, help="Port for the network connection (default is 5555)")

    # Parse the arguments
    args = parser.parse_args()

    if args.role == 'host':
        is_host = True
    else:
        is_host = False

    

    game.game_loop()
