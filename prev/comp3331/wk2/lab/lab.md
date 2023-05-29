# Lab 01 - Ryan McClue (z5346008)

## 1. Nslookup

1. The domain `www.koala.com.au` has 2 IP addresses: `104.21.45.210` and `172.67.219.46`.
In my opinion, the reason for having several IP addresses as an output is for load balancing reasons. Specifically, there are several webservers for the domain to allow traffic be distributed across multiple resources.

2. The IP address `127.0.0.1` is also known as localhost or the loopback device.
It's purpose is to provide an interface that allows a host to interact with its own network services.
Applies to all addresses with CIDR `127.0.0.1 /8`

## 2. Ping

* **www.unsw.edu.au:** reachable.
* **www.getfittest.com.au:** unreachable; unreachable via web browser as domain has no registered DNS records
* **www.mit.edu:** reachable
* **www.intel.com.au:** reachable
* **www.tpg.com.au:** reachable
* **www.hola.hp:** unreachable; unreachable via web browser as domain not registered under `.hp` name server, rather `.com`, i.e. `www.holahp.com` is accessible
* **www.amazon.com:** reachable
* **www.tsinghua.edu.cn:** reachable
* **www.kremlin.ru:** unreachable; reachable via web browser as server is configured to reject ping ICMP packets but to serve web pages
* **8.8.8.8:** reachable; not reachable via web browser as IP represents Google's Public DNS server and is therefore not configured to serve web pages.

## 3. Traceroute

```
traceroute to www.columbia.edu (128.59.105.24), 30 hops max, 60 byte packets
 1  cserouter1-server.orchestra.cse.unsw.EDU.AU (129.94.242.251)  0.042 ms  0.041 ms  0.044 ms
 2  129.94.39.17 (129.94.39.17)  0.876 ms  0.841 ms  0.859 ms
 3  172.17.31.154 (172.17.31.154)  14.464 ms  14.421 ms  14.472 ms
 4  po-3-1902.ombcr1.gw.unsw.edu.au (129.94.24.20)  1.128 ms  1.082 ms  1.141 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.098 ms  1.070 ms  1.108 ms
 6  138.44.5.0 (138.44.5.0)  1.431 ms  1.205 ms  1.221 ms
 7  et-1-1-0.pe1.mcqp.nsw.aarnet.net.au (113.197.15.4)  1.639 ms  1.608 ms  1.654 ms
 8  et-0_0_2.bdr1.guam.gum.aarnet.net.au (113.197.14.137)  71.585 ms  71.565 ms  71.510 ms
 9  138.44.228.5 (138.44.228.5)  186.544 ms  186.494 ms  186.462 ms
10  fourhundredge-0-0-0-2.4079.core2.salt.net.internet2.edu (163.253.1.115)  237.147 ms  237.108 ms  237.228 ms
11  fourhundredge-0-0-0-0.4079.core2.denv.net.internet2.edu (163.253.1.168)  237.218 ms fourhundredge-0-0-0-23.4079.core1.salt.net.internet2.edu (163.253.1.32)  237.472 ms fourhundredge-0-0-0-21.4079.core1.salt.net.internet2.edu (163.253.1.28)  237.090 ms
12  fourhundredge-0-0-0-0.4079.core1.denv.net.internet2.edu (163.253.1.170)  237.456 ms  236.560 ms fourhundredge-0-0-0-0.4079.core2.kans.net.internet2.edu (163.253.1.251)  236.627 ms
13  fourhundredge-0-0-0-0.4079.core1.kans.net.internet2.edu (163.253.1.243)  238.133 ms  238.006 ms fourhundredge-0-0-0-0.4079.core1.chic.net.internet2.edu (163.253.2.28)  236.037 ms
14  fourhundredge-0-0-0-3.4079.core2.chic.net.internet2.edu (163.253.1.244)  238.172 ms  238.773 ms  238.480 ms
15  fourhundredge-0-0-0-3.4079.core2.eqch.net.internet2.edu (163.253.2.19)  238.007 ms  236.924 ms  236.913 ms
16  fourhundredge-0-0-0-0.4079.core2.clev.net.internet2.edu (163.253.2.16)  237.643 ms  237.601 ms  237.234 ms
17  buf-9208-I2-CLEV.nysernet.net (199.109.11.33)  238.392 ms  238.306 ms  238.299 ms
18  syr-55a1-buf-9208.nysernet.net (199.109.7.213)  241.804 ms  241.515 ms  241.745 ms
19  nyc32-55a1-syr-55a1.nysernet.net (199.109.7.206)  247.140 ms  247.024 ms  247.277 ms
20  nyc32-9208-nyc32-55a1.nysernet.net (199.109.7.201)  246.735 ms  246.746 ms  246.960 ms
21  columbia.nyc-9208.nysernet.net (199.109.4.14)  246.769 ms  246.850 ms  246.978 ms
22  cc-core-1-x-nyser32-gw-1.net.columbia.edu (128.59.255.5)  247.145 ms  246.998 ms  247.072 ms
23  cc-conc-1-x-cc-core-1.net.columbia.edu (128.59.255.21)  247.336 ms  247.281 ms  247.188 ms
24  columbia.edu (128.59.105.24)  247.042 ms  247.073 ms  247.091 ms
```
1. There are 23 routers between my workstation and `www.columbia.edu`. 
There are 5 routers along the path that are part of the UNSW network.
Between routers 8 and 9 do packets cross the Pacific Ocean. 

```
traceroute to www.u-tokyo.ac.jp (210.152.243.234), 30 hops max, 60 byte packets
 1  cserouter1-server.orchestra.cse.unsw.EDU.AU (129.94.242.251)  0.083 ms  0.093 ms  0.085 ms
 2  129.94.39.17 (129.94.39.17)  0.933 ms  0.962 ms  0.938 ms
 3  172.17.31.154 (172.17.31.154)  1.607 ms  1.960 ms  1.927 ms
 4  po-3-1902.ombcr1.gw.unsw.edu.au (129.94.24.20)  1.225 ms  1.287 ms  1.242 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  18.167 ms  18.120 ms  18.196 ms
 6  138.44.5.0 (138.44.5.0)  1.293 ms  1.285 ms  1.248 ms
 7  et-0-3-0.pe1.bkvl.nsw.aarnet.net.au (113.197.15.147)  1.805 ms  1.740 ms  1.743 ms
 8  ge-4_0_0.bb1.a.pao.aarnet.net.au (202.158.194.177)  155.007 ms  155.037 ms  154.998 ms
 9  paloalto0.iij.net (198.32.176.24)  156.998 ms  156.974 ms  156.729 ms
10  osk004bb00.IIJ.Net (58.138.88.185)  274.746 ms osk011bb00.IIJ.Net (58.138.84.225)  274.486 ms osk011bb01.IIJ.Net (58.138.84.229)  266.406 ms
11  osk004ip56.IIJ.Net (58.138.81.66)  274.489 ms osk004ip56.IIJ.Net (58.138.81.70)  266.736 ms osk004ip57.IIJ.Net (58.138.81.78)  270.616 ms
12  210.130.135.130 (210.130.135.130)  277.394 ms 210.138.106.238 (210.138.106.238)  270.652 ms  270.630 ms
13  124.83.228.58 (124.83.228.58)  274.608 ms  270.852 ms  270.914 ms
14  124.83.252.170 (124.83.252.170)  273.077 ms 124.83.252.178 (124.83.252.178)  276.705 ms 124.83.252.170 (124.83.252.170)  289.695 ms
15  158.205.134.26 (158.205.134.26)  276.785 ms 158.205.134.22 (158.205.134.22)  280.927 ms 158.205.134.26 (158.205.134.26)  272.595 ms
16  * * *
17  * * *
18  * * *
```
```
traceroute to www.lancaster.ac.uk (148.88.65.80), 30 hops max, 60 byte packets
 1  cserouter1-server.orchestra.cse.unsw.EDU.AU (129.94.242.251)  0.042 ms  0.050 ms  0.092 ms
 2  129.94.39.17 (129.94.39.17)  0.876 ms  0.918 ms  0.886 ms
 3  172.17.31.154 (172.17.31.154)  1.623 ms  1.935 ms  1.857 ms
 4  po-3-1902.ombcr1.gw.unsw.edu.au (129.94.24.20)  1.432 ms  1.450 ms  1.339 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  23.433 ms  23.311 ms  23.387 ms
 6  138.44.5.0 (138.44.5.0)  1.355 ms  1.327 ms  1.315 ms
 7  et-2-0-5.bdr1.sing.sin.aarnet.net.au (113.197.15.233)  92.760 ms  92.724 ms  92.658 ms
 8  138.44.226.7 (138.44.226.7)  260.097 ms  260.083 ms  260.013 ms
 9  janet-gw.mx1.lon.uk.geant.net (62.40.124.198)  260.090 ms  260.041 ms  260.448 ms
10  ae29.londpg-sbr2.ja.net (146.97.33.2)  260.783 ms  260.676 ms  260.727 ms
11  ae31.erdiss-sbr2.ja.net (146.97.33.22)  264.333 ms  264.519 ms  264.463 ms
12  ae29.manckh-sbr2.ja.net (146.97.33.42)  266.117 ms  266.301 ms  266.280 ms
13  ae25.manckh-ban1.ja.net (146.97.35.50)  266.425 ms  266.430 ms  266.374 ms
14  lancaster-uni.ja.net (146.97.40.178)  286.608 ms  286.591 ms  286.550 ms
15  * * *
16  * * *
17  * * *
```
```
traceroute to www.ucla.edu (99.86.38.17), 30 hops max, 60 byte packets
 1  cserouter1-server.orchestra.cse.unsw.EDU.AU (129.94.242.251)  0.042 ms  0.052 ms  0.042 ms
 2  129.94.39.17 (129.94.39.17)  0.857 ms  0.874 ms  0.865 ms
 3  172.17.31.154 (172.17.31.154)  1.590 ms  1.596 ms  2.134 ms
 4  po-3-1902.ombcr1.gw.unsw.edu.au (129.94.24.20)  1.181 ms  1.234 ms  1.105 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.106 ms  1.125 ms  1.142 ms
 6  138.44.5.0 (138.44.5.0)  1.228 ms  1.229 ms  1.277 ms
 7  ae1.170.bdr1.b.sea.aarnet.net.au (113.197.15.63)  141.754 ms  143.719 ms  140.733 ms
 8  xe-4-1-1.mpr1.sea1.us.above.net (64.125.193.129)  140.886 ms  140.903 ms  140.829 ms
 9  ae27.cs1.sea1.us.eth.zayo.com (64.125.29.0)  140.769 ms  140.803 ms  140.871 ms
10  ae28.mpr2.sea1.us.zip.zayo.com (64.125.29.103)  149.467 ms  149.520 ms  149.476 ms
11  99.82.182.102 (99.82.182.102)  140.804 ms  140.763 ms  140.778 ms
12  150.222.136.69 (150.222.136.69)  141.519 ms 150.222.136.65 (150.222.136.65)  142.042 ms 150.222.136.61 (150.222.136.61)  142.041 ms
13  52.95.53.9 (52.95.53.9)  141.617 ms 52.95.52.210 (52.95.52.210)  141.184 ms 52.95.53.151 (52.95.53.151)  141.190 ms
14  205.251.225.233 (205.251.225.233)  141.379 ms 205.251.225.217 (205.251.225.217)  141.439 ms 205.251.225.231 (205.251.225.231)  141.358 ms
15  52.95.55.142 (52.95.55.142)  143.339 ms 52.95.55.6 (52.95.55.6)  142.801 ms 52.95.54.162 (52.95.54.162)  141.816 ms
16  205.251.225.51 (205.251.225.51)  140.937 ms 205.251.225.31 (205.251.225.31)  140.910 ms 205.251.225.41 (205.251.225.41)  141.429 ms
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  server-99-86-38-17.sea19.r.cloudfront.net (99.86.38.17)  140.804 ms  140.836 ms  140.841 ms
```
2. The router at which the paths from my machine to the 3 destinations diverge is `138.44.5.0`.
This router is part of the *Australian Academic and Research Network*, the ISP that serves UNSW.
The number of hops on each path is not proportional to distance.
Routers physically close to one another and others separated by large distances are interleaved with each other in each path.

```
traceroute to 129.94.242.119 (129.94.242.119), 30 hops max, 60 byte packets
 1  202.150.221.169 (202.150.221.169)  0.147 ms  0.166 ms  0.173 ms
 2  10.11.34.146 (10.11.34.146)  0.369 ms  0.489 ms  0.621 ms
 3  aarnet.sgix.sg (103.16.102.67)  213.672 ms  213.653 ms  213.673 ms
 4  et-7-3-0.pe1.nsw.brwy.aarnet.net.au (113.197.15.232)  211.193 ms  211.202 ms  211.165 ms
 5  138.44.5.1 (138.44.5.1)  224.230 ms  224.239 ms  224.137 ms
 6  libcr1-te-1-5.gw.unsw.edu.au (149.171.255.102)  224.116 ms  220.192 ms  216.195 ms
 7  * irb-51901.kecd1-176q4-cbl-e1.gw.unsw.edu.au (129.94.24.10)  214.673 ms  214.350 ms
 8  * * *
 9  129.94.39.23 (129.94.39.23)  214.366 ms  214.471 ms  214.378 ms
10  * * *
11  * * *
12  * * *
```
```
traceroute to 202.150.221.170 (202.150.221.170), 30 hops max, 60 byte packets
 1  cserouter1-server.orchestra.cse.unsw.EDU.AU (129.94.242.251)  0.073 ms  0.081 ms  0.072 ms
 2  129.94.39.17 (129.94.39.17)  0.868 ms  0.885 ms  0.903 ms
 3  172.17.31.154 (172.17.31.154)  1.986 ms  2.001 ms  1.574 ms
 4  po-3-1902.ombcr1.gw.unsw.edu.au (129.94.24.20)  1.165 ms  1.215 ms  1.330 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  1.303 ms  1.246 ms  1.261 ms
 6  138.44.5.0 (138.44.5.0)  1.401 ms  1.483 ms  1.500 ms
 7  et-0-3-0.pe1.alxd.nsw.aarnet.net.au (113.197.15.153)  2.140 ms  1.742 ms  1.736 ms
 8  xe-0-2-7.bdr1.a.lax.aarnet.net.au (202.158.194.173)  147.692 ms  147.787 ms  147.711 ms
 9  singtel.as7473.any2ix.coresite.com (206.72.210.63)  147.757 ms  147.931 ms  147.983 ms
10  203.208.149.253 (203.208.149.253)  156.013 ms 203.208.172.133 (203.208.172.133)  326.222 ms 203.208.171.117 (203.208.171.117)  151.807 ms
11  203.208.177.110 (203.208.177.110)  350.528 ms 203.208.172.234 (203.208.172.234)  157.685 ms 203.208.173.73 (203.208.173.73)  253.091 ms
12  * 203.208.173.165 (203.208.173.165)  327.747 ms  327.651 ms
13  202.150.221.170 (202.150.221.170)  213.095 ms 203.208.153.246 (203.208.153.246)  334.719 ms 202.150.221.170 (202.150.221.170)  213.471 ms
```

3. The IP of *www.speedtest.com.sg* is `202.150.221.170` (lab tutor mentioned only required to do 1 traceroute web service).
The reverse path does not go through the same routers as the forward path.
This is because of different routing tables used by the access ISPs serving my machine and the web traceroute service.
Furthermore, how a packet is routed through a network is dependent on network congestion. 
The state of the network when each traceroute is performed is different, therefore yielding a different path.
Common routers are `9 -> 2`, `7 -> 4`, `6 -> 5`, `5 -> 6`.
A single router has multiple interfaces, i.e. multiple IP addresses.
This is shown via the `whois` command that shows CIDR notation, e.g. `149.171.0.0/16`
This is because routers route between different networks, therefore requiring different IP addresses to interface between multiple networks.

## 4. Network Performance

![Berlin Scatter](lab1/www.tu-berlin.de_scatter.pdf)

![Berlin Delay](lab1/www.tu-berlin.de_delay.pdf)

![Serdang Scatter](lab1/www.upm.edu.my_scatter.pdf)

![Serdang Delay](lab1/www.upm.edu.my_delay.pdf)

![Brisbane Scatter](lab1/www.uq.edu.au_scatter.pdf)

![Brisbane Delay](lab1/www.uq.edu.au_delay.pdf)

![Compiled Graph](misc/q3.eps)

1. Reasons for y-axis being larger than 2 is because ping command measures round-trip-time, while shortest possible time is end-to-end.
Furthermore, there is associated nodal delay as the packet is routed, e.g. processing + queueing + transmission delays
2. Delay to destinations varies over time. 
Packets take different routes of different times based on network conditions, e.g. congestion.
As network conditions are not constant, the delay will not be constant.
3. Transmission delay depends on packet size. Propagation delay, processing delay and queuing delay don't.
