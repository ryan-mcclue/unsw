<!-- SPDX-License-Identifier: zlib-acknowledgement -->

TODO(Ryan): conversion required with network-byte ordering... Don't have to worry as sending bytes?

TODO(Ryan): Bizarre OS driver faking ethernet header unless in monitor mode?

TODO(Ryan): https://www.quora.com/What-is-the-exact-difference-between-packets-and-datagrams-that-are-used-in-communication-networks

By distinguishing data streams, transport layer provides logical communication between different hosts
Breaks and reassembles segments

Handling data from multiple sockets is multiplexing, which is performed by sender when it adds Transport header.
Reciever performs demultiplexing by inspecting IP of packet and ports of segment (i.e. segment and packet) to know what socket to direct to

TCP/UDP don't provide bandwidth or delay guarantees

connection orientated demultiplexing TCP uses 4-tuple, where UDP only about port (hence why TCP is connection based)
(so, these transport protocols differ in their demultiplexing procedures)

UDP simpler, smaller, no handshaking (HTTP3 will use UDP)
Implement reliability and congestion control
