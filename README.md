These are my original solutions to Udacity CS373 Artificial Intelligence for Robotics. I try to implement some unit tests as well to demonstrate the correctness of the algorithms. Proving that these algorithms are safe (not just correctly implemented in software) is not always trivial, and I would recommend consulting a Control Systems expert in the field to understand the challenges and implications for self-driving cars.

Key technologies implemented in this course are:

1. Localization: Given a known map, and a sensor reading (modeled probabilistically with error), determine the locations. The algorithm implemented in this course uses Bayesian localization. This is a multi-modal estimator for a discretely valued variable (position). This harkens back to Professor Thrun's early work on occupancy grids with sonar-based sensing. The problem with sensors is that there is error in the measurements. Sonar can reflect off of surfaces causing erroneous readings or false values, and the return values are distributed in a cone-like shape with the vertex originating from the sonar. Compare sonar to a laser pointer, which functions more like a single point in a ray. There are many types of sensors, and this algorithm provides a simple and robust way for driving the error in a random process to zero. Bayesian methods are very useful in many problem domains.

2. Kalman Filter: An point estimator (mean and variance) for tracking a continuously valued variable. It makes some assumptions about the underlying process which, for estimating position and velocity of a moving vehicle, are quite reasonable. This is very simple to implement, and it is even simpler with a robust linear algebra framework (Matlab, Numpy/Scipy, Eigen, etc...).

3. Particle Filters: Particle filters are a multi-modal technique for estimating a continuously valued variable. It is one of the most powerful observer algorithms and is incredibly simple to implement. Professor Thrun attributes this to his tenure at Stanford.

4. Search: Find a path from point A to point B. We would like this to be optimal in some sense. In this course, we implement Breadth-first-search for a 2D grid. We then modify it to use a heuristic (in this case, L1 distance between grid location and the goal). Professor Thrun points out in the lecture that choosing a good heuristic for A* is a deep question. Another approach to path planning is Dynamic Programming, which computes a directional policy grid for every point in the map. The Dynamic Programming method (i.e., compute everything approach) requires a lot more computation.

5. Control: In this section, we study the generation of smooth paths (i.e., from the discrete path search results) and motion control with PID controllers.

6. SLAM
