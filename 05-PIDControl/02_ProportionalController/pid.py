# -----------
# User Instructions
#
# Implement a P controller by running 100 iterations
# of robot motion. The desired trajectory for the
# robot is the x-axis. The steering angle should be set
# by the parameter tau so that:
#
# steering = -tau * crosstrack_error
#
# Note that tau is called "param" in the function
# below.
#
# Your code should print output that looks like
# the output shown in the video. That is, at each step:
# print myrobot, steering
#
# Only modify code at the bottom!
# ------------

from math import *
import random
import numpy as np
import matplotlib.pyplot as plt


def plot(history):

    X_IDX = 0
    Y_IDX = 1
    HEADING_IDX = 2
    STEERING_IDX = 3
    CROSSTRACK_ERROR = 4

    labels = ['X pos', 'Y pos', 'Heading', 'Steering', 'Error', 'Last Error', 'Tail of L2 Error']

    idx = np.arange(history.shape[0])
    variable_count = history.shape[1]

    plt.figure(1)

    for i in range(variable_count):
        ax = plt.subplot(variable_count, 1, i+1)
        ax.plot(idx, history[:, i])
        ax.set_title(labels[i])

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

# ------------------------------------------------
#
# this is the robot class
#

class robot:

    # --------
    # init:
    #    creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length = 20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    # --------
    # set:
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)


    # --------
    # set_noise:
    #	sets the noise parameters
    #

    def set_noise(self, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # set_steering_drift:
    #	sets the systematical steering drift parameter
    #

    def set_steering_drift(self, drift):
        self.steering_drift = drift

    # --------
    # move:
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative

    def move(self, steering, distance,
             tolerance = 0.001, max_steering_angle = pi / 4.0):

        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0


        # make a new copy
        res = robot()
        res.length         = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = tan(steering2) * distance2 / res.length

        if abs(turn) < tolerance:

            # approximate by straight line motion

            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2.0 * pi)

        else:

            # approximate bicycle model for motion

            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)

        return res

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)

############## ADD / MODIFY CODE BELOW ####################

# ------------------------------------------------------------------------
#
# run - does a single control run


def run(p_param, i_param=0.0, d_param=0.0, N=100):
    """This defines a control law governed by the following rule:

    steering = -tau * crosstrack_error

    This is a (P)roportional Controller of steering angle which
    minimizes the crosstrack_error. For simplicity in this exercise,
    our reference trajectory is defined as the positive x-axis, so the
    robot's y-coordinate is equal to the crosstrack_error.

    Steering is the derivative of orientation

    """
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    myrobot.set_steering_drift(10.0 / 180.0 * pi) # 10 degree bias, this will be added in by the move function, you do not need to add it below!


    # motion distance is equal to speed (we assume time = 1)
    speed = 1.0

    history = None

    # Set up Controller and initial conditions
    d = 0.0
    i = 0.0
    y_ref = 0.0
    int_l2_error = 0.0
    last_e = myrobot.y - y_ref

    for k in range(N):
        e = myrobot.y - y_ref
        d = e - last_e
        i += e
        steer = - p_param*e \
                - d_param*d \
                - i_param*i

        # Record the l2 error
        int_l2_error += (e**2)

        # Note saturation effects are modeled inside of robot.move
        myrobot = myrobot.move(steer, speed)
        state = [
            myrobot.x,
            myrobot.y,
            myrobot.orientation,
            steer,
            e,
            last_e,
            int_l2_error
        ]
        last_e = e
        if history is None:
            history = np.array([state])
        else:
            history = np.vstack([history, state])

    return history


def plot_path(x_coords, y_coords):
    plt.figure(2)
    plt.plot(x_coords, y_coords, 'bo')


def get_err(p):
    return p[-2]


def twiddle(threshold=0.2, algorithm=None):
    """Local hillcliming algorithm

    Algorithm must be a callable that returns an error
    """
    p = [0.0, 0.0, 0.0]
    dp = [1.0 for j in range(len(p))]

    def get_err(p):
        return algorithm(p)

    best_err = get_err(p)

    while sum(dp) > threshold:
        for i in range(len(p)):
            p[i] += dp[i]
            err = get_err(p)
            if err < best_err:
                best_err = err
                # Keep p and increment step size
                dp[i] *= 1.1
            else:
                # Case two: no improvement, try the other direction
                p[i] -= 2*dp[i]
                err = get_err(p)
                if err < best_err:
                    best_err = err
                    # Keep p and decrement dp
                    dp[i] *= 0.9
                else:
                    # Neither one shows improvement, so go back to
                    # where we started and decrease the step size
                    p[i] += dp[i]
                    dp[i] *= 0.9
    return p, get_err(p)


def twiddle_pid():
    """Auto-tune PID controller using twiddle algorithm."""

    def run_pid(p):
        """Adapter for running the PID controller with our twiddle
        implementation
        """
        history = run(p_param=p[0],
                      i_param=p[1],
                      d_param=p[2], N=100)
        return history[-1, :][6]

    best_param, error = twiddle(threshold=1e-6, algorithm=run_pid)
    print 'Best parameters: %s; error %.3lg' % (best_param, error)
    return best_param


def plot_pid(history, p, i, d, N=100):

    plot(history)
    tag = '{p}-{i}-{d}-{N}'.format(
        p=p,
        i=i,
        d=d,
        N=100)
    plt.savefig('history_{tag}.png'.format(tag=tag))
    plot_path(history[:, 0], history[:, 1])
    plt.savefig('path_{tag}.png'.format(tag=tag))


def get_args():
    import sys
    if len(sys.argv) > 3:
        print sys.argv
        p = float(sys.argv[1])
        i = float(sys.argv[2])
        d = float(sys.argv[3])
    else:
        print >> sys.stderr, 'Usage: pid <p> <i> <d>\n.or\nAuto-tune:\npid twiddle\n'
        p = 0.2
        i = 0.0
        d = 3.0
    params = [p, i, d]
    return params


def simulate_pid(params):

    p = params[0]
    i = params[1]
    d = params[2]

    history = run(
        p_param=p,
        d_param=d,
        i_param=i, N=100) # call function with parameter tau of 0.1 and print results

    return history, params


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'twiddle':
        print 'Auto-tuning pid...'
        p = twiddle_pid()
    else:
        p = get_args()
    history, p = simulate_pid(p)
    plot_pid(history, p=p[0], i=p[1], d=p[2], N=100)
