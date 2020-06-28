from Exceptions import *
from unittest import TestCase
from copy import deepcopy
import random


class Board:
    """
    0   -> empty square
    1   -> human move
    -1  -> computer move

    board   ->  a matrix of dimension length
    """

    def __init__(self, length):
        self.length = length
        self._board = [[0] * length for i in range(length)]
        self._turn = 1

    @property
    def get_board(self):
        return deepcopy(self._board)

    @property
    def get_turn(self):
        return self._turn

    def move(self, x, y):
        """
        Raises InvalidMove exception if:
                - move outside the board
                - square already occupied
        x, y - coordinates
        """
        if x < 0 or x >= self.length or y < 0 or y >= self.length:
            raise InvalidMove("Outside the board")

        if self._board[x][y] != 0:
            raise InvalidMove("Square taken")

        self._board[x][y] = self._turn
        self._turn *= -1



