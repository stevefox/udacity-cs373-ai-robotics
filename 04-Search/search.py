from collections import deque

# Grid format:
#   0 = navigable
#   1 = occupied
grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0],
         [0, -1],
         [1, 0],
         [0, 1]]

delta_name = ['^', '<', 'v', '>']


def in_grid(i, j, max_y, max_x):
    if i >= 0 and i <= max_y:
        if j >= 0 and j <= max_x:
            return True
    return False


def apply_move(pos, move):
    return [pos[0] + move[0],
            pos[1] + move[1]]


def position_equal(pos1, pos2):
    if pos1[0] != pos2[0] or pos1[1] != pos2[1]:
        return False
    else:
        return True

def search(grid, init, goal, cost=lambda x: 1):
    """Finds an optimal path using BFS.

    Parameters
    ----------
    grid : [[]]
        The map. 1 indicates occupied by an obstacle, 0 otherwise.
    init : [row(int), col(int)]
        Row and column of initial position in grid.
    goal : [row(int), col(int)]
        Coordinates of goal in grid.
    cost : callable(row, col)
        Cost function

    Returns
    -------
    list
        [optimal path length (int), row (int), col (int)]
    """

    open_ = deque([[0, 0, 0], ])
    visited = []
    expand = []

    while not position_equal(current, goal):
        open_.
    
if __name__ == '__main__':

    m = search(grid, init, goal, cost)
    for row in m:
        print row
