import copy

class ChessPiece():
    __dict = {'white':{'pawn':'♙','rook':'♖','knight':'♘','bishop':'♗','king':'♔','queen':'♕'},
              'black':{'pawn':'♟','rook':'♜','knight':'♞','bishop':'♝','king':'♚','queen':'♛'}}
    __row = '87654321'
    __col = 'ABCDEFGH'
    def __init__(self, piece, color, row, col):
        self.color = color
        self.piece = piece
        self.symbol = self.__dict[color][piece]
        self.dir = (1, -1)[color == 'white']
        self.row = row
        self.col = col
        self.row_char = self.__row[row]
        self.col_char = self.__col[col]
        self.has_moved = False
        self.moves = []
        
    def __repr__(self):
        return 'ChessPiece({}, {}{}, {})'.format(self.symbol, self.row_char, self.col_char, self.moves)

class Chess():
    __dict = {'white':{'pawn':'♙','rook':'♖','knight':'♘','bishop':'♗','king':'♔','queen':'♕'},
              'black':{'pawn':'♟','rook':'♜','knight':'♞','bishop':'♝','king':'♚','queen':'♛'}}
    __row = '87654321'
    __col = 'ABCDEFGH'
    __white_king = None
    __black_king = None
    
    def __init__(self):
        # contains all active pieces/pieces on the board
        self.white = []
        self.black = []
        # respective arrays contains opponent's pieces that were captured
        self.white_captures = []
        self.black_captures = []
        # contains moves
        self.white_move_set = []
        self.black_move_set = []
        # contains playable pieces, those that can move
        self.white_playables = []
        self.black_playables = []
        # play history
        self.history = []
        self.setup()

    def setup(self):
        self.board = [[None for i in range(8)] for j in range(8)]
        # create minor pieces(pawns)
        for col in range(8):
            self.white.append(ChessPiece('pawn', 'white', 6, col))
            self.black.append(ChessPiece('pawn', 'black', 1, col))
        # keeps track of kings and puts them on their respective sides
        self.__white_king = ChessPiece('king', 'white', 7, 4)
        self.__black_king = ChessPiece('king', 'black', 0, 4)
        # create major pieces
        self.white.append(ChessPiece('rook', 'white', 7, 0))
        self.white.append(ChessPiece('knight', 'white', 7, 1))
        self.white.append(ChessPiece('bishop', 'white', 7, 2))
        self.white.append(ChessPiece('queen', 'white', 7, 3))
        self.white.append(self.__white_king)
        self.white.append(ChessPiece('bishop', 'white', 7, 5))
        self.white.append(ChessPiece('knight', 'white', 7, 6))
        self.white.append(ChessPiece('rook', 'white', 7, 7))
        self.black.append(ChessPiece('rook', 'black', 0, 0))
        self.black.append(ChessPiece('knight', 'black', 0, 1))
        self.black.append(ChessPiece('bishop', 'black', 0, 2))
        self.black.append(ChessPiece('queen', 'black', 0, 3))
        self.black.append(self.__black_king)
        self.black.append(ChessPiece('bishop', 'black', 0, 5))
        self.black.append(ChessPiece('knight', 'black', 0, 6))
        self.black.append(ChessPiece('rook', 'black', 0, 7))
        # place pieces on chess board in starting position
        for w in self.white:
            self.board[w.row][w.col] = w
        for b in self.black:
            self.board[b.row][b.col] = b        
    
    # ray trace functions
    def __pawn_diagonal(self, piece):
        moves = []
        row_ = piece.row
        col_ = piece.col
        diag = [[piece.dir,-1], [piece.dir,1]]
        for d in diag:
            row = row_ + d[0]
            col = col_ + d[1]
            if (row in range(8)) and (col in range(8)):
                if self.board[row][col] != None:
                    if self.board[row][col].color != piece.color: 
                        moves.append(self.__row[row] + self.__col[col])
        return moves
    
    def __pawn_forward(self, piece):
        moves = []
        row_ = piece.row
        col_ = piece.col
        forward = ([[piece.dir,0], [2*piece.dir,0]], [[piece.dir,0]])[piece.has_moved]
        for f in forward:
            row = row_ + f[0]
            col = col_ + f[1]
            if (row in range(8)) and (col in range(8)):
                if self.board[row][col] == None:
                    moves.append(self.__row[row] + self.__col[col])
        return moves
    
    def __knight_jump(self, piece):
        moves = []
        row_ = piece.row
        col_ = piece.col
        jump = [[i, j] for i in [-2,2] for j in [-1,1]] + [[i, j] for i in [-1,1] for j in [-2,2]]
        for j in jump:
            row = row_ + j[0]
            col = col_ + j[1]
            if (row in range(8)) and (col in range(8)):
                if self.board[row][col] != None:
                    if self.board[row][col].color != piece.color:
                        moves.append(self.__row[row] + self.__col[col])
                else:
                    moves.append(self.__row[row] + self.__col[col])
        return moves
    
    def __horizontal_trace(self, piece, n):
        return self.__ray_trace(piece, 0, -1, n) + self.__ray_trace(piece, 0, 1, n)
    
    def __vertical_trace(self, piece, n):
        return self.__ray_trace(piece, -1, 0, n) + self.__ray_trace(piece, 1, 0, n)
    
    def __diagonal_trace(self, piece, n):
        return self.__ray_trace(piece, -1, -1, n) + self.__ray_trace(piece, 1, 1, n) + \
               self.__ray_trace(piece, -1, 1, n) + self.__ray_trace(piece, 1, -1, n)
    
    def __ray_trace(self, piece, r, c, n):
        moves = []
        row = piece.row
        col = piece.col
        while n > 0:
            row += r
            col += c
            n -= 1
            if (row in range(8)) and (col in range(8)):
                if self.board[row][col] != None: 
                    if self.board[row][col].color != piece.color:
                        moves.append(self.__row[row] + self.__col[col])
                        n=0
                    else:
                        n=0
                else:
                    moves.append(self.__row[row] + self.__col[col])
            else:
                n = 0
        return moves
    
    # setters
    def set_piece_moves(self, piece):
        piece.moves = []
        if piece.piece == 'pawn':
            piece.moves += self.__pawn_diagonal(piece) + self.__pawn_forward(piece)
        elif piece.piece == 'knight':
            piece.moves += self.__knight_jump(piece)
        elif piece.piece == 'bishop':
            piece.moves += self.__diagonal_trace(piece, 7)
        elif piece.piece == 'rook':
            piece.moves += self.__horizontal_trace(piece, 7) + self.__vertical_trace(piece, 7)
        elif piece.piece == 'queen':
            piece.moves += self.__horizontal_trace(piece, 7) + self.__vertical_trace(piece, 7) + self.__diagonal_trace(piece, 7)
        elif piece.piece == 'king':  
            piece.moves += self.__horizontal_trace(piece, 1) + self.__vertical_trace(piece, 1) + self.__diagonal_trace(piece, 1)
            
    def set_moves(self):
        del self.white_move_set[:]
        for w in self.white:
            self.set_piece_moves(w)
            self.white_move_set += w.moves
        self.white_move_set = list(set(self.white_move_set))
        del self.black_move_set[:]
        for b in self.black:
            self.set_piece_moves(b)
            self.black_move_set += b.moves
        self.black_move_set = list(set(self.black_move_set)) 
    
    def set_playables(self):
        # possible playables
        del self.white_playables[:]
        for w in self.white:
            if len(w.moves) > 0:
                self.white_playables.append(w)
        # remove those that expose the king
        for i in range(len(self.white_playables))[::-1]:
            piece = self.white_playables[i]
            move_count = 0
            for m in piece.moves:
                chess_copy = copy.deepcopy(self)
                piece = chess_copy.white_playables[i]
                row = chess_copy.__row.index(m[0])
                col = chess_copy.__col.index(m[1])
                if chess_copy.valid_move(piece, row, col) == True:
                    move_count += 1
            if move_count == 0:
                self.white_playables.remove(self.white_playables[i])        
        del self.black_playables[:]
        for b in self.black:
            if len(b.moves) > 0:
                self.black_playables.append(b)
        for i in range(len(self.black_playables))[::-1]:
            piece = self.black_playables[i]
            move_count = 0
            for m in piece.moves:
                chess_copy = copy.deepcopy(self)
                piece = chess_copy.black_playables[i]
                row = chess_copy.__row.index(m[0])
                col = chess_copy.__col.index(m[1])
                if chess_copy.valid_move(piece, row, col) == True:
                    move_count += 1
            if move_count == 0:
                self.black_playables.remove(self.black_playables[i])
                
    # move returns capture, with value {None, ChessPiece}
    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = None
        capture = self.board[row][col]
        # update the piece's position
        piece.row = row
        piece.col = col
        self.board[row][col] = piece
        piece.has_moved = True
        return capture

    # booleans 
    def is_check(self, king):
        pos = self.__row[king.row] + self.__col[king.col]
        if king.color == 'white':
            if pos in self.black_move_set:
                return True
        else:
            if pos in self.white_move_set:
                return True
        return False
    
    def exposes_king(self, piece):
        if piece.color == 'white':
            return self.is_check(self.__white_king)
        else:
            return self.is_check(self.__black_king)
    
    def valid_move(self, piece, row, col):
        # make sure new position is in the piece's available moves
        row_ = piece.row
        col_ = piece.col
        pos = self.__row[row] + self.__col[col]
        if pos in piece.moves:
            # make a deep copy
            chess_copy = copy.deepcopy(self)
            piece = chess_copy.board[row_][col_]
            capture = chess_copy.move(piece, row, col)
            chess_copy.set_moves()
            return chess_copy.exposes_king(piece) == False
        else: 
            return False
    
    # returns moves, the piece can make that doesn't put it under threat
    def alive_moves(self, piece):
        if piece.color == 'white':
            
            return [m for m in piece.moves if m not in self.black_move_set]
        else:
            return [m for m in piece.moves if m not in self.white_move_set]  
    
    def checkmate(self, king):
        if self.is_check(king):
            if len(self.alive_moves(king)) == 0:
                # king is in check and can't move out of check
                if king.color == 'white':
                    winner = 'black'
                    for piece in self.white:
                        for m in piece.moves:
                            row = self.__row.index(m[0])
                            col = self.__col.index(m[1])
                            if self.valid_move(piece, row, col):
                                print(king, ' is in check')
                                return False
                else:
                    winner = 'white'
                    for piece in self.black:
                        for m in piece.moves:
                            row = self.__row.index(m[0])
                            col = self.__col.index(m[1])
                            if self.valid_move(piece, row, col):
                                print(king, ' is in check')
                                return False
                print('Checkmate {} wins!'.format(winner))
                return True
            print(king, ' is in check')
        return False    
    
    def valid_playable(self, piece, time):
        self.set_playables()
        if time % 2 == 0:
            return piece in self.white_playables
        else:
            return piece in self.black_playables
        
    def get_valid_playable(self, time):
        valid_playable = False
        while valid_playable == False:
            from_ = input('Where is the piece you want to move? ').upper()
            row = self.__row.find(from_[0])
            col = self.__col.find(from_[1])
            piece = self.board[row][col]
            valid_playable = self.valid_playable(piece, time)
        return piece, from_
    
    def get_valid_move(self, piece):
        valid_move = False
        while valid_move == False:
            msg = 'Where do you want to move the piece {}@{}? '.format(piece.symbol, piece.row_char+piece.col_char)
            to_ = input(msg).upper()
            row = self.__row.find(to_[0])
            col = self.__col.find(to_[1])
            valid_move = self.valid_move(piece, row, col)
        return row, col, to_
    
    def promote(self, piece):
        if piece.piece == 'pawn':
            if piece.row == 0 or piece.row == 7:
                promote_set = ['knight', 'bishop', 'rook', 'queen']
                valid_input = False
                while valid_input == False:
                    promote = input('What do you want to promote your pawn to?').lower()
                    if promote in promote_set:
                        valid_input = True
                piece.piece = promote
                piece.symbol = self.__dict[piece.color][piece.piece]
    
    def show_board(self):
        s = 'black: ['
        for b in self.black:
            s += b.symbol
        s += ']    '
        s += 'black capture: ['
        for b in self.black_captures:
            s += b.symbol
        s += ']\n'
        s += '♡ '
        for i in self.__col:
            s += i + ' '
        s += '\n'
        for i, row in enumerate(self.board):
            s += self.__row[i] + ' '
            for r in row:
                if r == None:
                    s += '◻ '
                else:
                    s += r.symbol + ' '
            s += '\n'
        s += 'white: ['
        for w in self.white:
            s += w.symbol
        s += ']    '
        s += 'white capture: ['
        for w in self.white_captures:
            s += w.symbol
        s += ']\n'
        print(s)
         
    def new_game(self):
        time = 0
        checkmate = False
        self.set_moves()
        self.show_board()
        while checkmate == False:
            if time % 2 == 0:
                print('White\'s turn')
                self.set_moves()
                self.set_playables()
                playable, from_ = self.get_valid_playable(time)
                print(playable.moves)
                row, col, to_ = self.get_valid_move(playable)
                capture = self.move(playable, row, col)
                if capture != None:
                    self.black.remove(capture)
                    self.white_captures.append(capture)
                # stalemate 50 turn rule
                if (playable.piece == 'pawn') | (capture != None):
                    turn = 0
                else:
                    turn +=1
                if turn >= 50:
                    stalemate = input('Want to call stalemate?').lower()
                    if stalemate in ['y', 'yes']:
                        print('Stalemate!')
                        returnn
                self.promote(playable)
                move_tuple = (playable, from_, capture, to_)
                self.history.append(move_tuple)
                self.set_moves()
                checkmate = self.checkmate(self.__black_king)
                self.show_board()
                time += 1
            else:
                print('Black\'s turn')
                self.set_moves()
                self.set_playables()
                playable, from_ = self.get_valid_playable(time)
                print(playable.moves)
                row, col, to_ = self.get_valid_move(playable)
                capture = self.move(playable, row, col)
                if capture != None:
                    self.white.remove(capture)
                    self.black_captures.append(capture)
                if (playable.piece == 'pawn') | (capture != None):
                    turn = 0
                else:
                    turn +=1
                if turn >= 50:
                    stalemate = input('Want to call stalemate?').lower()
                    if stalemate in ['y', 'yes']:
                        print('Stalemate!')
                        return
                self.promote(playable)
                move_tuple = (playable, from_, capture, to_)
                self.history.append(move_tuple)
                self.set_moves()
                checkmate = self.checkmate(self.__white_king)
                self.show_board()
                time += 1
                
if __name__ == '__main__':
    Chess().new_game()