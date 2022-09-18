# Lab 01 - Ryan McClue (z5346008)

## 1. Nslookup

1. The domain `www.koala.com.au` has 2 IP addresses: `104.21.45.210` and `172.67.219.46`
In my opinion, the reason for having several IP addresses as an output is for load balancing reasons. Specifically, there are several webservers for the domain to allow traffic be distributed across multiple resources.

2. The IP address `127.0.0.1` is also known as localhost or the loopback device.
It's purpose is to provide an interface that allows a host to interact with its own network services

## 2. Ping

On my own machine not connected to the CSE network:

* **www.unsw.edu.au:** reachable.
* **www.getfittest.com.au:** unreachable; unreachable via web browser as domain has no registered DNS records
* **www.mit.edu:** reachable
* **www.intel.com.au:** reachable
* **www.tpg.com.au:** reachable
* **www.hola.hp:** unreachable; unreachable via web browser as not domain not registered under `.hp` name server, rather `.com`, i.e. `www.holahp.com` is accessible
* **www.amazon.com:** reachable
* **www.tsinghua.edu.cn:** reachable
* **www.kremlin.ru:** unreachable; reachable via web browser as server is configured to reject ping ICMP packets but to serve web pages
* **8.8.8.8:** unreachable; not reachable via web browser as IP represents Google's Public DNS server and is therefore not configured to serve web pages. Also server most likely configured to block ping ICMP packets

> kremlin ip resolved, no packets returned?

## 3. Traceroute

1. There are (24 - 1?) routers between my workstation and `www.columbia.edu`.
There are (5) routers along the path that are part of the UNSW network.
Between routers (9) and (10) do packets cross the Pacific Ocean.

> cross pacific only because of googling not RTT

2.
The router at which the paths from my machine to the 3 destinations diverge is `138.44.5.0`
CIDR:           138.44.0.0/16
Organization:   Asia Pacific Network Information Centre (APNIC)

Comment:        This IP address range is not registered in the ARIN database.
Comment:        This range was transferred to the APNIC Whois Database as
Comment:        part of the ERX (Early Registration Transfer) project.


OrgName:        Asia Pacific Network Information Centre
OrgId:          APNIC
Address:        PO Box 3646
City:           South Brisbane
StateProv:      QLD
PostalCode:     4101
Country:        AU

> multiple records? this one from APNIC as oppose to US ARIN?
netname:        AARNET
descr:          Australian Academic and Research Network
descr:          Building 9
descr:          Banks Street
country:        AU

**www.ucla.edu:** located at ..., () km away, () hops
**www.u-tokyo.ac.jp:** located at ..., () km away, () hops
**www.lancaster.ac.uk:** located at ..., () km away, () hops

> diverge from means last common router?
> how do geolocation tools like yougetsignal work? 
> interesting get 'direct IP not allowed' when using last IP given by traceroute for domain

> if traceroute '*' out, what does this mean? just use last IP for determining location?

3.
Run from my own machine not connected to CSE network

www.speedtest.com.sg (202.150.221.170)
portal.etsi.org (195.238.226.19) -- not working

determine public ip with: `dig +short myip.opendns.com @resolver1.opendns.com`

## 4. Network Performance
> gnuplot tutorial
