<!-- SPDX-License-Identifier: zlib-acknowledgement -->

TODO: byte size of protocol headers

CSE machines have firewalls that block external traffic like a UDP packet

Servers like the CSE machines aren't behind a NAT as we want them to have static publically addressable IPs.
So, users logged into them will share same IP. 
Comparatively, on uniwide recieve NAT 

telnet offers bidirectional text-oriented communication with server, e.g. can encapsulate HTTP server interaction over port 80 or port 443 
interesting HEAD request to only get header

a socket connection must have unique combination of (local-ip, local-port, remote-ip, remote-port)
∴ possible for sockets to share same port 
client sockets will use random port number assigned by OS

p2p, client+server are paradigms

write software for network-edge

IMAP and POP recieve emails. 
SMTP sends and exchanges between servers (atop TCP). 
Although HTTPS email user agent, between mail servers (so from protonmail to gmail) often plain-text (some use TLS). So, use PGP to be safe

socket (communication endpoint) for a client process (sending) and server process (responding)

application protocol considerations (data loss, timing, throughput, security)

TCP (flow/congestion control, reliable data transefer, connection oriented)

HTTP is a pull protocol, i.e. will wait for recieved reply (as oppose to SMTP which is push)
HTTP stateless. Responses/requests have status line, header lines, body

sends out cookie id which will be included in every HTTP request
3rd party cookies (different to domain you are on, e.g. could be an image provider) allows sites to track you
improve page load times with protocol enhancements, content providing location and caching

HTTP1.0 one TCP connection per resource served (incurs RTT penalty of 3-way handshake for TCP) 

HTTP1.1 introduced persistent TCP connection (allows pipelining, i.e. sending multiple objects one after the other without waiting for response)
The 'Keep-Alive' header sets the parameters for this persistence
Further prevents the 3-way handshake 2xRTT for each object, incurring this only for first object
(possibly may incur more burden on server maintaining this connection)
ISPs may install 'web caches' which are web proxy servers to increase load times.
HTTP 'conditional GET', i.e. client issues 'If-Modified-Since' to server, which if not changed, return 304 code  
Additionally uses ETag 'If-None-Match' based on content as oppose to timestamp

HTTP1.1 also introduced caching. ∴ must clear browser cache to properly inspect natural flow of packets

Accept-Ranges header for partial requests (resume downloads)  

HTTP2.0 decreases delay in multi-object responses (e.g. small object may be head-of-line blocked by larger object). 
objects divided into frames, so send say 16 bytes increments
This uses TCP splitting to increase performance via end-to-end delay (not say by decreasing overall packet size)

Without HTTPS, passwords just in base64 (binary-to-text)

* does a dynamic IP address imply a NAT?
* identify web cache proxy servers?

SNMP (simple network management protocol) get information about network devices

> if traceroute '*' out, what does this mean? just use last IP for determining location?
'*' and further traffic indicates it did pass router
if '*' tail at end, routers sensititve to information leaking and cannot say where it ends 

> car keys use Zigbee. holding to head increases signal strength

determine public ip with: `dig +short myip.opendns.com @resolver1.opendns.com`
> interesting $(ifconfig) gives public IP if connected via ethernet

(observe RTT; geolocation data from IP can be deliberatley forged for security reasons)
(different end result due to many end router destination server possibilities)
> IANA to regional, APNIC, ARIN, etc.
(can specify with $(whois -h whois.arin.net 163.253.1.115))
however, this just tells who the IP address is listed to and their location, not the router location 
> interesting get 'direct IP not allowed' when using last IP given by traceroute for domain
> how do geolocation tools like yougetsignal work? 

DNS server should be configured to return IP that best serves your location and in conjunction with load balancing

> as traceroute command sends 3 packets, it can return possibly 3 different IP addresses for the same router

processing delay: inspecting header to determine where packet needs to go. (fixed number based on header size, e.g UDP less bytes thans TCP)
queuing: depends on number of packets

> yes there is same router (look at IP address subnet)
> traceroute shows 56(84) meaning 56 byte payload + 8 byte ICMP + 20 byte IP
