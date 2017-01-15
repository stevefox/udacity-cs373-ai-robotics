# ----------
# User Instructions:
#
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space
from collections import deque
import copy


grid = [[0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1
delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']


def in_grid(grid, pos):
    i = pos[0]
    j = pos[1]
    if i < 0 or j < 0:
        return False
    if i >= len(grid) or j >= len(grid[0]):
        return False
    return True


def apply_move(pos, move):
    return [pos[0] + move[0],
            pos[1] + move[1]]


def position_equal(pos1, pos2):
    if pos1[0] != pos2[0] or pos1[1] != pos2[1]:
        return False
    else:
        return True


def is_occupied(grid, pos):
    return grid[pos[0]][pos[1]]


def is_visited(grid, pos):
    return is_occupied(grid, pos)


def grid_copy(grid):

    g2 = []
    for row in grid:
        g2.append(copy.deepcopy(row))
    return g2


def grid_invert(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]:
                grid[i][j] = -1
    return grid


def get_path(node):
    """Walk up the tree to produce the final path to goal"""
    path = deque([[node[0], node[1], node[4]], ])

    parent = node[3]
    while parent[0] != node[0] or parent[1] != node[1]:
        node = parent
        parent = parent[3]
        path.appendleft([node[0], node[1], node[4]])
    return path


def search(grid, init, goal, cost):

    # Shadow copy of grid
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    expansion_grid = [[-1 for row in range(len(grid[0]))]
                      for col in range(len(grid))]

    closed[init[0]][init[1]] = 1
    step_count = -1

    x = init[0]
    y = init[1]
    g = 0

    found = False
    giveup = False

    current = [x, y, g, [init[0], init[1], -1, -1], -1]
    open_ = deque([current, ])

    while not found and not giveup:
        # Resort the list of nodes
        open_ = deque(sorted(open_, key=lambda x: x[2]))
        try:
            current = open_.popleft()
            x = current[0]
            y = current[1]
            g = current[2]
            step_count += 1
            expansion_grid[x][y] = step_count
            print 'Current: {current}'.format(current=[current[0], current[1]])
        except:
            giveup = True
            break
        for idx, move in enumerate(delta):
            neighbor = apply_move([x, y], move)
            if position_equal(neighbor, goal):
                found = True
                x = neighbor[0]
                y = neighbor[1]
                g = g + 1
                parent = current
                move_idx = idx
                step_count += 1
                expansion_grid[goal[0]][goal[1]] = step_count
                found_goal = [x, y, g, parent, move_idx]
                break
            if in_grid(grid, neighbor) and \
               not is_visited(closed, neighbor) and \
               not is_occupied(grid, neighbor):
                # I would rather this be a reference/pointer to the
                # actual current object, but I am not certain how to
                # do this in Python TODO: Do this in Python
                parent = current
                open_.append([neighbor[0], neighbor[1], g+1, parent, idx])
                closed[neighbor[0]][neighbor[1]] = 1

    if giveup:
        return 'fail'
    if found:
        for row in expansion_grid:
            print row
        path = get_path(found_goal)
        return [x, y, g], path


def main():
    shortest_path, path = search(grid, init, goal, cost)
    print 'Path: %s' % (path)
    for node in path:
        grid[node[0]][node[1]] = delta_name[node[2]]
    for row in grid:
        print row


if __name__ == '__main__':
    main()
