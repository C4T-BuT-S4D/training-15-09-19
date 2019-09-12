CC=gcc
CFLAGS=-Wall
SECFLAGS=-pie -fPIE -Wl,-z,relro,-z,now -Wl,-z,noexecstack -fstack-protector-all

SOURCES=kpl.c account.c program.c


.PHONY: all clean


all:
	$(CC) $(CFLAGS) $(SECFLAGS) -o kpl $(SOURCES) -L. -l:./vm.so

clean:
	rm -f vm.so
