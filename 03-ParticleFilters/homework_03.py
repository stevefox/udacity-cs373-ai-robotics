from math import *
import random
import unittest

# --------
#
# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
#
# NOTE: Landmark coordinates are given in (y, x) form and NOT
# in the traditional (x, y) format!

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"
max_steering_angle = pi/4 # You don't need to use this value, but it is good to keep in mind the limitations of a real car.

# ------------------------------------------------
#
# this is the robot class
#

class robot:

    # --------

    # init:
    #	creates robot and initializes location/orientation
    #

    def __init__(self, length = 10.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
    # --------
    # set:
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)


    # --------
    # set_noise:
    #	sets the noise parameters
    #

    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    ############# ONLY ADD/MODIFY CODE BELOW HERE ###################

    # --------
    # move:
    #   move along a section of a circular path according to motion
    #

    def move(self, motion): # Do not change the name of this function

        TURNING_ANGLE_THRESHOLD = 0.001

        # Apply noise
        steering = motion[0] + random.gauss(0.0, self.steering_noise)
        distance = motion[1] + random.gauss(0.0, self.distance_noise)
        
        turning_angle = distance/self.length*tan(steering)

        if abs(turning_angle) > TURNING_ANGLE_THRESHOLD:
            # Bicycle model for motion
            R = distance/turning_angle
            cx = self.x - sin(self.orientation)*R
            cy = self.y + cos(self.orientation)*R
            x = cx + sin(self.orientation + turning_angle)*R
            y = cy - cos(self.orientation + turning_angle)*R
        else:
            # Approximate by straight line motion
            x = self.x + distance*cos(self.orientation)
            y = self.y + distance*sin(self.orientation)
        orientation = (self.orientation + turning_angle) % (2.0*pi)
        result = robot(self.length)
        result.set(x, y, orientation)
        result.set_noise(self.bearing_noise,
                         self.steering_noise,
                         self.distance_noise)
        # make sure your move function returns an instance
        # of the robot class with the correct coordinates.
        return result

    ############## ONLY ADD/MODIFY CODE ABOVE HERE ####################


class TestRobot(unittest.TestCase):

    def test_deterministic_move(self):
        motions = [[0.0, 10.0], [pi / 6.0, 10], [0.0, 20.0]]
        length = 20.0
        myrobot = robot(length)
        bearing_noise = 0.0
        steering_noise = 0.0
        distance_noise = 0.0
        myrobot.set(0.0, 0.0, 0.0)
        myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

        state = []
        state.append([myrobot.x, myrobot.y, myrobot.orientation])
        for i in range(len(motions)):
            myrobot = myrobot.move(motions[i])
            state.append([myrobot.x, myrobot.y, myrobot.orientation])
        expected_state = [[0.0, 0.0, 0.0],
                          [10.0, 0.0, 0.0],
                          [19.861, 1.4333, 0.2886],
                          [39.034, 7.1270, 0.2886]]
        for i in range(len(expected_state)):
            for j, k in zip(state[i], expected_state[i]):
                self.assertTrue(abs(j-k) < 0.001)

    def test_deterministic_move2(self):

        motions = [[0.2, 10.] for row in range(10)]
        length = 20.0
        myrobot = robot(length)
        bearing_noise = 0.0
        steering_noise = 0.0
        distance_noise = 0.0
        myrobot.set(0.0, 0.0, 0.0)
        myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

        state = []
        state.append([myrobot.x, myrobot.y, myrobot.orientation])
        for i in range(len(motions)):
            myrobot = myrobot.move(motions[i])
            state.append([myrobot.x, myrobot.y, myrobot.orientation])

        expected_state = [[0.0, 0.0, 0.0],
                          [9.9828, 0.5063, 0.1013],
                          [19.863, 2.0201, 0.2027],
                          [29.539, 4.5259, 0.3040],
                          [38.913, 7.9979, 0.4054],
                          [47.887, 12.400, 0.5067],
                          [56.369, 17.688, 0.6081],
                          [64.273, 23.807, 0.7094],
                          [71.517, 30.695, 0.8108],
                          [78.027, 38.280, 0.9121],
                          [83.736, 46.485, 1.0135]]

        for i in range(len(expected_state)):
            for j, k in zip(state[i], expected_state[i]):
                self.assertTrue(abs(j-k) < 0.001)

    def test_deterministic_move2(self):

        motions = [[0.2, 10.] for row in range(10)]
        length = 20.0
        myrobot = robot(length)
        bearing_noise = 0.05
        steering_noise = 0.05
        distance_noise = 1.0
        myrobot.set(0.0, 0.0, 0.0)
        myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

        state = []
        state.append([myrobot.x, myrobot.y, myrobot.orientation])
        for i in range(len(motions)):
            myrobot = myrobot.move(motions[i])
            state.append([myrobot.x, myrobot.y, myrobot.orientation])

        expected_state = [[0.0, 0.0, 0.0],
                          [9.9828, 0.5063, 0.1013],
                          [19.863, 2.0201, 0.2027],
                          [29.539, 4.5259, 0.3040],
                          [38.913, 7.9979, 0.4054],
                          [47.887, 12.400, 0.5067],
                          [56.369, 17.688, 0.6081],
                          [64.273, 23.807, 0.7094],
                          [71.517, 30.695, 0.8108],
                          [78.027, 38.280, 0.9121],
                          [83.736, 46.485, 1.0135]]

        for i in range(len(expected_state)):
            for j, k in zip(state[i], expected_state[i]):
                self.assertTrue(abs(j-k) < 0.001)

                
if __name__ == '__main__':
    unittest.main()
