def game_over(board, turn):
    """
    Checks if the game is over : five in a raw
                                 five on a column
                                 five on diagonal

    @return: True if the game is over
             False if game can continue
    """
    def five_consecutive(array):
        if len(array) < 5:
            return False
        c = 1
        for el in range(1, len(array)):
            if array[el] == array[el - 1] and array[el] == turn:
                c += 1
            else:
                c = 1
            if c == 5:
                return True
        return False

    # line
    for line in board:
        if five_consecutive(line):
            return True

    # column
    for i in range(len(board)):
        column = [board[k][i] for k in range(len(board))]
        if five_consecutive(column):
            return True

    # diagonal "/"  - secondary diagonal
    for i in range(len(board)):
        diagonal_above = [board[i - k][k] for k in range(i + 1)]
        diagonal_under = [board[len(board) - k - 1][len(board) - (i - k) - 1] for k in
                          range(i + 1)]
        if five_consecutive(diagonal_above) or five_consecutive(diagonal_under):
            return True

    # diagonal "\"  - main diagonal
    for i in range(len(board)):
        diagonal_under = [board[i + k][k] for k in range(len(board) - i)]
        diagonal_above = [board[k][i + k] for k in range(len(board) - i)]
        if five_consecutive(diagonal_under) or five_consecutive(diagonal_above):
            return True

    return False
