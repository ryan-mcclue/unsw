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
