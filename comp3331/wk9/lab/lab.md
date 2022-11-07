<!-- SPDX-License-Identifier: zlib-acknowledgement -->

# Lab 06 - Ryan McClue (z5346008)

## 1. Setting up NS2 simulation for measuring TCP throughput
1. *Why the throughput achieved by flow tcp2 is higher than tcp1 between 
time span 6 sec to 8 sec?*
As it's competing with more connections 

2. *Why the throughput for flow tcp1 is fluctuating between time span 0.5 sec to 2 sec?*
No other competing flows, so in the slow-start phase

3. *Why is the maximum throughput achieved by anyone flow capped at around 1.5Mbps?*
2.5Mbps maximum, but 2 connections so max 1.25Mbps. However, this fluctuates, so 1.5Mbps


## 2. Understanding IP Fragmentation

1. *Which data size has caused fragmentation and why?* 

*Which host/router has fragmented the original datagram?* 
*How many fragments have been created when the data size is specified as 2000?*

2. Did the reply from the destination 8.8.8.8. for 3500-byte data size also get fragmented? Why or why not?

3. Give the ID, length, flag and offset values for all the fragments of the first packet sent by 192.168.1.103 with a data size of 3500 bytes?

4. Has fragmentation of fragments occurred when data of size 3500 bytes has been used? Why or why not?

5. What will happen if for our example one fragment of the original datagram from 192.168.1.103 is lost? 

1. 2000, 3500 (larger than MTU)
host `192.168.1.103` fragments
2 fragments
(2000 - 80)

2. yes, > 1500

3. ID is same, offset different
first one with 3 sending (have to inspect 3rd closely)

4. 5 links (each link has different MTU, so fragmentation of fragments possible)
No (all of them meet requirement of further links)

5. retransmit all fragments
(this just design of IP)

## 3. Understanding the Impact of Network Dynamics on Routing 
1. *Which nodes communicate with which other nodes?* 
from file
*Which route do the packets follow?* 
0-1-4-5
0-1-4
2-3-1
2-3
*Does it change over time?*
No 

2. *What happens at time 1.0 and at time 1.2?* 
node 1-4 link goes down?
*Does the route between the communicating nodes change as a result of that?*
no, just gets dropped by 1

3. *Did you observe any additional traffic as compared to Step 3 above?* 
Notice a lot of smaller packets being transferred. These are routing protocol information?
*How does the network react to the changes that take place at time 1.0 and time 1.2 now?*
Packets travel from 1-2-3-5 instead of being dropped

4. *How does this change affect the routing? Explain why.*
packets intended for 5, go through 0-1-2-3-5 instead of original 0-1-4-5
this is because cost of path increased and reflected by using dynamic routing to find a better route
more routing information exchanged throughout not tjust start

5. *Describe what happens and deduce the effect of the line you just uncommented.*
packets from 2-3-5 are also being routed via 2-1-4-5
we have increased the cost of connection and allowed for bidrectional communication
so, sends in multiple directions to make most efficient cumulative transfer
taking into account transmission delay on various output links
