<!-- SPDX-License-Identifier: zlib-acknowledgement -->
# https://wiki.cse.unsw.edu.au/give/Classrun 
3231 classrun -sturec

```
http://jhshi.me/2012/04/24/os161-user-address-space/index.html
as_create()
{
  address ranges 
  10,10,12
}
struct addrspace
{
  heap_start;
  heap_end;
  stack_start;
  stack_end;
  Page pages;
}

struct Page
{
  state (dirty, i.e. it doesn't have copy in swap?; fixed, i.e. don't swap this out)
};

http://jhshi.me/2012/04/27/os161-tlb-miss-and-page-fault/index.html
vm_fault(int faulttype, vaddr_t faultaddress)
{
  switch (faulttype)
  {
VM_FAULT_READ (attempt read; no tlb entry)
VM_FAULT_WRITE (attempt write; no tlb entry)
VM_FAULT_READONLY (tlb entry has dirty bit 0)
  }

  // check if address is valid, e.g. not NULL, not in kernel memory, i.e in useg   
  if (!address_valid_range(faultaddress)) proc_getas()
   (code, data, heap, stack)
    return EFAULT;??
    kill_process?

  if (!address_backed(faultaddress))
  (search page table looking for PTE_P bit)
  {
    back_address(faultaddress);
    // zero page
  }

  fill_tlb(faultaddress);
  // int s = splhigh();
  // tlb_random()
  // splx(s);

	/* make sure it's page-aligned */
	// KASSERT((paddr & PAGE_FRAME) == paddr);

  // IMPORTANT: we can just flush TLB on a context switch
}


allocate our structures (this address range should be marked as fixed?)
IMPORTANT: don't have to consider paging?
paddr_t mem_size = ram_getsize();

init will mark address ranges, e.g. stack in useg

as_activate() flushes TLB, and fills with current process?


as_prepare_load()
```

IMPORTANT: use ass2 sys.conf and .gitignore

R3000 Reference Manual and Hardware Guide on the course website.

TLB miss if not matching found with a valid bit (or global bit and no matching ASID) 
For this assignment, you may largely ignore the ASID field and set it to zero in your TLB entries

OS/161 kernel [? for menu]: p /bin/true
Running program /bin/true failed: Function not implemented
(implement as_* functions)

struct addrspace
kern/vm/addrspace.c
kern/vm/vm.c

as_create() should initialise your page table, as_destroy() should clean it up.

allocate pages in vm_fault()
IMPORTANT: vm_fault() should insert, lookup, and update page table entries in your page table structure.
Note: Your implementation of TLB refill in vm_fault() should use tlb_random().
Implement the functions in kern/vm/addrspace.c that are required for basic functionality (e.g. as_create(), as_prepare_load(), etc.)

Note: Interrupts should be disabled when writing to the TLB, see dumbvm for an example. Otherwise, unexpected concurrency issues can occur.
as_activate() and as_deactivate() can be copied from dumbvm.

TODO: if ASID set to 0 then uniprocess? how does global bit handle process specific page tables?

Note: You may use a fixed-size stack region (say 16 pages) for each process.
extend OS/161 address spaces with a page table, 
and implement a TLB refill handler for the page table.

lazy allocate page table entries

2-level hierarchical.
11-9bits

Note: Applications expect pages to contain zeros when first used. 
This implies that newly allocated frames that are used to back pages should be zero-filled prior to mapping

To test this assignment, you should run a process that requires more virtual memory than the TLB can map at any one time. 
You should also ensure that touching memory not in a valid region will raise an exception. 
The huge and faulter tests in testbin may be useful. See the Wiki for more options.

Apart from GDB, you may also find the trace161 command useful. trace161 will run the simulator with tracing, for example
% trace161 -t t -f outfile kernel
IMPORTANT: don't use kprintf in TLB as context switches!
will record all TLB accesses in outfile.

(dirty/valid bit)
rwx = DV
rw- = DV
r-x = -V
r-- = -V
-wx = DV
-w- = DV
--x = -V
--- = --
