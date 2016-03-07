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
            c.execute("DROP TABLE IF EXISTS Clients;")
            c.execute("CREATE TABLE Clients (sessionId TEXT, ip TEXT, port TEXT);")

            # Creo la tabella dei file e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS Files;")
            c.execute("CREATE TABLE Files (name TEXT, md5 TEXT, sessionId TEXT);")

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 01 - initialize: %s:" % e.args[0])
            #raise Exception()

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
            c.execute("INSERT INTO Clients VALUES(?,?,?)", (sessionId, ip, port))

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 02 - addClient: %s:" % e.args[0])
            #raise Exception("Errore")

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
            c.execute("INSERT INTO Files VALUES(?,?,?)", name, md5, sessionId)

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
    def removeClient(self, ip):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il client
            c.execute("DELETE FROM Clients WHERE ip = " + ip + " );")

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
            c.execute("DELETE FROM Files WHERE sessionId = " + sessionId + " and md5 = " + md5 + " );")

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

    # Metodo per ricercare il client dai campi session id e port, per vedere se e' gia presente
    def findClient(self,ip, port):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il file
            c.execute("SELECT sessionID FROM Clientes WHERE ip = " + ip + " and port = " + port + " );")
            result=c.fetchall()
            if (len(result)==0):
                return -1
            else:
                for row in result:
                   return row[0]

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 06 - findClientForIP: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per ricercare le informazioni del client per sessionID
    # Ritorna due elementi, l'ip e la porta
    def findClient(self,sessionId):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il file
            c.execute("SELECT ip,port FROM Clients WHERE sessionID = " + sessionId + " );")
            result=c.fetchall()
            for row in result:
                return row[0],row[1]

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 07 - findClientForSessionID: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    #Metodo per ricercare il client dai campi session id e port, per vedere se è gia presente
    def findClient(self,ip, port):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il file
            c.execute("SELECT sessionID FROM Clientes WHERE ip = " + ip + " and port = port );")
            result=c.fetchall()
            if (len(result)==0):
                return -1
            else:
                for row in result:
                   return row[0]

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 06 - findClientForIP: %s:" % e.args[0])
            sys.exit(1)

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    #Metodo per ricercare le informazioni del client per sessionID
    #Ritorna due elementi, l'ip e la porta
    def findClient(self,sessionID):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il file
            c.execute("SELECT ip,port FROM Clientes WHERE sessionID = " + sessionID+" );")
            result=c.fetchall()
            for row in result:
                return row[0],row[1]

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 07 - findClientForSessionID: %s:" % e.args[0])
            sys.exit(1)

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

manager = ManageDB()
manager.addClient("1","192.168.0.2","3000")
print("aggiunto client");

