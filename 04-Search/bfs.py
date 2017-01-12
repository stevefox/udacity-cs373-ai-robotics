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


def search(grid, init, goal, cost):

    # Shadow copy of grid
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    x = init[0]
    y = init[1]
    g = 0

    open_ = deque([[x, y, g], ])
    # Algorithm
    # set this flag true if goal is found
    found = False
    # set this flag true if goal is not found and there are no further
    # options to expand
    giveup = False
    while not found and not giveup:
        # Resort the list of nodes
        open_ = deque(sorted(open_, key=lambda x: x[2]))
        try:
            current = open_.popleft()
            x = current[0]
            y = current[1]
            g = current[2]
            print 'Current: {current}'.format(current=current)
        except:
            giveup = True
            break
        for move in delta:
            neighbor = apply_move([x, y], move)
            if position_equal(neighbor, goal):
                found = True
                return [neighbor[0], neighbor[1], g+1]
            if in_grid(grid, neighbor) and \
               not is_visited(closed, neighbor) and \
               not is_occupied(grid, neighbor):
                open_.append([neighbor[0], neighbor[1], g+1])
                closed[neighbor[0]][neighbor[1]] = 1

    if giveup:
        return 'fail'
    else:
        return [x, y, g]


def main():
    print search(grid, init, goal, cost)


if __name__ == '__main__':
    main()
