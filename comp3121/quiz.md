<!-- SPDX-License-Identifier: zlib-acknowledgement -->
# Take Home Quiz
## Question 1.
* From BST definition, all elements in node X's left subtree \< node X 
* Therefore, successor of X cannot be in node X's left subtree. 
* From BST definition, if node X is left child of parent, then parent is \> node X
* From BST definition, all elements in node X's right subtree \> node X
* So, node X's parent will only be successor if node X is left child and node X has no right subtree.
* This is because elements in node X's right subtree are \> node X but \< node X's parent. 
* So, if node X has a right subtree, its successor will be minimum value its right subtree.
* From BST definition, the minimum value in right subtree cannot have a left child, as this child would be \< its parent, therefore making it the successor.
* As a result, if node X has a right child, i.e. right subtree, then the successor of node X does not have a left child.

## Question 2.
1. Given a binary tree of height *h*, a complete binary tree satisfies both:
   1. All *h - 1* levels are filled, i.e. all nodes have left and right children
   2. Level *h* is filled left to right, i.e. left child added on left subtree, then right child of added on right subtree etc.
2. A heap is a complete binary tree that satisifies either:
   1. For max-heap, all children \<= parent
   2. For min-heap, all children \>= parent
3. Starting max-heap
Node 100 has two children, so swap with largest child 30
```
     ___100__
    /        \
  _20         30
 /   \       /
10    5     6
```
Node 100 has one child, so swap with child 6
```
     ___30___
    /        \
  _20        100
 /   \      /
10    5    6
```
Node 100 has no child, so delete
```
     ___30____
    /         \
  _20         _6
 /   \       /
10    5    100
```
Resultant max-heap
```
     ___30
    /     \
  _20      6
 /   \
10    5
```
4. Swapping node 20 and node 30 from previous starting max-heap:
```
     ___100__
    /        \
  _30         20
 /   \       /
10    5     6
```
The resultant max-heap is:
```
  ___30__
 /       \
10        20
  \      /
   5    6
```
This does not preserve completeness property of heap.
Therefore, algorithm does not correctly implement pop operation.
5. Algorithm:
  * Swap root with last element and remove 
  * Until root is \>= both its children, swap it with the largest of its two children and recurse
Starting max-heap
```
     ___100__
    /        \
  _30         20
 /   \       /
10    5     6
```
Swap 100 with 6 and remove
```
     ___6
    /    \
  _30     20
 /   \
10    5
```

6 is \< children. Swap with largest, 30
```
     __30
    /    \
  _6      20
 /  \
10   5
```
6 is \< 10. Swap with 10
```
    ___30
   /     \
  10      20
 /  \
6    5
```

## Question 3
1. 
  * No, e.g: day 1 [1, 2, 3, 4], day 2 [5, 6], day 3 [7], day 4 [8], day 5 [9], day 6 [10]
  * Yes, e.g: day 1 [1, 2, 3, 4, 5], day 2 [6, 7], day 3 [8, 9], day 4 [10]
2. As truck can carry all packages in a single day, and K \>= 1
3. Algorithm:
  * Iterate over all packages and maintain a running sum of their weights
  * If the current package weight added to the running sum exceeds C, add one to required delivery days
    Otherwise, add to the running sum and proceed to next package
  * Once iterated over all packages, if required delivery days is <= K, it's possible to deliver
  Correctness:
  Time Complexity:
4. 
  * We know that the best possible scenario for minimising C is if all packages are the same weight.
    In this case, `C = sum(packages) / K`
  * We know that from question 2, `C = sum(packages)` is an hard upper limit
  * Therefore, as we have an upper and lower bound to the solution, binary search is feasible
5. Algorithm:
  * Perform a binary search as stated in part 3.4, to obtain a possible C.
  * Input this value of C into the algorithm stated in part 3.3
  * If the algorithm indicates not possible, then pick larger C via binary search. 
    Otherwise if possible, record capacity value. 
  * Then run algorithm again with smaller C obtained via binary search.
    If still possible to deliver, overwrite previous C value and continue until not possible.
  Correctness:
  Time Complexity:
  * Binary search is `O(log(n))`. Algorithm to check if delivery possible is `O(n)`.
    Therefore, `O(log(n)) · O(n) = `O(nlog(nM))`








The general rule of thumb is that algorithms introduced in this course (in either the lectures, tutorial, problem sets) does not need citation - 
simply citing which slide / problem set number (question #) is typically enough

Include diagrams as long as accompanied by written explanation.

A non-trivial example is essentially one with more than one value - you should try to include at least 3 values in the heap.

You can include pseudocode as a supplement to an otherwise complete response, but it is never necessary to do so.

You may wish to have separate sections for the algorithm, proof and time complexity, or you could combine them; and you may wish to describe your algorithm in paragraphs, dot points/numbered lists, or a mix of both.

1. 

```
Initially all m ∈ M and w ∈ W are free
While there is a man m who is free and hasn’t proposed to
every woman
Choose such a man m
Let w be the highest-ranked woman in m ’s preference list
to whom m has not yet proposed
If w is free then
(m, w) become engaged
Else w is currently engaged to m'
If w prefers m'  to m then
m remains free
Else w prefers m to m'
(m, w) become engaged
m' becomes free
Endif
Endif
Endwhile
Return the set S of engaged pairs
```

NOTE: Final exam probably on lab computers
