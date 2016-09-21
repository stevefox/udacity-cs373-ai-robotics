import unittest
from localization import \
    init_grid, \
    uniform_map, \
    localize, \
    format_map


def round_map(p, places=5):
    for i in range(len(p)):
        for j in range(len(p[0])):
            p[i][j] = int(p[i][j]*10**places)/float(10**places)
    return p


class TestMapFunctions(unittest.TestCase):

    def test_init_grid_base(self):
        m = init_grid(1, 1)
        self.assertEqual(m[0][0], 0.0)

    def test_init_dims(self):
        m = init_grid(2, 3)
        self.assertEqual(len(m), 2)
        self.assertEqual(len(m[0]), 3)

    def test_base(self):
        m = uniform_map(1, 1)
        self.assertEqual(m[0][0], 1.0)

    def test_square(self):
        m = uniform_map(3, 3)
        for i in range(len(m)):
            for j in range(len(m[0])):
                self.assertEqual(1.0/9.0, m[i][j])

    def test_dimensions(self):
        m = uniform_map(3, 4)
        self.assertEqual(len(m), 3)
        for i in m:
            self.assertEqual(len(i), 4)


class LocalizeSensorTests(unittest.TestCase):

    def test_ideal_sensor_base(self):
        # TEST 1
        colors = [['G', 'G', 'G'],
                  ['G', 'R', 'G'],
                  ['G', 'G', 'G']]
        measurements = ['R']
        motions = [[0, 0]]
        sensor_right = 1.0
        p_move = 1.0
        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0]]
        self.assertEqual(p, correct_answer)

    def test_test_ideal_sensor_case2(self):
        # TEST 2
        colors = [
            ['G', 'G', 'G'],
            ['G', 'R', 'R'],
            ['G', 'G', 'G']]
        measurements = ['R']
        motions = [[0, 0]]
        sensor_right = 1.0
        p_move = 1.0

        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 0.0, 0.0],
                          [0.0, 0.5, 0.5],
                          [0.0, 0.0, 0.0]]

        self.assertEqual(p, correct_answer)

    def test_uncertain_sensor_test3(self):
        # TEST 3
        colors = [
            ['G', 'G', 'G'],
            ['G', 'R', 'R'],
            ['G', 'G', 'G']]
        measurements = ['R']
        motions = [[0, 0]]
        sensor_right = 0.8
        p_move = 1.0

        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.06666666666, 0.06666666666, 0.06666666666],
                          [0.06666666666, 0.26666666666, 0.26666666666],
                          [0.06666666666, 0.06666666666, 0.06666666666]]

        self.assertEqual(round_map(p), round_map(correct_answer))

    def test_uncertain_sensor_ideal_move_test4(self):
        # TEST 4
        colors = [
            ['G', 'G', 'G'],
            ['G', 'R', 'R'],
            ['G', 'G', 'G']]
        measurements = ['R', 'R']
        motions = [[0, 0], [0, 1]]
        sensor_right = 0.8
        p_move = 1.0

        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.03333333333, 0.03333333333, 0.03333333333],
                          [0.13333333333, 0.13333333333, 0.53333333333],
                          [0.03333333333, 0.03333333333, 0.03333333333]]

        self.assertEqual(round_map(p), round_map(correct_answer))


class LocalizeMoveTests(unittest.TestCase):

    def test_ideal_move_nomove(self):
        colors = [['G', 'G', 'G'],
                  ['G', 'R', 'G'],
                  ['G', 'G', 'G']]
        measurements = ['R']
        motions = [[0, 0]]
        sensor_right = 1.0
        p_move = 1.0
        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0]]
        self.assertEqual(p, correct_answer)

    def test_ideal_move_nomove_G(self):
        colors = [['G', 'G', 'G'],
                  ['G', 'R', 'G'],
                  ['G', 'G', 'G']]
        measurements = ['G']
        motions = [[0, 0]]
        sensor_right = 1.0
        p_move = 1.0
        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.125, 0.125, 0.125],
                          [0.125, 0.0, 0.125],
                          [0.125, 0.125, 0.125]]
        self.assertEqual(round_map(p), round_map(correct_answer))

    def test_ideal_move_up(self):
        colors = [['G', 'G', 'G'],
                  ['G', 'R', 'G'],
                  ['G', 'G', 'G']]
        measurements = ['R', 'G']
        motions = [[0, 0], [-1, 0]]
        sensor_right = 1.0
        p_move = 1.0
        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0]]
        self.assertEqual(round_map(p), round_map(correct_answer))

    def test_ideal_move_down(self):
        colors = [['G', 'G', 'G'],
                  ['G', 'R', 'G'],
                  ['G', 'G', 'G']]
        measurements = ['R', 'G']
        motions = [[0, 0], [1, 0]]
        sensor_right = 1.0
        p_move = 1.0
        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0]]
        self.assertEqual(p, correct_answer)

    def test_ideal_move_left(self):
        colors = [['G', 'G', 'G'],
                  ['G', 'R', 'G'],
                  ['G', 'G', 'G']]
        measurements = ['R']
        motions = [[0, -1]]
        sensor_right = 1.0
        p_move = 1.0
        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0]]
        self.assertEqual(p, correct_answer)

    def test_ideal_move_right(self):
        colors = [['G', 'G', 'G'],
                  ['G', 'R', 'G'],
                  ['G', 'G', 'G']]
        measurements = ['R', 'G']
        motions = [[0, 0], [0, 1]]
        sensor_right = 1.0
        p_move = 1.0
        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0],
                          [0.0, 0.0, 0.0]]
        self.assertEqual(p, correct_answer)

    def test_ideal_move_ideal_sense_test5(self):
        # TEST 5
        colors = [
            ['G', 'G', 'G'],
            ['G', 'R', 'R'],
            ['G', 'G', 'G']]
        measurements = ['R', 'R']
        motions = [[0, 0], [0, 1]]
        sensor_right = 1.0
        p_move = 1.0

        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0],
                          [0.0, 0.0, 0.0]]
        self.assertEqual(p, correct_answer)

    def test_ideal_move2_ideal_sense_test6(self):
        # TEST 6
        colors = [
            ['G', 'G', 'G'],
            ['G', 'R', 'R'],
            ['G', 'G', 'G']]
        measurements = ['R', 'R']
        motions = [[0, 0], [0, 1]]
        sensor_right = 0.8
        p_move = 0.5

        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0289855072, 0.0289855072, 0.0289855072],
                          [0.0724637681, 0.2898550724, 0.4637681159],
                          [0.0289855072, 0.0289855072, 0.0289855072]]

        self.assertEqual(round_map(p), round_map(correct_answer))

    def test_ideal_move_uncertain_sense(self):
        # TEST 3
        colors = [
            ['G', 'G', 'G'],
            ['G', 'R', 'R'],
            ['G', 'G', 'G']]
        measurements = ['R']
        motions = [[0, 0]]
        sensor_right = 0.8
        p_move = 1.0

        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = \
            [[0.06666666666, 0.06666666666, 0.06666666666],
             [0.06666666666, 0.26666666666, 0.26666666666],
             [0.06666666666, 0.06666666666, 0.06666666666]]

        self.assertEqual(round_map(p), round_map(correct_answer))

    def test_ideal_move_uncertain_sense_test4(self):
        # TEST 4
        colors = [
            ['G', 'G', 'G'],
            ['G', 'R', 'R'],
            ['G', 'G', 'G']]
        measurements = ['R', 'R']
        motions = [[0, 0], [0, 1]]
        sensor_right = 0.8
        p_move = 1.0

        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.03333333333, 0.03333333333, 0.03333333333],
                          [0.13333333333, 0.13333333333, 0.53333333333],
                          [0.03333333333, 0.03333333333, 0.03333333333]]

        self.assertEqual(round_map(p), round_map(correct_answer))

    def test_uncertain_move_ideal_sense(self):
        """Test 7: Uncertain Move, Ideal Sense"""
        colors = [
            ['G', 'G', 'G'],
            ['G', 'R', 'R'],
            ['G', 'G', 'G']]
        measurements = ['R', 'R']
        motions = [[0, 0], [0, 1]]
        sensor_right = 1.0
        p_move = 0.5

        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 0.0, 0.0],
                          [0.0, 0.33333333, 0.66666666],
                          [0.0, 0.0, 0.0]]
        self.assertEqual(round_map(p), round_map(correct_answer))

    def test_uncertain_move3_ideal_sense(self):

        colors = [
            ['G', 'G', 'G'],
            ['G', 'R', 'R'],
            ['G', 'G', 'G']]
        measurements = ['R', 'G', 'G']
        motions = [[0, 0], [1, 0], [1, 0]]
        sensor_right = 1.0
        p_move = 1.0

        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.0, 0.5, 0.5],
                          [0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0]]
        self.assertEqual(round_map(p), round_map(correct_answer))

    def test_large_map(self):

        colors = [['R', 'G', 'G', 'R', 'R'],
                  ['R', 'R', 'G', 'R', 'R'],
                  ['R', 'R', 'G', 'G', 'R'],
                  ['R', 'R', 'R', 'R', 'R']]
        measurements = ['G', 'G', 'G', 'G', 'G']
        motions = [[0, 0],  [0, 1],  [1, 0],  [1, 0],  [0, 1]]
        sensor_right = 0.7
        p_move = 0.8
        p = localize(colors, measurements, motions, sensor_right, p_move)

        correct_answer = [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
                          [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
                          [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
                          [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]

        self.assertEqual(round_map(p, places=4), round_map(correct_answer, places=4))

if __name__ == '__main__':
    unittest.main()
