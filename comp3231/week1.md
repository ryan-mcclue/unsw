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

Append os161 path in .profile as this is login shell (could do .bash_profile)
vscode c/c++ c_cpp_properties.json for searchability
-exec in vscode for gdb console
cs3231/root/.gdbinit:
set can-use-hw-watchpoints 0
define connect
dir ~/cs3231/warmup-src/kern/compile/WARMUP
target remote unix:.sockets/gdb
b panic
end


OS UTILITIES
% cd ~/cs3231/warmup-src
% ./configure
% bmake WERROR="-Wno-error=uninitialized"
% bmake install
% ls ~/cs3231/root

CONFIGURE KERNEL
% cd ~/cs3231/warmup-src/kern/conf
% ./config WARMUP
% cd ../compile/WARMUP
% bmake depend
% bmake
% bmake install

REBUILDING KERNEL
% cd ~/cs3231/warmup-src/kern/compile/WARMUP
% bmake && bmake install

SIMULATOR
% cd ~/cs3231/root
% wget http://cgi.cse.unsw.edu.au/~cs3231/24T1/assignments/warmup/sys161.conf
% sys161 kernel
(sys161 kernel q)

DEBUGGING (IN ROOT)
% sys161 -w kernel
% os161-gdb kernel

