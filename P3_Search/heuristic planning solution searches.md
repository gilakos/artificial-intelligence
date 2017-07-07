
# heuristic planning solution searches

## Problem 1

```
(aind) GILs-MacBook-Pro:P3_Search gilakos$ python run_search.py -p 1 -s 8

Solving Air Cargo Problem 1 using astar_search with h_1...

Expansions   Goal Tests   New Nodes
    55          57         224    

Plan length: 6  Time elapsed in seconds: 0.033768467998015694
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P1, SFO, JFK)
Fly(P2, JFK, SFO)
Unload(C1, P1, JFK)
Unload(C2, P2, SFO)
```

## Problem 2

```
(aind) GILs-MacBook-Pro:P3_Search gilakos$ python run_search.py -p 2 -s 8

Solving Air Cargo Problem 2 using astar_search with h_1...

Expansions   Goal Tests   New Nodes
   4852        4854       44030   

Plan length: 9  Time elapsed in seconds: 11.055724150999595
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Load(C3, P3, ATL)
Fly(P1, SFO, JFK)
Fly(P2, JFK, SFO)
Fly(P3, ATL, SFO)
Unload(C3, P3, SFO)
Unload(C2, P2, SFO)
Unload(C1, P1, JFK)
```

## Problem 3

```
(aind) GILs-MacBook-Pro:P3_Search gilakos$ python run_search.py -p 3 -s 8

Solving Air Cargo Problem 3 using astar_search with h_1...

Expansions   Goal Tests   New Nodes
  18235       18237       159716  

Plan length: 12  Time elapsed in seconds: 49.89944749700226
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)
Fly(P2, ORD, SFO)
Fly(P1, ATL, JFK)
Unload(C4, P2, SFO)
Unload(C3, P1, JFK)
Unload(C2, P2, SFO)
Unload(C1, P1, JFK)
```