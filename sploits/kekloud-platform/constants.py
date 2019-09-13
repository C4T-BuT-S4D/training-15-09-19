#!/usr/bin/env python2


# VM

VM_PROGRAM_SIZE   = 1024
VM_DATA_SIZE      = 1024
VM_STACK_SIZE     = 1024


# SYSCALLS

SYS_EXIT     = 1
SYS_READ     = 2
SYS_WRITE    = 3
SYS_EXEC     = 4
SYS_RAND     = 5
SYS_CLEAR    = 6
SYS_BEEP     = 7


# OPCODES

OP_NONE    = 0

OP_MOV     = 1
OP_SET     = 2

OP_CMP     = 11
OP_TEST    = 12

OP_JMP     = 21
OP_JE      = 22
OP_JNE     = 23
OP_JG      = 24
OP_JGE     = 25
OP_JL      = 26
OP_JLE     = 27

OP_NOT     = 31
OP_AND     = 32
OP_OR      = 33
OP_XOR     = 34
OP_NEG     = 35

OP_INC     = 41
OP_DEC     = 42

OP_ADD     = 51
OP_SUB     = 52
OP_MUL     = 53
OP_DIV     = 54
OP_MOD     = 55

OP_LOOP    = 61

OP_CALL    = 71
OP_RET     = 72

OP_PUSH    = 81
OP_POP     = 82

OP_NOP     = 91

OP_SYS     = 101


#REGISTERS

REG_AX    = -1
REG_BX    = -2
REG_CX    = -3
REG_DX    = -4

REG_SP    = -5
REG_BP    = -6


# RETURN CODES

EXEC_SUCCESS                 = 0
EXEC_INTERRUPTED             = 1

EXEC_ERR_PROGRAM_TOO_LONG    = -1
EXEC_ERR_EXCEEDED_LIMIT      = -2
EXEC_ERR_INVALID_OP          = -3
EXEC_ERR_INVALID_ARG         = -4
EXEC_ERR_SYS_INVALID_OP      = -5
EXEC_ERR_SYS_INVALID_ARG     = -6
EXEC_ERR_STACK_OVERFLOW      = -7
EXEC_ERR_UNKNOWN             = -8
