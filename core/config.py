from dataclasses import dataclass
from enum import Enum

class Algorithm(Enum):
    MINI_MAX = 0
    ALPHA_BETA = 1
    ITERATIVE_DEEPENING_A_STAR = 2
    BAYESIAN_NETWORKS = 3

@dataclass
class Config:
    height: int
    width: int
    title: str
    rows: int
    cols: int
    
    distance_between_dots: float
    dot_width: float
    dot_color: str
    
    algorithm: Algorithm
    search_depth: int
   
    human_starts: bool  
    human_edge_color: str 
    human_box_color: str
    
    ai_edge_color: str
    ai_box_color: str
     
    edge_width: float
    
    @dataclass
    class Builder:
        height: int = 800
        width: int = 800
        title: str = "Dots and Boxes - Marius Scarlat"
        rows: int = 6
        cols: int = 6
        
        dot_color: str = '#7BC043'
        algorithm: Algorithm = Algorithm.ALPHA_BETA
        search_depth: int = 3
        
        human_starts: bool = True
        human_edge_color: str = "#0492CF"
        human_box_color: str = "#67B0CF"
       
        ai_edge_color: str = "#EE4035"
        ai_box_color: str = "#EE7E77"
        
        def build(self):
            distance_between_dots = self.width / self.rows
            dot_width = 0.25 * self.width / self.rows
            edge_width = 0.1 * self.width / self.rows
            
            return Config(
                height=self.height,
                width=self.width,
                title=self.title,
                rows=self.rows,
                cols=self.cols,
                distance_between_dots=distance_between_dots,
                dot_width=dot_width,
                dot_color=self.dot_color,
                algorithm=self.algorithm,
                search_depth=self.search_depth,
                human_starts=self.human_starts,
                human_edge_color=self.human_edge_color,
                human_box_color=self.human_box_color,
                ai_edge_color=self.ai_edge_color,
                ai_box_color=self.ai_box_color,
                edge_width=edge_width
            )
