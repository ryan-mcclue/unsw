<!-- SPDX-License-Identifier: zlib-acknowledgement -->
ready<->running
blocked->ready
running->blocked

RTEMS OS is monolithic where everything runs in priveleged mode, unlike say FreeRTOS.
Would open up possibilities to corrupt kernel data structures etc.
Main task of OS is concurrent access of resources (scheduler, synchronisation primitives) 
and hardware abstraction (virtual memory, vfs)
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
NOTE: a premptive lock allows to call acquire() multiple times from same owner
IMPORTANT: all build from locks and are OS implementation specific (e.g. os161 uses wait channels for cvs)
- A semaphore more state to overcome busy-waiting.
  Puts processes into a blocked queue if trying to access an unavailable resource, i.e. waits/sleeps; P
  (initial count determines how many waits proceed before blocking) 
  When available, resumes process from queue, i.e. signals/wakeup (can be error-prone to use); V

  allows you to sleep and wakeup
  a countable sleep/wake primitive
  wait() -> P() -> let us know when counter > 0. will decrement when wait()ed 
  (this is equivalent to acquiring resource)
  wake() -> V() -> increments counter, allowing any waiting threads to operate 
  (this is equivalent to releasing resource)
  allows you to tell several threads that some work is ready collectively 

- A monitor is a grouping of variables, functions that can only be accessed within itself.
  Compiler implements mutual exclusion.
  Condition variable used to wait inside monitor or signal process to resume
  (Seems better to use a condition variable first, then a semaphore if required)
  (easier to reason about an explicit critical region; and get more flexibility with lock)

cvs typically implemented with mesa semantics so:
 - are not woken up immediately in any order
 - spurious wakeups possible (so always wait in a loop on a variable check) 
(no spurious wakeups for semaphores)

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

DISABLE HANGMAN
In kern/conf/ASST1 at the bottom comment out options hangman (with a #)
then in the same directory run ./config ASST1
go back to kern/compile/ASST1 and bmake depend then bmake && bmake install

=======================
<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Livelock special form of starvation, in which each thread constantly swapping but making no progress 
IMPORTANT: only possible if some active waiting/resource resolution strategy i.e. if can't obtain release resources and try again etc.

Deadlock occurs when one thread with lock attempts to access other lock and other thread is doing the same. Yields cycle
Prevention:
1. Ostrich Algorithm (bury head in sand and ignore)
2. Allocate locks in a hierarchical order.
   So, if A requires 1 it must acquire it before 2. 
   However, release order not important
3. Detection and Recovery
Create a directed RAG (resource-allocation-graph) with locks and process nodes; look for cycles.
Arrow direction indicates 'wants', i.e. process wants resource

For resources with multiple types, at a point in time have:
* Allocation matrix (resources process has currently)
* Request matrix (resources process requests)
* Resources available
Want to see if there is an order of process execution that can satisfy requests
(so, run 1 process and return its resources)

To recover, can forcibly pre-empt/take resource from a process or can kill a process
4. Deadlock Avoidance
Require upfront knowledge of each processes maximum number of resource usage (banker's algorithm rarely used)

Safe state if a scheduling order exists even if each process requests their maximum resources
Unsafe not necessarily a deadlock, just no guarantee
So an avoidance algorithm would only grant requests that result in safe states 

First-come first-serve policy to help prevent starvation on lock acquisition. 
Time slices also to prevent long-running processes dominating.

=======================
<!-- SPDX-License-Identifier: zlib-acknowledgement -->
RISC generally means only load/store operations on memory.
e.g. MIPS to take offset from stack pointer `lw r5, 30(r29)` (could also do `sw v0, 0(at)`)

In MIPS, there are a family of instructions that have a delay slot, `sw/lw/j`
This is due to pipelining optimisation, they will always execute next instruction.
(so, common to have proceeding `nop`)

Function calling/returing with return adress register `jal 1f` --> `jr r31`

GCC MIPS calling convention (IMPORTANT: 'a' registers really r4-7):
`v0/1` return value, `a0/3` for arguments, `s0/s7` conflicts
`sp` (bottom of stack), `fp` frame pointer (top of stack frame)
os161 uses the similar convention for its syscall ABI
(gcc linux, where syscalls use a different register for argument 4 and return)
syscall number in `v0`, return in `v0` if `a3` indicates no errno

Syscalls have ABI and perform escalation with special cpu instructions

For MIPS R3000 have exception management registers in coprocessor 0 that can only be controlled in kernel mode 
Exception type could be interrupt, TLB, address/bus error etc., syscall etc.
Designated entry-point/vector addresses per exception type.
The PC will change to these, along with changing bits in status register (specifically priveleged and interrupts disabled)
The return address of exception in coprocessor 0 EPC register
For MIPS R3000, most exceptions fall under 'other' handler.
So, say a timer interrupt or a syscall will go to this generic handler:
  (IMPORTANT: if applicable, the compiler will save registers first to preserve compiler calling convention) 
  1. Set to kernel sp (if coming from userland)
  2. Save trapframe on kernel stack.
     Trapframe is all gpr, status, sp 
  3. Inspect type in Cause register and call specific handler
     TIMER: 
     - call scheduler
     - scheduler asks kernel to switch to thread
       (TCB associated with a PCB. Only schedule threads, so if part of another process, then PCB also involved)
     - kernel saves current sp and pc into specific TCB (so can be said processes share kernel stack memory)
       loads new sp from destination TCB, unloads trapframe and sets new pc
     SYSCALL:
     - restore trapframe
     - Will jump to EPC register to return, however will restore user mode in branch-delay slot
       So, `lw r27, epc; nop; jr r27; rfe`

User level threads only really better if have large numbers.
This is because they don't incur context switch operations with TCB/PCBs

=======================
<!-- SPDX-License-Identifier: zlib-acknowledgement -->
user<->filesystem:
* arbitrary-size:fixed-blocks
* contiguous:fragmented
* access-control, attributes
* hierarchical:flat

Generally have fixed block sizes:
* Large: fewer IO; good for sequential access
* Small: less unrelated data; good for random access

Block allocation strategies: (all have internal fragmentation)
(So, when create a file, will allocate as many blocks as needed and update as go)
* Contiguous
  - Access: Fast sequential, fast random
  - External Fragmentation (only really applicable for read-only)
* Linked
  - Access: Fast sequential, slow random
* Indexed (a data structure which has pointers to all blocks)
  (considered 1write as the shifting of block numbers occurs in inode that is in ram, not disk)
  - Access: Fast sequential, fast random
  (ext fs uses inodes with pointers for each file;
  (FAT has a single file allocation table for all files, index block, file control block etc.)
  IMPORTANT: FAT is indexed, i.e. in RAM, however stores with linked list allocation
  (there is memory overhead of maintaining )
  (updating/deleting are only 1 write)

Storing free blocks:
* Linked list: no extra space, slower as more disk accesses (storage free, as store free blocks in blocks themselves)
* Bitmap: faster search, contiguous (used by linux as contiguous faster for hardware and caching)
  (if deleted, actually only mark as free on bitmap, block is not physically cleared)

A sparse file has logical size different to physical, i.e. stores 0s in metadata rather than storing 

regular files, directories and device files (block, character)

a directory is mapping of file names to inode numbers (a hard link has same number, different name)
unique absolute path names from root directory of file system

file locks exist to prevent simultaneous access to a file
in linux, dentries (file names) are textual references to inode 
(a directory file is a mapping to dentries)
inode (indexed allocation) will be deleted when its reference counter is 0.
so, simultaneous read/write/deletion allowed on linux
on windows, mandatory file locks exist

SPI IC disk controller -> SPI driver -> filesystem (caching, write scheduling) -> VFS (vnode) 
FS (write/read/mount, allocation strategies, inodes, etc.)
VFS abstracts different filesystems, file types (device /dev, network, kernel data structure /proc files etc.), handles concurrency issues 

a particular filesystem type may optimise itself for a particular medium, 
e.g. flash/cdrom/magnetic etc.

=======================
<!-- SPDX-License-Identifier: zlib-acknowledgement -->
will work with file descriptors. need to know mode (e.g. read-only), read/write pointer

directory is just another inode; stores name, rec length, file names and inodes

for multiple processes, stdout might not be 1
dup means file descriptors share file pointers
global open file table, in which per process file descriptors point to this table

fs buffer exists in kernel RAM as different speeds (ram and disk) and sizes (app and block size)
an app sends non-uniform block sizes which are then transfered from the kernel buffer in whole block sizes
a write can happen quickly, as don't have to wait for disk controller 
(explicitly flushing with `sync` probably only required for larger writes, e.g. to USB)

(linux has 'raw' devices with no buffering)

inode and directory block writes are prioritised over data blocks, as more critical to system
cache also open disk blocks (may even do read-ahead preloading; LRU cache eviction)

EXT2 inode:
* blocks 
* atime/ctime/mtime 
* uid/gid
* mode 
* reference count (account for hard links; soft links have distinct inode, but share data blocks)
* size (to account for sparse files, size is offset of highest byte written)
       (also, the files blocks may store an indirect block)
* direct blocks (to keep metadata size static, can store max. number of block numbers)
  - 12 direct blocks
  - single (n), double (n^2), triple indirect (n^3), i.e. block numbers to block containing block numbers
  - 4 byte block numbers (so block_size / 4 would give number of block numbers single indirect can store)

Harddrive format:
* boot block (os bootstrap code) 
* equally sized block groups
  - redundant superblock (aid recovery)
  - block group header information, e.g. inode and data bitmaps
  - inode table
  - data blocks
(inodes stored in same location as block groups as often have to interact with both)

File operations occur in stages and are non-atomic
e.g. deleting a file could crash at any stage:
  1. removing directory entry 
  2. marking inode as free
  3. mark disk blocks as free
  IMPORTANT: files still persist, only actually deleted when overwritten with something else 
  IMPORTANT: The steps should be related to what disk blocks are involved, not metadata.

FS journalling layer aims to introduce a degree of atomicity. It keeps track of uncommited changes.
So, for deleting a file, first write deletion steps to journal block. 
Then perform actual deletion steps and remove corresponding journal entries.
On startup, will look at journal to see if any uncompleted steps and finish them if possible

SSDs still have seek time, albeit very small (so sequential still faster than random)

=======================
<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Memory management in RAM or paging to disk

Monoprogramming where entire memory dedicated for one process until it relinquishes control (paging could be added), e.g. mcu

Want to divide memory between processes.
Simple fixed size partitions with processes put into a queue waiting for a partition of appropriate size.
Although internal fragmentation, can be used on an mcu.

Dynamic partition results in external fragmentation that are holes.
IMPORTANT: paging uses static allocation of frames 
Frame allocation is contiguous:
  * first-fit (start linear search from first of memory region)
  * next-fit (start linear search from most recent allocation)
  * best-fit (linear search over entire memory region to find smallest possible allocation)
    (gives small, unusable holes)
  * worst-fit (linear search over entire memory region to find largest possible allocation)

(flexibility incur performance)
1. (compile-time) Compiler generates relocatable code (addresses are offsets to base address)
PIE is default to allow for ASLR security so harder to identify memory layout.
In theory, PIE only necessary for shared libraries to be loaded at any location.
non-PIE would allow compiler to do addresses (readelf -a)
IMPORTANT: if just using this, would require recompiling program every time
2. (load-time) loader binds addresses at run time (ld-linux.so)
IMPORTANT: if just using this, would require reloading program every time
3. (run-time) hw translates to physical addresses.

If want to compact external fragmentation (to make more contiguous space) require relocation of running programs 
(requiring run-time address binding, typically requiring hw support)
1.
  IMPORTANT: this provides a degree of memory isolation and relocation
  * bound/limit register is max. logical address 
  * base/relocation register is offset to add to logical to get physical
  (these are changed on a context switch and relocation/compaction time)
  not suitable for inactive processes, code sharing
2. 
  to handle processes larger than ram, have virtual memory.
  major implementation is paging
  * physical memory divided into page frames
  * virtual memory divided into pages
    address has page number and offset 
  * OS maintains page table mapping
    MMU takes virtual address and communicates to ram with physical address (so, page to frame conversion)
    Has TLB to cache conversions
  (only minimal internal fragmentation in last page)

=======================
<!-- SPDX-License-Identifier: zlib-acknowledgement -->
0th page typically not used as reserved for NULL pointers.
From high addresses to low:  (some address spaces may not be cachable/translated, e.g. ROM, devices; be only kernel accessible)
  - kernel (reserved, protected, shared region)
  - shared libraries
  - stack (grows downwards)
  - bss
  - data
  - text 
  - heap (grows upwards)

MIPS divides memory in separate address spaces (unlike x86 which uses a flat memory model and several segment registers):
  - kseg2 (kernel memory with TLB)
  - kseg1 (512MB; no MMU; no hardware cache, e.g. a write through cache)
  - kseg0 (512MB; no MMU; page modes)
    0x80000000 - 0x9fffffff virtual
    0x00000000 - 0x1fffffff physical  
    kernel + free ram (so, where kmalloc() goes, i.e. allocator already exists here)
    phys = virt - 0x80000000
  - kuseg (2GB)
    load_elf() will call our functions? to determine all regions required?
    do sanity check on region size
    looking at program headers (objdump -p), vaddr, filesz, memsz and flags 
    (IMPORTANT: if filesz different to memsz, zero pad)
    0x0 - 0x7f virtual
    determine physical with our allocator

Larger page sizes bring in more memory so fewer page faults and TLB misses, however greater internal fragmentation

Shared code must appear at same address in all processes

PTE (page table entry) has frame number but also other bits like present/absent, modified, caching (e.g. bypass cache in case of device registers) etc.

IMPORTANT: TLB miss is 3 accesses 

Page fault can be illegal address or page not resident (present bit not set)

Kernel stores page tables (and the frame table) in main memory. 
These are copied to MMU on page fault.
Has TLB to reduce cost of 2 memory accesses for a memory reference
IMPORTANT: Goes to MMU first
IMPORTANT: OS must follow CPU architecture MMU format.

As page table can get large (1 for every process), need compact and fast representation.
page table has 4 byte entries
1-level virtual address has 20bit page number (index into page table), and 12bit offset (added to frame number)
(the 12bit offset means page sizes are 2^12, i.e. 4K)
However, this gives `2^20 * 4`.
2-level has 2-10bit page numbers, so smaller `2^10 * 4 + 2^10 * 4`.
For 64bit addresses, top 16bits are unused. Have 4-level 4-9bit page numbers.

(page->addr/page_size; offset->addr%page_size)
(page table sizes are powers of 2 so:
/ page_size -> >> page_size
% page_size -> &(page_size - 1)

CPU register set on context switches, so MMU knows what process specific page table to use.
For RP3000 would be EntryHi register

IPT (inverted page table) only requires 1 shared table.
A virtual address has page number and offset.
The hash of page number gets entry into HAT (hash anchor table) which gives index into page table.
The PTE have next fields. The index of the match with same PID is used as frame number.
To allow for code sharing, an extension Hashed Page Table stores frame number in table entry (allowing the same frame to have different PTEs)

IMPORTANT: IPT frame number is index in table
HPT stores frame number (allowing different PIDs use same frame)

IPT and HPT are better for sparse virtual addresses as paging would create internal fragmentation.
However, collision lookup may be costly

The TLB (associative cache of PTEs) uses associative/content-addressable-memory (CAM) hardware.
TLB entries indexed by page number.
If TLB miss, need to refill:
  - hardware performs page table lookup and reloads TLB (x86, ARM)
  - or, exception generated and software reloads (MIPS)
TLB entries are process specific. 
TLB entries are tagged with address space id (ASID) (or would have to be flushed on each context switch)
  - EntryHi (page number)
   (VPN(20bits) | ASID(6bits))
  - EntryLo (frame number)
   (PFN(20bits) | no-cache | dirty | valid | global)
c0_Index register indexes a TLB entry.
c0_EntryHi/Lo registers to read/write indexed entry.
Use various TLB specific instructions.

R3000 has special exception handler for kuseg TLB misses. Other TLB misses handled by general exception handler.
Only uses `k0` and `k1` registers, than `tlbwr`
(Amdahls law means should optimise common case; or make more parallel so can be used more etc.)
c0_BadVaddr gives faulting address
c0_EntryHi_VPN page number of faulting address
So, on a TLB miss, only have to translate EntryLo from page table.

Have on-demand paging. So, on a page fault, will have to create page or reload page from disk.
If 'victim' page has no dirty bit (hasn't been written to since it was swapped in), than can cleanly replace?

The number of pages required by a process in a time window is its working set.
Want to keep this resident entire time.

Thrashing is when many processes running (typically on a multicore) constantly triggering page faults and stalling as memory overused.
Handle by suspending a few processes.

VM performace dictated by:
  - page table format
  - page size (ideally would want large for code, small for thread stacks etc.)
  - fetch policy, e.g. on page faults or pre-fetch
  - replacement policy, e.g FIFO, LRU (impossible to implement efficiently, so approximate), 
    Clock (each frame has a used bit; when scanning reset this bit for all entries searched past; replace first page with reset bit not set)
  - resident set size (each process is allowed a variable number of frames)
  - cleaning policy

Larger page sizes would decrease page faults, increase swapping I/O throughput
On-demand paging used as allows more flexibility for end user (they don't have to predict upfront like for pre-paging)

Thrashing is where all processes have high working set memory requiring many page faults/swaps.
Could alleviate by swapping process out.

=======================
<!-- SPDX-License-Identifier: zlib-acknowledgement -->
In a UMA (Uniform Memory Access) architecture, all cores share the same memory access time.
In contrast a NUMA, different cores may have different latencies for certain memory regions.
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

=======================
