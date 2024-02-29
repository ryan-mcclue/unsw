<!-- SPDX-License-Identifier: zlib-acknowledgement -->
RISC generally means load/store only operations on memory.
MIPS offset off stack pointer `lw r5, 30(r29)`

In MIPS, family of instructions that have delay slot, sw/lw/j

has branch-delay slot, i.e. will always execute instruction following a jump/branch before destination
(due to pipelining)

Function calling/returing with return adress register `jal 1f` --> `jr r31`

GCC MIPS calling convention, has register naming conventions, e.g. r2 -> v0 (value returned by subroutine)
Frame pointer is top of stack frame, stack pointer bottom

In addition to PCBs, kernel manages TCBs (which have a PCB associated with them)
A trapframe contains registers associated with user space thread
If scheduler determines new thread, then retrieve from TCB
Kernel only schedules threads, so if thread part of another process, then PCB also involved

A process has an in-kernel stack. 
On a context switch (of which a syscall will cause), will change stack pointer to this.
So, it can be said that kernel memory is shared between processes.
TODO: save user registers in kernel stack, but also TCB?

User level threads only really better if have large numbers.
This is because they don't incur context switch operations with TCB/PCBs

Syscalls have ABI and perform escalation with special cpu instructions
For MIPS R3000 have exception management registers in coprocessor 0 that can only be controlled in kernel mode 
Exception type could be interrupt, TLB, address/bus error etc., syscall etc.
Designated entry-point/vector addresses per exception type (PC will change to these, along with being in priveleged mode)
Exception will return to address in c0 EPC register 
Will jump to EPC register to return, however will restore user mode in branch-delay slot.
So, `lw r27, epc; nop; jr r27; rfe`



