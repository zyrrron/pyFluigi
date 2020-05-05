class Cell:
    def __init__(self, ID, x, y, xdim, ydim) -> None:
        self.ID = ID
        self.x = x
        self.y = y
        self.xdim = xdim
        self.ydim = ydim

        self.terminals = []
        self.topterminals = []
        self.rightterminals =[]
        self.bottomterminals = []
        self.leftterminals = []

    
    def sort_terminals(self):
        for terminal in self.terminals:
            pass

    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Cell) and o.ID == self.ID:
            return True
        else:
            return False