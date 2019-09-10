CC=gcc
CFLAGS=-Wall
SECFLAGS=-pie -fPIE -Wl,-z,relro,-z,now -Wl,-z,noexecstack -fstack-protector-all

.PHONY: all clean


all:
	$(CC) $(CFLAGS) $(SECFLAGS) -shared -fPIC -o vm.so \
		vm.c vm.h \
		commands.c commands.h \
		syscalls.c syscalls.h \
		flags.h

clean:
	rm -f vm.so
