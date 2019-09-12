#include <stdio.h>
#include <string.h>
#include <dirent.h>

#include "vm.h"
#include "account.h"
#include "program.h"


#define VM_FILENAME_SIZE 128


void make_program_filename(vm_account_t* vm_account, char* filename) {
    memset(filename, 0, VM_FILENAME_SIZE);

    strcat(filename, "./" DIR_MACHINES "/");
    strcat(filename, vm_account->name);
}

int save_program(vm_program_t* vm_program, vm_account_t* vm_account) {
    FILE* file;
    char filename[VM_FILENAME_SIZE];

    make_program_filename(vm_account, filename);

    if ((file = fopen(filename, "w")) == NULL) {
        puts("[-] Error while saving program.");
        return -1;
    }

    fwrite(vm_program->program, sizeof(int), vm_program->length, file);
    fclose(file);

    puts("[+] Program saved.");
    return 0;
}

int load_program(vm_program_t* vm_program, vm_account_t* vm_account) {
    FILE* file;
    char filename[VM_FILENAME_SIZE];

    make_program_filename(vm_account, filename);

    if ((file = fopen(filename, "r")) == NULL) {
        puts("[-] Error while loading program.");
        return -1;
    }

    fread(vm_program->program, sizeof(int), vm_program->length, file);
    fclose(file);

    puts("[+] Program loaded.");
    return 0;
}

int read_program(vm_program_t* vm_program) {
    int length;

    puts("[?] Please, input program length:");
    scanf("%d", &length);
    getchar();

    if (length <= 0 || length >= VM_PROGRAM_SIZE) {
        puts("[-] Wrong program length.");
        return -1;
    }

    vm_program->length = length;

    puts("[?] Please, input program:");
    fread(vm_program->program, sizeof(int), vm_program->length, stdin);

    puts("[+] Program loaded.");
    return 0;
}

int list_programs() {
    DIR *dir;
    struct dirent *ent;

    if ((dir = opendir("./" DIR_MACHINES "/")) == NULL) {
        puts("[-] Error while listing programs.");
        return -1;
    }

    while ((ent = readdir(dir)) != NULL) {
        if (ent->d_name[0] == '.')
            continue;

        puts(ent->d_name);
    }

    closedir(dir);

    return 0;
}
