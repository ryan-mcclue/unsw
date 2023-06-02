<!-- SPDX-License-Identifier: zlib-acknowledgement -->
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

