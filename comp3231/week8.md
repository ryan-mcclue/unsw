<!-- SPDX-License-Identifier: zlib-acknowledgement -->
0th page typically not used for NULL pointers.
From high addresses to low:  (some address spaces may not be cachable/translated, e.g. ROM, devices; be only kernel accessible)
  - kernel (reserved, protected, shared region)
  - shared libraries
  - stack (grows downwards)
  - bss
  - data
  - text 
  - heap (grows upwards)

Shared code must appear at same address in all processes

PTE (page table entry) has frame number but also other bits like present/absent, modified, caching (e.g. bypass cache in case of device registers) etc.

Page fault can be illegal address or page not resident (present bit not set)

Kernel stores page tables (and the frame table) in main memory. 
These are copied to MMU on page fault.
Has TLB to reduce cost of 2 memory accesses for a memory reference
IMPORTANT: Goes to MMU first
IMPORTANT: OS must follow CPU architecture MMU format.

As page table can get large (1 for every process), need compact and fast representation.
page table has 4 byte entries
1-level virtual address has 20bit page number (index into page table), and 12bit offset (added to frame number)
However, this gives `2^20 * 4`.
2-level has 2-10bit page numbers, so smaller `2^10 * 4 + 2^10 * 4`.
For 64bit addresses, top 16bits are unused. Have 4-level 4-9bit page numbers.

(page->addr/page_size; offset->addr%page_size)
(page table sizes are powers of 2 so:
/ page_size -> >> page_size
% page_size -> &(page_size - 1)

CPU register set on context switches, so MMU knows what process specific page table to use.

IPT (inverted page table) only requires 1 shared table.
A virtual address has page number and offset.
The hash of page number gets entry into HAT (hash anchor table) which gives index into page table.
The PTE have next fields. The index of the match with same PID is used as frame number.
To allow for code sharing, an extension Hashed Page Table stores frame number in table entry (allowing the same frame to have different PTEs)

The TLB (associative cache of PTEs) uses associative/content-addressable-memory (CAM) hardware.
TLB entries indexed by page number.
If TLB miss:
  - hardware performs page table lookup and reloads TLB (x86, ARM)
  - or, hardware generates exception and OS reloads (MIPS)
TLB entries are process specific. Entries are tagged with address space id (ASID) (or would have to be flushed on each context switch)
