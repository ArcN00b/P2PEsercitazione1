Directory centralizzata
L’approccio a directory centralizzato vede una serie di rapporti diretti tra il peer e la directory, tipicamente per poter indicare e ricercare i file.  Ogni comunicazione ha una azione di richiesta ed una corrispondente risposta, possibile in quanto l’interlocutore del peer è sempre unico e certo, nella fattispecie è il sistema di directory o un altro peer.
Login
Ogni peer con indirizzo IPP2P, abile a fornire contenuti sulla porta PP2P, deve registrarsi nel sistema di directory mediante un processo di login, indicando il proprio indirizzo e la relativa porta di comunicazione, che viene posta in ascolto. Il sistema di directory è in ascolto all’indirizzo IPD sulla porta 80. Il processo di login ritorna un codice di sessione SessionID di 16B, composto da una stringa di caratteri random generato da numeri e lettere maiuscole scelti casualmente. Qualora il peer sia già registrato o comunque vi siano problematiche per cui la registrazione risulti non possibile, il codice di ritorno è “0000000000000000”. SessionID non dipende dal tipo di comunicazione v4 o v6 utilizzato.

IPP2P:RND <> IPD:3000
> “LOGI”[4B].IPP2P[55B].PP2P[5B]
< “ALGI”[4B].SessionID[16B]
Aggiunta
Ogni peer registrato può aggiungere un file in un qualsiasi momento, mettendolo a disposizione di tutta la rete P2P. Il file è identificato da una stringa di 100B che lo descrive e sul quale è possibile effettuare una ricerca e da un identificativo md5 unico. In caso di descrizioni differenti relative allo stesso identificativo md5, l’ultima indicata sostituisce le precedenti, indipendentemente dal peer che la ha indicata. Peer differenti possono ospitare lo stesso file. Il pacchetto di risposta riporta quante versioni del file con lo stesso md5 sono presenti nella directory #copy, dopo l’aggiunta. Nel caso venga aggiunto dallo stesso peer un file con identificativo già inserito dallo stesso peer, viene solo aggiornato il nome.

IPP2P:RND <> IPD:3000
> “ADDF”[4B].SessionID[16B].Filemd5[16B].Filename[100B]
< “AADD”[4B].#copy[3B]
Rimozione
Ogni peer registrato può rimuovere un file che ha messo a disposizione dalla directory. La rimozione avviene specificando l’identificativo md5 del file da eliminare. Il pacchetto di risposta riporta quante versioni del file con lo stesso md5 #copy sono presenti nella directory, dopo la rimozione. Nel caso venga eliminato un file non presente non viene effettuata alcuna operazione sulla directory e #copy è posto a 999 per indicare al peer la assenza.

IPP2P:RND <> IPD:3000
> “DELF”[4B].SessionID[16B].Filemd5[16B]
< “ADEL”[4B].#copy[3B]
Ricerca
La ricerca di un file avviene indicando una stringa di ricerca di 20B. Tale stringa viene utilizzata per effettuare una ricerca case insensitive su tutti i titoli presenti, trovando tutti gli md5 relativi ad ogni occorrenza della stringa stessa. Sono possibili più riscontri di differenti titoli, con differente identificativo relativo alla stessa stringa di ricerca e per ogni identificativo sono possibili più peer che lo mettano a disposizione. La risposta è quindi articolata nel numero complessivo di identificativi md5 #idmd5 dove per ognuno di essi viene riportato l’identificativo md5, il nome del file e il numero di copie presenti #copy, mentre per ogni copia viene riportato l’IP e la porta del peer. Nel caso in cui non vi sia alcun riscontro si ha #idmd5=0. Una stringa di ricerca composta dal solo carattere * rappresenta il match con tutte le stringhe e permette di avere informazioni sull’intero contenuto della directory.

IPP2P:RND <> IPD:3000
> “FIND”[4B].SessionID[16B].Ricerca[20B]
< “AFIN”[4B].#idmd5[3B].{Filemd5_i[16B].Filename_i[100B].#copy_i[3B].
{IPP2P_i_j[55B].PP2P_i_j[5B]}}(j=1..#copy_i)}(i=1..#idmd5)
Download
Il peer interessato ad effettuare il download di un file ha effettuato la ricerca ed ha a disposizione un ampio potenziale di peer dai quali procedere con il download, ma procede a selezionare un solo corrispondente rispetto al quale effettuare il download. In questo contesto supponiamo che la scelta venga effettuata dall’utente. Il peer interessato al download si mette in diretta comunicazione con il peer selezionato grazie alla conoscenza di IPP2P e di PP2P. Ogni peer che partecipa alla rete P2P funge da server su tali indirizzi a partire dal login e sino al logout. Il download è organizzato in #chunk e per ognuno di essi viene specificata la lunghezza ed inviato i relativi dati in formato nativo. Infine per mantenere traccia delle attività di download viene segnalata l’azione al sistema di directory, indicando il file mediante l’identificativo md5. La directory risponde riportando il numero di download complessivi avvenuti per quel contenuto #download.

IPP2P:RND <> IPP2P:PP2P
> “RETR”[4B].Filemd5[16B]
< “ARET”[4B].#chunk[6B].{Lenchunk_i[5B].data[LB]}(i=1..#chunk)

IPP2P:RND <> IPD:3000
> “DREG”[4B].SessionID[16B].Filemd5[16B]
< “ADRE”[4B].#download[5B]
Logout
Ogni peer registrato può uscire dalla condivisione comunicando tale intenzione alla directory. La directory rimuove tutti i file legati a tale peer e restituisce il numero di file eliminati #delete che deve corrispondere al numero dei file che il peer aveva attivato nella condivisione. Con il logout il peer smette di ascoltare sull’IP e la porta specificata per le azioni di P2P.

IPP2P:RND <> IPD:3000
> “LOGO”[4B].SessionID[16B]
< “ALGO”[4B].#delete[3B]
