import socket

sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

sock.connect(("FC00::b:3",3000))

sock.sendall("LOGI173.010.007.0007|FC30:0000:0000:0000:0000:0000:0004:000112345".encode());

buffer = sock.recv(1024).decode();
sessionID = buffer[-16:];
print("ricevuto: " + buffer)

# aggiungo un file
filename = "pippo.txt"
space = ' '*(100-len(filename))
mess = "ADDF"+sessionID+"0001000100010001"+filename+space
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("ricevuto: " + buffer)

# aggiungo un altro file
filename = "pluto.txt"
space = ' '*(100-len(filename))
mess = "ADDF"+sessionID+"0002000200020002"+filename+space
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("ricevuto: " + buffer)

# aggiungo un altro file
filename = "topolino.txt"
space = ' '*(100-len(filename))
mess = "ADDF"+sessionID+"0003000300030003"+filename+space
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("ricevuto: " + buffer)

# test ricerca del file
find = "txt"
space = ' '*(20-len(find))
mess = "FIND"+sessionID+find+space
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("trovato: " + buffer)

sock.close()