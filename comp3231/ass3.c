<!-- SPDX-License-Identifier: zlib-acknowledgement -->
// https://wiki.cse.unsw.edu.au/give/Classrun 
//3231 classrun -sturec

struct L1Node
{
  L1Node *next;
  vaddr_t vpn;
  L2Node *first;
};

struct L2Node
{
  L2Node *next;
  vaddr_t vpn;
}

paddr_t global_last_paddr;
paddr_t global_first_free_paddr;
void vm_bootstrap(void)
{
  // NOTE(Ryan): kuseg after kseg0 in physical memory
  global_first_free_paddr = MIPS_KSEG1 - MIPS_KSEG0;
  global_last_paddr = ram_getsize();

  KASSERT((global_first_paddr & PAGE_FRAME) == global_first_paddr);
  KASSERT((global_last_paddr & PAGE_FRAME) == global_last_paddr);
}

struct addrspace
{
  L1Node *first;
};

struct addrspace *
as_create(void)
{
	struct addrspace *as = kmalloc(sizeof(struct addrspace));
	if (as == NULL) return NULL;

	return as;
}

void as_activate(void)
{
	struct addrspace *as = proc_getas();
	if (as == NULL) return;

  DISABLE_INTERRUPTS()
  {
	  for (int i = 0; i < NUM_TLB; i++)
    {
      // entryhi, entrylo, index
      // NOTE(Ryan): Invalidate all entries in TLB
	  	tlb_write(TLBHI_INVALID(i), TLBLO_INVALID(), i);
	  }
  }
}

#define L1_BITS 11
#define L1_SHIFT (sizeof(vaddr_t) - L1_BITS)
#define L1_MASK (((1 << L1_BITS) - 1) << L1_SHIFT

#define L2_BITS 9 
#define L2_SHIFT (L1_SHIFT - L2_BITS) 
#define L2_MASK ((1 << L2_BITS) - 1) << L2_SHIFT

int as_define_region(struct addrspace *as, vaddr_t vaddr, size_t memsize,
		                 int readable, int writeable, int executable)
{
// TODO: just setting up region permissions?
  size_t aligned_memsize = ALIGN_POW2_UP(memsize, PAGE_SIZE)
  size_t num_pages = aligned_memsize / PAGE_SIZE;

  uint32_t l1_vpn = vaddr & L1_MASK;

  L1Node *l1_entry = NULL;
  for (L1Node *l1_node = as->first; l1_node != NULL; l1_node = l1_node->next)
  {
    if (l1_node->vpn == l1_vpn)
    {
      l1_entry = l1_node;
      break;
    }
  }
  if (l1_entry == NULL)
  {
    l1_entry = kmalloc(sizeof(L1Node));
    l1_entry->vpn = l1_vpn;
    PUSH(as->first, l1_entry);
  }

  uint32_t l2_vpn = vaddr & L2_MASK;
  L2Node *l2_entry = NULL;
  for (L2Node *l2_node = l1_entry->first; l2_node != NULL; l2_node = l2_node->next)
  {
    if (l2_node->vpn == l2_vpn)
    {
      l2_entry = l2_node;
      break;
    }
  }
  if (l2_entry == NULL)
  {
    if (global_first_free_paddr + PAGE_SIZE > global_last_paddr)
      exception
    l2_entry = kmalloc(sizeof(L2Node));
    l2_entry->vpn = l2_vpn;
    l2_entry->frame = global_first_free_paddr;
    global_first_free_paddr += PAGE_SIZE;
    PUSH(l1_entryfirst, l2_entry);
  }
  

  vaddr_t base = vaddr;
  vaddr_t base_opl = base + aligned_memsize;

  map_pages(as);

	return ENOSYS; /* Unimplemented */
}


loadexec() -> as_create(),as_activate() 
  -> load_elf() -> as_define_region(),as_prepare_load(),as_complete_load()
-> as_define_stack()

kern/arch/mips/include/tlb.h

entryhi
base-virtualaddress-for-page...
entrylo
base-physicaladdress-for-frame...

TODO: if out of memory when allocating new page, just die?
struct trapframe *tf = curthread->t_context;
tf->tf_cause = EX_ADEL; // Set cause register to indicate Address Error
mips_trap(tf); // Trigger exception

kmalloc() on kernel heap so bypasses TLB?

as_copy() will create same number of frames and copy data over into it.

IMPORTANT: Dirty flag in TLB effectively means writable

```
http://jhshi.me/2012/04/24/os161-user-address-space/index.html
as_create()
{
  address ranges 
  10,10,12
}
kernel allocator allocates from 0x00000000 - 0x1fffffff physical  
struct addrspace (region and accessibility, e.g. kernel or usermode?)
{
  heap_start;
  heap_end;
  stack_start = top;
  stack_end = top - stack_size;
  Page pages;
}

specify regions, i.e. address ranges
 as_define_stack()
• as_define_region()
– usually implemented as a linked list
of region specifications
• as_prepare_load()
– make READONLY regions
READWRITE for loading
purposes
• as_complete_load()
– enforce READONLY again

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
  (break address into l1,l2 page table entries)
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

init will mark address ranges, e.g. stack in useg

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


