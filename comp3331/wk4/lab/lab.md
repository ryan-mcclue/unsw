# Lab 03 - Ryan McClue (z5346008)

## 1. Digging into DNS 
have to 
```
; <<>> DiG 9.16.1-Ubuntu <<>> www.eecs.berkeley.edu A
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41872
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;www.eecs.berkeley.edu.		IN	A

;; ANSWER SECTION:
www.eecs.berkeley.edu.	86400	IN	CNAME	live-eecs.pantheonsite.io.
live-eecs.pantheonsite.io. 599	IN	CNAME	fe1.edge.pantheon.io.
fe1.edge.pantheon.io.	299	IN	A	23.185.0.1

;; Query time: 180 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Wed Oct 05 18:12:35 AEDT 2022
;; MSG SIZE  rcvd: 137
```
type A

2.
CNAME for devlopers to use to help developers
alias for end users ease of use (name on left)

3. authority info relating domain name servers for that domain
additional is IP for above authority section
query time is RTT

4. server is local CSE DNS

5.a domain has many servers within
$(dig eecs.berkely.edu NS) (remove www for domain, otherwise get webserver)

6. 
dig -x 111.68.101.54
PTR record

7. dig @129. yahoo.com MX
not authorative, as we are going through CSE authorative, not yahoo
(so virtually impossible to get authorative from 3rd party)
>>HEADER<< shows 'aa' for authorative in DNS record
to get authorative, send query to authorative server from additional information

8. Berkely did not give outside access to their DNS servers
(no response)

9.

10. iterative DNS query (root -> TLD (.au, .sg) -> authorative (.edu) -> .unsw)
hostname -f 

dig . NS (root name servers)
dig @2 A (iteratively replace nameserver until get ANSWER section)

11. router multiple IP
CNAME records, so one machine have differnt names 
