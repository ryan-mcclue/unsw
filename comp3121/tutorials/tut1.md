<!-- SPDX-License-Identifier: zlib-acknowledgement -->
1.1
Algorithm:
* Sort array A and array B with Quick Sort
* Iterate over array A and B with two separate indexes i and j respectively
* If A[i] = B[j], we have a common match
  If A[i] > B[j], increment j as a larger sorted item will only appear further down B
  If A[i] < B[j], increment i as a larger sorted item will only appear further down A 
* Terminate iteration if the length of A or B are reached.
(could alternatively sort one array and then do a binary search)
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
* Yes. Each day, pair minimum with maximum
2.2
* As truck can take all packages in one day
2.3
Algorithm:
* Iterate over all packages and maintain a running sum of their weights
* If the current package weight added to the running sum exceeds C, add one to required delivery days
  Otherwise, add to the running sum and proceed to next package
* Once all package iteration finishes, if required delivery days is <= K, it's possible to deliver
Correctness:
* By commutative law, assigning packages in any order such that <= C, will compute same sum
Time Complexity:
* As iterating over package array, O(n)
2.4
* Smallest possible is sum(packages) / K. However, discounts individual package size, e.g. one very large and one very small 
  Guaranteed capacity is is sum(packages).
  Binary search between these until one search after capacity sufficient is no longer sufficient.
  O(nlog(n)) as each step of log(n) binary search, execute O(n) algorithm to verify capacity
* Monotonically increasing for as package number and package weights increase
  Monotonically decreasing as capacity increases
