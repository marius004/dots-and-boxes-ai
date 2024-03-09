from ui.window import Window
from core.config import Config

config = Config.Builder(total_rows=5, total_cols=5).build()
board = Window(config)

board.mainloop()
