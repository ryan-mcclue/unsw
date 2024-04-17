<!-- SPDX-License-Identifier: zlib-acknowledgement -->
An AddressRegion is a linked list node that contains a min,max exclusive address range and 
memory permissions for that range.
A L2Page is a linked list node of level 2 page table entries.
It contains the physical address of the frame for a particular page and it's 
9bit virtual page number for lookup.
A L1Page is a linked list node of level 1 page table entries containing a linked list 
of L2Pages and its 11bit virtual page number for lookup.
AddressRegion and page structures are linked lists to allow for simple lazy allocation 
to not result in large internal fragmentation.
The AddressRegion and L1Page linked lists are added to the per-process addrspace struct 
so page tables are per-process.

vm_fault() is invoked on a TLB miss or an attempt to write to a readonly TLB entry.
It's primary purpose is to translate a virtual address into a physical address.

It gracefully handles processes trying to access invalid address regions, 
e.g. kernel addresses, undefined regions etc.
This adds system robustness in that a process won't crash the kernel on an invalid access
and also provides security in that processes can't access kernel memory.

Next, it walks the page table to find a matching entry for the faultaddress.
It's copied to the TLB if it exists.
This implements cache locality for the fast but small TLB content-addressable memory.

If no entry is found, a page and it's associated frame are lazily allocated.
This means a page only occupies memory if read/written to.
This allows a process to allocate large amounts of memory, but only consume 
what it actually uses.

Overall, these additions to vm_fault() improve security, address translation performance 
and system memory conservation.
