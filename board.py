from config import Config
from tkinter import *
import numpy as np

class Board:
    def __init__(self, config: Config) -> None:
        self.scoredPoints = False
        self.player1_turn = True
        self.reset_board = False
        self.turn_handle = None
        self.marked_boxes = {}
        self.config = config
        self.board = {}
        
        self.window = Tk()
        self.window.title(config.game_title)
        self.canvas = Canvas(self.window, 
                            width=config.board_width, 
                            height=config.board_height)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.handleClick)
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
    
    def position(self, x, y):
        position = (np.array([x, y]) - self.config.dots_distance / 4) // (self.config.dots_distance / 2)

        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0] - 1) // 2)
            c = int(position[1] // 2)
            return [r,c], "row"
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            return [r, c], "col"

        return [], ""
    
    def is_occupied(self, position, type):
        r, c = position[0], position[1]
        return self.board.get((r, c, type), None) is not None 
    
    def update(self, position, type): 
        r, c = position[0], position[1]
        self.board[(r, c, type)] = 1
    
    def connect_edge(self, position, type): 
        if type == "row":
            start_x = self.config.dots_distance / 2 + position[0] * self.config.dots_distance
            end_x = start_x + self.config.dots_distance
            start_y = self.config.dots_distance /2 + position[1] * self.config.dots_distance
            end_y = start_y
        elif type == "col": 
            start_y = self.config.dots_distance / 2 + position[1] * self.config.dots_distance 
            end_y = start_y + self.config.dots_distance
            start_x =  self.config.dots_distance / 2 + position[0] * self.config.dots_distance 
            end_x = start_x
        
        color = self.config.player1_colors[0] if self.player1_turn \
                                else self.config.player2_colors[0]
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=self.config.edge_width)
        
    def connect_edge(self, position, type): 
        if type == "row":
            start_x = self.config.dots_distance / 2 + position[0] * self.config.dots_distance
            end_x = start_x + self.config.dots_distance
            start_y = self.config.dots_distance /2 + position[1] * self.config.dots_distance
            end_y = start_y
        elif type == "col": 
            start_y = self.config.dots_distance / 2 + position[1] * self.config.dots_distance 
            end_y = start_y + self.config.dots_distance
            start_x =  self.config.dots_distance / 2 + position[0] * self.config.dots_distance 
            end_x = start_x
        
        color = self.config.player1_colors[0] if self.player1_turn \
                                else self.config.player2_colors[0]
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=self.config.edge_width)
    
    def is_gameover(self):
        return len(self.marked_boxes) == (self.config.total_rows - 1) * (self.config.total_cols - 1)
    
    def fill_boxes(self):
        color = self.config.player1_colors[1] if self.player1_turn else self.config.player2_colors[1]
        player = 1 if self.player1_turn else 2
        
        for (r, c, type) in self.board.keys():
            if type == "row":
                # below [r, c]
                if self.board.get((r, c + 1, "row"), None) is not None \
                    and self.board.get((r + 1, c, "col"), None) is not None \
                    and self.board.get((r, c, "col"), None) is not None \
                    and not self.marked_boxes.get((r, c), False):  
                        self.marked_boxes[(r, c)] = player
                        self.shade_box([r, c], color)
                        self.scoredPoints = True
                # above [r, c]
                elif self.board.get((r, c - 1, "row"), None) is not None \
                    and self.board.get((r, c - 1, "col"), None) is not None \
                    and self.board.get((r + 1, c - 1, "col"), None) is not None \
                    and not self.marked_boxes.get((r, c - 1), False):
                        self.marked_boxes[(r, c - 1)] = player
                        self.shade_box([r, c - 1], color)
                        self.scoredPoints = True
    
    def show_gameover(self):
        player1_score = len([0 for (_, value) in self.marked_boxes.items() if value == 1])
        player2_score = len([0 for (_, value) in self.marked_boxes.items() if value == 2])

        if player1_score > player2_score:
            text = 'Winner: Player 1 '
            color = self.config.player1_colors[0]
        elif player2_score > player1_score:
            text = 'Winner: Player 2 '
            color = self.config.player2_colors[0]
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(self.config.board_width / 2, self.config.board_height / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(self.config.board_width / 2, 5 * self.config.board_height / 8, font="cmr 40 bold", fill='#7BC043',
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_score) + '\n'
        
        self.canvas.create_text(self.config.board_width / 2, 3 * self.config.board_height / 4, font="cmr 30 bold", fill='#7BC043',
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(self.config.board_width / 2, 15 * self.config.board_height / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)   
    
    def update_turn(self):
        text  = f"Next turn: Player {1 if self.player1_turn else 2}"
        color = self.config.player1_colors[0] if self.player1_turn else self.config.player2_colors[0]
        
        self.canvas.delete(self.turn_handle)
        self.turn_handle = self.canvas.create_text(self.config.board_width - 6 * len(text),
                                                       self.config.board_height - self.config.dots_distance / 8,
                                                       font="cmr 15 bold", text=text, fill=color)
    
    def shade_box(self, box, color):
        start_x = self.config.dots_distance / 2 + box[0] * self.config.dots_distance + self.config.edge_width / 2
        start_y = self.config.dots_distance / 2 + box[1] * self.config.dots_distance + self.config.edge_width / 2
        end_x = start_x + self.config.dots_distance - self.config.edge_width
        end_y = start_y + self.config.dots_distance - self.config.edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')  
    
    def handleClick(self, event): 
        if not self.reset_board:
            position, type = self.position(event.x, event.y)
            if position and not self.is_occupied(position, type): 
                self.update(position, type)
                self.connect_edge(position, type)
                self.fill_boxes()
                self.refresh()
                
                self.player1_turn = (not self.player1_turn) if not self.scoredPoints else self.player1_turn
                self.scoredPoints = False
                
                if self.is_gameover():
                    self.show_gameover()
                else: 
                    self.update_turn()
        else: 
            self.canvas.delete("all")
            self.restore()
            self.reset_board = False  