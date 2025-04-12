#include <stdio.h>
#include <stdint.h>

int main(int argc, char* argv[]){
	
	int topolino;
	uint16_t pluto;
	char buf[34];
	
	topolino = 0;
	pluto = 0;
	gets(buf);
	
	if (topolino == 0x41414141){
		printf("Ottimo! Hai modificato correttamente la variabile\n");
	}
	else{
		printf("Sbagliato! Topolino vale: 0x%08x\n", topolino);
	}
}
