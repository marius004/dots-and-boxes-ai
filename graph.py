class Graph: 
    def __init__(self) -> None:
        self.graph = {}
        self.added = {}
        self.index = 0
        
    def add_edge(self, node,  neighbor, color): 
        # todo: add more validation here
        if neighbor in self.graph.get(node, set()):
            return  
        
        data = (node, neighbor, color)
        if self.graph.get(node, None) is None: 
            self.graph[node] = set([data])
        elif neighbor not in self.graph[node]: 
            self.graph[node].add(data)
        
        self.added[node] = self.index 
        self.index += 1
    
    def neighbors(self, node): 
        return self.graph.get(node, set())

    def winning_state(self, color):
        def latest_neighbor_color(r, c, type):
            index, color = -1, ""
            for data in self.neighbors((r, c, type)):
                neighbor = data.neighbor
                edge_color = data.color
                
                if self.added[neighbor] > index: 
                    index = self.added[neighbor]
                    color = edge_color
            
            return color
        
        def box_below_row_coordinate(r, c):
            return [(r, c + 1, "row"),(r + 1, c, "col"), (r, c, "col")] \
                    in self.neighbors(r, c, "row")
        
        def box_above_row_coordinate(r, c):
            return [(r, c - 1, "row"),(r, c - 1, "col"),(r + 1, c - 1, "col")] \
                    in self.neighbors(r, c, "row")

        states = []

        # node is a tuple (r, c, type) where type is either "row" or "col"
        for (r, c, type) in filter(lambda key: key[3] == "row", self.graph.keys()): 
            # below [r, c]
            if box_below_row_coordinate(r, c) \
                and latest_neighbor_color(r, c, type) == color:
                    states.append({
                        "neighbors": [
                            (r, c + 1, "row"),
                            (r + 1, c, "col"),
                            (r, c, "col"),
                        ],
                        "node": (r, c, type),
                        "type": "below" 
                    })
            if box_above_row_coordinate(r, c) \
                and latest_neighbor_color(r, c, type) == color:
                    states.append({
                        "neighbors": [
                            (r, c - 1, "row"),
                            (r, c - 1, "col"),
                            (r + 1, c - 1, "col")
                        ], 
                        "node": (r, c, type), 
                        "type": "above"
                    })                              
            
        return states