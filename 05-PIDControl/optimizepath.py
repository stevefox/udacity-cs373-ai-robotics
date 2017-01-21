import copy
import matplotlib.pyplot as plt
import math


path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]


def copy_path(path):
    new_path = [copy.deepcopy(i) for i in path]
    return new_path


def compare_path(path1, path2):
    assert len(path1) == len(path2)

    error_vector = [0 for i in range(len(path1))]
    total_error = 0

    zipped_path = [(path1[i], path2[i]) for i in range(len(path1))]

    for index, point in enumerate(zipped_path):
        # Compute the distance between each point
        p = point[0]
        q = point[1]

        error = 0
        for coord in range(len(p)):
            error += (p[coord] - q[coord])**2
        error = math.sqrt(error)
        error_vector[index] = error
        total_error += error

    return total_error, error_vector


def smooth(path, weight_data=0.5, weight_smooth=0.1, tolerance=0.0001, keep_history=True):
    """Take a path defined by discrete grid cells and return a turn path of x, y coordinates"""

    # Initialize
    new_path = copy_path(path)
    error = 100

    history = []

    iterations = 0

    while error > tolerance:
        last_path = copy_path(new_path)
        # For each step in the path
        for i, j in enumerate(new_path[1:-1]):
            # For each coordinate/dimension
            for k in range(len(new_path[i+1])):
                new_path[i+1][k] += \
                    weight_data*(path[i+1][k] - new_path[i+1][k]) + \
                    weight_smooth*(new_path[i][k] +
                                   new_path[i+2][k] -
                                   2.0*new_path[i+1][k])
            # Optionally store each step of the path for debugging
            if keep_history:
                history.append(copy.deepcopy(new_path))
            error, _ = compare_path(last_path, new_path)
            print 'Error is: %s' % (error)
    return new_path, history


def plot_path(plt, path):
    """Plot path onto plot"""

    x = [i[0] for i in path]
    y = [i[1] for i in path]

    plt.plot(x, y, linewidth=2.0)

    return plt


if __name__ == '__main__':
    new_path, history = smooth(path)
    print 'iterations: %s' % (len(history))
    print new_path[1:-1]
    plt.axis([-1, 5, -1, 5])

    plot_path(plt, path)
    plot_path(plt, new_path)

    plt.savefig('test.png')
    plt.show()
