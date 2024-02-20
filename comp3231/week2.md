<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Deadlock

Deadlock occurs when one thread with lock attempts to access other lock and other thread is doing the same

Livelock special form of starvation, in which each thread constantly swapping but making no progress 
(can fix starvation with a first-come first-serve policy)

Feasible ways of preventing:
1. Ostrich Algorithm (ignore)
2. Removing  'hold-and-wait' condition
Allocate locks in a hierarchy/order.
So, if A requires 1 it must acquire it before 2. 
Likewise must release 2 before releasing 1.
3. Detection and Recovery
Create a directed RAG (resource-allocation-graph) with locks and process nodes; look for cycles.

For resources with multiple types, require additional:

have this for a point in time, i.e. thread has this many locks and requests this many locks; are we in a deadlock?

4. Deadlock Avoidance
Require upfront knowledge of maximum number of each resources (banker's algorithm rarely used)

* Claim matrix (fixed for each process): for each process, max. number resources required at any given time 
* Allocation matrix (changes as system executes): for each process, how many resources currently has
* Resource vector (fixed for the system)

We execute a process, add its used resources back to available and do another. 
If can run all processes, no deadlock

resources available (request matrix) = resources that exist


Safe state if there exists a scheduling order that results in every process running
to completion, even if they all request their maximum resources
immediately
TODO: safe and unsafe states
Unsafe not necessarily a deadlock, just no guarantee
So an avoidance algorithm would only grant requests that result in safe states 

have max. resources available for system and each thread has max. resources required
