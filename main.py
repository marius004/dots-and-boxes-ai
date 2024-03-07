from ui.window import Window
from core.config import Config

config = Config.Builder(total_rows=6, total_cols=6).build()
board = Window(config)

board.mainloop()
