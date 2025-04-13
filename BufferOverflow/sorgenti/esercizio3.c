void win() {
	printf("Hai modificato correttamente il flusso di esecuzione\n");
}

int main(int argc, char *argv[]) {
	int (*fp)();
	char buffer[10];
	
	fp = 0;
	gets(buffer);
	if(fp) {
		printf("Chiamo l'indirizzo della funzione, salto a 0x%08x\n", fp);
		fp();
  	}
}
