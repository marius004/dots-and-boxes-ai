from ui.window import Window
from core.config import Config

config = Config.Builder(rows=5, cols=5, human_starts=True).build()
board = Window(config)

board.mainloop()
