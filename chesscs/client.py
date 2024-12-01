import socket

# how to play after connection is made
# enter your moves in format example "e2e4"
# columns are a,b,c,d,e,f,g,h
# rows count from 1 to 8 bottom up

# socket object
s = socket.socket()

# your port connection
port = input("Please select port: ")

# connect to the server
s.connect(('127.0.0.1', int(port)))

response = s.recv(1024)
print("Received:", response.decode())
# data from server
while True:
    response = s.recv(1024)
    print(response.decode())
    move = input("My Move: ")
    s.send(move.encode())
    response = s.recv(1024)
    print(response.decode())




