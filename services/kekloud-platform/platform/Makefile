CC=gcc
CFLAGS=-Wall -pie -s -fvisibility=hidden
SECFLAGS=-fPIC -Wl,-z,relro,-z,now -Wl,-z,noexecstack -fstack-protector-strong

SOURCES=kpl.c account.c program.c


.PHONY: all clean


all:
	$(CC) $(CFLAGS) $(SECFLAGS) $(SOURCES) -o kpl -L . -l :./vm.so

clean:
	rm -f vm.so
