import math
import random
from copy import deepcopy
import utils


class AlgorithmLvl1:

    @staticmethod
    def get_valid_locations(board):
        """

        @param board:   the board
        @return:  a list of all points that are in neighborhood with any point + the center point
        """
        locations = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 0:
                    continue
                if i > 0:
                    if j > 0:
                        if board[i - 1][j - 1] != 0 or board[i][j - 1] != 0:
                            locations.append((i, j))
                            continue
                    if j < len(board) - 1:
                        if board[i - 1][j + 1] != 0 or board[i][j + 1] != 0:
                            locations.append((i, j))
                            continue
                    if board[i - 1][j] != 0:
                        locations.append((i, j))
                        continue
                if i < len(board) - 1:
                    if j > 0:
                        if board[i + 1][j - 1] != 0 or board[i][j - 1] != 0:
                            locations.append((i, j))
                            continue
                    if j < len(board) - 1:
                        if board[i + 1][j + 1] != 0 or board[i][j + 1] != 0:
                            locations.append((i, j))
                            continue
                    if board[i + 1][j] != 0:
                        locations.append((i, j))
                        continue
        if board[len(board) // 2][len(board) // 2] == 0:
            locations.append((len(board) // 2, len(board) // 2))

        return list(set(locations))

    def next_move(self, board_obj):
        """
        @param board_obj:   the board
        @return:   a random valid point that is in neighborhood with another point on the board
        """
        board = board_obj.get_board
        locations = self.get_valid_locations(board)
        point = random.choice(locations)
        return point[0], point[1]


class AlgorithmLvl2(AlgorithmLvl1):
    def next_move(self, board):
        """
        @param board:
        @return: a valid point on the board returned by best_move method
        """
        point = self.best_move(board)
        return point[0], point[1]

    def score_board(self, board, piece):
        """

            computes the score of the given board for a given piece

        @param board:  the board
        @param piece:   the piece(AI turn or Human turn) to which the score is computed
        @return:
        """
        score = 0
        if board[len(board)//2][len(board)//2] == piece:
            score += 3

        # score on lines
        for line in board:
            for i in range(len(line) - 4):
                array = line[i:i+5]
                score += self.score_array(array, piece)

        # score on columns
        for i in range(len(board)):
            column = [board[k][i] for k in range(len(board))]
            for j in range(len(column) - 4):
                array = column[j:j+5]
                score += self.score_array(array, piece)

        # score on diagonal /
        for i in range(len(board)-1):
            diagonal_above = [board[i - k][k] for k in range(i + 1)]
            diagonal_under = [board[len(board) - k - 1][len(board) - (i - k) - 1] for k in
                              range(i + 1)]
            for j in range(len(diagonal_above) - 4):
                array = diagonal_above[j:j+5]
                score += self.score_array(array, piece)
            for j in range(len(diagonal_under) - 4):
                array = diagonal_under[j:j + 5]
                score += self.score_array(array, piece)

        diagonal = [board[len(board) - 1 - k][k] for k in range(len(board))]
        for j in range(len(diagonal) - 4):
            array = diagonal[j:j + 5]
            score += self.score_array(array, piece)

        # score on diagonal \
        for i in range(1, len(board)):
            diagonal_under = [board[i + k][k] for k in range(len(board) - i)]
            diagonal_above = [board[k][i + k] for k in range(len(board) - i)]
            for j in range(len(diagonal_above) - 4):
                array = diagonal_above[j:j + 5]
                score += self.score_array(array, piece)
            for j in range(len(diagonal_under) - 4):
                array = diagonal_under[j:j + 5]
                score += self.score_array(array, piece)

        diagonal = [board[k][k] for k in range(len(board))]
        for j in range(len(diagonal) - 4):
            array = diagonal[j:j + 5]
            score += self.score_array(array, piece)
        return score

    @staticmethod
    def score_array(array, piece):
        if len(array) != 5:
            return 0
        opp_piece = -1 * piece
        score = 0
        if array.count(piece) == 2 and array.count(0) == 3:
            score += 5
        elif array.count(piece) == 3 and array.count(0) == 2:
            score += 500
        elif array.count(piece) == 4 and array.count(0) == 1:
            score += 250000
        elif array.count(piece) == 5:
            score += 1000000000

        elif array.count(opp_piece) == 4 and array.count(0) == 1:
            score -= 100000000
        elif array.count(opp_piece) == 3 and array.count(0) == 2:
            score -= 600
        elif array.count(opp_piece) == 2 and array.count(0) == 3:
            score -= 6

        return score

    def best_move(self, board):
        """
            checks all possible next moves and selects the one with highest score

        @param board:
        @return:
        """
        valid_locations = self.get_valid_locations(board.get_board)
        best_score = -math.inf
        best_point = random.choice(valid_locations)
        for point in valid_locations:
            row = point[0]
            col = point[1]
            temp_board = deepcopy(board)
            temp_board.move(row, col)
            score = self.score_board(temp_board.get_board, -1)
            if score > best_score:
                best_score = score
                best_point = point
        return best_point


class AlgorithmMiniMax(AlgorithmLvl2):
    """
        Mini-max algorithm with Alpha-Beta pruning
    """
    def __init__(self, depth):
        self.depth = depth

    def is_terminal_node(self, board):
        return utils.game_over(board.get_board, -1) or utils.game_over(board.get_board, 1) or len(
            self.get_valid_locations(board.get_board)) == 0

    def mini_max(self, board_obj, depth, alpha, beta, maximizing_player):
        """
            function alphabeta(node, depth, α, β, maximizingPlayer) is
                if depth = 0 or node is a terminal node then
                    return the heuristic value of node
                if maximizingPlayer then
                    value := −∞
                    for each child of node do
                        value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
                        α := max(α, value)
                        if α ≥ β then
                            break (* β cut-off *)
                    return value
                else
                    value := +∞
                    for each child of node do
                        value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
                        β := min(β, value)
                        if α ≥ β then
                            break (* α cut-off *)
                    return value
        """
        board = board_obj.get_board
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board_obj)
        if depth == 0 or is_terminal:
            if is_terminal:
                if utils.game_over(board, -1):
                    return None, 100000000
                elif utils.game_over(board, 1):
                    return None, -100000000
            else:  # Depth is zero
                return None, self.score_board(board, -1)
        if maximizing_player:
            value = -math.inf
            point_good = random.choice(valid_locations)
            for point in valid_locations:
                row = point[0]
                col = point[1]
                b_copy = deepcopy(board_obj)
                b_copy.move(row, col)
                new_score = self.mini_max(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    point_good = point
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return point_good, value
        else:  # Minimizing player
            value = math.inf
            point_good = random.choice(valid_locations)
            for point in valid_locations:
                row = point[0]
                col = point[1]
                b_copy = deepcopy(board_obj)
                b_copy.move(row, col)
                new_score = self.mini_max(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    point_good = point
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return point_good, value

    def next_move(self, board):
        point, value = self.mini_max(board, self.depth, -math.inf, math.inf, True)
        return point[0], point[1]


class Service:
    def __init__(self, board, algorithm):
        self._board = board
        self._algorithm = algorithm

    def get_board(self):
        return self._board.get_board

    def get_length(self):
        return self._board.length

    def get_turn(self):
        return self._board.get_turn

    def game_over(self):
        return self._board.game_over(self.get_board(), self.get_turn())

    def player_move(self, x, y):
        self._board.move(x, y)

    def computer_move(self):
        square = self._algorithm.next_move(self._board)
        self._board.move(square[0], square[1])
