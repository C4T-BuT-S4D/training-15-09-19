#ifndef KPL_ACCOUNT_H
#define KPL_ACCOUNT_H


#define VM_NAME_SIZE 32
#define VM_PASSWORD_SIZE 32


typedef struct vm_account_t {
    char name[VM_NAME_SIZE];
    char password[VM_PASSWORD_SIZE];
} vm_account_t;


int check_vm_name(vm_account_t* vm_account);
int check_vm_password(vm_account_t* vm_account);

int generate_vm_name(vm_account_t* vm_account);
int generate_vm_password(vm_account_t* vm_account);

int verify_account(vm_account_t* vm_account);


#endif
