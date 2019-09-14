#!/bin/bash

gcc -s -fno-stack-protector -o runner runner.c -L . -l :./vm.so
