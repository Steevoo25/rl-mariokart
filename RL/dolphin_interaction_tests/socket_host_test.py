import socket

# A test script to connect to dolphin and accept a message (the current value of frame counter)
# -- set up Host socket
HOST = socket.gethostname()
PORT = 5555
sock = socket.socket()
sock.bind((HOST, PORT))
# -- wait for a connection
sock.listen(1)
# -- accept connection
connection, address = sock.accept()
# -- print connection address
print("Connected by ", address)
while True:
    #recieve bytes
    message = connection.recv(4)
    # print recieved value
    print(int.from_bytes(message, byteorder="big"))