CC=gcc
CFLAGS=-Wall
SECFLAGS=-pie -fPIE -Wl,-z,relro,-z,now -Wl,-z,noexecstack -fstack-protector-all

.PHONY: all clean


all:
	$(CC) $(CFLAGS) $(SECFLAGS) -o kpl \
		vm.h \
		kpl.c \
		account.c account.h \
		program.c program.h \
		-L. -l:./vm.so

clean:
	rm -f vm.so
