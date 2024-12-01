import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
BOARD_ROWS, BOARD_COLS = 8, 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLS
PIECE_SCALE = 0.75  # Scale pieces to 75% of the square size
PIECE_SIZE = int(SQUARE_SIZE * PIECE_SCALE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)

# Load piece images and scale them
PIECE_IMAGES = {
    "white_pawn": pygame.transform.scale(pygame.image.load("pieces-basic-png/white-pawn.png"), (PIECE_SIZE, PIECE_SIZE)),
    "black_pawn": pygame.transform.scale(pygame.image.load("pieces-basic-png/black-pawn.png"), (PIECE_SIZE, PIECE_SIZE)),
    "white_rook": pygame.transform.scale(pygame.image.load("pieces-basic-png/white-rook.png"), (PIECE_SIZE, PIECE_SIZE)),
    "black_rook": pygame.transform.scale(pygame.image.load("pieces-basic-png/black-rook.png"), (PIECE_SIZE, PIECE_SIZE)),
    "white_knight": pygame.transform.scale(pygame.image.load("pieces-basic-png/white-knight.png"), (PIECE_SIZE, PIECE_SIZE)),
    "black_knight": pygame.transform.scale(pygame.image.load("pieces-basic-png/black-knight.png"), (PIECE_SIZE, PIECE_SIZE)),
    "white_bishop": pygame.transform.scale(pygame.image.load("pieces-basic-png/white-bishop.png"), (PIECE_SIZE, PIECE_SIZE)),
    "black_bishop": pygame.transform.scale(pygame.image.load("pieces-basic-png/black-bishop.png"), (PIECE_SIZE, PIECE_SIZE)),
    "white_queen": pygame.transform.scale(pygame.image.load("pieces-basic-png/white-queen.png"), (PIECE_SIZE, PIECE_SIZE)),
    "black_queen": pygame.transform.scale(pygame.image.load("pieces-basic-png/black-queen.png"), (PIECE_SIZE, PIECE_SIZE)),
    "white_king": pygame.transform.scale(pygame.image.load("pieces-basic-png/white-king.png"), (PIECE_SIZE, PIECE_SIZE)),
    "black_king": pygame.transform.scale(pygame.image.load("pieces-basic-png/black-king.png"), (PIECE_SIZE, PIECE_SIZE)),
}

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")


# Piece classes
class Piece:
    def __init__(self, color):
        self.color = color
        self.image = None

    def get_valid_moves(self, start_pos, board):
        """
        start_pos: A tuple (row, col) of starting position.
        board: The current state of the board.
        return: A list of all valid move positions [(row, col), ...]
        """
        return False


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.image = PIECE_IMAGES[f"{color}_pawn"]
        self.color = color

    def get_valid_moves(self, start_pos, board):
        start_row, start_col = start_pos
        valid_moves = []
        direction = 1 if self.color == "white" else -1
        
        # Normal move: one square forward
        if 0 <= start_row + direction < 8 and board[start_row + direction][start_col] is None:
            valid_moves.append((start_row + direction, start_col))
        
        # Initial move: two squares forward
        if (self.color == "white" and start_row == 1 or self.color == "black" and start_row == 6):
            if board[start_row + 2 * direction][start_col] is None:
                valid_moves.append((start_row + 2 * direction, start_col))
        
        # Captures diagonally
        for d_col in [-1, 1]:
            if 0 <= start_row + direction < 8 and 0 <= start_col + d_col < 8:
                target_piece = board[start_row + direction][start_col + d_col]
                if target_piece and target_piece.color != self.color:
                    valid_moves.append((start_row + direction, start_col + d_col))

        return valid_moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.image = PIECE_IMAGES[f"{color}_rook"]
    
    def get_valid_moves(self, start_pos, board):
        start_row, start_col = start_pos
        valid_moves = []

        # Directions: horizontal and vertical
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d_row, d_col in directions:
            row, col = start_row, start_col
            while True:
                row += d_row
                col += d_col
                if 0 <= row < 8 and 0 <= col < 8:  # Stay within bounds
                    target_piece = board[row][col]
                    if target_piece is None:
                        valid_moves.append((row, col))  # Empty square
                    elif target_piece.color != self.color:
                        valid_moves.append((row, col))  # Capture opponent piece
                        break
                    else:
                        break  # Blocked by friendly piece
                else:
                    break

        return valid_moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.image = PIECE_IMAGES[f"{color}_knight"]
    
    def get_valid_moves(self, start_pos, board):
        start_row, start_col = start_pos
        valid_moves = []
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for d_row, d_col in knight_moves:
            new_row = start_row + d_row
            new_col = start_col + d_col
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board[new_row][new_col]
                if target_piece is None or target_piece.color != self.color:
                    valid_moves.append((new_row, new_col))

        return valid_moves


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.image = PIECE_IMAGES[f"{color}_bishop"]
    
    def get_valid_moves(self, start_pos, board):
        start_row, start_col = start_pos
        valid_moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d_row, d_col in directions:
            row, col = start_row, start_col
            while True:
                row += d_row
                col += d_col
                if 0 <= row < 8 and 0 <= col < 8:
                    target_piece = board[row][col]
                    if target_piece is None:
                        valid_moves.append((row, col))  # Empty square
                    elif target_piece.color != self.color:
                        valid_moves.append((row, col))  # Capture opponent piece
                        break  # Stop after capturing
                    else:
                        break  # Blocked by friendly piece
                else:
                    break  # Out of bounds

        return valid_moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.image = PIECE_IMAGES[f"{color}_queen"]
    
    def get_valid_moves(self, start_pos, board):
        start_row, start_col = start_pos
        valid_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        for d_row, d_col in directions:
            row, col = start_row, start_col
            while True:
                row += d_row
                col += d_col
                if 0 <= row < 8 and 0 <= col < 8:
                    target_piece = board[row][col]
                    if target_piece is None:
                        valid_moves.append((row, col))  # Empty square
                    elif target_piece.color != self.color:
                        valid_moves.append((row, col))  # Capture opponent piece
                        break  # Stop after capturing
                    else:
                        break  # Blocked by friendly piece
                else:
                    break  # Out of bounds

        return valid_moves


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.image = PIECE_IMAGES[f"{color}_king"]

    def get_valid_moves(self, start_pos, board):
        start_row, start_col = start_pos
        valid_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        for d_row, d_col in directions:
            new_row = start_row + d_row
            new_col = start_col + d_col
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board[new_row][new_col]
                if target_piece is None or target_piece.color != self.color:
                    valid_moves.append((new_row, new_col))  # Empty or capture opponent piece

        return valid_moves

# Board class contains all logic for the board state, as well as setup for pieces and their positions
class Board:
    def __init__(self, game_state):
        self.game_state = game_state
        self.white_king_pos = self.get_king_position("white")
        self.black_king_pos = self.get_king_position("black")

    def draw(self, screen):
        """
        Draw the board and pieces on the screen.
        """
        square_size = screen.get_width() // 8
        colors = [(235, 235, 208), (119, 149, 86)]  # Light and dark colors for squares
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

        # Draw the pieces
        for row in range(8):
            for col in range(8):
                piece = self.game_state.board[row][col]
                if piece:
                    piece_image = pygame.transform.scale(piece.image, (int(square_size * 0.75), int(square_size * 0.75)))
                    screen.blit(piece_image, (col * square_size + square_size * 0.125, row * square_size + square_size * 0.125))

    def update_with_move(self, move):
        """
        Update the board visuals based on a move.
        :param move: A dictionary like {"from": "e2", "to": "e4"}
        """
        self.game_state.apply_move(move)
        # After the move, update the board and check for game over conditions
        self.white_king_pos = self.get_king_position("white")
        self.black_king_pos = self.get_king_position("black")

    def get_king_position(self, color):
        """Return the position of the king for the given color."""
        for row in range(8):
            for col in range(8):
                piece = self.game_state.board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def is_in_check(self, color):
        """Check if the king of the given color is in check."""
        king_position = self.white_king_pos if color == "white" else self.black_king_pos
        opponent_color = "black" if color == "white" else "white"

        # Loop over all pieces of the opponent to check if they can attack the king's position
        for row in range(8):
            for col in range(8):
                piece = self.game_state.board[row][col]
                if piece and piece.color == opponent_color:
                    if king_position in piece.get_valid_moves():
                        return True
        return False

    def is_checkmate(self, color):
        """Check if the current player's king is in checkmate."""
        if not self.is_in_check(color):
            return False
        
        # Get all the valid moves for all pieces of the current player
        for row in range(8):
            for col in range(8):
                piece = self.game_state.board[row][col]
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves()
                    for move in valid_moves:
                        # Temporarily make the move and check if it removes the check
                        original_position = piece.position
                        piece.move(move)  # Assuming move method moves the piece
                        if not self.is_in_check(color):
                            piece.position = original_position  # Undo the move
                            return False
                        piece.position = original_position  # Undo the move
        return True

    def is_stalemate(self, color):
        """Check if the current player's position is a stalemate."""
        if self.is_in_check(color):  # Can't be a stalemate if the player is in check
            return False
        
        # Get all the valid moves for all pieces of the current player
        for row in range(8):
            for col in range(8):
                piece = self.game_state.board[row][col]
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves()
                    if valid_moves:  # If there is at least one valid move, not a stalemate
                        return False
        return True

class GameState:
    def __init__(self):
        # Initialize the board as an 8x8 grid, which is empty at the start
        self.board = self.initialize_board()
        self.current_turn = "white"  # Example: "white" starts first

    def initialize_board(self):
        """Initialize the board with pieces at their starting positions."""
        # Example initialization of the board (simplified):
        board = [[None for _ in range(8)] for _ in range(8)]
        # Place the pieces (simplified, assuming piece classes are created)
        board[0] = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rook("black")]
        board[1] = [Pawn("black")]*8
        board[6] = [Pawn("white")]*8
        board[7] = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")]
        return board

    def apply_move(self, move):
        """
        Update the game state by applying a move.
        Validates the move before applying it.

        :param move: A dictionary like {"from": (start_row, start_col), "to": (end_row, end_col)}
        """
        from_row, from_col = move["from"]
        to_row, to_col = move["to"]
        piece = self.board[from_row][from_col]

        if piece is None:
            raise ValueError("No piece at the starting position.")
        
        # Validate the move
        valid_moves = piece.get_valid_moves((from_row, from_col), self.board)
        if (to_row, to_col) not in valid_moves:
            raise ValueError(f"Invalid move for {type(piece).__name__} from {move['from']} to {move['to']}.")

        # Execute the move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        # Switch turns
        self.current_turn = "black" if self.current_turn == "white" else "white"
