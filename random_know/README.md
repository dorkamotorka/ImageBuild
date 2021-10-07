# Newby Dictionary

# TODO: Emulation

## System call(syscall)

System calls are the most critical interface of all user space software. 
They are the means of invoking kernel's functionality. 
Without them, software would not be able to communicate with the user, access the file system or establish network connections. 
Every kernel provides a very specific set of system calls. For example, the system call set greatly differs between Linux and FreeBSD.

## binfmt_misc (miscellaneous Binary Formats)

binfmt_misc is a capability of the Linux kernel to recognize any executable files and to transfer them to a specific program in user mode, such as an interpreter that loads the program into the main memory.

## Binary Translation(BT)

In computing, binary translation is a form of binary recompilation where sequences of instructions are translated from a source instruction set to the target instruction set.

### Static BT

A translator using static binary translation aims to convert all of the code of an executable file into code that runs on the target architecture without having to run the code first, as is done in dynamic binary translation.

### Dynamic BT

Dynamic binary translation (DBT) looks at a short sequence of code—typically on the order of a single basic block—then translates it and caches the resulting sequence.
