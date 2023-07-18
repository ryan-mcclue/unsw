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
