<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Autonomous System (AS)/domain is a region of network under one authority, i.e. network of routers 
Connecting ASs will be border routers

Internet routing two levels:
1. Intra-domain protocols, e.g. link state OSPF, distance vector RIP
2. Inter-domain protocols, e.g. path vector BGP 

Routing algorithms balance static/dynamic (e.g how frequently routes update) 
and global/decentralised (are routes known beforehand or iteratively determined) 

Djikstra's link state algorithm: (centralised; each router implement algorithm on their own)
* link state is directly attached links and costs
* each node floods neighbour with link states which will then forward it on to its neighbours (more bandwidth)
* eventually all nodes learn entire network topology, i.e. via link state broadcast
* converges fast
IMPORTANT: O(n²) messages sent; may have oscillations; slower error propagation 
Implementations: OSPF, IS-IS

Bellman-Ford distance vector algorithm: (decentralised; iterative; takes time for information to propagate)
* from time to time, each node sends out its own distance vector estimate to neighbours   
* under natural conditions, estimate converges to actual least cost
* issues arise with slow convergence (good news fast, bad news slow)
* node's don't know entire network topology
Poisoned Reverse rule is a heuristic to avoid count-to-infinity
(B routes via C to A, tells C its distance to A is ∞ to avoid routing A through B)
IMPORTANT: only send messages to neighbours; convergence time varies, may have routing loops;
Implementations: RIP, IGRP-Cisco, BGP 
TODO: Does dynamic programming mean value is converged on?

ICMP used by hosts and routers to communicate network information (not reachable, TTL expired, etc.)
Not TCP or UDP, only 8 bytes of IP payload
