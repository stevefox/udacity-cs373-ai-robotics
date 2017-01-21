In this section, we study:

1. Generating Smooth Paths

2. PID Control


# Smoothing Algorithm (smooth:optimize.py)

1. y_i = x_i
2. Optimize:
   - (x_i-y_i)^2 -> min
     - this constraint is for the original path
   - (y_i - y_{i+1)^2 -> min
     - constrains all y_i points to be as similar as possible
     - interpoint distance

   -> weight the second constraint with a weighting term, \alpha
   -> keep the endpoints fixed: apply optimization only to the intermediate points
