import socket

HOST = socket.gethostname()
PORT = 5555
sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
connection, address = sock.accept()
print("Connected by ", address)

#recieve 4 byte integer
message = connection.recv(1024)
print(int.from_bytes(message, byteorder="big"))