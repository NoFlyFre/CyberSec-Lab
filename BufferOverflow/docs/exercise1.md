# Esercizio 1

## Codice C

```c
#include <stdio.h>

int main(int argc, char *argv[]){
    char buffer[1738];
    gets(buffer);
    return 0;
}
```

Compiliamo ed eseguiamo il programma sotto GDB per analizzarne il comportamento.

---

## Analisi con GDB

### Avvio di GDB

```bash
gdb ./esercizio1
```

### Disassemblaggio della funzione `main`

```gdb
(gdb) disassemble main
```

**Output di esempio**:

```
Dump of assembler code for function main:
   0x0804840b <main+0>:  lea    0x4(%esp),%ecx
   0x0804840f <main+4>:  and    $0xfffffff0,%esp
   0x08048412 <main+7>:  pushl  -0x4(%ecx)
   0x08048415 <main+10>: push   %ebp
   0x08048416 <main+11>: mov    %esp,%ebp
   0x08048418 <main+13>: push   %ecx
   0x08048419 <main+14>: sub    $0x6d4,%esp
   0x0804841f <main+20>: sub    $0xc,%esp
   0x08048422 <main+23>: lea    -0x6d2(%ebp),%eax
   0x08048428 <main+29>: push   %eax
   0x08048429 <main+30>: call   0x80482e0 <gets@plt>
   0x0804842e <main+35>: add    $0x10,%esp
   0x08048431 <main+38>: mov    $0x0,%eax
   0x08048436 <main+43>: mov    -0x4(%ebp),%ecx
   0x08048439 <main+46>: leave
   0x0804843a <main+47>: lea    -0x4(%ecx),%esp
   0x0804843d <main+50>: ret
End of assembler dump.
```

---

## Stack Frame e Registri

### Layout dello Stack Frame

Durante l'esecuzione, il compilatore crea uno **stack frame** che contiene:

- Le variabili locali (in questo caso il nostro `buffer`).
- Il **saved EBP** (il vecchio base pointer) e il **return address**.

Lo schema visivo dello stack è:

```
   ┌────────────────────────────┐   ← indirizzo maggiore (ad esempio, EBP)
   │   Saved EBP                │   ← salvato in automatico per collegare i frame
   ├────────────────────────────┤
   │   Return Address           │   ← indirizzo a cui tornare al termine della funzione
   ├────────────────────────────┤
   │   Variabili Locali         │   ← ad esempio, il nostro buffer (buffer[1738])
   │   ... (padding, etc.)      │
   └────────────────────────────┘   ← indirizzo inferiore (ESP)
```

Notiamo che il compilatore riserva **0x6d4 (1748) byte** sullo stack, anche se il `buffer` è di 1738 byte. I byte aggiuntivi servono per **allineamento** e **padding**.

In particolare:

```asm
lea -0x6d2(%ebp), %eax
```

calcola l'indirizzo di partenza del buffer come `EBP - 0x6d2` (1746 in decimale). Pertanto, pur dichiarando un array di 1738 byte, lo spazio effettivo allocato è di circa 1746 byte.

### Registri Principali

- **ESP (Stack Pointer):** punta al top dello stack, aggiornato con ogni `push`/`pop`.
- **EBP (Base Pointer):** punta alla base del frame della funzione; fisso per accedere a variabili locali.
- **EAX:** registro generico, spesso usato per il return value o calcoli aritmetici. Qui contiene l'indirizzo di `buffer` dopo `lea`.
- **ECX:** registro generico; nel prologo, usato per salvare valori temporanei.

### Calcolo dello Spazio Allocato

Se, ad esempio:
```
ebp = 0xffffd5c8
eax = 0xffffcef6  (risultato di lea -0x6d2(%ebp), %eax)
```

allora:
```
spazio_allocato = ebp - eax = 0xffffd5c8 - 0xffffcef6 = 0x6d2 (1746 in decimale)
```

## Costruzione di un Exploit

Conoscere la dimensione esatta del buffer e l'offset tra l'inizio del buffer e il return address (o altre variabili) è fondamentale per costruire un payload di overflow corretto.

## Conclusioni per Esercizio 1

- Il buffer ha circa 1746 byte disponibili, anche se dichiarato a 1738.
- L'ABI e l'allineamento introducono padding.
- Sapere l'offset effettivo consente di costruire exploit precisi.

