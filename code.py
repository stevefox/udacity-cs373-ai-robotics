import copy

def uniform_v(n):
    return [1.0/n]*n


def sense(p, Z):
    q = [0]*len(p)
    q_sum = 0
    for i in range(len(p)):
        if world[i] == Z:
            q[i] = p[i]*pHit
        else:
            q[i] = p[i]*pMiss
        q_sum += q[i]
    for i in range(len(q)):
        q[i] /= q_sum
    return q


def circular_shift(p, U):
    shift = -1*(U % len(p))
    if isinstance(p, list):
        q = p[shift:] + p[:shift]
    else:
        raise Exception("Not implemented")
    return q


def move(p, U):

    move = [0]*len(p)
    move[0] = pExact
    move[1] = pOvershoot
    move[-1] = pUndershoot

#    measured_movement = circular_shift(move, U)
    measured_movement = move
    # Implement 1D circular convolution for movement
    q = [0]*len(p)
    N = len(p)
    for m in range(len(p)):
        for i in range(len(measured_movement)):
            q[i] += p[m]*measured_movement[(i-m-U) % N]

    return q


def update(q, measurement, motion):
    q = sense(q, measurement)
    q = move(q, motion)
    return q


def simulate(p, measurements, motions):
    q = copy.deepcopy(p)
    for i in range(len(measurements)):
        q = update(q, measurements[i], motions[i])
    return q


def main():
    # World size
    n = 5
    global world
    global pHit
    global pMiss
    global pExact
    global pOvershoot
    global pUndershoot
    world = ['green', 'red', 'red', 'green', 'green']
    pHit = 0.6
    pMiss = 0.2
    pExact = 0.8
    pOvershoot = 0.1
    pUndershoot = 0.1
    Z = 'red'

    #p = uniform_v(n)
    p = [0, 0.5, 0, 0.5, 0]

    measurements = ['red', 'red']
    motions = [1, 1]

    p = simulate(p, measurements, motions)
    print p


if __name__ == '__main__':
    main()
