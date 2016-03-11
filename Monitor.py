import threading
import socket
import struct
from Parser import *
from Response import *


class Monitor(threading.Thread):

    # Lista di attributi del Monitor
    thread_list = {}
    database = None
    lock = None

    # Costruttore che inizializza gli attributi del Monitor
    def __init__(self, thread_list, database, lock):
        # definizione thread del monitor
        threading.Thread.__init__(self)
        self.thread_list = thread_list
        self.database = database
        self.lock = lock

    # Overriding della funzione run per gestire le eccezioni
    def run(self):
        try:
            self.interact();
        except Exception as e:
            print("errore: ", e);
            self.lock.release()

    # Funzione che gestisce l'interfaccia testuale
    def interact(self):

        # Definisco un flag che mi permetta di uscire dal ciclo se necessario
        running = True
        while running:

            # Menù con le varie scelte che possono essere compiute
            choose = -1
            while choose not in (0, 1, 2, 3):
                print('---- Interfaccia di gestione del server ----')
                print('1. Visualizza i client connessi')
                print('2. Visualizza gli md5 registrati')
                print('3. Visualizza i file più scaricati')
                print('0. Chiudi il server')
                choose = input('Fai la tua scelta')

            # Devo procedere per stampare a video i client connessi
            if choose == 1:

                # Intestazione del menù
                print("\n\n---- Client Connessi ----")
                print("SessionID                                    IPP2P                                      PORT")

                # Opero sul database
                self.lock.acquire()
                resp = self.database.listClients()
                self.lock.release()

                # Stampo a video la lista dei client
                for row in resp:
                    print(row)


            # Devo procedere per visualizzare gli md5 registrati
            elif choose == 2:

                # Intestazione del menù
                print("\n\n---- Lista file ----")
                print("MD5      SESSIONID       NUMDOWNLOAD FILENAME")

                # Opero sul database
                self.lock.acquire()
                resp = self.database.listMD5()
                self.lock.release()

                # Stampo a video la lista dei client
                for row in resp:
                    print(row)

            # Visualizzo la lista di file più scaricati
            elif choose == 3:

                # Intestazione del menù
                print("\n\n---- File più scaricati ----")
                print("NUMDOWNLOAD  MD5     SESSIONID    FILENAME")

                # Opero sul database
                self.lock.acquire()
                resp = self.database.mostDownladed()
                self.lock.release()

                # Stampo a video la lista dei client
                for row in resp:
                    print(row)

            # Chiudo tutti i thread e chiudo il server
            elif choose == 0:

                # Controllo i thread attivi per rimuovere dalla lista i thread che sono stati chiusi
                self.thread_list = self.thread_list.intersect(threading.enumerate())

                # Chiudo tutti i thread worker controllando di non chiudere questo thread
                running = False
                this_thread = threading.main_thread()
                for t in self.thread_list:
                    if t != this_thread:
                        t.stop()
                        t.join()
