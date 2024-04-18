<!-- SPDX-License-Identifier: zlib-acknowledgement -->
In a UMA (Uniform Memory Access) architecture, all cores share the same memory access time.
In contrast a NUMA, different cores may have different latencie for certain memory regions.
For UMA, a shared memory bus architecture typically used.
Hardware handles cache consistency, e.g. 1 core writing to an address will invalidate other core's address etc. 
(example implementation may be coherent write-back cache; write-back meaning write to cache first than memory)
Maintaining cache consistency consumes bus bandwidth (so want limited data sharing?)
So, UMA is limited if tasks are memory or IO bound (effectively, resource contention limits performance)
(e.g. 3 2-core machines might be better than a single 6-core machine for CSE servers as memory bound)
The simplicity of UMA makes it useful, however as number of CPUs increase, NUMA might reduce bus contention.

SMP (symmetric multiprocessors) implies the kernel is shared among all cores. 
For a 'big-lock' kernel, mutexes will be associated for largely independent code portions.
For better performance, require hardware support.
A TSL instruction blocks other CPUs from accessing memory bus. 
It's atomic, yet is an effective spinlock.
To reduce bus contention, read before acquiring lock (as when reading from bus require exclusive access)
All cores can read lock without accessing bus. 
`while (*lock == BUSY || test_and_set(lock))`

IMPORTANT: a spinlock will not rely on a context switch like a block (however if lock holder is preempted; long time waits)
So, might be useful for small critical sections (in effect, if shorter than context switching software operations and hardware, e.g. cache, TLB etc.)
On a uniprocessor, spinlocking generally not advisable.
For SMP, either could be viable.

Scheduling can affect performance and correctness of a system with deadlines
Generally favour I/O-bound processes as they relinquish control to a CPU-bound process, but not the other way round.

Pre-emptive on timer interrupt.
Scheduling when multiple ready processes or a thread can no longer run.
Scheduling algorithm dependent on system:
  - Batch (optimise for overall system utilisation)
  - Interactive (percieved performance)
    * 'short' jobs have short response time, 'long' jobs have long response time
      - Round robin:
        Each process has a timeslice and priority
        Priority can be internal (I/O or CPU bound) and external (user importance)
        Priorities need to be adapted/recalculated based on ageing/execution history to avoid starvation (e.g. penalise CPU-bound)
  - Realtime (must meet deadline)

Linux uses 2-level scheduler.
Top level (global scheduler; easier load balancing but lock contention) is assigning process to a core (Multiple Queue SMP Scheduling).
Lower level is per core CPU scheduler, so can do affinity scheduling (re-run process timeslice on same previous core). 
If nothing ready, work steal from another CPU.
`priority = cpu_usage + niceness + base` (base is hardwired scheduler specific)
An I/O bound task generally uses less CPU, so wil have a higher priority.
The CPU usage of a waiting process is dynamically reduced, so a CPU bound task will not starve.
