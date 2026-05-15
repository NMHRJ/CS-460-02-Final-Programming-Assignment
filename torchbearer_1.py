"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Nikhil Maharaj
Student ID:   828304185


Submit this file as: torchbearer.py
"""

import heapq


# PART 1

def explain_problem():
	return (
		"Why a single shortest-path run from S is not enough: "
		"Dijkstra from S finds the cheapest path to each node individually but "
		"cannot determine the best order to visit all relic chambers.\n\n"
		"What decision remains after all inter-location costs are known: "
		"We must still choose the ordering in which to visit the relic chambers.\n\n"
		"Why this requires a search over orders: "
		"No greedy rule reliably produces the optimal visit sequence so the "
		"algorithm must explore candidate orderings and prune those that cannot "
		"beat the best found so far."
	)


# PART 2
def select_sources(spawn, relics, exit_node):
	sources = set()
	sources.add(spawn)
	for r in relics:
		sources.add(r)
	# exit_node excluded: Torchbearer never departs from the exit
	return list(sources)


def run_dijkstra(graph, source):
	dist = {node: float('inf') for node in graph}
	dist[source] = 0
	heap = [(0, source)]

	while heap:
		current_cost, u = heapq.heappop(heap)
		if current_cost > dist[u]:
			continue
		for v, edge_cost in graph[u]:
			new_cost = dist[u] + edge_cost
			if new_cost < dist[v]:
				dist[v] = new_cost
				heapq.heappush(heap, (new_cost, v))

	return dist


def precompute_distances(graph, spawn, relics, exit_node):
	sources = select_sources(spawn, relics, exit_node)
	dist_table = {}
	for src in sources:
		dist_table[src] = run_dijkstra(graph, src)
	return dist_table


# PART 3

def dijkstra_invariant_check():
	return (
		"Part 3a: For finalized nodes, dist[v] is the exact shortest-path distance "
		"from the source and will never change. For non-finalized nodes, dist[u] is "
		"the cheapest path found whose intermediate nodes all lie in S.\n\n"
		"Part 3b: Initialization: only source in S with dist=0. "
		"All others are inf. maintenance: we extract the non-finalized node u with "
		"minimum dist[u]. Because all edge weights are nonnegative, any path to u through "
		"a non-finalized node costs at least as much, so finalizing u is safe. "
		"Termination: when the heap empties every reachable node is finalized and "
		"dist[v] is the true shortest-path distance.\n\n"
		"Part 3c: Incorrect distances would cause the planner to either discard the "
		"optimal relic ordering or select a suboptimal one."
	)


# PART 4

def explain_search():
	return (
		"Greedy fails as always choosing the nearest unvisited relic commits to a "
		"locally cheap hop without considering how that constrains future legs. "
		"Example from spec: S->B costs 1 (greedy will pick), then B->D->C->T costs "
		"1+1+100=102 and the total is 103. Optimal is S->B->D->C->T = 1+1+1+1 = 4. Greedy "
		"picks B first and forces the D->T leg (expensive).\n\n"
		"What the algorithm must explore: every possible order in which to visit the "
		"relic chambers, pruning partial orders that cannot beat the best found so far."
	)


# PARTS 5 + 6

def find_optimal_route(dist_table, spawn, relics, exit_node):
	relics_remaining = set(relics)
	best = [float('inf'), []]

	_explore(
		dist_table=dist_table,
		current_loc=spawn,
		relics_remaining=relics_remaining,
		relics_visited_order=[],
		cost_so_far=0.0,
		exit_node=exit_node,
		best=best,
	)

	return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
	# base case: all relics collected, try to reach exit
	if not relics_remaining:
		cost_to_exit = dist_table[current_loc].get(exit_node, float('inf'))
		total_cost = cost_so_far + cost_to_exit
		if total_cost < best[0]:
			best[0] = total_cost
			best[1] = list(relics_visited_order)
		return

	# lower bound: cheapest single hop from here to any remaining relic.
	# safe to prune as shortest-path distances never overestimate true
	# travel cost so if even the cheapest next hop plus cost so far cannot
	# beat best[0] and no completion of this branch can either.
	lower_bound = min(
		dist_table[current_loc].get(r, float('inf'))
		for r in relics_remaining
	)

	if cost_so_far + lower_bound >= best[0]:
		return

	for next_relic in list(relics_remaining):
		travel_cost = dist_table[current_loc].get(next_relic, float('inf'))
		if travel_cost == float('inf'):
			continue
		new_cost = cost_so_far + travel_cost
		if new_cost >= best[0]:
			continue

		relics_remaining.remove(next_relic)
		relics_visited_order.append(next_relic)

		_explore(
			dist_table=dist_table,
			current_loc=next_relic,
			relics_remaining=relics_remaining,
			relics_visited_order=relics_visited_order,
			cost_so_far=new_cost,
			exit_node=exit_node,
			best=best,
		)

		relics_visited_order.pop()
		relics_remaining.add(next_relic)


# PIPELINE

def solve(graph, spawn, relics, exit_node):
	dist_table = precompute_distances(graph, spawn, relics, exit_node)
	return find_optimal_route(dist_table, spawn, relics, exit_node)


# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.

def _run_tests():
	print("Running provided tests...")

	# Test 1: Spec illustration. Optimal cost = 4.
	graph_1 = {
		'S': [('B', 1), ('C', 2), ('D', 2)],
		'B': [('D', 1), ('T', 1)],
		'C': [('B', 1), ('T', 1)],
		'D': [('B', 1), ('C', 1)],
		'T': []
	}
	cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
	assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
	print(f"  Test 1 passed  cost={cost}  order={order}")

	# Test 2: Single relic. Optimal cost = 5.
	graph_2 = {
		'S': [('R', 3)],
		'R': [('T', 2)],
		'T': []
	}
	cost, order = solve(graph_2, 'S', ['R'], 'T')
	assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
	print(f"  Test 2 passed  cost={cost}  order={order}")

	# Test 3: No valid path to exit. Must return (inf, []).
	graph_3 = {
		'S': [('R', 1)],
		'R': [],
		'T': []
	}
	cost, order = solve(graph_3, 'S', ['R'], 'T')
	assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
	print(f"  Test 3 passed  cost={cost}")

	# Test 4: Relics reachable only through intermediate rooms.
	# Optimal cost = 6.
	graph_4 = {
		'S': [('X', 1)],
		'X': [('R1', 2), ('R2', 5)],
		'R1': [('Y', 1)],
		'Y': [('R2', 1)],
		'R2': [('T', 1)],
		'T': []
	}
	cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
	assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
	print(f"  Test 4 passed  cost={cost}  order={order}")

	# Test 5: Explanation functions must return non-placeholder strings.
	for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
		result = fn()
		assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
			f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
	print("  Test 5 passed  explanation functions are non-empty")

	print("\nAll provided tests passed.")


if __name__ == "__main__":
	_run_tests()
