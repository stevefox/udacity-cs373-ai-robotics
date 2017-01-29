# PID Control

In this section, we implement a PID Controller to control regulate the vertical position of the robot. PID Controllers are extremely useful in industry because it provides a simple linear controller than can be implemented in digitally with a microcontroller, in analog with simple op-amps and resistor tuning knobs, or even with mechanical hardware. I would recommend Ogata's Modern Control for encyclopedic treatment of linear control concepts.

## Proportional Control (P Control)
A P-Controller is a controller with the following update law:

steering = -p * error

We define the error in this case as the cross-track error, or the distance of the robot from the trajectory y_ref(t)

error(t) = y_robot(t) - y_ref(t)

In any control law, we would like to drive the error to 0, so we do this with a simple proportional controller. We set the steering angle inversely proportional to the error.

## Derivative Control (D Control)

In the regulation problem, a proportional controller suffers from one major defect: overshoot. Overshoot can also be described as sustained oscillation around the regulation point. Tuning the derivative term can help correct this. It has the effect of dampening oscillations just as simple low pass filter. In this code, we compute it in the following way:

diff_error(t) = error(t) - error(t-1)

Note that this is a simple backward derivative approximation.

## Integral Control (I Control)

The integral term corrects steady-state error around the regulation point (or reference trajectory). This makes it possible to correct a controller to track a trajectory even if there is steering drift. We compute the integral of the error by summing it at each time step:

integral_error(t) = sum(error(i)) for 0 <= i <=t

This is simple to compute with low memory requirement (i.e., it isn't required to store the entire vector of errors for all time):

integral_error(t) = integral_error(t-1) + error(t)

or simply

integral_error(t) += error(t)


# Auto-tuning a PID Controller

In the Udacity CS373 course, we use an algorithm called Twiddle to auto-tune the parameters for the PID Controller. This is a local hillclimbing algorithm. Indeed tuning a PID Controller is a bit of an art form and in industry it is often done on-the-fly, but Twiddle provides a method for finding parameters that track the trajectory once the reference trajectory has been reached.

In the case of a self-driving car where the control parameters depend very much on the plant, we may need to be continuously monitoring performance of the controller and potentially using adaptive control techniques to update the parameter. Often times we assume that the plant is not time-varying, but in practice, equipment and components age; integrating error over all time can also have some nasty effects (this is known as integrator windup); and, there are also much more powerful control techniques for non-linear control systems. Consider for example controlling the trajectory of a tractor trailor - a large truck is similar to a double pendulum and would benefit from a more advanced controller.
