<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Memory management in RAM or paging to disk

Monoprogramming where entire memory dedicated for one process until it relinquishes control (paging could be added), e.g. mcu

Want to divide memory between processes.
Simple fixed size partitions with processes put into a queue waiting for a partition of appropriate size.
Although internal fragmentation, can be used on an mcu.

Dynamic partition results in external fragmentation that are holes.
how does handle relocation?
how does handle process memory protection?
First fit scans free list for first entry that fits.
Superceded by virtual memory?
