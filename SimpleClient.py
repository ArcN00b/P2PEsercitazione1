import socket

sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

print('Sto per collegarmi')

sock.connect(("::1",3000))

print('Sono connesso')

sock.sendall("LOGI173.010.007.006|FC30:0000:0000:0000:0000:0000:0004:000112345".encode());

buffer = sock.recv(1024);

print("ricevuto: " + buffer.decode())

sock.close();