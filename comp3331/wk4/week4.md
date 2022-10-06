<!-- SPDX-License-Identifier: zlib-acknowledgement -->

NOTE(Ryan): Can do pair programming by attaching to tmux session on same ssh server

TODO(Ryan): Bizarre OS driver faking ethernet header unless in monitor mode?

TODO(Ryan): https://www.quora.com/What-is-the-exact-difference-between-packets-and-datagrams-that-are-used-in-communication-networks

By distinguishing data streams, transport layer provides logical communication between different hosts
Breaks and reassembles segments

Handling data from multiple sockets is multiplexing, which is performed by sender when it adds Transport header.
Reciever performs demultiplexing by inspecting IP of packet and ports of segment (i.e. segment and packet) to know what socket to direct to

TCP/UDP don't provide bandwidth or delay guarantees

connection orientated demultiplexing TCP uses 4-tuple, where UDP only about port (hence why TCP is connection based)
(so, these transport protocols differ in their demultiplexing procedures)

UDP simpler, smaller, no handshaking (HTTP3 will use UDP), no head-of-line blocking (work when network service compromised)
Implement reliability and congestion control

Always refer to transport segments as will contain payload. 
TCP and UDP header contains 16bit ones complement checksum of IP header and itself (can be disabled for UDP in IPv4) that will be checked by reciever

Reliably ordered data:
* checksum detects bit errors
* sequence number to detect duplicates (just 0 and 1, i.e. reciever waiting for 0, then waiting for 1)
* ACK on success, ACK with same sequence number on errors (so send and wait?)
* wait on timeout for ACK and retransmit if necessary to handle lost data
However, performance for stop-and-wait is poor, so implement pipelining (sliding windows for efficiency), i.e. send multiple unACK'd packets at once
Go-Back-N (cumulative): So, send 4 packets, if packet 2 errors, retransmit 2,3,4,5
Selective-Repeat (selective): Only retransmit specific errored packet
