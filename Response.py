import random.py
import ManageDB.py

class Response:

    #Metodo per la generazione della risposta ad una richiesta di login
    #Ritorna una stringa rappresentante il messaggio da inviare
    def login(self,database,ip,port):
        tmp='ALGI.'
        #il metodo ricerca un client per id e port e se presente ritorna il sessionID altrimenti -1
        if (database.findClient(ip,port)==-1):
            tmp=tmp+'0000000000000000'
        else:
            s='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            for i in range(0,16):
                tmp=tmp+s(random.randint(0,15))
        return tmp

    #Metodo per la generazione della risposta ad una richiesta di add
    #Ritorna una stringa rappresentante la risposta
    def addFile(self,database,fileMd5,sessionId,fileName):
        tmp='AADD.'

        #metodo che aggiune un file file md5 al database
        database.addFile(fileMd5,sessionId,fileName)
        #il metodo conta il numero di file con quel Md5, si suppone che l'aggiunta sia gia stata fatta
        n=database.numOfFile(fileMd5)
        tmp=tmp+'{:0>3}'.format(n)
        return tmp

    def remove(self,database,fileMd5,sessionId):
        tmp='ADEL.'
        #chiamo il metodo per la rimozione del file, ritorna -1 se la rimozione è fallita
        n=database.removeFile(fileMd5,sessionId)
        if (n==-1):
            n=999
        else:
            n=database.numOfFile(fileMd5)
        tmp=tmp+'{:0>3}'.format(n)
        return tmp

    def logout(self,database,sessionId):
        tmp='ALGO.'
        #conto quanti file quel peer aveva condiviso
        n=database.numOfFileForSession(sessionId)
        #chiamo il metodo per la rimozione di tutti i file di quel peer
        database.removeFileOfSession(sessionId)
        #sono stati usati due metodi perchè non si sa se il database restituisca il numero
        #di righe eliminate con una delete
        tmp=tmp+'{:0>3}'.format(n)
        return tmp

    #ricerca da sistemare per vedere reale implementazione del database
    def search(self,database,stringa):
        tmp='AFIN.'
        return tmp


