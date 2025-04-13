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
