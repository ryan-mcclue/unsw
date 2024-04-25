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

IMPORTANT: reading from a 2-level page table takes 2 memory accesses

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
