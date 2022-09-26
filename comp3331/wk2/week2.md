<!-- SPDX-License-Identifier: zlib-acknowledgement -->

TODO: byte size of protocol headers

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

HTTP2.0 stateless. Responses/requests have status line, header lines, body
sends out cookie id which will be included in every HTTP request
3rd party cookies (different to domain you are on, e.g. could be an image provider) allows sites to track you
improve page load times with protocol enhancements, content providing location and caching
HTTP1.0 one TCP connection per resource served (incurs RTT penalty of 3-way handshake for TCP) 
HTTP1.1 introduced persistent TCP connection (allows pipelining, i.e. sending multiple objects one after the other without waiting for response)
The 'Keep-Alive' header sets the parameters for this persistence
Further prevents the 3-way handshake 2xRTT for each object, incurring this only for first object
(possibly may incur more burden on server maintaining this connection)
ISPs may install 'web caches' which are web proxy servers to increase load times.
HTTP 'conditional GET', i.e. if-modified-since header 
HTTP2.0 decreases delay in multi-object responses (e.g. small object may be head-of-line blocked by larger object). 
objects divided into frames, so send say 16 bytes increments

Without HTTPS, passwords just in base64 (binary-to-text)

* does a dynamic IP address imply a NAT?
* identify web cache proxy servers?


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

> DNS server should be configured to return IP that best serves your location?

> as traceroute command sends 3 packets, it can return possibly 3 different IP addresses for the same router

brisbane: 756km,  17.1ms / 0.00252secs (6.8)
serdang: 6,605, 99.7ms / 0.022 (4.5)
berlin: 16,100km, 279ms / 0.0537 (5.2) 

processing delay: inspecting header to determine where packet needs to go. (fixed number based on header size, e.g UDP less bytes thans TCP)
queuing: depends on number of packets

> yes there is same router (look at IP address subnet)
> traceroute shows 56(84) meaning 56 byte payload + 8 byte ICMP + 20 byte IP
