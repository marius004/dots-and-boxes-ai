from core.config import Config
from core.board import Board
from tkinter import *
import numpy as np

class Window():
    def __init__(self, config: Config) -> None:
        self.board = Board(config.total_rows, config.total_cols)
        self.config = config
        
        self.human_player = True
        self.reset_board = False
        self.turn_handle = None
        self.marked_boxes = {}
        
        self.window = Tk()
        self.window.title(config.game_title)
        self.canvas = Canvas(self.window, 
                            width=config.board_width, 
                            height=config.board_height)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.handle_click)
        self.restore()
        
    def mainloop(self):
        self.window.mainloop()
    
    def restore(self): 
        self.refresh()
        self.update_turn()
        
    def refresh(self): 
        for i in range(self.config.total_rows): 
            x = i * self.config.dots_distance + self.config.dots_distance / 2
            self.canvas.create_line(x, self.config.dots_distance / 2, x,
                                    self.config.board_width - self.config.dots_distance / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(self.config.dots_distance / 2, x,
                                    self.config.board_height - self.config.dots_distance / 2, x,
                                    fill='gray', dash=(2, 2))
            
        for i in range(self.config.total_rows):
            for j in range(self.config.total_cols):
                start_x = i * self.config.dots_distance + self.config.dots_distance / 2
                end_x = j * self.config.dots_distance + self.config.dots_distance / 2
                self.canvas.create_oval(start_x - self.config.dot_width / 2, end_x - self.config.dot_width / 2,
                                        start_x + self.config.dot_width / 2, end_x + self.config.dot_width / 2,
                                        fill=self.config.dot_color, outline=self.config.dot_color)   
    
    def update_turn(self):
        text  = f"Next turn:  {'You' if self.human_player else 'AI'}"
        color = self.config.player1_colors[0] if self.human_player else self.config.player2_colors[0]
        
        self.canvas.delete(self.turn_handle)
        self.turn_handle = self.canvas.create_text(self.config.board_width - 6 * len(text),
                                                       self.config.board_height - self.config.dots_distance / 8,
                                                       font="cmr 15 bold", text=text, fill=color)
    
    def position(self, x, y):
        min_distance = float('inf')
        closest_dot1 = closest_dot2 = None

        for i in range(self.config.total_rows):
            for j in range(self.config.total_cols):
                dot_x = i * self.config.dots_distance + self.config.dots_distance / 2
                dot_y = j * self.config.dots_distance + self.config.dots_distance / 2

                distance = abs(x - dot_x) + abs(y - dot_y)

                if distance < min_distance:
                    min_distance = distance
                    closest_dot1 = (i, j)
                    
        min_distance = float('inf')
        for i in range(self.config.total_rows):
            for j in range(self.config.total_cols):
                dot_x = i * self.config.dots_distance + self.config.dots_distance / 2
                dot_y = j * self.config.dots_distance + self.config.dots_distance / 2

                distance = abs(x - dot_x) + abs(y - dot_y)

                if distance < min_distance and (i, j) != closest_dot1:
                    min_distance = distance
                    closest_dot2 = (i, j)

        return sorted((closest_dot1, closest_dot2))
    
    def handle_click(self, event): 
        if not self.reset_board:
            position = self.position(event.x, event.y)
            # nu merge
            if position in self.board.allowed_moves(): 
                print(position)