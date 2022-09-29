<!-- SPDX-License-Identifier: zlib-acknowledgement -->

DNS UDP:53
Request and response same format

A domain is name of a network. A hostname is end-point
Essentially, a hostname extends DNS to within a network, e.g. machine-host-name.domain
So, 'could' use hostname to communicate with other machine on same network

DNS is application-level. DNSSEC authenticates domain name responses to ensure DNS requests can't be manipulated.
Hierarchical in namespace and administration (zone) for scalability and fast lookups
Can allow for load balancing and host alaising, e.g. 
relay1.west-coast.enterprise.com (canonical) two aliases www.enterprise.com and enterprise.com

13 logical root nameservers with many instances replicated across the world

DNS registries:
* root: ICANN
* .com: Network Solutions
* .edu: Educause

DNS registrar: sells domain names, e.g. GoDaddy

The local DNS server given by DHCP, i.e. run by your ISP is not part of this hierarchy, rather it connects you to it.

Once DNS server learns mapping it caches it for a TTL (can also have negative caching, i.e. storing what doesn't exist)
So, a changed domain may not be known until TTL expires and is automatically updated.
This caching is also performed by web browser and/or OS

DNS is database of DNS resource records in format (type, name, value, ttl)
type=A,hostname,IP
type=CNAME,alias,canonical
type=NS,domain,authorative-name-server
type=MX

when creating a domain:
* NS(networkutopia.com, dns1.networkutopia.com)
* A(dns1.networkutopia.com, 212.212.212.1)

DNS requests: CNAME->web (why not A?), MX->mail, NS->dns

observe CDN (caching from origin server to local servers) usage with $(dig) that shows CNAME for CDN, e.g. www.mit.edu -> www.mit.edu.edgekey.net

Skype is P2P
Offers high availability, but complex management
Better file distribution time than client server

