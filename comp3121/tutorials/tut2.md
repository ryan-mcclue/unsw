<!-- SPDX-License-Identifier: zlib-acknowledgement -->
1.1 justify base case:
for n=2, we know that only one way to do this
inductively, assume works for any n/2·n/2 (n = k)
for n = k+1
for any n/2·n/2, we know that pattern tesselates, i.e. can be tiled/overlayed over any other n/2·n/2

master theorem critical exponent = logba
critical polynomial n^(c*)

1.2 a=4, b=2
f(n) = O(1)

4 lots of n/2·n/2 solutions. so b = 2 (as we are not splitting to 1x1, rather 2x2 as power of 2)

2.1 only 1, as n/2 + n/2 = n 
2.2:
divide: split into n/2
conquer: find majority element in subarray
combine: return element that is majority in subarray
2.3:
justify:
base case has array size = 1, majority element is single element
merge/combine solution:

NOTE: there is an online master theorem calculator
