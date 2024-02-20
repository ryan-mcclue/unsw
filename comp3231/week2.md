<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Livelock special form of starvation, in which each thread constantly swapping but making no progress 

Deadlock occurs when one thread with lock attempts to access other lock and other thread is doing the same. Yields cycle
Prevention:
1. Ostrich Algorithm (bury head in sand and ignore)
2. Allocate locks in a hierarchical order.
   So, if A requires 1 it must acquire it before 2. 
   Conversely must release 2 before releasing 1.
3. Detection and Recovery
Create a directed RAG (resource-allocation-graph) with locks and process nodes; look for cycles.
Arrow direction indicates 'wants', i.e. process wants resource

For resources with multiple types, at a point in time have:
* Allocation matrix (resources process has currently)
* Request matrix (resources process requests)
* Resources available
Want to see if there is an order of process execution that can satisfy requests (so, run 1 process and return its resources)

To recover, can forcibly pre-empt/take resource from a process or can kill a process
4. Deadlock Avoidance
Require upfront knowledge of each processes maximum number of resource usage (banker's algorithm rarely used)

Safe state if a scheduling order exists even if each process requests their maximum resources
Unsafe not necessarily a deadlock, just no guarantee
So an avoidance algorithm would only grant requests that result in safe states 

First-come first-serve policy to help prevent starvation
