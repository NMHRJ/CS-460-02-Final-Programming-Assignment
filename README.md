# The Torchbearer

Student Name: Nikhil Maharaj
Student ID: 828304185
Course: CS 460 - Algorithms | Spring 2026

## Part 1: Problem Analysis

- Why a single shortest-path run from S is not enough:
  It finds the cheapest path to each node but not the best order to visit all the relics. Knowing the cheapest way to reach relic B does not tell you whether going to C first would be cheaper overall.

- What decision remains after all inter-location costs are known:
  Which order to visit the relic chambers. The pairwise costs do not tell you the best sequence.

- Why this requires a search over orders:
  Because there is no single rule that always picks the right order, you have to try different orderings and keep track of the best one found.


## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Spawn | The route starts here so we need distances from spawn to all relics and the exit. |
| Each relic chamber | After collecting a relic we continue from there, so we need distances from each relic to the others and the exit. |

Exit node is not a source because we only ever travel to it, never from it.

### Part 2b: Distance Storage

| Property | Answer |
|---|---|
| Data structure name | Nested dictionary |
| What the keys represent | Source node |
| What the values represent | A dictionary mapping each destination to the minimum cost from that source |
| Lookup time complexity | O(1) average |
| Why O(1) lookup is possible | Python dicts use hashing so lookup time does not depend on the number of entries |

### Part 2c: Precomputation Complexity

- Number of Dijkstra runs: k + 1 (one for spawn and one per relic)
- Cost per run: O(m log n)
- Total complexity: O(k * m log n)
- Justification: We run Dijkstra at most k + 1 times and each run is O(m log n) so total is O(k * m log n)

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- For nodes already finalized (in S):
  dist[v] is the true shortest-path distance from the source and will not be updated again.

- For nodes not yet finalized (not in S):
  dist[u] is the cheapest path we have found so far, but only counting paths where every intermediate stop is already finalized.

### Part 3b: Why Each Phase Holds

- Initialization:
  Only the source is in S with dist = 0, which is correct since it costs nothing to start there. Everything else is inf because no paths have been explored yet.

- Maintenance:
  We pick the unfinalized node u with the smallest dist[u]. Since all edge weights are nonneg, no path through an unfinalized node can be cheaper, so dist[u] is already final. We then relax u's neighbors.

- Termination:
  When the heap is empty every reachable node has been finalized with its true shortest-path distance. Unreachable nodes stay at inf.


### Part 3c: Why This Matters for the Route Planner

If the distances are wrong the planner might pick a bad relic order or throw out the actual best route, so everything depends on Dijkstra being correct.

## Part 4: Search Design

### Why Greedy Fails

- The failure mode: Greedy picks the nearest unvisited relic each time without looking at how that choice affects the rest of the route.
- Counter-example setup: Entrance S, relics B/C/D, exit T. S->B=1, S->C=2, S->D=2. B->D=1, D->C=1, C->T=1, D->T=100.
- What greedy picks: S->B->D->C->T but then has to pay D->T=100. Total = 103.
- What optimal picks: S->B->D->C->T = 1+1+1+1 = 4.
- Why greedy loses: Picking the cheapest next hop first can force an expensive leg at the end.

### What the Algorithm Must Explore

- The algorithm must try every possible order in which to visit the relic chambers, pruning any partial order whose cost already cannot beat the best complete order found so far.


## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node | Where the Torchbearer is right now |
| Relics already collected | relics_visited_order / relics_remaining | list / set | List tracks the order visited, set tracks what is left |
| Fuel cost so far | cost_so_far | float | Total fuel spent to get to current_loc |

### Part 5b: Data Structure for Visited Relics

| Property | Answer |
|---|---|
| Data structure chosen | Python set |
| Operation: check if relic already collected | O(1) average |
| Operation: mark a relic as collected | O(1) average |
| Operation: unmark a relic (backtrack) | O(1) average |
| Why this structure fits | Add, remove, and membership check are all O(1) which is what backtracking needs. |

### Part 5c: Worst-Case Search Space

- Worst-case number of orders considered: O(k!) where k = |M|
- Why: There are k! ways to order k relics and in the worst case we try all of them.


## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- What is tracked: The minimum total cost found so far and the relic order that produced it, stored in a list called best.
- When it is used: Before going deeper into a branch, and updated whenever a complete route does better than the current best.
- What it allows the algorithm to skip: Any branch where the cost so far plus the lower bound is already at or above best can be dropped entirely.

### Part 6b: Lower Bound Estimation

- What information is available at the current state: current location, relics still to visit, fuel spent so far, and the precomputed distance table.
- What the lower bound accounts for: The cheapest single hop from the current location to any remaining relic.
- Why it never overestimates: It only looks at the next hop and ignores everything after, so it always undercounts the true remaining cost.

### Part 6c: Pruning Correctness

- Since the lower bound never overestimates, if cost_so_far plus the lower bound is already at or above best, then no completion of this branch can do better. Safe to prune.
- The optimal solution will never get pruned because the lower bound only cuts branches that genuinely cannot beat the current best.


## References

- Professor Muralidharan lectures
