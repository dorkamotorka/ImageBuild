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

# QEMU 

QEMU is a processor emulator knows as Hypervisor of type 2. 
It has two operating modes:
- User mode emulation: QEMU can launch Linux processes compiled for one CPU on another CPU, translating syscalls on the fly.
- Full system emulation: QEMU emulates a full system (virtual machine), including a processor and various peripherals such as disk, ethernet controller etc.

## User mode emulation

In summary, user mode emulation is a nice mode when it works and should be preferred when speed matters, but is not a perfect astraction. e.g. This mode does not cover all syscalls.
Full system emulation mode should be used for a more complete emulation.

#### TODO: Full System emulation
# https://www.cnblogs.com/pengdonglin137/p/5020143.html

## debootstrap vs qemu-debootstrap

qemu-deboostrap is just like debootstrap, but copies a static qemu interpreter in the chroot as well.

Usage:	sudo qemu-debootstrap --arch=<target-arch> <target-distro> <path-to-directory>

## Known Issues

ISSUE 1:
In the User mode emulation QEMU does not cover all syscalls so it might result in the debug output like:

	qemu: Unsupported syscall: 335

ISSUE 2:
The error message sudo: no tty present and no askpass program specified will occur when the sudo command is trying to execute a command that requires a password but sudo does not have access to a tty to prompt the user for a passphrase. As it can’t find a tty, sudo fall back to an askpass method but can’t find an askpass command configured.
	
	sudo: no tty present and no askpass program specified
