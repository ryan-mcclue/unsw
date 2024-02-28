<!-- SPDX-License-Identifier: zlib-acknowledgement -->
RISC generally means load/store only operations on memory.
MIPS offset off stack pointer `lw r5, 30(r29)`

MIPS has branch-delay slot, i.e. will always execute instruction following a jump/branch before destination
(due to pipelining)

Function calling/returing with return adress register `jal 1f` --> `jr r31`

GCC MIPS calling convention, has register naming conventions, e.g. r2 -> v0 (value returned by subroutine)
Frame pointer is top of stack frame, stack pointer bottom

A process has an in-kernel stack, which is what is used to handle say a system call
So, it can be said that kernel memory is shared between processes

User level threads only really better if have large numbers

In addition to PCBs, kernel manages TCBs (which have a PCB associated with them)
A trapframe contains registers associated with user space thread
If scheduler determines new thread, then retrieve from TCB
Kernel only schedules threads, so if thread part of another process, then PCB also involved
