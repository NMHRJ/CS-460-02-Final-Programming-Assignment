# Development Log - The Torchbearer

Student Name: Nikhil Maharaj
Student ID: 828304185


## Entry 1 - 2026-05-12: Initial Plan

I read through the assignment and starter code before writing anything. The problem needs two main things: shortest path distances between all relevant nodes, and then figuring out the best order to visit the relics. Going to implement the Dijkstra part first since the search depends on it. Not sure yet how to handle the pruning but will figure it out as I go.


## Entry 2 - 2026-05-12: Bug in source selection

First draft of select_sources included exit_node as a source which was wrong. The Torchbearer never leaves from the exit so there is no point running Dijkstra from there. Removed it and all tests still passed.

## Entry 3 - 2026-05-12: Backtracking implementation

Implemented _explore with the base case, pruning, branching, and backtracking. Ran into an issue where best[1] was getting corrupted because I stored the list reference instead of a copy. Fixed it by copying the list when updating best. All four provided tests pass including the unreachable-exit case.


## Entry 4 - 2026-05-14: Post-Implementation Reflection

All tests pass. If I had more time I would improve the lower bound in the _explore since right now it only looks at the next hop and ignores the rest of the route. I think the backtracking approach could also get slow on larger inputs with many relics but for the scale of this assignment it works fine


## Final Entry - 2026-05-14: Time Estimate

| Part | Estimated Hrs |
|---|---|
| Part 1: Problem Analysis | 0.5 |
| Part 2: Precomputation Design | 1 |
| Part 3: Algorithm Correctness | 0.75 |
| Part 4: Search Design | 0.5 |
| Part 5: State and Search Space | 0.75 |
| Part 6: Pruning | 1 |
| Part 7: Implementation | 2 |
| README and DEVLOG writing | 1 |
| Total | 7.5 |
