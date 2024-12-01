import socket
import chess

board = chess.Board()

# socket objects
s1 = socket.socket()
s2 = socket.socket()
print("Socket created")


# white = 12345, black = 12346
player1_port = 12345
player2_port = 12346

# assigning ports to sockets and players
s1.bind(('', player1_port))
print("socket binded to %s" %(player1_port))
s2.bind(('', player2_port))
print("socket binded to %s" %(player2_port))

# socket set to listen
s1.listen(1)
print("socket 1 is listening")
s2.listen(1)
print("socket 2 is listening")

# blocking call, sits and waits until players connect
c1, addr1 = s1.accept()
print("Player 1 has connected from ", addr1)
c1.send("Your are playing as WHITE".encode())

c2, addr2 = s2.accept()
print("Player 2 has connected from ", addr2)
c2.send("You are playing as BLACK".encode())

# turn order tracking
white_turn = True

fen = board.fen() # Get the FEN representation of the board
send_str = f"Board:\n{fen}"
c1.send(send_str.encode())
c2.send(send_str.encode())

# game running until it ends
while True:
    print("Turn: ", board.turn)
    # sending board to white
    if board.turn:

        # Receive move 
        print("Waiting for White to play")
        data = c1.recv(1024)
        print("Data received : ", data.decode())
        try:
            # trying to make a move out of sent input
            # chess class from the library handles all this
            move = chess.Move.from_uci(data.decode())
            if move in board.legal_moves:
                board.push(move)
                if board.is_game_over():
                    win = "\nYou Win!\nBoard:\n" + str(board)
                    lose = "\nYou Lose!\nBoard:\n" + str(board)
                    c1.send(win.encode())
                    c2.send(lose.encode())
                    c1.close()
                    c2.close()
                    break
                else:
                    c1.send("Move is legal".encode())
                    fen = board.fen() # Get the FEN representation of the board
                    send_str = f"Board:\n{fen}"
                    c1.send(send_str.encode())
                    c2.send(send_str.encode())
            else:
                c1.send("Illegal Move, try again".encode())
                continue
        except ValueError:
            c1.send("Wrong Format".encode())
            continue
    # same but for black
    else:
        
        # Receive Move
        print("Waiting for Black to play")
        data = c2.recv(1024)
        print("Data received : ", data.decode())

        try:
            move = chess.Move.from_uci(data.decode())
            if move in board.legal_moves:
                board.push(move)
                if board.is_game_over():
                    win = "\nYou Win!\nBoard:\n" + str(board)
                    lose = "\nYou Lose!\nBoard:\n" + str(board)
                    c2.send(win.encode())
                    c1.send(lose.encode())
                    c1.close()
                    c2.close()
                    break
                else:
                    c2.send("Move is legal".encode())
                    fen = board.fen() # Get the FEN representation of the board
                    send_str = f"Board:\n{fen}"
                    c1.send(send_str.encode())
                    c2.send(send_str.encode())
            else:
                c2.send("Illegal Move, try again".encode())
                continue
        except ValueError:
            c2.send("Wrong Format".encode())
            continue
    
    # stopping when connection ends
