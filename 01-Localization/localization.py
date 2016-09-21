import copy

colors = [['green', 'green', 'green'],
          ['green', 'red', 'red'],
          ['green', 'green', 'green']]


def init_grid(n, m, initial=0.0):
    q = []
    for i in range(n):
        q.append(copy.deepcopy([initial]*m))
    return q


def uniform_map(n, m):
    """Initialize a 2D map with uniform random proability

    Returns:
       list of lists (n x m)
    """
    p_init = 1.0/(n*m)
    q = init_grid(n, m, initial=p_init)
    return q


def format_map(p):
    result = ''
    for i in p:
        formatted_list = ['%.2f' % v for v in i]
        result += '%s\n' % formatted_list
    return result


def copy_map(p):
    q = []
    for i in range(len(p)):
        q.append(copy.deepcopy(p[i]))
    return q


def sense(p, Z, world, sensor_right):
    q = init_grid(len(p), len(p[0]))

    total_sum = 0.0

    for i in range(len(p)):
        for j in range(len(p[0])):
            hit = int(Z == world[i][j])
            value = p[i][j]*(hit*sensor_right + (1-hit)*(1-sensor_right))
            total_sum += value
            q[i][j] += value

    for i in range(len(q)):
        for j in range(len(q[0])):
            q[i][j] /= total_sum
    return q


def move(p, U, p_move):
    q = init_grid(len(p), len(p[0]))
    move = init_grid(len(p), len(p[0]))

    # Construct move filter
    if U[0] == 0 and U[1] == 0:
        return p

    move[U[0]][U[1]] = p_move
    move[0][0] = 1-p_move

    format_map(move)
    format_map(p)
    for i in range(len(p)):
        for j in range(len(p[0])):
            for m in range(len(move)):
                M = len(move)
                for n in range(len(move[m])):
                    N = len(move[m])
                    value = move[m][n]*p[(i-m) % M][(j-n) % N]
                    q[i][j] += value

    return q


def localize(colors, measurements, motions, sensor_right, p_move):
    """Sense and Move localization

    """
    p = uniform_map(len(colors), len(colors[0]))

    for i in range(len(measurements)):
        p = move(p, motions[i], p_move)
        p = sense(p, measurements[i], colors, sensor_right)

    return p


def main():
    measurements = ['red', 'red']
    motions = [[0, 0], [0, 1]]
    p_sensor_correct = 1.0
    p_move = 0.5
    print format_map(localize(colors,
                              measurements,
                              motions,
                              p_sensor_correct,
                              p_move))

if __name__ == '__main__':
    main()
