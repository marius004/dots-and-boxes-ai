from core.config import Config
from core.board import Board
from core.constants import * 
from core.box import Box
from tkinter import *

class Window():
    def __init__(self, config: Config) -> None:
        self.board = Board(config.total_rows, config.total_cols)
        self.config = config
        
        self.scoredPoints = False
        self.human_player = True
        self.reset_board = False
        self.turn_handle = None
        self.marked_boxes = set()
        
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
    def update(self, coordinates): 
        (x1, y1), (x2, y2) = coordinates
        box_x1 = x1 * self.config.dots_distance + self.config.dots_distance / 2
        box_y1 = y1 * self.config.dots_distance + self.config.dots_distance / 2
        
        box_x2 = x2 * self.config.dots_distance + self.config.dots_distance / 2
        box_y2 = y2 * self.config.dots_distance + self.config.dots_distance / 2
       
        color = self.config.player1_colors[0] if self.human_player \
                                else self.config.player2_colors[0]
        self.canvas.create_line(box_x1, box_y1, box_x2, box_y2, fill=color, width=self.config.edge_width) 
    
    def fill_boxes(self): 
        for box in self.board.completed_boxes(): 
            if box not in self.marked_boxes:
                self.shade_box(box)  
                self.scoredPoints = True
                self.marked_boxes.add(box)
    
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

        return tuple(sorted((closest_dot1, closest_dot2)))
    
    def shade_box(self, box: Box):
        coordinates = box.all_coordinates()
        start_x = min(coord[0] * self.config.dots_distance + self.config.dots_distance / 2 for coord in coordinates)
        start_y = min(coord[1] * self.config.dots_distance + self.config.dots_distance / 2 for coord in coordinates)
        
        end_x = max(coord[0] * self.config.dots_distance + self.config.dots_distance / 2 for coord in coordinates)
        end_y = max(coord[1] * self.config.dots_distance + self.config.dots_distance / 2 for coord in coordinates)
       
        color = self.config.player1_colors[1] if box.box_owner() == HUMAN_PLAYER \
                                else self.config.player2_colors[1]
        self.canvas.create_rectangle(start_x + 6,
                                    start_y + 6,
                                    end_x - 6,
                                    end_y - 6,
                                    fill=color,
                                    outline='')       
    
    def show_gameover(self):
        human_score = self.board.player_score(HUMAN_PLAYER)
        ai_score = self.board.player_score(AI_PLAYER)

        if human_score > ai_score:
            text = 'Winner: You '
            color = self.config.player1_colors[0]
        elif ai_score > human_score:
            text = 'Winner: AI '
            color = self.config.player2_colors[0]
        else:
            text = "Tie"
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(self.config.board_width / 2, self.config.board_height / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(self.config.board_width / 2, 5 * self.config.board_height / 8, font="cmr 40 bold", fill='#7BC043',
                                text=score_text)

        score_text = 'Player 1 : ' + str(human_score) + '\n'
        score_text += 'Player 2 : ' + str(ai_score) + '\n'

        self.canvas.create_text(self.config.board_width / 2, 3 * self.config.board_height / 4, font="cmr 30 bold", fill='#7BC043',
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(self.config.board_width / 2, 15 * self.config.board_height / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)   
   
    
    def handle_click(self, event): 
        if not self.reset_board:
            position = self.position(event.x, event.y)
            if self.board.move(position, HUMAN_PLAYER if self.human_player else AI_PLAYER):
                self.update(position)
                self.fill_boxes()
                self.refresh()
                
                self.human_player = (not self.human_player) if not self.scoredPoints else self.human_player
                self.scoredPoints = False
                
                if self.board.is_gameover(): 
                    self.show_gameover()
                else: 
                    self.update_turn()
        else: 
            self.canvas.delete("all")
            self.reset_board = False 
            self.restore()