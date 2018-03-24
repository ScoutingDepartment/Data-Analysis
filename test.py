from processor import board, decoder
bd = board.find("data/board", int("e3bb3f98", 16))
a = list(decoder.decode("4001430b4d014e004f005000510452025300540555005602474b4a6a4a724776", bd))

import pandas
b = pandas.DataFrame(a)
print(b)