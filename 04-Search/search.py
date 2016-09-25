import copy
from collections import deque

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

delta_name = ['^', '<', 'V', '>']


def in_grid(i, j, max_y, max_x):
    if i >= 0 and i <= max_y:
        if j >= 0 and j <= max_x:
            return True
    return False


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


if __name__ == '__main__':
    
    print search(grid, init, goal, cost)
