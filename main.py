from ui.window import Window
from core.config import Config

config = Config.Builder(rows=4, cols=4, search_depth=4, human_starts=True, dot_color="#fb8c00").build()
board = Window(config)

board.mainloop()
