import socket
import json
from socket_test_frame_proc import dump_pixel_data
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
    message = json.loads(connection.recv(100).decode("utf-8"))
    reward = message[0]
    done = message[1]
    frame = message[2]
    observation = dump_pixel_data(frame)
    # print recieved value
    print(f"{message},{observation[1]}")