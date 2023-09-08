<!-- SPDX-License-Identifier: zlib-acknowledgement -->

1.
Let x be activity starting last
Let S be another optimal solution not containing x
Let y be an activity in S that starts last

x must start later than y
now, y can be replaced with x as x will similarly not conflict with anything y doesn't conflict with
therefore, choosing x instead of y will still yield same number of activities
as a result, can iteratively transform S into a new schedule that contains the activity that starts last 

e. and f. work

2.
Let i be ith job in S
Let p(i) be processing time for i
Let c(s) be total time for S

Inversion is i, j where p(i) > p(j)
Greedy will not have inversion

less inversions in schedule is more optimal

(prooving that inversion exists between adjacent jobs)

Let x and y be non-adjacent jobs that form inversion
If x before y, p(x) > p(y)
x + 1 will not be y as non-adjacent
  - p(x) > p(x + 1); inversion
  - p(x) < p(x + 1); then x+1 and y form closer inversion
    * x + 1 and y are adjacent, then inversion
    * x + 1 and y are not adjacent; repeat argument with x+1 and y (as inversion will eventually appear at y-1, y)

Now argue that a schedule with less inversions is more optimal:
Consider a schedule S with job i that violates greedy schedule
Therefore, job i will have an inversion in S, j, such that p(i) > p(j)
So there exists an inversion between adjacent jobs

Consider another schedule S', which is given by swapping jobs i and i+1 in S
As we have swapped, have 1 less inversion than in S

c(S) - c(S') = p(i) - p(i + 1) > 0 (as p(i) > p(i + 1))
c(S) > c(S')
S' has one less inversion, we can repeat for each inversion in S
Because our greedy solution has no inversions, must be optimal
