class ChessPiece():
    __dict = {'white':{'pawn':'♙','rook':'♖','knight':'♘','bishop':'♗','king':'♔','queen':'♕'},
              'black':{'pawn':'♟','rook':'♜','knight':'♞','bishop':'♝','king':'♚','queen':'♛'}}
    def __init__(self, color, piece, row, col):
        self.color = color
        self.piece = piece
        self.symbol = self.__dict[color][piece]
        self.dir = (1, -1)[color == 'white']
        self.row = row
        self.col = col
        self.has_moved = False
        self.plays = []
        
    def set_plays(self, moves):
        self.play = [list(play) for play in set(tuple(play) for play in self.plays + moves)]
        
    def __repr__(self):
        return 'ChessPiece({}, [{},{}], {}, {})'.format(self.symbol, self.row, self.col, self.plays, self.has_moved)