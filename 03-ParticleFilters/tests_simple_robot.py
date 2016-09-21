import unittest
from simple_robot import run_robot


class SimpleRobotTest(unittest.TestCase):

    def test_simple_motions(self):
        sense1_expected = [39.05124837953327, 46.09772228646444,
                           39.05124837953327, 46.09772228646444]
        sense2_expected = [32.01562118716424, 53.150729063673246,
                           47.16990566028302, 40.311288741492746]

        [sense1, sense2] = run_robot()
        self.assertEqual(sense1, sense1_expected)
        self.assertEqual(sense2, sense2_expected)

if __name__ == '__main__':
    unittest.main()
