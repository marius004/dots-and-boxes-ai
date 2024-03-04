from dataclasses import dataclass, field
from typing import List

@dataclass
class Config:
    board_width: int
    board_height: int
    total_rows: int
    total_cols: int
    thickness: int
    
    dot_color: str
    game_title: str
    
    player1_colors: List[str]
    player2_colors: List[str]
    
    dots_distance: float
    symbol_size: float
    edge_width: float
    dot_width: float
    
    @dataclass
    class Builder:
        board_width: int = 800
        board_height: int = 800
        
        total_rows: int = 6
        total_cols: int = 6
        thickness: int = 50
        
        dot_color: str = '#7BC043'
        game_title: str = 'Dots and Boxes'
        
        player1_colors: List[str] = field(default_factory=lambda: ['#0492CF', '#67B0CF'])
        player2_colors: List[str] = field(default_factory=lambda: ['#EE4035', '#EE7E77'])

        def build(self):
            dots_distance = self.board_width / self.total_rows
            symbol_size = (self.board_width / 3 - self.board_width / 8) / 2
            dot_width = 0.25 * self.board_width / self.total_rows
            edge_width = 0.1 * self.board_width / self.total_rows
            
            return Config(
                board_width=self.board_width,
                board_height=self.board_height,
                total_rows=self.total_rows,
                total_cols=self.total_cols,
                thickness=self.thickness,
                dot_color=self.dot_color,
                game_title=self.game_title,
                player1_colors=self.player1_colors,
                player2_colors=self.player2_colors,
                dots_distance=dots_distance,
                symbol_size=symbol_size,
                edge_width=edge_width,
                dot_width=dot_width
            )
