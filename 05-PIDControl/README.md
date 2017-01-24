In this section, we study:

1. Generating Smooth Paths
2. PID Control

# 1. Smoothing Algorithm (smooth:01_OptimizePath/optimizepath.py)

1. y_i = x_i
2. Optimize:
   - (x_i-y_i)^2 -> min
     - this constraint is for the original path
   - (y_i - y_{i+1)^2 -> min
     - constrains all y_i points to be as similar as possible
     - interpoint distance

   -> weight the second constraint with a weighting term, \alpha
   -> keep the endpoints fixed: apply optimization only to the intermediate points

# 2. PID Control
This section convers PID Control. The steering problem is set up as a problem where a robot should track a desired trajectory (i.e., the path). The error in this problem is defined as the cross-track error, or the distance between the robot and the nearest point on the path. In the first exercise, we control steering angle to drive the cross-track error to zero.

  ## Proportional Control
  The limitation of P-controllers is that they are only marginally stable. The implications of this is that oscillations persist in the output. This tends to manifest itself as overshoot.
