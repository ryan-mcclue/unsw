<!-- SPDX-License-Identifier: zlib-acknowledgement -->
TODO: https://handmade.network/p/29/swedish-cubes-for-unity/blog/p/2723-how_media_molecule_does_serialization 

RTEMS OS is monolithic where everything runs in priveleged mode, unlike say FreeRTOS.
Would open up possibilities to corrupt kernel data structures etc.
Main task on OS is efficient and secure interleaved execution
Process is memory (so has stack, data and text sections) and resource owner.
Per process has globals, open files, address space, pid, working directory etc.
Per thread has GPRs, SP, PC
Dispatcher thread like scanning for files and worker thread like summing portion of numbers.
Process would be blocked as oppose to ready for efficiency reasons. 
Have a process ready queue to select next.
Also have separate process block queues for distinct events e.g. waiting for file, timer, lock etc.

Race condition can still occur on single-core, e.g. counter increment pre-empted between load and store
`ldr r1, =var; ldr r2, [r1]; add r2, r2, #1; str r2, [r1]` 
(on x86 can do in 1 instruction, `add dword ptr var, 1`)
In fact, still concurrency in a single-threaded application from in-kernel concurrency

Critical region where shared resources operated on.
Mutual exclusion solutions 
- taking turns (poor if need at differing rates)
- disable interrupts (only possible on single-core) 
- atomic hardware TSL instruction (spinlock/busy-wait, so can get starved if many)
IMPORTANT: all build from locks
- A semaphore more state to overcome busy-waiting.
  Puts processes into a blocked queue if trying to access an unavailable resource, i.e. waits/sleeps; P
  (initial count determines how many waits proceed before blocking) 
  When available, resumes process from queue, i.e. signals/wakeup (can be error-prone to use); V

  allows you to sleep and wakeup
  a countable sleep/wake primitive
  wait() -> let us know when counter > 0. will decrement when wait()ed (this is equivalent to acquiring resource)
  wake() -> increments counter, allowing any waiting threads to operate (this is equivalent to releasing resource)
  allows you to tell several threads that some work is ready collectively 

- A monitor is a grouping of variables, functions that can only be accessed within itself.
  Compiler implements mutual exclusion.
  Condition variable used to wait inside monitor or signal process to resume
  (Seems better to use a condition variable first, then a semaphore if required)
  (easier to reason about an explicit critical region; and get more flexibility with lock)

bounded-buffer has a consumer and a producer


Shared memory communication (usually) requires a form of locking (semaphores, mutexes, monitors, etc) to coordinate the processes/threads.
Whilst message passing based communication does so by exchanging "messages" between the different processes/threads.
I was about to say that the message-based models may still require "locks" of some sort, but they are not explicitly handled by the user.

1 requester to 1 source == trivial   -> (straight-forward single-thread code)
M requesters to 1 source == shared memory -> (for example: multiple threads accessing a hash-table)
1 requester to N sources == message -> (for example: a thread that receives network packets from multiple sockets and puts information in a hashtable)
M requesters to N sources == hybrid -> (for example: multiple threads that receive network packets from multiple sockets and put information in a hashtable)



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

