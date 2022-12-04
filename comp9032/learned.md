<!-- SPDX-License-Identifier: zlib-acknowledgement -->
add/sub/compare with carry

signed/unsigned branches

simple conflict register pushing and larger stack usage

sub same as cmp

mul typically in two different output registers

carry is for unsigned arithmetic
overflow is for signed arithmetic

must preserve status register value inside interrupt to avoid nasty logic errors

TODO: dynamic data structure implementations in C, e.g. queue
