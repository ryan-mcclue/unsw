<!-- SPDX-License-Identifier: zlib-acknowledgement -->

IMPORTANT: TCP segment in lectures means just data bytes (going against convention....)

routers route (determine end-to-end path taken; routing algorithm; control plane) and then
forward (determine from input link to what output link; forwarding table; data plane)

control plane approaches: 
1. per-router (traditional)
2. software-defined networking (on remote server)

'best effort' service model, i.e. datagrams lost, out-of-order, etc. successful
due to 'bursty/elastic' nature of traffic

routing protocols are for routers to exchange information, e.g BGP
ICMP protocol for reporting errors

IP packet format has version number, header length, total length, checksum,
TTL, fragmentation (different links have different MTUs), 
fragmentation-flags (MF-more-fragmentation, NF-no-fragmentation:in this case, could get ICMP telling us MTU),
higher-level protocol? etc. 

* On refragmentation, will next router wait for all fragments to be recieved and re-assembled 
before sending to next hop?
