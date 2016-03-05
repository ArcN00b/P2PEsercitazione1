import re

class Parser:

    # Inizializzo la stringa che contiene il comando e il vettore di stringhe che contengono i campi del messaggio
    commands = None
    fields = [None] * 3

    '''
    Devo aggiungere le exception inerenti al fatto che p.search potrebbe restituire None
    Per ora ci sono le regex che permettono il parsing del messaggio login
    '''

    # Metodo che fa il parsing dei dati
    def parse(self, data):

        # Prendo i primi 4 caratteri maiuscoli all'interno di data e li inserisco in command
        p = re.compile('^[A-Z]{4}')
        self.command = p.search(data).group()

        # Trovo se è presente la componente IPP2P
        p = re.compile('(\d{3}\.){3}\d{3}\|([0-9a-fA-F]{4}\:){7}[0-9a-fA-F]{4}')
        self.fields[0] = p.search(data).group()

        # Trovo se è presente la componente PP2P e lo salvo il fields
        p = re.compile('\d{5}$')
        self.fields[1] = p.search(data).group()