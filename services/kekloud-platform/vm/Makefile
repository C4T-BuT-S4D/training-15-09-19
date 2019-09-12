CC=gcc
CFLAGS=-Wall -shared -fvisibility=hidden
CSTRIP=-s
SECFLAGS=-fPIC -Wl,-z,relro,-z,now -Wl,-z,noexecstack -fstack-protector-strong

SOURCES=vm.c commands.c syscalls.c


.PHONY: all debug clean


all:
	$(CC) $(CFLAGS) $(SECFLAGS) $(SOURCES) $(CSTRIP) -o vm.so

debug:
	$(CC) $(CFLAGS) $(SECFLAGS) $(SOURCES) -o vm.so

clean:
	rm -f vm.so
