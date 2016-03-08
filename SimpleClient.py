import socket

sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

sock.connect(("::1",3000))

sock.sendall("LOGI.173.010.007.006|FC30:0000:0000:0000:0000:0000:0004:0001.12345".encode());

sock.close();