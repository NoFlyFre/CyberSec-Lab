#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool login(){
	char password[37];
	printf("Inserisci la parola d'ordine: \n");
	gets(password);
	return strcmp(password,"segreto")==0;
}

void accedi(){
	printf("Hai eseguito l'accesso correttamente\n");		
}

void impossibile(){
	printf("Funzione mai invocata!\n");
}


int main (int argc, char* argv[]){	
	bool autorizzato;

	autorizzato = login();
	
	if (autorizzato)
		accedi();
	else
		printf("Spiacente, parola d'ordine errata. Accesso negato\r\n");

	return 0;
}
