import socket
import pygame
import chess

# Pygame GUI helper functions
def draw_board(board):
    # draw the chess board
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    # draw pieces
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                piece_image = pygame.image.load(f"../whitePieces/{piece.symbol().upper()}.png")
            else:
                piece_image = pygame.image.load(f"../blackPieces/{piece.symbol().lower()}.png")
            piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)  # Invert row for Pygame
            screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_from_mouse(pos):
    # Return the square based on the mouse click position
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

# how to play after connection is made
# enter your moves in format example "e2e4"
# columns are a,b,c,d,e,f,g,h
# rows count from 1 to 8 bottom up

# Pygame Constants
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
WHITE = (240, 217, 181)
BLACK = (181, 138, 99)
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Chess Client")
# socket object
s = socket.socket()

# your port connection
port = input("Please select port: ")
# connect to the server
s.connect(('127.0.0.1', int(port)))
response = s.recv(1024)
print("Received:", response.decode())

# Get player piece color
color = response.decode().split()[-1]
print(color)

board = chess.Board()
selected_square = None
turn = "WHITE"

while True:
    # Receive the initial board state at start of turn
    print("Turn: ", turn)
    server_data = s.recv(1024).decode()
    if "Board:" in server_data:
        board_str = server_data.split("Board:")[1].strip()
        position_fen = board_str.split(' ')[0]
        board.set_fen(position_fen)
        print("Received board state:\n", str(board))
    draw_board(board)
    pygame.display.flip()

    if turn == color:
        move = None
        while move is None:
        # Handle user input for move
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_square = get_square_from_mouse(event.pos)
                    print("Clicked square: ", clicked_square)
                    if selected_square is None: # First click - select target piece
                        selected_square = clicked_square
                    else: # Second click - select target square
                        print("Move: ", selected_square, "-", clicked_square)
                        move = chess.Move(selected_square, clicked_square)
                        if move in board.legal_moves:
                            s.send(move.uci().encode()) # Send move to the server
                            response = s.recv(1024).decode()
                            print(response)
                            if "Move is legal" in response:
                                board.push(move)
                                turn = "WHITE" if turn == "BLACK" else "BLACK"
                        else: # Not a legal move, reset selected square and move
                            print("Not a legal move")
                            move = None
                        selected_square = None
                        
    else:
        # Receive the board state
        server_data = s.recv(1024).decode()
        if "Board:" in server_data:
            board_str = server_data.split("Board:")[1].strip()
            position_fen = board_str.split(' ')[0]
            board.set_fen(position_fen)
            print("Received updated board state:\n", str(board))
            turn = "WHITE" if turn == "BLACK" else "BLACK"

    # Draw the board and update the display after receiving an update from the server
    draw_board(board)
    pygame.display.flip()





