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
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid, init, goal, cost):

    open_ = deque([[0, 0, 0],])
    visited = []

    max_y = len(grid)
    max_x = len(grid[0])

    while len(open_) > 0:

        active = open_.pop()
        visited.append([active[1], active[2]])

        for move in delta:
            next_step = [active[0] + 1, active[1] + move[0], active[2] + move[1]]
            if next_step[1] < 0 or next_step[1] >= len(grid) or \
               next_step[2] < 0 or next_step[2] >= len(grid[0]):
                continue
            else:
                if [next_step[1], next_step[2]] in visited:
                    continue
                elif grid[next_step[1]][next_step[2]] == 1:
                    # Occupied
                    continue
                elif next_step[1] == goal[0] and next_step[2] == goal[1]:
                    path = next_step
                    return path
                else:
                    open_.append(next_step)

    return 'fail'


def main():
    print search(grid, init, goal, cost)


if __name__ == '__main__':
    main()
