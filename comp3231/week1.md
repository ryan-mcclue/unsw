<!-- SPDX-License-Identifier: zlib-acknowledgement -->
RTEMS OS is monolithic where everything runs in priveleged mode, unlike say FreeRTOS.
Would open up possibilities to corrupt kernel data structures etc.
Main task on OS is efficient and secure interleaved execution
Process is memory and resource owner.
Per process has globals, open files, address space, pid, working directory etc.
Per thread has GPRs, SP, PC
Dispatcher thread like scanning for files and worker thread like summing portion of numbers.
Process would be blocked as oppose to ready for efficiency reasons. 
Have a process ready queue to select next.
Also have separate process block queues for distinct events e.g. waiting for file, timer, lock etc.
