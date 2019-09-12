CC=gcc
CFLAGS=-Wall
SECFLAGS=-pie -fPIE -Wl,-z,relro,-z,now -Wl,-z,noexecstack -fstack-protector-all

SOURCES=vm.c commands.c syscalls.c


.PHONY: all clean


all:
	$(CC) $(CFLAGS) $(SECFLAGS) -shared -fPIC -o vm.so $(SOURCES)
		

clean:
	rm -f vm.so
