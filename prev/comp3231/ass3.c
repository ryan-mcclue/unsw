<!-- SPDX-License-Identifier: zlib-acknowledgement -->
// https://wiki.cse.unsw.edu.au/give/Classrun 
//3231 classrun -sturec

// TODO(Ryan): 
// vaddr_t frame_vaddr = alloc_kpage(); (wrapper for alloc_ppage())
// paddr_t frame_paddr = KVADDR_TO_PADDR(frame_vaddr);
// memfill(frame_paddr, 0);
// uint32_t frame_num = frame_paddr & frame_num_mask; (top 20 bits)
// we map the vpn to frame_num in page table
// we store the frame num in entrylo?
// so, actually in kernel memory but irrelevent?

// (alloc_kpages() ensures not in kseg0?)
// (but kmalloc() calls it?)
// or, allocating page table nodes at startup? (2048 and 512 entries)

// frame 0 reserved for NULL?

// ENOMEM for kmalloc() fail

// TODO: ok to preallocate l1 page table entries

// TODO: first 20bits of virtual address become last 20bits of page number

#define PASTE_(a, b) a##b
#define PASTE(a, b) PASTE_(a, b)
#define UNIQUE_NAME(name) PASTE(name, __LINE__)

#define DISABLE_INTERRUPTS() \
  for (struct {int spl; int i;} UNIQUE_NAME(l) = {splhigh(), 0}; \
       UNIQUE_NAME(l).i == 0; \
       splx(UNIQUE_NAME(l).spl), UNIQUE_NAME(l).i++)

#define __SLL_STACK_PUSH(first, node, next) \
(\
  ((node)->next = (first)), \
  ((first) = (node)) \
)
#define SLL_STACK_PUSH(first, node) \
  __SLL_STACK_PUSH(first, node, next)


typedef struct RangeU32 RangeU32;
struct RangeU32
{
  uint32_t min, max;
};

bool 
range_u32_contains(RangeU32 r, uint32_t v)
{ 
  return r.min <= v && v < r.max; 
}

typedef struct L1Page L1Page;
struct L1Page
{
  L1Page *next;
  vaddr_t vpn;
  L2Page *l2_pages;
};

typedef struct L2Page L2Page;
struct L2Page
{
  L2Page *next;
  vaddr_t vpn;
  paddr_t frame;
};

typedef enum
{
  MEM_PERM_R = 1 << 0,
  MEM_PERM_W = 1 << 1,
  MEM_PERM_X = 1 << 2
} MEM_PERM;

typedef struct AddrRegion AddrRegion
struct AddrRegion
{
  RangeU32 range;
  MEMORY_PERM cur_permissions;
  MEMORY_PERM prev_permissions;
};

struct addrspace
{
  L1Page *l1_pages;
  AddrRegion *addr_regions;
  vaddr_t recent_region_end;
};

void vm_bootstrap(void)
{
}

struct addrspace *
as_create(void)
{
	struct addrspace *as = kmalloc(sizeof(struct addrspace));
	if (as == NULL) return NULL;

  as->l1_pages = NULL;
  as->addr_regions = NULL;

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
  as_activate();
}

void as_destroy(struct addrspace *as)
{
  L1Page *l1_page = as->l1_pages;
  while (l1_page != NULL)
  {
    L2Page *l2_page = l1_page->l2_pages;
    while (l2_page != NULL)
    {
      free_kpages(l2->frame_vaddr); 
      L2Page *tmp = l2_page;
      l2_page = l2_page->next;
      kfree(tmp);
    }

    L1Page *tmp = l1_page;
    l1_page = l1_page->next;
    kfree(tmp);
  }

	kfree(as);
}

int as_copy(struct addrspace *old, struct addrspace **ret)
{
	struct addrspace *newas = as_create();
	if (newas==NULL)  return ENOMEM;
  
  for (L1Page *l1_page = as->l1_pages; l1_page != NULL; l1_page = l1_page->next)
  {
    L1Page *l1 = kmalloc(sizeof(L1Page));
    if (l1 == NULL) return ENOMEM;
    l1->next = NULL;
    l1->vpn = l1_page->vpn;

    for (L2Page *l2_page = l1_page->l2_pages; l2_page != NULL; l2_page = l2_page->next)
    {
      L2Page *l2 = kmalloc(sizeof(L2Page));
      if (l2 == NULL) return ENOMEM;
      l2->next = NULL;
      l2->vpn = l2_page->vpn;

      l2->frame_num = new_frame_num;
      memset(new_memory);

      SLL_STACK_PUSH(l1->l2_pages, l2);
    }

    SLL_STACK_PUSH(newas->l1_pages, l1);
  }

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
  AddrRegion *region = kmalloc(sizeof(AddrRegion));
  if (region == NULL) fatal;
  region->range.min = vaddr;
  region->range.max = memsize;
  region->orig_permissions = readable | writeable | executable; 
  region->cur_permissions = region->orig_permissions;
  SLL_STACK_PUSH(as->regions, region);
  
  as->recent_region_end = region->range.max;

  return 0;
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
  if (heap_region == NULL) return ENOMEM;
  heap_region->range.min = as->cur_heap_start;
  heap_region->range.max = USERSTACK - stack_size;
  heap_region->orig_permissions = MEM_PERM_R | MEM_PERM_W | MEM_PERM_X; 
  heap_region->cur_permissions = heap_region->orig_permissions;
  SLL_STACK_PUSH(as->addr_regions, heap_region);

  AddrRegion *stack_region = kmalloc(sizeof(AddrRegion));
  if (stack_region == NULL) return ENOMEM;
  stack_region->range.min = heap_region->range.max;
  stack_region->range.max = USERSTACK;
  stack_region->orig_permissions = MEM_PERM_R | MEM_PERM_W; 
  stack_region->cur_permissions = stack_region->orig_permissions;
  SLL_STACK_PUSH(as->addr_regions, stack_region);

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
      if ((faultcode == VM_FAULT_READ && r->cur_permissions & MEM_PERM_R) ||
          (faultcode == VM_FAULT_WRITE && r->cur_permissions & MEM_PERM_W))
      {
        valid_region = true;
      }
      break;
    }
  }
  // VM_FAULT_READ (attempt read; no tlb entry)
  // VM_FAULT_WRITE (attempt write; no tlb entry)
  // VM_FAULT_READONLY (attempt write on read only; tlb entry has dirty bit 0)
  if (!valid_region || faulttype == VM_FAULT_READONLY)
  {
    return EFAULT;
  }

  uint32_t l1_vpn = faultaddress & L1_MASK;
  L1Page *l1_entry = NULL;
  for (L1Page *l1_page = as->l1_pages; l1_page != NULL; l1_page = l1_page->next)
  {
    if (l1_page->vpn == l1_vpn)
    {
      l1_entry = l1_page;
      break;
    }
  }
  if (l1_entry == NULL)
  {
    l1_entry = kmalloc(sizeof(L1Page));
    if (l1_entry == NULL) return ENOMEM;
    l1_entry->next = NULL;
    l1_entry->vpn = l1_vpn;
    SLL_STACK_PUSH(as->l1_pages, l1_entry);
  }

  uint32_t l2_vpn = vaddr & L2_MASK;
  L2Page *l2_entry = NULL;
  for (L2Page *l2_page = l1_entry->l2_pages; l2_page != NULL; l2_page = l2_page->next)
  {
    if (l2_page->vpn == l2_vpn)
    {
      l2_entry = l2_page;
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
    l2_entry = kmalloc(sizeof(L2Page));
    if (l2_entry == NULL) return ENOMEM;
    l2_entry->vpn = l2_vpn;
    // paddr_t v_page = alloc_kpage();
    // if (v_page == 0) return ENOMEM;
    // vaddr_t p_page = KVADDR_TO_PADDR(v_page);
    // uint32_t frame_num = p_page & TLB_NUM_MASK;
    // l2_entry->frame_num = frame_num;

    // zero frame
    memset(global_first_free_paddr, 0, PAGE_SIZE);

    global_first_free_paddr += PAGE_SIZE;
    SLL_STACK_PUSH(l1_entry->l2_pages, l2_entry);
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

  return 0;
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


