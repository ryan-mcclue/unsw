<!-- SPDX-License-Identifier: zlib-acknowledgement -->
# COMP3331 Assignment - Ryan McClue (z5346008)
(no more than 3 pages)

## Program Design

Utilise a unity build system to reduce linkage time and remove need for an external build tool.
Build by running script `chmod +x build && ./build`, which will produce `client` and `server` binaries.

### File Structure
Entrypoints to client and server binaries are `client.c` and `server.c` respectively.

`common.h` contains various common includes and function definitions that are used by both the client and server.

`io.h/io.c` contain functions related to file reading/writing and string parsing

`commands.c` contains functions implementing client side commands 

`messages.h` contains definitions for application layer message format

Files produced by `EDG` are placed in the current working directory of the `client` binary and are named `[device-name]-[fileid].txt`

Files uploaded by `UED` are placed in the current working directory of the `server` binary and are named `server-[device-name]-[fileid].txt`

Files uploaded by `UVF` are placed in a folder named `[recieving-device-name]/[sending-file-name]` 

### Key Functions/Definitions
`readx()`, `writex()`, `write_entire_file()`, `read_entire_file()`, `get_ms_epoch()`

#### Client
`split_into_tokens()`
`process_edg_command()`


#### Server
structs here
`SharedState`, `BlockedDevice`, `DevInfo`

`parse_credentials()`, `verify_credentials()`
`clear_file()`, `append_to_file()`
`write_active_devices_to_log_file()`
`populate_timestamp()`

### Application Layer Message Format
Defined in `messages.h` is a discriminated union

### Program Flow
a brief description of how your system works. 

## Design Tradeoffs
Also, discuss any design tradeoffs considered and made. 

Describe possible improvements and extensions to your program and 
indicate how you could realise them.

Security (encryption, packet length manipulation, authentication spoofing)
Bandwidth
Endianness
Scalability (assume no more than 32 clients connected in one session)
Concurrency (no locks)

## Program Features Not Working
If your program does not work under any particular circumstances, please
report this here.
