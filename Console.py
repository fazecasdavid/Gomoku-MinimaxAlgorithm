import texttable
from Exceptions import *
import utils


class Console:
    def __init__(self, service):
        self._service = service

    @staticmethod
    def get_player_coord():
        cmd = input('> ').split(' ')
        return int(cmd[0]), int(cmd[1])

    def start(self):
        game_over = False
        while not game_over:
            if self._service.get_turn() == 1:
                try:
                    square = self.get_player_coord()
                    self._service.player_move(square[0], square[1])
                    if utils.game_over(self._service.get_board(), 1):
                        game_over = True

                except (ValueError, IndexError):
                    print("Bad input")
                except InvalidMove as msg:
                    print(msg)
            else:
                self._service.computer_move()
                if utils.game_over(self._service.get_board(), -1):
                    game_over = True
            self.print_board()  # refresh screen
        if self._service.get_turn() == -1:
            print("You Won the game!!!")
        else:
            print("You lost the game!!!")

    def print_board(self):
        board = self._service.get_board()
        table = texttable.Texttable()
        d = {0: '  ', 1: ' X ', -1: ' O '}
        for line in board:
            table.add_row(list(d[i] for i in line))
        print(table.draw())
        print()



