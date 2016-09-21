import unittest
from kalman import *


class TestGaussian(unittest.TestCase):

    def test_guasssian_simple(self):
        mu = 10.
        sigma2 = 4.
        x = 8.
        result = gaussian(mu, sigma2, x)
        expected = 0.12
        self.assertTrue(round(result-expected, 2) == 0)


class TestMeasurementUpdate(unittest.TestCase):

    def test_measurement(self):
        m1 = 10.
        m2 = 13.
        v1 = 8.
        v2 = 2.
        [m1p, v1p] = update(m1, v1, m2, v2)
        self.assertEqual(m1p, 12.4)
        self.assertEqual(v1p, 1.6)


class TestMotionUpdate(unittest.TestCase):

    def test_predict(self):
        m1 = 10.
        m2 = 12.
        v1 = 4.
        v2 = 4.
        [m1p, v1p] = predict(m1, v1, m2, v2)
        self.assertEqual(m1p, 22)
        self.assertEqual(v1p, 8)


class TestKalmanFilter(unittest.TestCase):

    def test_kalman_1d(self):
        """Simple 1D Gaussian Random Variable Point Estimator

        Kalman Filter estimates mu, sigma
        """
        measurements = [5., 6., 7., 9., 10.]
        motions = [1., 1., 2., 1., 1.]
        measurement_sig = 4.
        motion_sig = 2.
        mu = 0.
        sig = 10000.
        mf, sf = simulate(measurements, motions,
                          measurement_sig, motion_sig,
                          mu, sig)
        mu_expected = 10.999906177177365
        sig_expected = 4.0058615808441944
        self.assertEqual(mf, mu_expected)
        self.assertEqual(sf, sig_expected)

    def test_kalman_2d(self):

        measurements = [1., 2., 3.]
        # initial state (location and velocity)
        x = matrix([[0.], [0.]])
        # initial uncertainty
        # Initialize with high variance (compared to the expected) and
        # assume they will be independent
        P = matrix([[1000., 0.], [0., 1000.]])
        # external motion
        u = matrix([[0.], [0.]])
        # next state function
        F = matrix([[1., 1.], [0, 1.]])
        # measurement function
        H = matrix([[1., 0.]])
        # measurement uncertainty
        R = matrix([[1.]])
        x_expected = [[3.9996664447958645], [0.9999998335552873]]
        P_expected = [[2.3318904241194827, 0.9991676099921091],
                      [0.9991676099921067, 0.49950058263974184]]
        x, P = simulate_kalman_filter_matrix(x, P, measurements, u,
                                             F=F, H=H, R=R)
        self.assertEqual(x.value, x_expected)
        self.assertEqual(P.value, P_expected)

    def test_kalman_4d(self):
        initial_xy = [4., 12.]
        measurements = [[5., 10.],
                        [6., 8.],
                        [7., 6.],
                        [8., 4],
                        [9., 2],
                        [10., 0.]]

        # s.v. representation
        # [x, y, x_dot, y_dot]^T
        x_init = matrix([[initial_xy[0]],
                         [initial_xy[1]],
                         [0.],
                         [0.]])
        dt = 0.1
        u = matrix([[0.], [0.], [0.], [0.]])
        P = matrix([[0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1000.0, 0.0],
                    [0.0, 0.0, 0.0, 1000.0]])
        F = matrix([[1.0, 0.0, dt, 0.0],
                    [0.0, 1.0, 0.0, dt],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0]])
        H = matrix([[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0]])
        R = matrix([[0.1, 0.0],
                    [0.0, 0.1]])
        x, P = simulate_kalman_filter_matrix(
            x_init, P, measurements, u, F=F, H=H, R=R)
        print x, P

if __name__ == '__main__':
    unittest.main()
