import threading
import socket
import struct
from Parser import *
from Response import *


class Worker(threading.Thread):
    client = 0
    database = None

    def __init__(self, client, database):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.client = client
        self.database = database

    def run(self):
        try:
            self.comunication();
        except Exception as e:
            print("errore: ", e);

    def comunication(self):

        data = " "
        running = True

        # ciclo continua a ricevere i dati
        while running and len(data) > 0:
            # ricezione del dato e immagazzinamento fino al max
            data = self.client.recv(2048).decode()

            # recupero del comando
            command, fields = Parser.parse(data)
            # risposta da inviare
            resp = ""

            # controllo del comando effettuato
            # LOGI
            if command == "LOGI":
                # recupero ip e porta
                ipp2p = fields[0]
                pp2p = fields[1]

                # costruzione della risposta "ALGI"
                resp = Response.login(self.database, ipp2p, pp2p)
            # ADDF
            elif command == "ADDF":
                # recupero session id
                sessionID = fields[0]
                # recupero filemd5
                fileMD5 = fields[1]
                # recupero file name
                fileName = fields[2]

                resp = Response.addFile(self.database, fileMD5, sessionID, fileName)
            # DELF
            elif command == "DELF":
                # recupero sessionID
                sessionID = fields[0]
                # recupero del fileMD5
                fileMD5 = fields[1]

                resp = Response.remove(self.database, fileMD5, sessionID)
            # FIND
            elif command == "FIND":
                # recupero sessionID
                sessionID = fields[0]
                # recupero campo di ricerca
                campo = fields[1];

                resp = Response.search(self.database, campo)
            # DREG
            elif command == "DREG":
                # recupero del sessionID
                sessionID = fields[0]
                # recupero fileMD5
                fileMD5 = fields[1]

                resp = Response.download(self.database, sessionID, fileMD5)
            # LOGO
            elif command == "LOGO":
                # recupero sessionID
                sessionID = fields[0]

                resp = Response.logout(self.database, sessionID)

                # termine del ciclo
                running = False
            # se non ricevo niente di valido response va a none
            else:
                resp = None

            # invio della risposta creata controllando che sia valida
            if resp is not None:
                self.client.sendall(resp.encode())
            print("comando inviato")
        # fine del ciclo

        # chiude la connessione quando non ci sono più dati
        print("Chiusura socket di connessione")
        # chiude il client
        self.client.close();
