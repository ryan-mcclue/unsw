<!-- SPDX-License-Identifier: zlib-acknowledgement -->

> if traceroute '*' out, what does this mean? just use last IP for determining location?
'*' and further traffic indicates it did pass router
if '*' tail at end, routers sensititve to information leaking and cannot say where it ends 
> how does it give a '*' and then continue onwards?

> car keys use Zigbee. holding to head increases signal strength

determine public ip with: `dig +short myip.opendns.com @resolver1.opendns.com`
> interesting $(ifconfig) gives public IP if connected via ethernet

(observe RTT; geolocation data from IP can be deliberatley forged for security reasons)
(different end result due to many end router destination server possibilities)
> IANA to regional, APNIC, ARIN, etc.
> interesting get 'direct IP not allowed' when using last IP given by traceroute for domain
> how do geolocation tools like yougetsignal work? 

brisbane: 756km,  17.1ms / 0.00252secs (6.8)
serdang: 6,605, 99.7ms / 0.022 (4.5)
berlin: 16,100km, 279ms / 0.0537 (5.2) 

processing delay: inspecting header to determine where packet needs to go. (fixed number based on header size, e.g UDP less bytes thans TCP)
queuing: depends on number of packets
