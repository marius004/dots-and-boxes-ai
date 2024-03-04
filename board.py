from config import Config
from tkinter import *
import numpy as np

class Board():
    
    def __init__(self, config: Config):
        self.config = config
        
        self.window = Tk()
        self.window.title(config.game_title)
        self.canvas = Canvas(self.window, width=config.board_width, height=config.board_height)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.play_again()
    
    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(self.config.total_rows - 1, self.config.total_cols - 1))
        self.row_status = np.zeros(shape=(self.config.total_rows, self.config.total_cols - 1))
        self.col_status = np.zeros(shape=(self.config.total_rows - 1, self.config.total_cols))
        
        self.pointsScored = False
        
        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()
        
    def pointScored(self):
        self.pointsScored = True
        
    def mainloop(self): 
        self.window.mainloop()

    def refresh_board(self):
        for i in range(self.config.total_rows):
            x = i * self.config.dots_distance + self.config.dots_distance / 2
            self.canvas.create_line(x, self.config.dots_distance / 2, x,
                                    self.config.board_height - self.config.dots_distance / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(self.config.dots_distance / 2, x,
                                    self.config.board_width - self.config.dots_distance / 2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(self.config.total_rows):
            for j in range(self.config.total_cols):
                start_x = i * self.config.dots_distance + self.config.dots_distance / 2
                end_x = j * self.config.dots_distance + self.config.dots_distance / 2
                self.canvas.create_oval(start_x - self.config.dot_width / 2, end_x - self.config.dot_width / 2,
                                        start_x + self.config.dot_width / 2, end_x + self.config.dot_width / 2,
                                        fill=self.config.dot_color, outline=self.config.dot_color)

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = self.config.player1_colors[0]
        else:
            text += 'Player2'
            color = self.config.player2_colors[0]

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(self.config.board_width - 5 * len(text),
                                                       self.config.board_height - self.config.dots_distance / 8,
                                                       font="cmr 15 bold", text=text, fill=color)

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_position, valid_input = self.convert_grid_to_logical_position(grid_position)
            if valid_input and not self.is_grid_occupied(logical_position, valid_input):
                self.update_board(valid_input, logical_position)
                self.make_edge(valid_input, logical_position)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = (not self.player1_turn) if not self.pointsScored else self.player1_turn
                self.pointsScored = False

                if self.is_gameover():
                    self.display_gameover()
                else:
                    self.display_turn_text()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position - self.config.dots_distance / 4) // (self.config.dots_distance / 2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0] - 1) // 2)
            c = int(position[1] // 2)
            logical_position = [r, c]
            type = 'row'
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def mark_box(self):
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = self.config.player1_colors[1]
                self.shade_box(box, color)

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = self.config.player2_colors[1]
                self.shade_box(box, color)

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        player_modifier = 1
        
        if self.player1_turn:
            val = -1
            player_modifier = -1

        if c < (self.config.total_rows - 1) and r < (self.config.total_cols - 1):
            self.board_status[c][r] = (abs(self.board_status[c][r]) + val) * player_modifier
            if abs(self.board_status[c][r]) == 4:
                self.pointScored()

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] = (abs(self.board_status[c-1][r]) + val) * player_modifier
                if abs(self.board_status[c - 1][r]) == 4:
                    self.pointScored()

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] = (abs(self.board_status[c][r-1]) + val) * player_modifier
                if abs(self.board_status[c][r - 1]) == 4:
                    self.pointScored()

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = self.config.dots_distance / 2 + logical_position[0] * self.config.dots_distance
            end_x = start_x + self.config.dots_distance
            start_y = self.config.dots_distance /2 + logical_position[1] * self.config.dots_distance
            end_y = start_y
        elif type == 'col': 
            start_y = self.config.dots_distance / 2 + logical_position[1] * self.config.dots_distance 
            end_y = start_y + self.config.dots_distance
            start_x =  self.config.dots_distance / 2 + logical_position[0] * self.config.dots_distance 
            end_x = start_x
        
        if self.player1_turn:
            color = self.config.player1_colors[0]
        else:
            color = self.config.player2_colors[0]
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=self.config.edge_width)
        
    def display_gameover(self):
        player1_score = len(np.argwhere(self.board_status == -4))
        player2_score = len(np.argwhere(self.board_status == 4))

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
        
    def refresh_board(self):
        for i in range(self.config.total_rows):
            x = i*self.config.dots_distance + self.config.dots_distance/2
            self.canvas.create_line(x, self.config.dots_distance/2, x,
                                    self.config.board_width-self.config.dots_distance/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(self.config.dots_distance/2, x,
                                    self.config.board_width-self.config.dots_distance/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(self.config.total_rows):
            for j in range(self.config.total_cols):
                start_x = i*self.config.dots_distance+self.config.dots_distance/2
                end_x = j*self.config.dots_distance+self.config.dots_distance/2
                self.canvas.create_oval(start_x-self.config.dot_width/2, end_x-self.config.dot_width/2, start_x+self.config.dot_width/2,
                                        end_x+self.config.dot_width/2, fill=self.config.dot_color,
                                        outline=self.config.dot_color)
    
    def shade_box(self, box, color):
        start_x = self.config.dots_distance / 2 + box[1] * self.config.dots_distance + self.config.edge_width / 2
        start_y = self.config.dots_distance / 2 + box[0] * self.config.dots_distance + self.config.edge_width / 2
        end_x = start_x + self.config.dots_distance - self.config.edge_width
        end_y = start_y + self.config.dots_distance - self.config.edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')   
