<!-- SPDX-License-Identifier: zlib-acknowledgement -->
RISC generally means only load/store operations on memory.
e.g. MIPS to take offset from stack pointer `lw r5, 30(r29)` (could also do `sw v0, 0(at)`)

In MIPS, there are a family of instructions that have a delay slot, `sw/lw/j`
This is due to pipelining optimisation, they will always execute next instruction.
(so, common to have proceeding `nop`)

Function calling/returing with return adress register `jal 1f` --> `jr r31`

For MIPS R3000 have exception management registers in coprocessor 0 that can only be controlled in kernel mode 
Exception type could be interrupt, TLB, address/bus error etc., syscall etc.
Designated entry-point/vector addresses per exception type.
The PC will change to these, along with changing bits in status register (specifically priveleged and interrupts disabled)
The return address of exception in coprocessor 0 EPC register
For MIPS R3000, most exceptions go to 'other' handler.
So, say a timer interrupt or a syscall will go to this generic handler:
  1. Set to kernel sp (if coming from userland)
  2. Save source of interrupt registers onto stack 
  save registers onto kernel stack (this is trapframe. how big? contents arch dependent?)

  3. Inspect type in Cause register and call specific handler
  4. If timer interrupt, handler will call scheduler
  5. Schedular asks kernel to switch processes (really would be thread?)
  6. Kernel saves current sp into specific TCB.
     Loads new SP of target from TCB (which would have trapframe layout) and its context 

  xxx. restore registers
  xx. switch back to user stack

  IMPORTANT: would jump back to new PC if say a hardware interrupt as oppose to a syscall
  x. Will jump to EPC register to return, however will restore user mode in branch-delay slot
     So, `lw r27, epc; nop; jr r27; rfe`



GCC MIPS calling convention (IMPORTANT: 'a' registers really r4-7):
`v0/1` return value, `a0/3` for arguments, `s0/s7` conflicts
`sp` (bottom of stack), `fp` frame pointer (top of stack frame)
os161 uses the similar convention for its syscall ABI
(gcc linux, where syscalls use a different register for argument 4 and return)
syscall number in `v0`, return in `v0` if `a3` indicates no errno

Syscalls have ABI and perform escalation with special cpu instructions


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
