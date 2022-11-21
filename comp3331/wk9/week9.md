<!-- SPDX-License-Identifier: zlib-acknowledgement -->

IMPORTANT: MAC is about accessing the physical channel, wire or wireless

link layer technology underpin LANs, as devices in a LAN will typically share same channel, e.g. 6 node LAN

link layer occurences localised to subnet

link layer connect adajacent nodes via wireless (ethernet) or wired (WiFi, 4G, satellite) via framing (adding header and trailer bytes)

each link protocol provides different services, e.g. ethernet low bit error link so reliability typically only used in WiFi
(half-duplex, error detection, error correction, flow control, etc.)
TODO(Ryan): Why both link-level and end-end reliability (some form of bit checking in UDP/IP/Ethernet)?
(is it because to say transport checksum only on its headers, so not all encompassing?)

IMPORTANT: bandwidth is for channel, rate is for node

link layer implemented by NIC

parity bits (even or odd number of 1s) form of error detection in link layer (as oppose to checksums used by higher layers)
in practice bit errors in bursts, so parity not that useful.
(the parity bit set is determined if using say either a even or odd parity protocol)
∴, CRC is widely used (which performs a more computational intensive operation, i.e. division and check if remainder is 0)

IMPORTANT: CRC can't provide error correction (rather error detection)

wireless is broadcast (share medium/link)
ethernet can be point-to-point or broadcast, i.e. bus or switched (this is most common today)

broadcast implies multiple access-network, meaning nodes could simultaneously transmit can cause a collision
so, multiple access protocols exist to determine how to best share channel (part of link layer protocol)
various categories:
* Channel Partitioning (divide into slots. not decentralised):
share channel efficiently at high load
  - TDMA (each node gets fixed length slot dependent on transmission time)
  - FDMA (slots divided into frequency bands)
* Random Access (collisions allowed, recover from them. with a collision, entire packet transmission time wasted): 
share channel efficiently at low load
  - ALOHA (transmit at full channel data rate). very poor efficiency
  - CSMA (carrier sense multiple access). listen before transmitting (collision still occur due to delays)
  - CSMA/CD (collision detection). if detects another transmission while sending, abort. good efficiency
  (ethernet, WiFi)
* Taking Turns (nodes with more to send take longer turns):
  - Polling (captain node invites other nodes to transmit in turn) 
  - Token passing (central token passed sequentially to nodes)
  (bluetooth, fddi (fibre optic LAN))

48bit MAC a.k.a LAN address
IEEE allocates MAC addresses. NIC manufacturer buys portion of MAC addresses
Hardcoded and not hierarchical like IP

Hosts will have ARP table. Possible for ARP poisoning, however have to be on same network (how does Uni prevent against this?)

Ethernet byte layout:
  * preamble (synchronise reciever/sender rates)
  * type (indicates higher level protocol to allow for demultiplexing)
unreliable (no ACKs), connectionless

Switch is link-layer device (store-forward also). 
Allows for no collisions, full-duplex connections (this is where the concept of output links become more apparent)
Has switching table
Is self-learning (i.e. no explicit routing protocol) by flooding and recording
By sending spoofed MAC source addresses, could slow down network by overflowing switching table and requiring more broadcasts
