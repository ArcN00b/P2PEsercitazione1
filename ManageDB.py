# In questo file viene definita una classe che definisce metodi utili a gestire il database SQLite di Python
# Per creare il database, usare il comando da shell: sqlite3 data.db

import sqlite3
import sys

class ManageDB:
    # Metodo che inizializza il database
    def __init__(self):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Creo la tabella dei client e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS CLIENTS;")
            c.execute("CREATE TABLE CLIENTS (SESSIONID TEXT NOT NULL, IP TEXT NOT NULL, PORT TEXT NOT NULL);")

            # Creo la tabella dei file e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS FILES;")
            c.execute("CREATE TABLE FILES (NAME TEXT NOT NULL, MD5 TEXT NOT NULL, SESSIONID TEXT NOT NULL);")

            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 01 - initialize: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che aggiunge un client che ha fatto il login
    def addClient(self, sessionId, ip, port):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il client
            c.execute("INSERT INTO CLIENTS (SESSIONID, IP, PORT) VALUES (?,?,?)" , (sessionId,ip, port))
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 02 - addClient: %s:" % e.args[0])
            raise Exception("Errore")

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che aggiunge un file aggiunto da un client
    def addFile(self, md5, sessionId, name):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il file
            c.execute("INSERT INTO FILES (NAME, MD5, SESSIONID) VALUES (?,?,?)" , (name, md5, sessionId))
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 03 - addFile: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina il client tramite indirizzo ip
    def removeClient(self, sessionId):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il client
            c.execute("DELETE FROM CLIENTS WHERE SESSIONID = ? " , (sessionId,))
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 04 - removeClient: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina il file identificato da nome e md5
    def removeFile(self, md5, sessionId):

        # Il metodo non fa distinzione da chi ha caricato il file
        # Risulta raro che per errore vada a rimuovere un file caricato da piu' utenti, dato che md5 identifica il file

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il file
            c.execute("DELETE FROM FILES WHERE SESSIONID=:ID AND MD5=:COD" , {"ID": sessionId, "COD": md5} )
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 05 - removeFile: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    #ID IP PORTA metodo 1 ritorno sessionID

    # Metodo per ricercare il client dai campi session id e port, per vedere se e' gia presente
    # Ritorna l'id del client
    def findClient(self, sessionId, ip, port, flag):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il client
            if flag == '1':
                c.execute("SELECT SESSIONID FROM CLIENTS WHERE IP=:INDIP AND PORT=:PORTA" , {"INDIP": ip, "PORTA": port} )
            else:
                c.execute("SELECT IP, PORT FROM CLIENTS WHERE SESSIONID = ? " , (sessionId,))
            conn.commit()

            result=c.fetchall()
            return result


        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 06 - findClientForIP: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    '''
    # Metodo per ricercare le informazioni del client per sessionID
    # Ritorna due elementi, l'ip e la porta
    def findClient(self,sessionId):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il file
            c.execute("SELECT IP, PORT FROM CLIENTS WHERE SESSIONID = ? " , (sessionId,))
            conn.commit()

            result = c.fetchall()
            return result

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 07 - findClientForSessionID: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()
    '''

manager = ManageDB()
manager.addClient("1","192.168.0.2","3000")

print ("Test primo findClient: " )
all_rows = manager.findClient("1", "0", "0", "2")
for row in all_rows:
    print('ip: {0}, porta: {1}'.format(row[0], row[1]))


print ("Test seondo findClient: " )
all_rows = manager.findClient("0", "192.168.0.2", "3000", "1")
for row in all_rows:
    print('id: {0}'.format(row[0]))


manager.removeClient("1")
all_rows = manager.findClient("1", "0", "0", "1")
print ("Dopo eliminazione: " )
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))




