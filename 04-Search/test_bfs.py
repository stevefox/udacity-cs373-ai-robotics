import unittest

from bfs import \
    search, \
    in_grid, \
    apply_move, \
    position_equal, \
    is_occupied, \
    is_visited


class AuxiliaryTests(unittest.TestCase):

    def test_in_grid_trivial(self):

        self.grid = [[]]
        pos = [[0, 0], [-1, 0], [0, -1], [1, 1]]
        for i in pos:
            self.assertFalse(in_grid(self.grid, i))

    def test_in_grid_expect_true(self):

        self.grid = [[0 for i in range(10)] for j in range(15)]
        pos = [[i, j] for i in range(15) for j in range(10)]
        for p in pos:
            self.assertTrue(in_grid(self.grid, p), p)

    def test_apply_move(self):

        move = [[i, j] for i in range(-1, 2, 1)
                for j in range(-1, 2, 1)]
        pos = [[i, j] for i in range(5) for j in range(3)]

        for p in pos:
            for m in move:
                new_pos = apply_move(p, m)
                self.assertEqual(new_pos[0], p[0]+m[0])
                self.assertEqual(new_pos[1], p[1]+m[1])

    def test_position_equal(self):

        pos1 = [[i, j] for i in range(-10, 10) for j in range(-10, 10)]
        pos2 = [[i, j] for i in range(-5, 5) for j in range(-5, 5)]

        for p1 in pos1:
            for p2 in pos2:
                self.assertEqual((p1[0] == p2[0] and p1[1] == p2[1]),
                                 position_equal(p1, p2))

    def test_is_occupied(self):
        self.grid = [[1]]
        self.assertTrue(is_occupied(self.grid, [0, 0]))

        self.grid = [[0]]
        self.assertFalse(is_occupied(self.grid, [0, 0]))

        self.grid = [[0, 1], [1, 1]]

        for j in range(len(self.grid)):
            for i in range(len(self.grid[0])):
                self.assertEqual(self.grid[i][j] == 1,
                                 is_occupied(self.grid, [i, j]))
                self.assertEqual(self.grid[i][j] == 1,
                                 is_visited(self.grid, [i, j]))


class TestSearch(unittest.TestCase):

    def test_trivial_case(self):
        """Test the trivial case where the start and goal are the same

        """
        grid = [[0, 0]]
        init = [0, 0]
        goal = [0, 0]

        result = search(grid, init, goal, 1)
        self.assertTrue(result[0] == 0 and result[1] == 0 and result[2] == 0,
                        '%s' % result)

if __name__ == '__main__':
    unittest.main()
