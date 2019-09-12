#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "vm.h"
#include "account.h"
#include "program.h"


#define LIFETIME 30
#define VM_EXEC_LIMIT 1024


char banner[] = "\x20\x5f\x5f\x20\x20\x5f\x5f\x5f\x20\x20\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x20\x20\x5f\x5f\x20\x20\x5f\x5f\x5f\x20\x20\x5f\x5f\x20\x20\x20\x20\x20\x20\x20\x20\x5f\x5f\x5f\x5f\x5f\x5f\x20\x20\x20\x20\x5f\x5f\x20\x20\x20\x20\x5f\x5f\x20\x20\x20\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x20\x20\x0a\x7c\x20\x20\x7c\x2f\x20\x20\x2f\x20\x7c\x20\x20\x20\x5f\x5f\x5f\x5f\x7c\x7c\x20\x20\x7c\x2f\x20\x20\x2f\x20\x7c\x20\x20\x7c\x20\x20\x20\x20\x20\x20\x2f\x20\x20\x5f\x5f\x20\x20\x5c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x20\x20\x20\x20\x20\x5c\x20\x0a\x7c\x20\x20\x27\x20\x20\x2f\x20\x20\x7c\x20\x20\x7c\x5f\x5f\x20\x20\x20\x7c\x20\x20\x27\x20\x20\x2f\x20\x20\x7c\x20\x20\x7c\x20\x20\x20\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x2e\x2d\x2d\x2e\x20\x20\x7c\x0a\x7c\x20\x20\x20\x20\x3c\x20\x20\x20\x7c\x20\x20\x20\x5f\x5f\x7c\x20\x20\x7c\x20\x20\x20\x20\x3c\x20\x20\x20\x7c\x20\x20\x7c\x20\x20\x20\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x7c\x20\x20\x7c\x20\x20\x7c\x20\x20\x7c\x0a\x7c\x20\x20\x2e\x20\x20\x5c\x20\x20\x7c\x20\x20\x7c\x5f\x5f\x5f\x5f\x20\x7c\x20\x20\x2e\x20\x20\x5c\x20\x20\x7c\x20\x20\x60\x2d\x2d\x2d\x2d\x2e\x7c\x20\x20\x60\x2d\x2d\x27\x20\x20\x7c\x20\x7c\x20\x20\x60\x2d\x2d\x27\x20\x20\x7c\x20\x7c\x20\x20\x27\x2d\x2d\x27\x20\x20\x7c\x0a\x7c\x5f\x5f\x7c\x5c\x5f\x5f\x5c\x20\x7c\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x7c\x7c\x5f\x5f\x7c\x5c\x5f\x5f\x5c\x20\x7c\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x7c\x20\x5c\x5f\x5f\x5f\x5f\x5f\x5f\x2f\x20\x20\x20\x5c\x5f\x5f\x5f\x5f\x5f\x5f\x2f\x20\x20\x7c\x5f\x5f\x5f\x5f\x5f\x5f\x5f\x2f\x20\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20";


int create_vm(vm_account_t* vm_account, vm_program_t* vm_program) {
    int result;

    if ((result = read_program(vm_program)))
        return result;

    if ((result = generate_vm_name(vm_account)))
        return result;

    if ((result = generate_vm_password(vm_account)))
        return result;

    return 0;
}

int load_vm(vm_account_t* vm_account, vm_program_t* vm_program) {
    int result;
    char* newline;

    puts("[?] Please, input VM name:");
    fgets(vm_account->name, VM_NAME_SIZE, stdin);
    if ((newline = strchr(vm_account->name, '\n')) != NULL)
        *newline = '\0';

    if ((result = check_vm_name(vm_account)))
        return result;

    puts("[?] Please, input VM password:");
    fgets(vm_account->password, VM_PASSWORD_SIZE, stdin);
    if ((newline = strchr(vm_account->password, '\n')) != NULL)
        *newline = '\0';

    if ((result = check_vm_password(vm_account)))
        return result;

    if ((result = verify_account(vm_account)))
        return result;

    if ((result = load_program(vm_program, vm_account)))
        return result;

    return 0;
}

int save_vm(vm_account_t* vm_account, vm_program_t* vm_program) {
    int result;

    if ((result = save_program(vm_program, vm_account)))
        return result;

    puts("[+] Your VM was saved.");
    printf("[*] Name: %s\n", vm_account->name);
    printf("[*] Password: %s\n", vm_account->password);

    return 0;
}

int run_vm(vm_program_t* vm_program) {
    int result;

    result = run_program(vm_program, VM_EXEC_LIMIT);

    printf("[*] You VM exited with code %d\n", result);

    return 0;
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    
    alarm(LIFETIME);
}

int main(int argc, char** argv, char** envp) {
    int result;

    int choice;
    vm_account_t vm_account;
    vm_program_t vm_program;

    setup();
    puts(banner);

    while (1) {
        puts("[1] Create VM");
        puts("[2] Load VM");
        puts("[3] List VMs");
        puts("[4] Exit");
    
        scanf("%d", &choice);
        getchar();

        if (choice == 1) {
            if ((result = create_vm(&vm_account, &vm_program)))
                return result;
            break;
        }
        else if (choice == 2) {
            if ((result = load_vm(&vm_account, &vm_program)))
                return result;
            break;
        }
        else if (choice == 3) {
            if ((result = list_programs()))
                return result;
        }
        else if (choice == 4) {
            puts("[*] Bye!");
            return 0;
        }
        else {
            puts("[-] Incorrect choice. Please, try again.");
            continue;
        }
    }

    puts("[?] Do you want to run VM?");
    puts("[1] Yes");
    puts("[2] No");

    scanf("%d", &choice);
    getchar();
    
    if (choice == 1) {
        if ((result = run_vm(&vm_program)))
            return result;

        puts("[?] Do you want to save VM? (Y/N)");
        puts("[1] Yes");
        puts("[2] No");

        scanf("%d", &choice);
        getchar();

        if (choice == 1) {
            if ((result = save_vm(&vm_account, &vm_program)))
                return result;
        }
    }

    puts("[*] Bye!");

    return 0;
}
