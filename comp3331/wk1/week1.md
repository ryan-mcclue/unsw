<!-- SPDX-License-Identifier: zlib-acknowledgement -->
## Fundamentals

A POP (point-of-presence) is an artificial communication point between two networks, 
e.g. ISP POP   

In general, if doesn't know address of sorts, perform broadcast/flooding
Note that a signal is unicast or broadcast, however the action of the device might be to flood

IANA (Internet Assigned Numbers Authority) allocates blocks of IPs which ISPs will use.
router networks designed to run as 'autonomous systems'.
they use BGP (border gateway protocol) to exchange routing information
BGP used by routers to decide what they should do with packet on their network
e.g. should I go through path A or path B
so, routers constantly sharing information with other directly connected routers via BGP 
(perhaps updating hop length to a network)

IP addresses can be static or dynamic.
(is from your ISP static?)
(advantages just for security?)

NAT used to extend IPv4 address space by converting from private IPs: 
10.0.0.0 /8, 172.16.0.0 /12, 192.168.0.0 /16

* Hosts: any device that sends or recieves traffic
  - client: initiates
  - server: respond
  - to be connected to the Internet require 4 things 
  (IP, subnet mask (/8, 255.0.0.0), default gateway, resolving DNS server IP)
  when a host first connects to a network it will send out a DHCP discover to get these 4 things (router will typically run this server)
  resolving name server should know how to get to root name server.
  from there, root name server will know where top level domain name servers are, e.g. .com, .org etc.
  from there, authoratative name server, e.g. example.com
  an authoratative name server has resource records for any DNS servers that been delegated to its authority, e.g. eecs.example.com
* IP Address: identifies each host
  - IPv4, 32bits, 4 octets
  - Assigned hierarchically, e.g. Ry, Inc. 10.x.x.x (broken up into hierarchies via subnetting, i.e. subnet of Ry, Inc IP space)
  - 192.0.0.1 /24 means matches on LSB three octets
  - DNS converts domain names for websites and email to IP. Stored in OS host table
* Network: connection of hosts. share IP address space
  - purpose is to share information
  - in reality, a logical grouping of hosts with similar connectivity
  - can have network within another network, i.e. a subnet
* Repeater: regenerates signal so can span large distances as signal decays (do routers have this in them?)
* Hub: multi-port repeater. Everyone recieves everyone's data
* Bridge: sits between two hubs. can contain traffic to one side


* Switch: hub + bridge. facilitates communication within a network
only concerned with MAC (media access control) 
  - Learn: maintain MAC Address Table (mapping of switch ports to MAC addresses)
  - Flood: duplicate frame to all ports 
  - Forward: use MAC address table
dividing switch ports into isolated groups is creating VLANs

* Router: facilitate connection between networks. traffic control point (security, filtering, etc.)
forwards packets not destined for themselves (wheres a host would just drop the packet)
  - maintain knowledge of other networks they know about; a route stored in routing table (10.40.66.0 /24, i.e. a slash 24 route)
  0.0.0.0 /0 is default route, which matches all IPv4 addresses
  packet matching multiple routes will go to more specific route entry
  ∴, a router will have different IP address interfaces it uses to coordinate with various routes
  will also have an ARP table for directly connected routes
    route types (if router doesn't know how to get to IP, it will drop the packet):
    * directly connected
    * static route (directly entered by administrator)
    * dynamic route (routers learning/sharing information via a routing protocol; essentially automatically adding a static route)
  - IP address of router is gateway as it serves as host's way out of network
  a host will have a default gateway, which is a particular interface IP address of a router (router can have multiple interface IP addresses)
  - routers typically deployed in hierarchies, allowing better scaling, faster connections, more robusticity and route summarisation (i.e. reduction of routes through subnetting)


* OSI (just a model to conceptualise, not rigid. e.g. router that has Access Control List will look at L4 header):
  - layer of rules that govern network communication (layered so as each protocol does not have to reimplement network technologies, however can make packet sizes large)
   L1: Physical (transport bits). ethernet, wifi, bluetooth
   L2: Data (hop-to-hop; places and retrieves bits). From one NIC to another NIC
   Each NIC uses MAC addressing scheme, 48bits, 12 hex digits
   Switches also L2 technology
   Every hop, the L2 header of the packet is changed to point to another router's MAC 
   L3: Network (end-to-end). Uses IP addressing scheme. Routers, hosts (anything with an IP address)
   ARP links L3 address to L2 address
   L4: Transport (service-to-service). Distinguish data streams
   Port addressing scheme. TCP, UDP
   Clients will randomly choose port (allows multiple connections to same server), while server will use well known
   L5: (session), L6: (presentation), L7: (application). 
   Merge all into Application. The application can perform these 3 layers in any way it wants.
   FTP, SMTP, HTTPS (HTTP secured with SSL/TLS tunnel)
* Encapsulation: (((data + L4 header)segment + L3 header)packet/datagram + L2 header)frame
i.e. L3 header and its data is known as packet, L2 header and its data is known as frame, etc.
So, a frame is the largest encapsulation
* De-encapsulation: will iteratively strip away headers if matches 
i.e. checks L3 header and sees it matches, so moves up to L2

* Hosts on Same Network:
A host will have a MAC, IP, a subnet mask (identifies size of IP network, e.g. 255.255.255.0, /24), and a default gateway
It will have the destination IP (possibly obtained with DNS or ping)
It will know that the destination is in its own IP network by looking at it's own IP and subnet
However, it does not known destination MAC address
So, it sends out an ARP request saying who has the MAC address of a certain IP.
This ARP request has the reserved MAC address ffff.ffff.ffff which will send to everyone on the network (so all broadcast signals have this)
unicast ARP response will give information to be placed into ARP cache (anything with IP address has an ARP cache)
(Further communication will be quicker as ARP can be bypassed)
* Hosts on Different Network:
Identifies on different network by comparing subnet.
Obtains router's MAC via ARP
Once sending to the router, host's job is done.



IMPORTANT:
  - switching is process of moving data within network
  - routing is process of moving data between networks
  - many network devices exists, yet these are the fundamental operations they could perform

> when sending out ARP requests, how does the signal generation differ based on distance,
e.g. ARP within network, as oppose to ARP made by router to another router? (must be some minimum distance; another reason for having a router)
en extension of this is the difference between a unicast and broadcast signal
------------------------------------------------------------------------------------


• Internet is a complex global infrastructure
• What are the organising principles behind the Internet?
• What really happens when you “browse the Web”?
• What are TCP/IP, DNS, HTTP, NAT, VPNs, 802.11,.... anyway?
• What issue you need to take into consideration to make a
computer network work well?
• What design strategies have proven valuable?
• How do we evaluate network performance?

network speed faster if closer to the ISPs switching network

network edge: hosts/end systems (run networked apps that provide services), 
access network (edge routers connecting to ISPs network core), physical media
network core: packet switching (breaks into packets of header+payload ∴ each packet independent), i.e. routers, switches (imagine an ISP network is interconnected routers)
(as oppose to message switching which will send entire message; more reliable but slower as packet switching allows transmission earlier)
legacy circuit switching dedicates resources (not appropriate for bursty, variable data rate connections on the Internet. furthermore, not as economical as can't allow more users than hardware permits)
main functions:
1. packet forwarding (input to output)
2. packet routing (routing algorithm, i.e. path determination based on header)
we assume store-and-forward switching, i.e. router takes header and payload before transmitting (as oppose to 'cut through switching')
packet switching utilises statistical multiplexing, i.e. educated assumption of bursty traffic (TDM (time) and FDM (frequency))
if queue overloaded, packets go into buffer (transient overload) resulting in a delay
if buffer excedded (persistent overload), packets dropped
as a result, packet switching requires protocols to ensure reliable data transfer and congestion control

performance: loss, delay, throughput 

ISPs like AARNET might publish 'network maps', i.e image showing network connections

so your home network is a type of access network, as well as connection to ISP? (i.e. access network just network to a router that goes to the ISP)
however, you have access ISPs that are interconnected via a global ISP 
(Optus, Telstra, TPG etc. are access networks. IAA (internet association of australia) operate some IX (Internet exchange) points which would be core)
access networks:
* WLAN (wifi?)
* WAN (wide area network; cellular)
* Enterprise networks (mail servers, switches in hardware etc.)

Internet Structure (with IXPs intermingled between some junctions to connect ISPs together):
1. Tier 1 ISP / CDN
2. Regional ISP
3. Access ISP

UNSW ISP is AARNET

When sending time, normally use UTC/GMT(no offset from UTC)/Zulu 

(Abstracting from these, we can have Internet delay, access link delay, LAN delay, etc.)
Delays: 
1. Processing; time to process header and determine where going and place into queue
2. Queueing; time in routing queue to go onto output link (packets_arriving x packet_length / link_bandwidth) 
3. Transmission; time to place entire packet on the wire (packet_length / transmission_rate_10Mbps)
IMPORTANT: At the end of transmission delay, the last bit of the packet is on the wire.
The router will wait for entire packet to arrive, i.e. wait for last bit to arrive
IMPORTANT: Travelling through a router from A-to-B, the first packet transmission delay is times-2, but all others are times-1 due to overlap
4. Propagation; time for bit to cross physical medium
IMPORTANT: As using store and forward switching, transmission and propagation (prop. normally less than trans.) are additive

coaxial cables used in copper transmission lines (inner conductor surrounded by shield).
ethernet twisted pair wires to reduce interference
fibre optic glass carries light

so network core are just ISPs interconnected routers?

the router+modem will go to the headend or central office?

connect end systems to edge routers via access network:
* DSL (phone line). ADSL referring to asynchronous upstream/downstream transmission rates (half-duplex means send or recieve at one time)
* HFC (hybrid fibre coax)
* Fibre optic

IETF and RFC govern a lot of Internet standards

VoIP is just sending voice over IP networks

* network edge includes communication links like fibre optic?
* distinction between a protocol like TCP and a game protocol?
* distinction between WAN/LAN. just size?
what about LPWAN?
* difference between cable headend and central office?
* hierarchy:topology
p2p:(mesh, bus)
client-server:star
So, WAN vs Mesh? (perhaps WAN is another distinction like size? would probably have another like radio technology e.g. cellular/wifi etc.)
* what is net neutrality? (Computerphile, Dr Richard Mortier networking)
* traceroute gaps? why delays decrease as going down?

In practice, end-to-end throughput bottleneck is that which exists in network edge

stochastic means random distribution but may still be analysed with statistics, e.g. stock market graphs

bernoulli trial is binomial experiment whereby probability stays the same across repetitions
binomial question: probability of 'x' successes in 'n' trials?
calculate number of ways to acheive said number and multiply by probability
number of ways is: N choose X

calculate exponent by taking the natural log and moving exponent out

minimum value of quadratic, equate derivative to 0

------------------------------------------------------------------------------------------
$(ping) generates RTT, not end-to-end/latency delay. operates under ICMP (diagnose network issues)
generally just to establish connection

$(traceroute) identify hop locations
exploits TTL field in IP packet header. TTL is decremented each router it passes through, i.e. each hop
most routers are configured to return an ICMP time exceeded message when TTL=0.
some routers are configured to block this ICMP response
sends out UDP
* do all routers have to have publically acessible IP addresses? concept of a private IP?

SSH is a secure protocol on top of TCP 

$(ifconfig) lists network interfaces (software connection to network card, e.g. virbr0, wlp6s0)

$(netstat -i) list interfaces and thier MTU, flags (e.g. promiscious mode, running etc.)
$(netstat -r) displays kernel routing table
* what are 0.0.0.0 and 255.255.255.0

$(netperf) measures throughput

$(dig) ip⟷  host-name by contacting DNS servers 

$(wireshark) captures all link-level (ethernet) frames
