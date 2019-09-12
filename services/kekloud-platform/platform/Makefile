CC=gcc
CFLAGS=-Wall -pie -fvisibility=hidden
CSTRIP=-s
SECFLAGS=-fPIC -Wl,-z,relro,-z,now -Wl,-z,noexecstack -fstack-protector-strong

SOURCES=kpl.c account.c program.c


.PHONY: all debug clean


all:
	$(CC) $(CFLAGS) $(SECFLAGS) $(SOURCES) $(CSTRIP) -o kpl -L . -l :./vm.so

debug:
	$(CC) $(CFLAGS) $(SECFLAGS) $(SOURCES) -o kpl -L . -l :./vm.so

clean:
	rm -f kpl
