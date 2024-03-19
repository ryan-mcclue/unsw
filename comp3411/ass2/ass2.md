<!-- SPDX-License-Identifier: zlib-acknowledgement -->
1a.
| Start State | BFS                        | IDS                         | Greedy                    | A\*                     |
|-------------|----------------------------|-----------------------------|---------------------------|-------------------------|
| *start1*    |Expanded: 10978, Length: 12 |Expanded: 25121, Length: 12  |Expanded: 59182, Length: 12|Expanded: 30, Length: 12 |
| *start2*    |Expanded: 344890, Length: 17|Expanded: 349380, Length: 17 |Expanded: 19, Length: 17   |Expanded: 35, Length: 17 |
| *start3*    |Expanded: 641252, Length: 18|Expanded: 1209934, Length: 18|Expanded: 59196, Length: 22|Expanded: 133, Length: 18|

#python3 search.py --start "2634-5178-AB0C-9DEF" --s "bfs"
# [bfs] Generated: 23415. Expanded: 10978. Length: 12. Cost: 12.
#python3 search.py --start "2634-5178-AB0C-9DEF" --s "dfs" --id
# [dfs,id] Generated: 53489. Expanded: 25121. Length: 12. Cost: 12.
#python3 search.py --start "2634-5178-AB0C-9DEF" --s "greedy"
# [greedy] Generated: 127276. Expanded: 59182. Length: 12. Cost: 12.
#python3 search.py --start "2634-5178-AB0C-9DEF" --s "astar"
# [astar] Generated: 60. Expanded: 30. Length: 12. Cost: 12.


#python3 search.py --start "1034-728B-5D6A-E9FC" --s "bfs"
# [bfs] Generated: 734381. Expanded: 344890. Length: 17. Cost: 17.
#python3 search.py --start "1034-728B-5D6A-E9FC" --s "dfs" --id
# [dfs,id] Generated: 743882. Expanded: 349380. Length: 17. Cost: 17.
#python3 search.py --start "1034-728B-5D6A-E9FC" --s "greedy"
# [greedy] Generated: 44. Expanded: 19. Length: 17. Cost: 17.
#python3 search.py --start "1034-728B-5D6A-E9FC" --s "astar"
# [astar] Generated: 80. Expanded: 35. Length: 17. Cost: 17


#python3 search.py --start "5247-61C0-9A83-DEBF" --s "bfs"
# [bfs] Generated: 1365538. Expanded: 641252. Length: 18. Cost: 18.
#python3 search.py --start "5247-61C0-9A83-DEBF" --s "dfs" --id
# [dfs,id] Generated: 2576823. Expanded: 1209934. Length: 18. Cost: 18.
#python3 search.py --start "5247-61C0-9A83-DEBF" --s "greedy"
# [greedy] Generated: 126774. Expanded: 59196. Length: 22. Cost: 22. 
#python3 search.py --start "5247-61C0-9A83-DEBF" --s "astar"
# [astar] Generated: 270. Expanded: 133. Length: 18. Cost: 18.

1b.
BFS is optimal when there are no weights, as is this case here.
Therefore, the length found will always be the smallest possible.
It's an uninformed search, which causes it to expand more nodes than necessary.
This can be seen comparing its number of expanded nodes with that of A\*.
It has exponential space complexity.
IDS is optimal and uninformed like BFS. 
However, as it's a repeated DFS search, it will always expand more nodes than BFS.
This can be seen in comparing the expanded node count between IDS and BFS.
It has more efficient linear space complexity compared to BFS.
Greedy is suboptimal, meaning the length found may not always be the smallest possible.
This can be seen in start state 3.
It's an informed search, with a heuristic estimating the cost to the goal. 
So, it makes decisions in isolation, i.e. no thinking ahead.
As a result, it can potentially expand more nodes than an uninformed search as seen in start state 1.
Or, it could possibly expand less nodes as seen in start state 2.
A\* is an informed search.
It uses a heuristic that estimates the combined cost of reaching the next node and goal.
If this heuristic is admissable, i.e. doesn't overestimate cost, it's optimal.
In most cases, A\* will expand the fewest nodes, as its guided by the most information.




3a.
M(1) = [+,-] 

s,k
1,1
(2, 3, 4)
2,1
(5, 7, 9)
2,2
(6, 8, 9)


M(2) = [+,o,-] 
M(3) = [+,o,o,-]
M(4) = [+,+,-,-] 
M(5) = [+,+,-,o,-]
M(6) = [+,+,o,-,-] (s^2+s+k)?
M(7) = [+,+,o,-,o,-] 
M(8) = [+,+,o,o,-,-] (s^2+k)? s=k=2
M(9) = [+,+,+,-,-,-] (s=2)

M(16) = [+,+,+,+,-,-,-,-] (s+1)^2
