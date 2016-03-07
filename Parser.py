# Metodo statico che si occupa di suddividere i vari campi di data in modo consono
def parse(data):

    # Inizializzo il contenitore dei vari campi
    fields = None

    # Prendo i primi 4 caratteri maiuscoli all'interno di data e li inserisco in command
    command = data[0:4]

    # Se il comando è LOGI suddivido data in questo modo
    if command == 'LOGI':
        fields[0] = data[5:-6] #IPP2P[55B]
        fields[1] = data[-5:] #PP2P[5B]

    # Se il comando è ADDF o DELF suddivido data in questo modo
    elif command == 'ADDF':
        fields[0] = data[5:21] #SessionID[16]
        fields[1] = data[22:38] #FileMD5[16]
        fields[2] = data[-100:] #Filename[16]

    # Se il comando è DELF suddivido data in questo modo
    elif command == 'DELF':
        fields[0] = data[5:21] #SessionID[16]
        fields[1] = data[-16:] #FileMD5[16]

    # Se il comando è FIND suddivido data in questo modo
    elif command == 'FIND':
        fields[0] = data[5:21] #SessionID[16]
        fields[1] = data[-20:] #Ricerca[20]

    # Se il comando è LOGO suddivido data in questo modo
    elif command == 'LOGO':
        fields[0] = data[-16:] #SessionID[16]

    # Se questo else viene eseguito significa che il comando ricevuto non è previsto
    else:
        print('Errore durante il parsing del messaggio\n')

    # Eseguo il return del comando e dei campi del messaggio
    return command, fields