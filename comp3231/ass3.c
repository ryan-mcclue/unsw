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
  RangeU32 *regions;
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

void as_deactive(void)
{
  // nothing? maybe just do same as as_activate()?
}

void as_destroy(struct addrspace *as)
{
  // TODO: cleanup linked lists

	kfree(as);
}

int as_copy(struct addrspace *old, struct addrspace **ret)
{
	struct addrspace *newas = as_create();
	if (newas==NULL)  return ENOMEM;

// as_copy() will create same number of frames and copy data over into it.
	/*
	 * Write this.
	 */

	(void)old;

	*ret = newas;

	return 0;
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
  size_t aligned_memsize = ALIGN_POW2_UP(memsize, PAGE_SIZE)

  AddrRegion *region = kmalloc(sizeof(AddrRegion));
  if (region == NULL) fatal;
  region->range.min = vaddr;
  region->range.max = aligned_memsize;
  region->orig_permissions = readable | writeable | executable; 
  region->cur_permissions = region->orig_permissions;
  PUSH(as, region);
  
  as->heap_start;
  
	return ENOSYS; /* Unimplemented */
}

int as_prepare_load(struct addrspace *as)
{
  for (AddrRegion *addr_region = as->regions;)
  {
    if (addr_region->cur_permissions & READONLY)
      addr_region->cur_permissions &= ~READONLY;
  }
	return 0;
}

int as_complete_load(struct addrspace *as)
{
  for (AddrRegion *addr_region = as->regions;)
    addr_region->cur_permissions = addr_region->orig_permissions;

	return 0;
}

int as_define_stack(struct addrspace *as, vaddr_t *stackptr)
{
  size_t stack_size = PAGE_SIZE * 16;

  // heap is after last region
  AddrRegion *heap_region = kmalloc(sizeof(AddrRegion));
  if (region == NULL) fatal;
  region->range.min = as->cur_heap_start;
  region->range.max = USERSTACK - stack_size;
  region->orig_permissions = readable | writeable | executable; 
  region->cur_permissions = region->orig_permissions;
  PUSH(as, region);

  AddrRegion *region = kmalloc(sizeof(AddrRegion));
  if (region == NULL) fatal;
  region->range.min = heap_region->range.max;
  region->range.max = USERSTACK;
  region->orig_permissions = readable | writeable; 
  region->cur_permissions = region->orig_permissions;
  PUSH(as, region);

	*stackptr = USERSTACK;

	return 0;
}



loadexec() -> as_create(),as_activate() 
  -> load_elf() -> as_define_region(),as_prepare_load(),as_complete_load()
-> as_define_stack()

kern/arch/mips/include/tlb.h

// http://jhshi.me/2012/04/27/os161-tlb-miss-and-page-fault/index.html
#define TLB_NUM_BITS 20
#define TLB_NUM_MASK (((1 << TLB_NUM_BITS) - 1) << (sizeof(uint32_t) - TLB_NUM_BITS))
int
vm_fault(int faulttype, vaddr_t faultaddress)
{
  struct addrspace *as = proc_getas();
  bool valid_region = false;
  for (AddrRegion *r = as->regions; r != NULL; r = r->next)
  {
    if (range_u32_contains(r->range, faultaddress))
    {
      if ((faultcode == VM_FAULT_READ && r->cur_permissions & READ_PERMISSION) ||
          (faultcode == VM_FAULT_WRITE && r->cur_permissions & WRITE_PERMISSION))
      {
        valid_region = true;
      }
      break;
    }
  }
  // VM_FAULT_READ (attempt read; no tlb entry)
  // VM_FAULT_WRITE (attempt write; no tlb entry)
  // attempt write on read only; tlb entry has dirty bit 0
  if (!valid_region || faulttype == VM_FAULT_READONLY)
  {
    struct trapframe *tf = curthread->t_context;
    kill_curthread(tf->tf_epc, EX_ADEL, faultaddress);
  }

  uint32_t l1_vpn = faultaddress & L1_MASK;
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
    {
      struct trapframe *tf = curthread->t_context;
      kill_curthread(tf->tf_epc, EX_IBE, faultaddress);
    }
    l2_entry = kmalloc(sizeof(L2Node));
    l2_entry->vpn = l2_vpn;
    l2_entry->frame = global_first_free_paddr;

    // zero frame
    memset(global_first_free_paddr, 0, PAGE_SIZE);

    global_first_free_paddr += PAGE_SIZE;
    PUSH(l1_entryfirst, l2_entry);
  }

  DISABLE_INTERRUPTS()
  {
    // we can ignore ASID
    uint32_t hi = faultaddress & TLB_NUM_MASK;

    uint32_t lo = l2_entry->frame & TLB_NUM_MASK;
    if (active_region->cur_permissions & WRITE_PERMISSION)
      lo |= (1 << DIRTY_BIT);
    // always valid
    lo |= (1 << VALID_BIT);

    tlb_random(hi, lo);
  }

  return EFAULT;
}



allocate our structures (this address range should be marked as fixed?)
IMPORTANT: don't have to consider paging?

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


