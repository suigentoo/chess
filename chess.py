class ChessPiece():
    __dict = {'white':{'pawn':'♙','rook':'♖','knight':'♘','bishop':'♗','king':'♔','queen':'♕'},
              'black':{'pawn':'♟','rook':'♜','knight':'♞','bishop':'♝','king':'♚','queen':'♛'}}
    def __init__(self, piece, color, row, col):
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

class Chess():
    __col = 'ABCDEFGH'
    __row = '87654321'
    
    whites = []
    blacks = []
    
    whites_plays = []
    blacks_plays = []
    
    
    def __init__(self):
        self.setup()

    def setup(self):
        self.board = [[None for i in range(8)] for j in range(8)]
        # create minor pieces(pawns)
        for col in range(8):
            self.whites.append(ChessPiece('pawn', 'white', 6, col))
            self.blacks.append(ChessPiece('pawn', 'black', 1, col))
        # create white major pieces
        self.whites.append(ChessPiece('rook', 'white', 7, 0))
        self.whites.append(ChessPiece('knight', 'white', 7, 1))
        self.whites.append(ChessPiece('bishop', 'white', 7, 2))
        self.whites.append(ChessPiece('queen', 'white', 7, 3))
        self.whites.append(ChessPiece('king', 'white', 7, 4))
        self.whites.append(ChessPiece('bishop', 'white', 7, 5))
        self.whites.append(ChessPiece('knight', 'white', 7, 6))
        self.whites.append(ChessPiece('rook', 'white', 7, 7))
        # create black major pieces
        self.blacks.append(ChessPiece('rook', 'black', 0, 0))
        self.blacks.append(ChessPiece('knight', 'black', 0, 1))
        self.blacks.append(ChessPiece('bishop', 'black', 0, 2))
        self.blacks.append(ChessPiece('queen', 'black', 0, 3))
        self.blacks.append(ChessPiece('king', 'black', 0, 4))
        self.blacks.append(ChessPiece('bishop', 'black', 0, 5))
        self.blacks.append(ChessPiece('knight', 'black', 0, 6))
        self.blacks.append(ChessPiece('rook', 'black', 0, 7))
        # place pieces on chess board in starting position
        # and keep track of the kings
        for w in self.whites:
            if w.piece == 'king':
                self.__white_king = w
            self.board[w.row][w.col] = w
        for b in self.blacks:
            if b.piece == 'king':
                self.__black_king = b
            self.board[b.row][b.col] = b
            
    def ray_trace(self, piece, x, y, n, can_capture=True, has_to_capture=False):
        moves = []
        color = piece.color
        row = piece.row
        col = piece.col
        while n != 0:
            row += y
            col += x
            n -= 1
            if (row in range(8)) and (col in range(8)):
                # pawn's diagnol capture
                if has_to_capture == True:
                    if self.board[row][col] == None:
                        n = 0
                    elif self.board[row][col].color != color:
                        play.append([row, col])
                        n = 0
                # pawn's vertical movement and other piece's movements excluding knight
                else:
                    if self.board[row][col] == None: 
                        moves.append([row, col])
                    elif (can_capture == True) and (self.board[row][col].color != color):
                        moves.append([row, col])
                        n = 0
                    elif self.board[row][col].color == color:
                        n = 0
            else:
                n = 0
        return moves
    
    def pawn_plays(self, piece):
        if piece.has_moved == False:
            piece.set_plays(self.ray_trace(piece, piece.dir, 0, 2, False))
            
        else:
            piece.set_plays(self.ray_trace(piece, piece.dir, 0, 1, False))
        piece.set_plays(self.ray_trace(piece, piece.dir, 1, 1, True, True))
        piece.set_plays(self.ray_trace(piece, piece.dir, 1, 1, True, True))
        
    def knight_plays(self, piece):
        set_ = [[i, j] for i in [-2,2] for j in [-1,1]] + [[i, j] for i in [-1,1] for j in [-2,2]]
        moves = []
        color = piece.color
        for s in set_:
            row = piece.row
            col = piece.col
            row += s[0]
            col += s[1]
            if (row in range(8)) and (col in range(8)):
                if self.board[row][col] == None:
                    moves.append([row, col])
                elif self.board[row][col].color != color:
                    moves.append([row, col])
        piece.set_plays(moves)
        
    def bishop_plays(self, piece):
        diag = [[i, j] for i in [-1,1] for j in [-1,1]]
        for i in diag:
            piece.set_plays(self.ray_trace(piece, i[0], i[1], 7))
    
    def rook_plays(self, piece):
        perp = [[0, j] for j in [-1,1]] + [[i, 0] for i in [-1,1]]
        for i in perp:
            piece.set_plays(self.ray_trace(piece, i[0], i[1], 7))
            
    def queen_plays(self, piece):
        diag = [[i, j] for i in [-1,1] for j in [-1,1]]
        perp = [[0, j] for j in [-1,1]] + [[i, 0] for i in [-1,1]]
        for i in diag+perp:
            piece.set_plays(self.ray_trace(piece, i[0], i[1], 7))
            
    def king_plays(self, piece):
        diag = [[i, j] for i in [-1,1] for j in [-1,1]]
        perp = [[0, j] for j in [-1,1]] + [[i, 0] for i in [-1,1]]
        for i in diag+perp:
            piece.set_plays(self.ray_trace(piece, i[0], i[1], 1))
            
    def piece_plays(self, piece):
        if piece.piece == 'pawn':
            self.pawn_plays(piece)
        elif piece.piece == 'knight':
            self.knight_plays(piece)
        elif piece.piece == 'bishop':
            self.bishop_plays(piece)
        elif piece.piece == 'rook':
            self.rook_plays(piece)
        elif piece.piece == 'queen':
            self.queen_plays(piece)
        elif piece.piece == 'king':
            self.king_plays(piece)

    def set_plays(self):
        for w in whites:
            self.whites_plays = [list(play) for play in set(tuple(play) for play in self.whites_plays + w.plays)]
        for b in blacks:
            self.blacks_plays = [list(play) for play in set(tuple(play) for play in self.blacks_plays + b.plays)]

    def valid_move(self, piece, row, col):
        if [row,col] in piece.plays:
            color = piece.color
            rho = piece.row
            kol = piece.col
            capture = self.move(piece, row, col)
            # moving piece puts self in check
            if self.self_check(color) == True:
                self.move(piece, rho, kol)
                self.move(capture, row, col)
                return False
            # capture a piece
            elif capture != None:
                # remove piece from opponents playable pieces 
                # and adds it to captures
                if color == 'white':
                    self.whites_captures.append(capture)
                    self.whites.remove(capture)
                else:
                    self.blacks_captures.append(capture)
                    self.blacks.remove(capture)
            return True
        else:
            return False

    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = None
        # item at [row,col]
        capture = self.board[row][col]
        # modify piece properties and moving
        piece.row = row
        piece.col = col
        self.board[row][col] = piece
        return capture
                
    def self_check(self, color):
        if color == 'white':
            if [self.__white_king.row, self.__white_king.col] in self.blacks_plays:
                return True
        else:
            if [self.__black_king.row, self.__black_king.col] in self.whites_plays:
                return True
        return False