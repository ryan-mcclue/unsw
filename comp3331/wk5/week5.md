<!-- SPDX-License-Identifier: zlib-acknowledgement -->

MTU is determined by IP, typically 1500 bytes.
So TCP MSS (Maximum Segment Size) will be 1500 - 20 - 20 = 1460

Piggybacking is combining acknowledgement with next outgoing frame

Recieve window TCP header component is for flow control, i.e. to indicate how many bytes reciever is willing to recieve
This is number of bytes (can be 0) 

handshake agrees upon starting sequence number (random to avoid ambigious connection from same hosts)
