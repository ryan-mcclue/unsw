<!-- SPDX-License-Identifier: zlib-acknowledgement -->

TODO: Search for Quiz in lecture slides

No general 'optimally' sized packet, e.g. large size if error have be resent, link capacities etc.

IMPORTANT: All TCP messages will have an ACK response 
(piggybacking is combining acknowledgement with next outgoing frame)

IMPORTANT: FIN and SYN consume 1 byte, i.e. 1 sequence number

RDT (reliable data transfer) 3.0 is stop-and-wait, ∴ ACKs don't require SEQ numbers

MTU is determined by IP, typically 1500 bytes.
So TCP MSS (Maximum Segment Size) will be 1500 - 20 - 20 = 1460
IMPORTANT: MSS is number of bytes in TCP payload (as oppose to the encompassing header and payload in a TCP segment) 

ACK number indicates next sequence number it's ready for
IMPORTANT: byte number will be -1 sequence number, e.g. seq 100, len 5: bytes from 100-104

TCP reciever employs delayed ACK mechanism to send cumulutive ACKs to reduce bandwidth
(if dropped packets in middle, may send back cumulative ACK, i.e. for multiple packets to avoid resending, however depends on selective-repeat or go-back-n)

NOTE: SEQ and ACK numbers calculated on payload size

Flow control: sender-reciever
Congestion control: sender-network

Recieve window TCP header component is for flow control, 
i.e. to indicate how many bytes reciever is willing to recieve 
(to avoid overrunning host buffer)
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

Window size is how many bytes. To avoid wrap-around issues,
maximum window size is half of sequence number space
IMPORTANT: this is for MAX, so for general, just calculate binary as normal

IMPORTANT: slow-start phase at the beginning of every TCP connection 

Congestion detected with:
  1. Duplicated ACKS (CWDN /= 2)
  2. Timeout (much more serious, i.e. CWDN=1)
Phases of congestion control:
  1. Discovering bandwidth/slow-start (start with CWND low, then increase exponentially until first loss, or RWND or ssthres)
  2. Adjusting to bandwidth/congestion-avoidance (AIMD (additive increase multiplicative decrease, i.e halve on loss) leads to saw-tooth)
  (The various methods by which to update the CWND such as AIAD affect fairness (0.5 + 0.5 = 1) and efficiency (x + y = 1) differently)
  (Therefore, CWND update methodolgy impacts on thoroughput)
  (So, if SSthreshold=6, will double CWND by 2 (1,2,4,8...) each RTT until 6, then start congestion avoidance increasing by 1)
  (A CWND of 1 indicates sending 1xMSS, i.e. 1 packet)

TCP-Tahoe (window set to 1, ssthres. halved always), 
TCP-Reno (most common; window halved on triple duplicate; set to 1 on timeout)

For about to send, consider first sent and retransmission scenarios

TODO: Understand ACK numbers for lost packets
TODO: fast retransmit vs fast recovery?
