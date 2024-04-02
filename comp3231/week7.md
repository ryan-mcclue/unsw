<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Memory management in RAM or paging to disk

Monoprogramming where entire memory dedicated for one process until it relinquishes control (paging could be added), e.g. mcu

Want to divide memory between processes.
Simple fixed size partitions with processes put into a queue waiting for a partition of appropriate size.
Although internal fragmentation, can be used on an mcu.

Dynamic partition results in external fragmentation that are holes.
First fit scans free list for first entry that fits.

If want to compact external fragmentation require relocation of running programs, typically requiring hw support
Compiler generates relocatable code, loader binds addresses at run time, hw translates to physical addresses.
1.
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
