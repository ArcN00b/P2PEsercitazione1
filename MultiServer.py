import select
import socket

# Insieme di costanti utilizzate nel progetto
TCP_IP4 = ''  # Con questo ip il bind viene effettuato su tutte le interfacce di rete
TCP_IP6 = ''  # Con questo ip il bind viene effettuato su tutte le interfacce di rete
TCP_PORT = 3000

class MultiServer:

    def start(self):

        # Creo il socket ipv4, imposto l'eventuale riutilizzo, lo assegno all'ip e alla porta
        server_socket4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket4.bind((TCP_IP4, TCP_PORT)) #forse bisogna gestire errori

        # Creo il socket ipv4, imposto l'eventuale riutilizzo, lo assegno all'ip e alla porta
        server_socket6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        server_socket6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket6.bind((TCP_IP6, TCP_PORT)) #forse bisogna gestire errori

        # Metto il server in ascolto per eventuali richieste sui socket appena creati
        server_socket4.listen(5)
        server_socket6.listen(5)

        # Eseguo le operazioni seguenti finchè il server non viene chiuso
        running = True #Impostare su false per fermare il server e chiudere i thread
        '''
        Lanciare eventualmente in questo punto il thread che si occupa della gestione degli input per controllare lo
        stato del server (per esempio, sapere quanti file sono registrati al momento, chiudere il tutto, ecc)
        '''
        while running:

            # Per non rendere accept() bloccante uso l'oggetto select con il metodo select() sui socket messi in ascolto
            input_ready, read_ready, error_ready = select.select([server_socket4, server_socket6], [], [])

            # Ora controllo quale dei due socket ha ricevuto una richiesta
            for s in input_ready:

                # Il client si è collegato tramite socket IPv4, accetto quindi la sua richiesta avviando il worker
                if s == client_socket4:
                    client_socket4, address4 = server_socket4.accept()
                    client_thread = Worker(client_socket4)
                    client_thread.run()

                # Il client si è collegato tramite socket IPv6, accetto quindi la sua richiesta avviando il worker
                elif s == client_socket6:
                    client_socket6, address6 = server_socket6.accept()
                    client_thread = Worker(client_socket6)
                    client_thread.run()

        # Chiudo i socket
        server_socket4.close()
        server_socket6.close()

tcpServer = MultiServer()
tcpServer.start()