from course_provided_functions_03 import robot, thrun_resample, eval
import random


def init_filter(count=1000, noise=[0.05, 0.05, 5.0]):
    particles = []
    for i in range(count):
        p = robot()
        p.set_noise(*noise)
        particles.append(p)
    return particles


def update(particles, movement):
    for i in range(len(particles)):
        particles[i] = particles[i].move(movement[0], movement[1])
    return particles


def sense(particles, Z):
    """Update particle filter using measurement

    Args:
      particles - list of "robots" (particles)
    """
    weights = []
    for i in particles:
        weight = i.measurement_prob(Z)
        weights.append(weight)
    return weights


def resample(particles, weights, count=None):
    """This is a terrible resampling implementation.
    
    Do not use it!

    The right way to do this is to take a random step around a unit
    cirlce.
    """
    sample_set = []
    if count is None:
        count = len(particles)
    W = sum(weights)
    for i in range(count):
        choice = random.randint(0, count-1)
        threshold = 1.0
        weight = weights[choice]/W
        while weight < threshold:
            choice = random.randint(0, count-1)
            threshold = random.random()
            weight = weights[choice]/W
        sample_set.append(particles[choice])
    return sample_set


def simulate_filter(size, motions):
    particles = init_filter(size)
    myrobot = robot()
    # Initialize
    resampled = particles
    for i in range(len(motions)):
        particles = resampled
        myrobot.move(*motions[i])
        particles = update(particles, motions[i])
        Z = myrobot.sense()
        weights = sense(particles, Z)
        resampled = thrun_resample(particles, weights)
    return myrobot, particles


if __name__ == '__main__':
    motions = [[0.1, 5.0], [0.1, 5.0]]
    myrobot, p = simulate_filter(1000, motions)
    print eval(myrobot, p)
    
