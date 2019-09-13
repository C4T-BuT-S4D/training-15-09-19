#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "program.h"
#include "account.h"

#define VM_NAME_GEN_SIZE 20
#define VM_PASSWORD_GEN_SIZE 20


int check_vm_name(vm_account_t* vm_account) {
    int i;

    for (i = 0; i < strlen(vm_account->name); i++) {
        if (!(vm_account->name[i] >= 'a' && vm_account->name[i] <= 'z') &&
            !(vm_account->name[i] >= 'A' && vm_account->name[i] <= 'Z') &&
            !(vm_account->name[i] >= '0' && vm_account->name[i] <= '9') &&
            !(vm_account->name[i] == '-')) {
            puts("[-] Invalid character in name.");
            return -1;
        }
    }

    return 0;
}

int check_vm_password(vm_account_t* vm_account) {
    int i;

    for (i = 0; i < strlen(vm_account->password); i++) {
        if (!(vm_account->password[i] >= '0' && vm_account->password[i] <= '9')) {
            puts("[-] Invalid character in password.");
            return -1;
        }
    }

    return 0;
}

int generate_vm_name(vm_account_t* vm_account) {
    int i;
    FILE* file;
    char buffer[VM_NAME_SIZE];

    if ((file = fopen("/dev/urandom", "r")) == NULL) {
        puts("[-] Error while generating VM name.");
        return -1;
    }

    fread(buffer, 1, VM_NAME_GEN_SIZE, file);
    fclose(file);

    for (i = 0; i < VM_NAME_SIZE; i++)
        vm_account->name[i] = 'A' + (unsigned char)buffer[i] % 26;

    vm_account->name[VM_NAME_GEN_SIZE] = 0;

    return 0;
}

int generate_vm_password(vm_account_t* vm_account) {
    int i;

    srand(0x31337);

    for (i = 0; i < VM_PASSWORD_GEN_SIZE; i++)
        vm_account->password[i] = '0' + (unsigned char)(vm_account->name[i] + rand()) % 10;

    vm_account->password[VM_PASSWORD_GEN_SIZE] = 0;

    return 0;
}

int verify_account(vm_account_t* vm_account) {
    vm_account_t expected_account;

    strcpy(expected_account.name, vm_account->name);
    
    if (generate_vm_password(&expected_account)) {
        puts("[-] Error while verifying account.");
        return -1;
    }

    if (strcmp(vm_account->password, expected_account.password)) {
        puts("[-] Invalid password.");
        return 1;
    }

    return 0;
}
