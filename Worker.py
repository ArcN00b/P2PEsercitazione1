import threading;
import socket;
import struct;
import Parser

class Worker(threading.Thread):
    client = 0;

    def __init__(self, client, address):
        # definizione thread del client
        threading.Thread.__init__(self);
        self.client = client;

    def run(self):
        try:
            self.comunication();
        except Exception as e:
            print("errore: ", e);

    def comunication(self):
        # ricezione del dato e immagazzinamento fino al max
        data = self.client.recv(2048);

        # ciclo continua a ricevere i dati
        while data:
            # recupero del comando
            cmd = Parser.parse(data);

            # TODO: aggironamento del database e altro

            # TODO: per creare il pacchetto ben formattato da inviare bisogna utilizzare pack
            # pack: args, numero byte seguito dalla sequenza di byte da inviare
            # https://docs.python.org/3.0/library/struct.html

            # esempio per login: LOGI[4B]+IPP2P[55B]+PP2P[5B] = 64B
            resp = Parser.login();
            packet = struct.pack('64B', resp);
            # questo metodo invia tutto il pacchetto costruito
            self.client.sendall(packet);
            print("Comando Inviato");

            # resta in attesa del prossimo comando
            data = self.client.recv(2048);

        # chiude la connessione quando non ci sono più dati
        print("Chiusura socket di connessione");
        # chiude il client
        self.client.close();
