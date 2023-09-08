<!-- SPDX-License-Identifier: zlib-acknowledgement -->

## 1D
Subproblem:
1 < i < n, let opt(i) be maximum sum of an independent subset of indices from 1..n

Order:
multiple base cases is opt(1), opt(2)
starting from i=1, continue until i=n

Recurrence (i.e. how we combine opt's):
1. Take ith element:
   opt(i) = A[i] + opt(i - 2)
2. Not taking ith element
   opt(i) = opt(i - 1)
-> opt(i) = max(A[i] + opt(i - 2), opt(i - 1))

Time:
n problems, O(1) lookup, giving O(n)

## 
Base Case:
while i < k: num(i) = 1
Recurrence (when i >= k):
1. ith bit is 1: num(i - 1)
2. ith bit is 0: can form valid or invalid, so num(i - k) 
num(i - 1) + num(i - k)

##
split text into 2 portions, s[1..k] (valid text) s[k+1..i] (1 more valid word)
1. valid text
2. 1 more valid word

Consider all cases from k to i-1. is there any k where portion 1 is text and other portion is a valid word?
Since for each n problem, must check previous i subproblems
So, O(n^2)

