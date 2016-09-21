from course_provided_functions_03 import robot
from math import pi


def run_robot():
    myrobot = robot()
    myrobot.set(30., 50., pi/2.)
    myrobot = myrobot.move(-pi/2., 0.)
    myrobot = myrobot.move(0., 15.)
    sense1 = myrobot.sense()
    myrobot = myrobot.move(-pi/2., 0.)
    myrobot = myrobot.move(0., 10.)
    sense2 = myrobot.sense()

    return [sense1, sense2]
