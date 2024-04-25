#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement
def top(v, n, l):
  return (v & (((1 << n) - 1) << (l - n))) >> (l - n)
# f"{0x200:012b}"
