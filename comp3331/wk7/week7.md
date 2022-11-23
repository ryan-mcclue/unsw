<!-- SPDX-License-Identifier: zlib-acknowledgement -->

IMPORTANT: TCP segment in lectures means just data bytes (going against convention....)

IMPORTANT: technically when a router recieves packet it will first perform forwarding,
however to complete forwarding, must perform routing:
* routers route (determine end-to-end path taken; routing algorithm; control plane) and then
* forward (determine from input link to what output link; forwarding table; data plane)

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

Subnet contains devices that can communicate with each other with no router?
Subnet part is higher-order bits, host part lower-order
/24 == 255.255.255.0
not assigned to any host are:
* broadcast address has all host bits as 1, e.g. .255
* network address has all host bits as 0, e.g. .0

Network classes:
* A (8 bit net-id)
* B (16 bit net-id)
* C (24 bit net-id)

Subnetting is process of dividing networks into more fine-grained sizes 
(than what the standard network classes allow)
Gives net-id, subnet-id and host-id (the subnet-id bits are taken from the host-id bits)
Allows for heirarchical structure, therefore more efficient routing

Router can be attached to various subnets (DHCP request/offer/accept/ack)

CIDR (classless interdomain routing) have network/subnet part and host part each of 
(arbitrary length dictates use of subnet masks)
Will recursively break down chunks as get closer to host, e.g. 12.0.0.0/8 -> 12.0.0.0/16 etc 

IPs geographical, e.g. ICANN -> APNIC -> Telstra -> UNSW -> CSE -> host

Host may get IP from DHCP (which itself could be dynamically or statically allocated) or /etc/rc.config 
Network get IP from block of IPs allocated to ISP

NAT addresses cannot be routed
All devices on network share one public IPv4 address
Requires NAT router to maintain NAT translation table to replace outgoing and incoming datagrams to appropriate sources
(∴ IP checksum must be recalculated)
IMPORTANT: Some legacy protocols embed port number payload, so NAT would have to translate these
IMPORTANT: NAT no issues if acting as client
If server behind a NAT:
1. Statically configure NAT to forward based on port number
2. UPnP (Universal Plug and Play; protocols that allow devices to discover each other's presence on network) 
   IGN (Internet Gateway Device) automates NAT port configuration with lease times   
3. Client communicates with a relay server (what Skype uses) that then communicates to the NAT server 

As TCP is stream orientated, will automatically handle size larger than MTU for us

* On refragmentation, will next router wait for all fragments to be recieved and re-assembled 
before sending to next hop?
* Network classes obselete, they why mentioned in questions?
* I suppose ethernet heavily used due to lack of range of radio?
