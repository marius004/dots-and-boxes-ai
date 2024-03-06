from board import Board
from config import Config

config = Config.Builder(total_rows=6, total_cols=6).build()
board = Board(config)

board.mainloop()
