<!-- SPDX-License-Identifier: zlib-acknowledgement -->
1a.
| Start State | BFS | IDS | Greedy | A\* |
|-------------|-----|-----|--------|----|
| *start1*    |10978|25121|59182|30|
| *start2*    |344890|349380|19|35|
| *start3*    |10978|25121|59182|30|

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


#python3 search.py --start "2634-5178-AB0C-9DEF" --s "bfs"
# [bfs] Generated: 23415. Expanded: 10978. Length: 12. Cost: 12.
#python3 search.py --start "2634-5178-AB0C-9DEF" --s "dfs" --id
# [dfs,id] Generated: 53489. Expanded: 25121. Length: 12. Cost: 12.
#python3 search.py --start "2634-5178-AB0C-9DEF" --s "greedy"
# [greedy] Generated: 127276. Expanded: 59182. Length: 12. Cost: 12.
#python3 search.py --start "2634-5178-AB0C-9DEF" --s "astar"
# [astar] Generated: 60. Expanded: 30. Length: 12. Cost: 12.





1b.




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
