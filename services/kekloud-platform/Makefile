CC=gcc
CFLAGS=-Wall
SECFLAGS=-pie -fPIE -Wl,-z,relro,-z,now -Wl,-z,noexecstack -fstack-protector-all

.PHONY: all clean


all:
	$(CC) $(CFLAGS) $(SECFLAGS) main.c -o main -L. -l:./vm.so

clean:
	rm -f main
