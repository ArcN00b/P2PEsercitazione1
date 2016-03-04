# questo file gestisce le connessioni del server

import threading;
import socket;

# from ServerThread import ServerThread

# indirizzo di rete v4
TCP_IP_V4 = "0.0.0.0"
# indirizzo di rete v6
TCP_IP_V6 = "0:0:0:0:0:0:0:0"
# numero della porta
TCP_PORT = 3000;


class MultiServer:
    def accept_v4(server_socket_v4):
        # accetto connessione ipv4
        (client, address) = server_socket_v4.accept();
        # connessione in arrivo da address
        print("....client: ", address);
        thread = ServerThread(client, address);
        thread.start();

    def accept_v6(server_socket_v6):
        # accetto la connessione v6
        (client, address) = server_socket_v6.accept();
        # connessione in arrivo da address
        print("....client: ", address);
        thread = ServerThread(client, address);
        thread.start();

    def start(self):
        # socket server INET di tipo STREAM per TCP per ip v4
        server_sock_v4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

        # socket server INET6 di tipo STREAM per TCP per ip v6
        server_sock_v6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM);

        # imposta riutilizzo della connessione
        server_sock_v4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock_v6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # associa il socket a un indirizzo pubblico con una porta
        server_sock_v4.bind((TCP_IP_V4, TCP_PORT));
        server_sock_v6.bind((TCP_IP_V6, TCP_PORT));

        # si mette in ascolto, per numero di connessioni pendenti
        server_sock_v4.listen(5);
        server_sock_v6.listen(5);

        # TODO: sistemare la connessione per entrambi gli indirizzi
        while True:
            print("....Server in ascolto....");

            # thread per gestire la connessione ipv4
            thread_v4 = threading.Thread(target=accept_v4, args=server_sock_v4);
            thread_v4.start();

            # thread per gestire la connessione ipv6
            thread_v4 = threading.Thread(target=accept_v6, args=server_sock_v4);
            thread_v4.start();

tcpServer = MultiServer();
tcpServer.start();
