<!-- SPDX-License-Identifier: zlib-acknowledgement -->

NOTE(Ryan): Can do pair programming by attaching to tmux session on same ssh server

TODO(Ryan): Bizarre OS driver faking ethernet header unless in monitor mode?

TODO(Ryan): https://www.quora.com/What-is-the-exact-difference-between-packets-and-datagrams-that-are-used-in-communication-networks

By distinguishing data streams, transport layer provides logical communication between different hosts
Breaks and reassembles segments

NACk only better for data being sent often and with few errors

Handling data from multiple sockets is multiplexing, which is performed by sender 
when it adds Transport header.
Reciever performs demultiplexing by inspecting IP of packet and ports of segment 
(i.e. segment and packet) to know what socket to direct to

TCP/UDP don't provide bandwidth or delay guarantees

connection orientated demultiplexing TCP uses 4-tuple, where UDP only about port 
(hence why TCP is connection based)
(so, these transport protocols differ in their demultiplexing procedures)

UDP simpler, smaller, no handshaking (HTTP3 will use UDP; this is why DNS uses UDP as the process of contacting many name servers would require many handshakes), 
no head-of-line blocking (work when network service compromised)
Have to implement reliability and congestion control on top of

Always refer to transport segments as will contain payload. 
TCP and UDP header contains 16bit ones complement checksum of IP header and itself (can be disabled for UDP in IPv4) that will be checked by reciever

Window size is number of bytes
MTU for loopback is 65535 because packet len is 16bits

Reliably ordered data:
* checksum detects 2-bit errors (is 1's complement of 1's complement sum of all 16-bit words in header) 
will send NACK on corruption
* sequence number to detect duplicates 
(is byte offset within a particular direction, i.e. towards server or client. calculated by adding particular TCP payload size to random ISN)
(acknowledgement number in an ACK mirrors (sequence number + 1)  in that it says I'm good until this byte offset)
(can buffer out of sequence packets)
* ACK on success
selective ACK sends a single ACK for each individual packet 
cumulative ACK (TCP uses) sends a single ACK for a group of packets
* wait on timeout for ACK and retransmit if necessary to handle lost data (also have max. retransmit counters)
(`EstimatedRTT = (1- a)*EstimatedRTT + a*SampleRTT`)
(timeout = `EstimatedRTT + 4*DevRTT`)
(fast retransmit optimisation ignores this timer when it has recieved 3 duplicated ACKs)
* However, performance for stop-and-wait is poor, so implement sliding windows for efficiency 
(pipelining), i.e. send multiple unACK'd packets at once
  - Go-Back-N: So, send 4 packets, if packet 2 errors, retransmit 2,3,4,5 (heuristic based)
  - Selective-Repeat: Only retransmit specific errored packet

duplicate ACKs could be because of high latency
will get duplicate ACKs when say sending 10 packets and packet 2 doesn't make it. 
reciever will send same ACK back for all packets after 2 to indicate it hasn't recieved 2
