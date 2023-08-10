<!-- SPDX-License-Identifier: zlib-acknowledgement -->
`f(n) = O(g(n))`, if `f(n)/g(n) <= C` or `lim∞ f'(n)/g'(n) = 0` *(limit asymptotic theorem)*
`f(n) = Ω(g(n))`, if `f(n)/g(n) > C` or `lim∞ f'(n)/g'(n) = ∞`
`f(n) = θ(g(n))`, if `O(n) = Ω(n)` or `lim∞ f'(n)/g'(n) = 0`

`T(n) = a·T(n/b) + f(n)`, *a = num-subproblems*, *b = size-subproblems*
`n^(logbᵃ)`, `< θ(n^(logbᵃ))`, `= θ(n^(logbᵃ)·log2ⁿ)`, `> θ(f(n))` 


divide-and-conquer (binary-search)
greedy
flow
dp
