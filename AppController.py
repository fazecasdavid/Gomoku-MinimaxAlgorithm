from Service import Service, AlgorithmLvl1, AlgorithmMiniMax, AlgorithmLvl2
from Domain import Board
from Console import Console
from GUI import Graphical


b = Board(15)

# depth for MiniMax algorithm
depth = 3

# alg = AlgorithmLvl1()
alg = AlgorithmLvl2()
# alg = AlgorithmMiniMax(depth)

s = Service(b, alg)

# ui = Console(s)
ui = Graphical(s)

ui.start()
