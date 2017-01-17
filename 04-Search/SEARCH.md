In this section we study search algorithms for path finding. For the use of these algorithms, we assume that we have a known, deterministic map as input to the search algorithm.

# Breadth First Search (bfs.py)
We first implement Breadth First Search (BFS) which expands each node in the tree until an optimal path is found. This is implemented in bfs.py.

# Utility Output (expansiongrid.py, printpath.py)
We then write some utility functions to help us print out the output to review the actual path selected and the order in which nodes are expanded.

# A-Star Search (astarsearch.py)
Next we implement an optimization of BFS called A* Search. A* Search is guaranteed to find an optimal path if one exists by using an admissible heuristic function to prune the search tree. Rather than expanding every node of the map as

# Dynamic Programming (dynamicprogramming.py)
Dynamic programming find a path from every cell in the map. This provides a datastructure for implementing a policy, or a preference such as preferring to make left turns when possible. However, since the path from every cell in the map to the goal needs to be computed, the computational requirements are much higher by a factor of N^2 (assuming an N x N discrete map). On the other hand, finding a path from each cell to the goal could be done in parallel independently from the others.
