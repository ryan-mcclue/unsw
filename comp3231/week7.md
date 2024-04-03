<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Memory management in RAM or paging to disk

Monoprogramming where entire memory dedicated for one process until it relinquishes control (paging could be added), e.g. mcu

Want to divide memory between processes.
Simple fixed size partitions with processes put into a queue waiting for a partition of appropriate size.
Although internal fragmentation, can be used on an mcu.

Dynamic partition results in external fragmentation that are holes.
Allocation is contiguous:
  * first-fit (start linear search from first of memory region)
  * next-fit (start linear search from most recent allocation)
  * best-fit (start bidirectional search from most recent allocation)
  * worst-fit 

(flexibility incur performance)
1. (compile-time) Compiler generates relocatable code (addresses are offsets to base address)
PIE is default to allow for ASLR security so harder to identify memory layout.
In theory, PIE only necessary for shared libraries to be loaded at any location.
non-PIE would allow compiler to do addresses (readelf -a)
2. (load-time) loader binds addresses at run time (ld-linux.so)
3. (run-time) hw translates to physical addresses.

If want to compact external fragmentation (to make more contiguous space) require relocation of running programs, typically requiring hw support
1.
  * bound/limit register is max. logical address 
  * base/relocation register is offset to add to logical to get physical
  (these are changed on a context switch and relocation/compaction time)
  provides a degree of memory isolation and relocation.
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
