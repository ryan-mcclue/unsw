<!-- SPDX-License-Identifier: zlib-acknowledgement -->
1.1
Algorithm:
* Sort array A and array B with Quick Sort
* Iterate over array A and B with two separate indexes i and j respectively
* If A[i] = B[j], we have a common match
  If A[i] < B[j], increment j as a larger sorted item will only appear further down B
  If A[i] > B[j], increment i as a smaller sorted item will only appear further down A 
* Terminate iteration if the length of A or B are reached.
Time Complexity:
* Quick Sort is O(nlog(n))
* Iterating over the array is O(m), where m is largest length of A and B
* Total: 2O(nlog(n)) + O(m) = O(nlog(n)) 
1.2
Algorithm:
* Populate a hash table with elements of A as both key and value
* Iterate over array B and check if element is present in hash table
Time Complexity:
* Creating hash table of A is O(n)
* Iterating over B is O(n)
* Checking element in hash table has expected O(1), worse case O(n) (if all elements reside in same hash table bucket)
* Total: O(n) + O(n)O(n) = O(n^2)

2.1

