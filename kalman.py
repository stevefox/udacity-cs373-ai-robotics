import math
from course_provided_functions import matrix


def gaussian(mu, sigma2, x):
    const = 1.0/math.sqrt(2*math.pi*sigma2)
    exp = -0.5*(x-mu)**2/sigma2
    result = const*math.exp(exp)
    return result


def update(m1, v1, m2, v2):
    """Measurement Update

    Bayes Rule (multiplication of Gaussians)

    Returns:
       [mean, var]
    """
    new_mean = (v2*m1+v1*m2)/(v1+v2)
    new_variance = 1.0/((1./v1)+(1./v2))
    return [new_mean, new_variance]


def predict(m1, v1, m2, v2):
    """Motion Update

    Prediction using total probability

    Returns:
       [mean, var]
    """
    new_mean = m1+m2
    new_variance = v1+v2
    return [new_mean, new_variance]


def simulate(measurements, motions, measurement_sig, motion_sig, mu, sig):
    """Simulate measurement and update"""

    for i in range(len(measurements)):
        mu, sig = update(mu, sig, measurements[i], measurement_sig)
        mu, sig = predict(mu, sig, motions[i], motion_sig)

    return [mu, sig]


# Implement the filter function below
def matrix_measure(x, z, P, H, R):
    y = matrix([[z]])-H*x
    S = H*P*H.transpose() + R
    K = P*H.transpose()*S.inverse()
    x_hat = x + K*y
    I = matrix([[1., 0.], [0., 1.]])
    P_hat = (I - K*H)*P
    return [x_hat, P_hat]


def matrix_predict(x, P, F, u):
    x_hat = F*x + u
    P_hat = F*P*F.transpose()
    return [x_hat, P_hat]


def simulate_kalman_filter_matrix(
        x, P, measurements, u, F=None, H=None, R=None):
    """Simulate a Kalman filter

    State Variables:
      x = [x, x_dot] (initial state)
      P = COV(x, x_dot)
    Measurement at time step $i$:
      Z_i = measurements[i]
    External Movement:
      u

    Returns:
      [ x_i^hat, x_i_dot^hat ]
    """
    # Set defaults for the Kalman Filter
    # next state function
    if F is None:
        F = matrix([[1., 1.], [0, 1.]])
    # measurement function
    if H is None:
        H = matrix([[1., 0.]])
    # measurement uncertainty
    if R is None:
        R = matrix([[1.]])

    u = matrix([[0.], [0.]])
    for i in range(len(measurements)):
        # measurement update
        x, P = matrix_measure(x, measurements[i], P, H, R)
        # prediction
        x, P = matrix_predict(x, P, F, u)

    return x, P


def main():
    measurements = [5., 6., 7., 9., 10.]
    motions = [1., 1., 2., 1., 1.]
    measurement_sig = 4.
    motion_sig = 2.
    mu = 0.
    sig = 10000.
    print simulate(measurements, motions, measurement_sig, motion_sig, mu, sig)


if __name__ == '__main__':
    main()
