import random.py
import ManageDB.py

#Tutti i metodi eseguono le operazioni sul database
#Necessitano quindi che sia passato il database in ingresso
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
            val=''
            for i in range(0,16):
                val=val+s(random.randint(0,len(s)-1))
            database.addClient(val,ip,port)
        return tmp

    #Metodo per la generazione della risposta ad una richiesta di add
    #Ritorna una stringa rappresentante la risposta
    def addFile(self,database,fileMd5,sessionId,fileName):
        tmp='AADD.'
        nome=fileName
        if (len(fileName)<100):
            nome=fileName+(' '*(100-len(fileName)))
        #metodo che aggiune un file file md5 al database, aggiorna anche gli altri nome dei file
        database.addFile(sessionId,fileMd5,nome)
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
        #metodo che ricerca ricerca il numero distinto di Md5 sulla base della stringa di ricerca
        listMd5=database.findMd5(stringa)
        tmp=tmp+'{:0>3}'.format(listMd5)
        for i in range(0,len(listMd5)):
            tmp=tmp+'{'+listMd5[i]+'.'
            #Ritorna la il fileName di un determinato Md5
            val=database.findFileName(listMd5[i])
            #aggiungo il nome del file alla stringa di ritorno
            tmp=tmp+val+'.'
            #aggiungo il numero file presenti con lo stesso md5
            val=database.numOfFile(listMd5[i])
            tmp=tmp+'{:0>3}'.format(val)+'.'
            #metodo per ricercare tutte le persone che hanno il file con quel Md5, ritorna una lista di sessionId
            listSessionId=database.findSessionID(listMd5[i])
            for j in range(0,len(listSessionId[i])):
                ip,port=database.findClient(listSessionId[i])
                tmp=tmp+'{'+ip+'.'+port+'}'
            tmp=tmp+'}'


        return tmp


