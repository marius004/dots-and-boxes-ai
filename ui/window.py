from core.config import Algorithm
from core.config import Config
from core.board import Board
from core.constants import * 
from core.box import Box

from ai.minimax import MiniMax
from ai.alphabeta import AlphaBeta

from tkinter import *
from time import sleep
from math import inf

class Window():
    def __init__(self, config: Config) -> None:
        self.board = Board(config.rows, config.cols, config.human_starts)
        self.config = config
        
        self.reset_board = False
        self.turn_handle = None
        self.marked_boxes = set()
        
        self.window = Tk()
        self.window.title(config.title)
        self.canvas = Canvas(self.window, width=config.width, height=config.height)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.handle_click)
        self.restore()
        
        self.window.update()
        if not self.config.human_starts:
            self.ai_move()
        
    def mainloop(self):
        self.window.mainloop()
    
    def restore(self): 
        self.draw()
        self.board = Board(self.config.rows, self.config.cols, self.config.human_starts)
        self.update_turn()
        
    def draw(self): 
        for i in range(self.config.rows): 
            x = i * self.config.distance_between_dots + self.config.distance_between_dots / 2
            self.canvas.create_line(x, self.config.distance_between_dots / 2, x,
                                    self.config.width - self.config.distance_between_dots / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(self.config.distance_between_dots / 2, x,
                                    self.config.height - self.config.distance_between_dots / 2, x,
                                    fill='gray', dash=(2, 2))
            
        for i in range(self.config.rows):
            for j in range(self.config.cols):
                start_x = i * self.config.distance_between_dots + self.config.distance_between_dots / 2
                end_x = j * self.config.distance_between_dots + self.config.distance_between_dots / 2
                self.canvas.create_oval(start_x - self.config.dot_width / 2, end_x - self.config.dot_width / 2,
                                        start_x + self.config.dot_width / 2, end_x + self.config.dot_width / 2,
                                        fill=self.config.dot_color, outline=self.config.dot_color)   
    
    def update_turn(self):
        text  = f"Next turn:  {'You' if self.board.player_turn() == HUMAN_PLAYER else 'AI'}"
        color = self.config.human_edge_color if self.board.player_turn() == HUMAN_PLAYER else self.config.ai_edge_color
        
        self.canvas.delete(self.turn_handle)
        self.turn_handle = self.canvas.create_text(self.config.width - 6 * len(text),
                                                       self.config.height - self.config.distance_between_dots / 8,
                                                       font="cmr 15 bold", text=text, fill=color)
    def connect_line(self, coordinates, player): 
        (x1, y1), (x2, y2) = coordinates
        box_x1 = x1 * self.config.distance_between_dots + self.config.distance_between_dots / 2
        box_y1 = y1 * self.config.distance_between_dots + self.config.distance_between_dots / 2
        
        box_x2 = x2 * self.config.distance_between_dots + self.config.distance_between_dots / 2
        box_y2 = y2 * self.config.distance_between_dots + self.config.distance_between_dots / 2
       
        color = self.config.human_edge_color if player == HUMAN_PLAYER else self.config.ai_edge_color
        self.canvas.create_line(box_x1, box_y1, box_x2, box_y2, fill=color, width=self.config.edge_width) 
    
    def fill_boxes(self): 
        for box in self.board.completed_boxes(): 
            if box not in self.marked_boxes:
                self.shade_box(box)  
                self.marked_boxes.add(box)
    
    def position(self, x, y):
        min_distance, min_distance2 = float('inf'), float('inf')
        closest_dot1 = closest_dot2 = None

        for i in range(self.config.rows):
            for j in range(self.config.cols):
                dot_x = i * self.config.distance_between_dots + self.config.distance_between_dots / 2
                dot_y = j * self.config.distance_between_dots + self.config.distance_between_dots / 2

                distance = abs(x - dot_x) + abs(y - dot_y)
                
                if distance < min_distance:
                    min_distance2 = min_distance 
                    min_distance  = distance                    
                    closest_dot2 = closest_dot1
                    closest_dot1 = (i, j)
                elif distance < min_distance2:
                    min_distance2 = distance
                    closest_dot2 = (i, j)
                    
        return tuple(sorted((closest_dot1, closest_dot2)))
    
    def shade_box(self, box: Box):
        coordinates = box.all_coordinates()
        start_x = min(coord[0] * self.config.distance_between_dots + self.config.distance_between_dots / 2 for coord in coordinates)
        start_y = min(coord[1] * self.config.distance_between_dots + self.config.distance_between_dots / 2 for coord in coordinates)
        
        end_x = max(coord[0] * self.config.distance_between_dots + self.config.distance_between_dots / 2 for coord in coordinates)
        end_y = max(coord[1] * self.config.distance_between_dots + self.config.distance_between_dots / 2 for coord in coordinates)
       
        color = self.config.human_box_color if box.box_owner() == HUMAN_PLAYER else self.config.ai_box_color
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
            color = self.config.human_edge_color
        elif ai_score > human_score:
            text = 'Winner: AI '
            color = self.config.ai_edge_color
        else:
            text = "It is a tie"
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(self.config.width / 2, self.config.height / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(self.config.width / 2, 5 * self.config.height / 8, font="cmr 40 bold", fill='#7BC043',
                                text=score_text)

        score_text = 'You : ' + str(human_score) + '\n'
        score_text += 'AI : ' + str(ai_score) + '\n'

        self.canvas.create_text(self.config.width / 2, 3 * self.config.height / 4, font="cmr 30 bold", fill='#7BC043',
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(self.config.width / 2, 15 * self.config.height / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)
    
    def check_state(self):
        if self.board.is_gameover(): 
            self.show_gameover()
        else: 
            self.update_turn()
   
    def make_move(self, position): 
        player = self.board.player_turn()
        if self.board.move(position):
            self.connect_line(position, player)
            self.fill_boxes()
            self.draw()    
        self.check_state()
        self.window.update()
        
    def ai_move(self):
        if self.config.algorithm == Algorithm.MINI_MAX: 
            score, position = MiniMax().minimax(self.board, self.config.search_depth, True)
        elif self.config.algorithm == Algorithm.ALPHA_BETA:
            score, position = AlphaBeta().alpha_beta(self.board, self.config.search_depth, -inf, inf, True)
        else: 
            raise Exception("Not implemented!")
        
        print(score, position)
        self.make_move(position)
        
        while self.board.player_turn() == AI_PLAYER and not self.board.is_gameover():
            self.ai_move()
            
    def handle_click(self, event): 
        if not self.reset_board and self.board.player_turn() == HUMAN_PLAYER:   
            self.make_move(self.position(event.x, event.y))
            if self.board.player_turn() == AI_PLAYER:
                self.ai_move()
        elif self.reset_board: 
            self.canvas.delete("all")
            self.reset_board = False 
            self.restore()