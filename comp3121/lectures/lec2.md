<!-- SPDX-License-Identifier: zlib-acknowledgement -->
multiplication of polynomials faster than large numbers? (don't need as many large integer multiplications, as are computing coefficients)
multiplying two polynomials of degree 2 gives degree 4
splitting into 3 sections with polynomials faster than Karatsuba

although asymoptotically faster slicing into smaller pieces, constants (i.e. coefficients) grow very fast, e.g. 1million·n or 10^8·n etc.
so, most always know what constants are. 
not enough to just look at asymptotic to say faster than another

TODO: warden puzzle write-up

eigenvector used to google page rank algorithm?

## Greedy Method (lots of combinatorial problems?)
chooses choice which assumes is best at that time (dynamic programming is more global?)
greedy most useful technique for solving problem? 

Activity Selection (pick largest number of non-conflicting activities):
greedy with respect to time, i.e picking shortest activity is suboptimal
greedy with respect to least conflicts is suboptimal
working left to right, greedy with respect to earliest finishing time is optimal
*Greedy Proof 1*: proof exchange argument (show that any allegedely better solution can be morphed into our greedy solution)
we know that at any stage, any better solution activity can be replaced with greedy solution
as anything on right we know won't conflict with (as earlier)
O(nlogn) as sort by earliest finishing time

Petrol Stations:
pick furthest petrol station from where at
*Greedy Proof 2*: proof greedy stays ahead (no other solution beats greedy at any stage)

Cell Towers:
Start from first house not covered. place tower 5km from that house. repeat
proof exchange: any solution can be shifted

Minimising Job Lateness:
sort jobs in increasing order of deadlines

suppose alternative solution that pick out-of-order
show that swapping will increase, i.e. will be more optimal
(i.e. swapping adjacent inverted jobs reduces lateness)

Tape Storage:
pick where probability/file-size is smallest
proof: show that optimal solution does not have inversions (subtract lists)

Interval Stabbing:
stab in the interval that ends the earliest at this place

Fractional Knapsack:
Take most valuable per unit weight. However, if don't fill entire knapsack; suboptimal
So, trial and error

TODO: after lectures do practice problems (as reinforce lecture problem solving)

TODO: know what type of greedy to use particular proof

NOTE: seems that for greedy just sort on desired trait?

greedy won't work if local and global maximas?
