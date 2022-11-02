<!-- SPDX-License-Identifier: zlib-acknowledgement -->
# COMP3331 Assignment - Ryan McClue (z5346008)
(no more than 3 pages)

## Program Design

Utilise a unity build system to reduce linkage time and remove need for an external build tool.
Build by running script `./build`

### File Structure
Entrypoints to client and server binaries are `client.c` and `server.c` respectively.
`common.h` contains various common includes and function definitions that are used by both the client and server.
`io.h/io.c`
`commands.c`
`messages.h`

Files produced by UED placed in ...
Files produced by UVF placed in ...

### Key Functions
names of key functions

### Program Flow
a brief description of how your system works. 

### Application Layer Message Format

## Design Tradeoffs
Also, discuss any design tradeoffs considered and made. 

Describe possible improvements and extensions to your program and 
indicate how you could realise them.

Security (encryption, packet length manipulation, authentication spoofing)
Bandwidth
Endianness
Scalability (assume no more than 32 clients connected in one session)
Concurrency (assume no concurrent connect)

## Program Features Not Working
If your program does not work under any particular circumstances, please
report this here.
