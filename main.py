from ui.window import Window
from core.config import Config

config = Config.Builder(total_rows=4, total_cols=4).build()
board = Window(config)

board.mainloop()
