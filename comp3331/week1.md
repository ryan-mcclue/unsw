<!-- SPDX-License-Identifier: zlib-acknowledgement -->
• Internet is a complex global infrastructure
• What are the organising principles behind the Internet?
• What really happens when you “browse the Web”?
• What are TCP/IP, DNS, HTTP, NAT, VPNs, 802.11,.... anyway? (define format and order)
• What issue you need to take into consideration to make a
computer network work well?
• What design strategies have proven valuable?
• How do we evaluate network performance?

network edge: hosts/end systems (run networked apps that provide services), access network (edge routers connecting to ISPs network core), physical media
network core: packet switching (breaks into packets of header+payload ∴ each packet independent), i.e. routers, switches (imagine an ISP network is interconnected routers)
legacy circuit switching dedicates resources (not appropriate for bursty, variable data rate connections on the Internet. furthermore, not as economical as can't allow more users than hardware permits)
main functions:
1. packet forwarding (input to output)
2. packet routing (routing algorithm, i.e. path determination based on header)
we assume store-and-forward switching, i.e. router takes header and payload before transmitting 
packet switching utilises statistical multiplexing, i.e. educated assumption of bursty traffic
if queue overloaded, packets go into buffer (transient overload) resulting in a delay
if buffer excedded (persistent overload), packets dropped

performance: loss, delay, throughput 

so your home network is a type of access network, as well as connection to ISP? (i.e. access network just network to a router that goes to the ISP)
access networks:
* WLAN (wifi?)
* WAN (wide area network; cellular)
* Enterprise networks (mail servers, etc.)

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

stochastic means random distribution but may still be analysed with statistics, e.g. stock market graphs

bernoulli trial is binomial experiment whereby probability stays the same across repetitions
binomial question: probability of 'x' successes in 'n' trials?   (mrnicholltv)
calculate number of ways to acheive said number and multiply by probability
number of ways is: N choose X
