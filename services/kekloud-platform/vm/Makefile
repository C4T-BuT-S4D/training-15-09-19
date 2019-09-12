CC=gcc
CFLAGS=-Wall -shared -s -fvisibility=hidden
SECFLAGS=-fPIC -Wl,-z,relro,-z,now -Wl,-z,noexecstack -fstack-protector-strong

SOURCES=vm.c commands.c syscalls.c


.PHONY: all clean


all:
	$(CC) $(CFLAGS) $(SECFLAGS) $(SOURCES) -o vm.so

clean:
	rm -f vm.so
