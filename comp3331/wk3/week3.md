<!-- SPDX-License-Identifier: zlib-acknowledgement -->

DNS UDP:53
Request and response same format

A domain is string name of a network. A hostname is end-point
Essentially, a hostname extends DNS to within a network, e.g. machine-host-name.domain
So, 'could' use hostname to communicate with other machine on same network

Can have internationalised domain names, e.g. not in English

Authoratative name server typically have primary and secondary (which is just a duplicate to handle load balancing)

NOTE: multiple DNS servers for a domain will all have identical information in them

mywebsite.com is apex domain, it only has A record

www.mywebsite.com and mail.mywebsite.com are sub-domains, specifically hostnames. 
They can have CNAME records. This means, say using a www. allows for CDN usage

DNS is application-level. DNSSEC authenticates domain name responses to ensure DNS requests can't be manipulated.
Hierarchical in namespace and administration (zone) for scalability and fast lookups
Can allow for load balancing and host alaising, e.g. 
relay1.west-coast.enterprise.com (canonical) two aliases www.enterprise.com and enterprise.com
NOTE: DNS sent first than can do application-level like HTTP

13 logical root nameservers with many instances replicated across the world

(IANA is department within ICANN)
ICANN is the governing body for all domain name extensions (search ICANN registry agreements to see particular gDNS registry)
DNS registrar: sells domain names, e.g. GoDaddy and adds records to TLD
For specific domains, where it adds are different, e.g. for .au is auda.org, .com Verisign

The local DNS server given by DHCP, i.e. run by your ISP is not part of this hierarchy, rather it connects you to it.

Once DNS server learns mapping it caches it for a TTL (can also have negative caching, i.e. storing what doesn't exist)
So, a changed domain may not be known until TTL expires and is automatically updated.
This caching is also performed by web browser and/or OS

DNS is database of DNS resource records in format (type, name, value, ttl)
type=A,hostname,IP
type=CNAME,alias,canonical (for load balancing, say with CDN)
type=NS,domain,authorative-name-server (where to go to find any sub-domains also)
type=MX

PTR (reverse, IP to domain)

when creating a domain:
* NS(networkutopia.com, dns1.networkutopia.com)
* A(dns1.networkutopia.com, 212.212.212.1)

DNS requests: CNAME->web (why not A? assuming CDN use?), MX->mail, NS->dns

observe CDN (caching from origin server to local servers) usage with $(dig) that shows CNAME for CDN, e.g. www.mit.edu -> www.mit.edu.edgekey.net

Skype is P2P
Offers high availability, but complex management
Better file distribution time than client server

Tracker is a server that records all people downloading/uploading a file (different to a torrent site that hosts .torrent files)
A .torrent file contains all information to download file, e.g. size, tracker, hash of file chunks

Torrent is collection of peers exchanging chunks of a file
Peers may upload (periodicaly reevaluate what top-four peers they send to; tit-for-tat) and download chunks between other peers
DHT (distributed hash table), i.e. a P2P hash table database
New keys are assigned to closest current ID
Circular DHT each peer aware of successor and predecessor

DHT is a structured P2P, i.e. rigid way of finding peers to in turn find resource
In DHT, each node only connected to its direct neighbours, i.e. successor and predecessor
Each node has a hash table. 
All data keys less than server key
Node 2 owns all data keys [1..2), Node 3 [2..3)
Exception is first server that owns all keys less than it normally (0,..1), but also all keys greater than final servers key [8..MAX_KEY)   
When a request is recieved, a hash table lookup is performed. 
Say request data key 4.2, will follow peers based on this rule to find destination
If a server is removed, keys migrate to maintain this rule


80% of ISP bandwidth is video streaming (acheived with: compression + DASH + playout buffering)
Spatial compression (within image), temporal compression (from one image to next, i.e. frame delta)
Playout delay is time sent to time played
DASH (dynamic adaptive streaming over HTTPS), chunks stored at different coding rates (manifest file; i.e. any file containing metadata for accompanying files)
This allows client to choose appropriate rate for current bandwidth
A video streaming CDN will typically implement a DASH server and so will send out a manifest file first

A TCP server will have a 'welcoming' socket that clients use to perform 3way handshakes on. 
Then a new 'connection' socket will be created
Seems that multithreaded TCP server easier as specific connection sockets can be forked

P2P network debugging use `xterm -hold`
