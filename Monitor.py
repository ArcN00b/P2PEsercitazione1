import select
import sys
import threading

class Monitor(threading.Thread):

    # Lista di attributi del Monitor
    thread_list = {}
    database = None
    lock = None

    # Costruttore che inizializza gli attributi del Monitor
    def __init__(self, database, lock):
        # definizione thread del monitor
        threading.Thread.__init__(self)
        self.database = database
        self.lock = lock

    # Overriding della funzione run per gestire le eccezioni
    def run(self):
        try:
            self.interact();
        except Exception as e:
            print('errore: ', e);
            self.lock.release()

    # Funzione che gestisce l'interfaccia testuale
    def interact(self):

        # Definisco un flag che mi permetta di uscire dal ciclo se necessario
        while True:

            # Menù con le varie scelte che possono essere compiute
            choose = -1
            while choose not in (1, 2, 3):
                print('\n\n---- Interfaccia di gestione del server ----')
            while choose not in ('0', '1', '2', '3'):
                print('---- Interfaccia di gestione del server ----')
                print('1. Visualizza i client connessi')
                print('2. Visualizza gli md5 registrati')
                print('3. Visualizza i file più scaricati')
                print('Fai la tua scelta ')

                # Leggo in modo non bloccante l'input dell'utente @funziona solo su Linux
                if sys.stdin in select.select([sys.stdin], [], []):
                    choose = int(sys.stdin.readline())

            # Devo procedere per stampare a video i client connessi
            if choose == '1':

                # Opero sul database
                self.lock.acquire()
                resp = self.database.listClient()
                self.lock.release()

                # Stampo a video la lista dei client
                if len(resp) > 0:

                    # Intestazione del menù
                    print('\n\n---- Client Connessi ----')
                    print('SessionID                                    IPP2P                                      PORT')

                    # Stampa della riposta
                    for row in resp:
                        print(row)
                else:
                    print('Non ci sono client connessi')


            # Devo procedere per visualizzare gli md5 registrati
            elif choose == '2':

                # Opero sul database
                self.lock.acquire()
                resp = self.database.listMD5()
                self.lock.release()

                # Stampo a video la lista dei file
                if len(resp) > 0:

                    # Intestazione del menù
                    print('\n\n---- Lista file ----')
                    print('MD5      SESSIONID       NUMDOWNLOAD FILENAME')

                    # Stampa della riposta
                    for row in resp:
                        print(row)
                else:
                    print('Non ci sono file registrati')

            # Visualizzo la lista di file più scaricati
            elif choose == '3':

                # Opero sul database
                self.lock.acquire()
                resp = self.database.topDownload()
                self.lock.release()

                # Stampo a video la lista dei file
                if len(resp) > '0':

                    # Intestazione del menù
                    print('\n\n---- File più scaricati ----')
                    print('NUMDOWNLOAD  MD5     SESSIONID    FILENAME')

                    # Stampa della riposta
                    for row in resp:
                        print(row)
                else:
                    print('Non ci sono file registrati')