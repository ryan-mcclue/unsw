<!-- SPDX-License-Identifier: zlib-acknowledgement -->
# String Matching
## Rabin-Karp Algorithm (linear average case)
Hashing + recursion

hash(string) = hash(digit_array) · mod(large_prime)
(if prime is large enough, reduce false-positives, i.e. collisions?)

for i in string:
  if hash(string[i:]) == hash(substring):
    for j in string[i:]:
      if string[j] != substring[j]:
        break
    
horner's rule: polynomial rolling hash?

by computing hash from previous hash, can compare hash value of shifted string (i.e. one character up) from previous string

## Finite Automata (Knuth-Morris-Pratt, DP algorithm)
Maintain a table with current match count

Failure function is longest prefix of substring which is a suffix of string 

For imperfect matches of at most 'k' errors, split substring into 'k + 1' substrings. 
At least 1 of these must match perfectly

# Linear Programming (Ellipsoid and Simplex Methods)
Have an objective function and constraint functions

Working around Standard Form:
* negatives: replace with difference of two new variables
* equalities: replace with 2 inequalities, e.g >= and <=

maximise: c-transpose·x
such that: Ax <= b AND x >= 0

L(A, b, c)
c is a column-vector of coefficients of objective function 
A is matrix of coefficients for constraints 
b is a column-vector of right hand side values of constraints

Dual problem is problem of finding a tight bound for objective function by linear combination of constraints?

Primal (original) linear program P: maximise objective, subject to constraint
Its dual (Pprime): minimise
So, feasible solutions to primal are lower bounds for dual; solutions for dual are upper bound for primal (weak duality theorem)
So LP algorithms know when optimal solution is found, i.e when to stop, when solution is also solution for dual 

# Intractability
Problems considered easily solvable can be solved in polynomial time (even though say n^10 not really feasible)
Decision problem has answer either TRUE or FALSE. 
Would be in class P, is exists polynomial time solution
Would be in class NP (non-deterministic polynomial time)
  * non-deterministic turing machine? (NP solved on a machine like this in P time)
  * B(x, y), a problem/predicate, certificate?
  * A(x) = integer x is not a prime
    B(x, y) = x is divisible by y
    A(x) true,  
  ...
  * IMPORTANT: If given an example solution and can check if verifiable in polynomial time, then NP?

Primality Testing (testing primes).
Length of input is O(logx). O(root(x)) not P?

Compare 'hardness' of 2 decision problems
polynomial reduction
say U and V problems
U(x) is YES if V(f(x)) is YES, where f(x) is P
so problem U is not harder than V
(contrapositive, i.e. reversing this logic also solves)

Satisifiablility is grouping of truth variables
3SAT has every bracket of length 3, i.e. 3 variables
(can reduce SAT to 3SAT by adding propositional variables)

Cook's Theorem states that every NP problem polynomially reducible to SAT problem 
(so can find function to convert input to SAT problem)
SAT is NP-complete (SAT is hardest type of NP problems)
NP-complete is if every other NP problem is polynomially reducible to it
IMPORTANT: P != NP, so NP-complete no polynomial time solution
(however P is subset of NP, just not other way around)

NP-Complete Problems: 
  * Travelling Salesman
  * Register Allocation (possible to colour vertices with at most K colours, so no edge has ends with same colour?)
  TODO: graph colouring seems to be NP-Complete?
