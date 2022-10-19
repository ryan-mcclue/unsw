<!-- SPDX-License-Identifier: zlib-acknowledgement -->

TODO: Search for Quiz in lecture slides

No general 'optimally' sized packet, e.g. large size if error have be resent, link capacities etc.

IMPORTANT: All TCP messages will have an ACK response (piggybacking is combining acknowledgement with next outgoing frame)

MTU is determined by IP, typically 1500 bytes.
So TCP MSS (Maximum Segment Size) will be 1500 - 20 - 20 = 1460

NOTE: SEQ and ACK numbers calculated on payload size

Recieve window TCP header component is for flow control, i.e. to indicate how many bytes reciever is willing to recieve (to avoid overrunning host buffer)
This is number of bytes (can be 0) 

handshake agrees upon starting sequence number (random to avoid ambigious connection from same hosts)
SYN (synchronise with my ISN) -> SYN+ACK (acknowledge and synchronise with my ISN) -> ACK

Both client and server send FIN bit in message to say no longer sending data
(sending FIN is initiated by `close()`. handling corresponding ACK is what ties up the socket in TIME_WAIT)
RST requires no acknowledgement. It won't send anything and won't recieve anything

During the time SYN+ACK is waiting for ACK, buffers created. So, SYN flood as an attack
However, using TCP SYN cookies, we only create sequence number based off source IP and port.
Therefore, if get valid ACK, we know what its sequence number should be

Congestion control is refering to routers.
Congestion collapse throughput approaches 0 and delays approach infinity
Fix is to limit voluntarily limit sender rate
Network-assisted has routers send bit indicating congestion
End-end congestion (TCP uses) has host infer congestion
  * CWND (congestion window) how many bytes sent to not overflow routers (so sender will use MIN(CWND, RWND))

Congestion detected with:
  1. Duplicated ACKS (CWDN /= 2)
  2. Timeout (much more serious, i.e. CWDN=1)
Phases of congestion control:
  1. Discovering bandwidth/slow-start (start with CWND low, then increase exponentially until first loss, or RWND or ssthres)
  2. Adjusting to bandwidth/congestion-avoidance (AIMD (additive increase multiplicative decrease, i.e halve on loss) leads to saw-tooth)
  (The various methods by which to update the CWND such as AIAD affect fairness (0.5 + 0.5 = 1) and efficiency (x + y = 1) differently)
  (Therefore, CWND update methodolgy impacts on thoroughput)

TCP-Tahoe, TCP-Reno (most common)

IMPORTANT: ssthres. is continually updated.
Furthermore, the slow-start can be repeated

TODO: Understand ACK numbers for lost packets
TODO: fast retransmit vs fast recovery?
