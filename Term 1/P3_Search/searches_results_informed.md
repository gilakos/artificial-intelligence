# heuristic planning solution searches (informed)

## List of Searches
9. astar_search h_ignore_preconditions
10. astar_search h_pg_levelsum

## Problem 1

```
(aind) GILs-MacBook-Pro:P3_Search gilakos$ python run_search.py -p 1 -s 9

Solving Air Cargo Problem 1 using astar_search with h_ignore_preconditions...

Expansions   Goal Tests   New Nodes
    41          43         170    

Plan length: 6  Time elapsed in seconds: 0.039211472001625225
Load(C1, P1, SFO)
Fly(P1, SFO, JFK)
Unload(C1, P1, JFK)
Load(C2, P2, JFK)
Fly(P2, JFK, SFO)
Unload(C2, P2, SFO)

(aind) GILs-MacBook-Pro:P3_Search gilakos$ python run_search.py -p 1 -s 10

Solving Air Cargo Problem 1 using astar_search with h_pg_levelsum...

Expansions   Goal Tests   New Nodes
    45          47         188    

Plan length: 6  Time elapsed in seconds: 0.9324947230015823
Load(C1, P1, SFO)
Fly(P1, SFO, JFK)
Load(C2, P2, JFK)
Fly(P2, JFK, SFO)
Unload(C1, P1, JFK)
Unload(C2, P2, SFO)
```

## Problem 2

```
(aind) GILs-MacBook-Pro:P3_Search gilakos$ python run_search.py -p 2 -s 9

Solving Air Cargo Problem 2 using astar_search with h_ignore_preconditions...

Expansions   Goal Tests   New Nodes
   1450        1452       13303   

Plan length: 9  Time elapsed in seconds: 4.474345351998636
Load(C3, P3, ATL)
Fly(P3, ATL, SFO)
Unload(C3, P3, SFO)
Load(C2, P2, JFK)
Fly(P2, JFK, SFO)
Unload(C2, P2, SFO)
Load(C1, P1, SFO)
Fly(P1, SFO, JFK)
Unload(C1, P1, JFK)

(aind) GILs-MacBook-Pro:P3_Search gilakos$ python run_search.py -p 2 -s 10

Solving Air Cargo Problem 2 using astar_search with h_pg_levelsum...

Expansions   Goal Tests   New Nodes
   1643        1645       15414   

Plan length: 9  Time elapsed in seconds: 333.07471831899966
Load(C1, P1, SFO)
Fly(P1, SFO, JFK)
Load(C2, P2, JFK)
Fly(P2, JFK, SFO)
Load(C3, P3, ATL)
Fly(P3, ATL, SFO)
Unload(C3, P3, SFO)
Unload(C2, P2, SFO)
Unload(C1, P1, JFK)

```

## Problem 3

```
(aind) GILs-MacBook-Pro:P3_Search gilakos$ python run_search.py -p 3 -s 9

Solving Air Cargo Problem 3 using astar_search with h_ignore_preconditions...

Expansions   Goal Tests   New Nodes
   5040        5042       44944   

Plan length: 12  Time elapsed in seconds: 17.001131807999627
Load(C2, P2, JFK)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)
Fly(P2, ORD, SFO)
Unload(C4, P2, SFO)
Load(C1, P1, SFO)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P1, ATL, JFK)
Unload(C3, P1, JFK)
Unload(C2, P2, SFO)
Unload(C1, P1, JFK)

(aind) GILs-MacBook-Pro:P3_Search gilakos$ python run_search.py -p 3 -s 10

Solving Air Cargo Problem 3 using astar_search with h_pg_levelsum...


Expansions   Goal Tests   New Nodes
   2841        2843       27040   

Plan length: 12  Time elapsed in seconds: 1250.8853138390004
Load(C2, P2, JFK)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)
Fly(P2, ORD, SFO)
Load(C1, P1, SFO)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P1, ATL, JFK)
Unload(C4, P2, SFO)
Unload(C3, P1, JFK)
Unload(C2, P2, SFO)
Unload(C1, P1, JFK)

```