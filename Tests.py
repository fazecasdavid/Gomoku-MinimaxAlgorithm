from unittest import TestCase
from Exceptions import *
from Domain import Board
from utils import game_over
from Service import AlgorithmLvl1, AlgorithmLvl2


class GameTest(TestCase):
    def test_move(self):
        b = Board(15)
        b.move(0, 0)
        bo = b.get_board
        self.assertNotEqual(bo[0][0], 0)
        self.assertEqual(len(bo), 15)
        with self.assertRaises(InvalidMove):
            b.move(0, 0)
        with self.assertRaises(InvalidMove):
            b.move(-1, 1)

    def test_game_over(self):
        b = Board(15)
        for i in range(5):
            b._board[i][i] = 1
        self.assertTrue(game_over(b.get_board, 1))
        self.assertFalse(game_over(b.get_board, -1))

    def test_get_valid_locations(self):
        b = Board(15)
        b.move(7, 7)
        alg = AlgorithmLvl1()
        ls = alg.get_valid_locations(b.get_board)
        self.assertEqual(len(ls), 8)

    def test_best_move_lvl_2(self):
        b = Board(15)
        alg = AlgorithmLvl2()
        b.move(0, 0)
        b.move(7, 7)
        b.move(0, 1)
        b.move(7, 8)
        b.move(0, 2)
        b.move(7, 9)
        b.move(0, 3)
        """
            will block the win of the opponent
        """
        point = alg.next_move(b)
        self.assertEqual(point[0], 0)
        self.assertEqual(point[1], 4)


