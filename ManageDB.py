# In questo file viene definita una classe che definisce metodi utili a gestire il database SQLite di Python
# Per creare il database, usare il comando da shell: sqlite3 data.db

import sqlite3
import sys

class ManageDB:

    # Metodo che inizializza il database
    def initialize(self):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Creo la tabella dei client e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS Clients;")
            c.execute("CREATE TABLE Clients (ip TEXT, port INT);")

            # Creo la tabella dei file e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS Files;")
            c.execute("CREATE TABLE Files (name TEXT, md5 TEXT);")

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 01 - initialize: %s:" % e.args[0])
            sys.exit(1)

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()


    # Metodo che aggiunge un client che ha fatto il login
    def addClient(self, ip, port):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il client
            c.execute("INSERT INTO Clients VALUES('" + ip + "' , " + port + " );")

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print ("Codice Errore 02 - addClient: %s:" % e.args[0])
            sys.exit(1)

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()


    # Metodo che aggiunge un file aggiunto da un client
    def addFile(self, name, md5):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il file
            c.execute("INSERT INTO Files VALUES('" + name + "' , '" + md5 + "' );")

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print ("Codice Errore 03 - addFile: %s:" % e.args[0])
            sys.exit(1)

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina il client tramite indirizzo ip
    def removeClient(self,ip):

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
            sys.exit(1)

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()


    # Metodo che elimina il file identificato da nome e md5
    def removeFile(self,name,md5):

        # Il metodo non fa distinzione da chi ha caricato il file
        # Risulta raro che per errore vada a rimuovere un file caricato da piu' utenti, dato che md5 identifica il file

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il file
            c.execute("DELETE FROM Files WHERE name = " + name + " and md5 = " + md5 + " );")

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print ("Codice Errore 05 - removeFile: %s:" % e.args[0])
            sys.exit(1)

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()




