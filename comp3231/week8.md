<!-- SPDX-License-Identifier: zlib-acknowledgement -->
0th page typically not used for NULL pointers.
From high addresses to low: 
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

Kernel stores page tables in main memory. 
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

IPT (inverted page table) only requires 1 shared table.
A virtual address has page number and offset.
The hash of page number gets entry into HAT (hash anchor table) which gives index into page table.
The PTE have next fields. The index of the match with same PID is used as frame number.
To allow for code sharing, an extension Hashed Page Table stores frame number in table entry (allowing the same frame to have different PTEs)
