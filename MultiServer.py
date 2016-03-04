

# questo file gestisce le connessioni del server


import socket;
# from ServerThread import ServerThread

# indirizzo di rete
TCP_IP = "0.0.0.0"
# numero della porta
TCP_PORT = 3000;

class MultiServer:

    def start(self):
        # socket server INET di tipo STREAM per TCP
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        # imposta riutilizzo della connessione
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # associa il socket a un indirizzo pubblico con una porta
        serversock.bind((TCP_IP, TCP_PORT));

        # si mette in ascolto, per numero di connessioni pendenti
        serversock.listen(5);

        while True:
            print("....Server in ascolto....");
            # accetta le connessioni client e indirizzo
            (client, address) = serversock.accept();
            # connessione in arrivo da address
            print("....client: ", address);
            thread = ServerThread(client, address);
            thread.start();

# fine della classe MultiServer

tcpServer = MultiServer();
tcpServer.start();