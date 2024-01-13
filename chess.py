import numpy as np
import statistics as st

class Piece:
    def __init__(self, name, color, moves, attacks, num):
        self.name = name
        self.color = color
        self.moves = moves
        self.attacks = attacks
        self.num = num
        self.isDefended = False
        self.hasMoved = False
    
    def __eq__(self, other):
        if not isinstance(other, __class__):
            # we can't handle the other type, inform Python
            return NotImplemented
        return self.color == other.color

def resetDefended(state):
    if isinstance(state, Piece):
        state.isDefended = False

resetDefended = np.frompyfunc(resetDefended, 1, 0)  
    
class Pawn(Piece):
    def __init__(self, name, color, location):
        self.location = location
        self.enPassant = False
        #centered at 7,7
        self.first_move = np.zeros((15,15))
        moves = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        attacks = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        if color == 1:
            self.first_move[8][7] = 1
            self.first_move[9][7] = 1
            moves[8][7] = 1
            attacks[8][6] = 1
            attacks[8][8] = 1
        if color == 2:
            self.first_move[6][7] = 1
            self.first_move[5][7] = 1
            moves[6][7] = 1
            attacks[6][6] = 1
            attacks[6][8] = 1
        
        moves[7][7] = -1
        attacks[7][7] = -1
        super().__init__(name if name else 'Pawn', color, moves, attacks, 1)
    
class Rook(Piece):
    def __init__(self, name, color, location):
        self.location = location
        #centered at 7,7
        moves = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        attacks = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        moves[:,7] = 1
        attacks[:,7] = 1
        
        moves[7,:] = 1
        attacks[7,:] = 1

        moves[7][7] = -1
        attacks[7][7] = -1
        
        super().__init__(name if name else 'Rook', color, moves, attacks, 2)

class Bishop(Piece):
    def __init__(self, name, color, location):
        self.location = location
        #centered at 7,7
        moves = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        attacks = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        np.fill_diagonal(np.fliplr(moves), 1)
        np.fill_diagonal(np.fliplr(attacks), 1)
        
        np.fill_diagonal(moves, 1)
        np.fill_diagonal(attacks, 1)

        moves[7][7] = -1
        attacks[7][7] = -1
        
        super().__init__(name if name else 'Bishop', color, moves, attacks, 3)
        
class Knight(Piece):
    def __init__(self, name, color, location):
        self.location = location
        #centered at 7,7
        moves = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        attacks = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        
        moves[9][6] = 1
        moves[9][8] = 1
        moves[8][5] = 1
        moves[6][5] = 1
        moves[8][9] = 1
        moves[5][8] = 1
        moves[6][9] = 1
        moves[5][6] = 1
        
        attacks[9][6] = 1
        attacks[9][8] = 1
        attacks[8][5] = 1
        attacks[6][5] = 1
        attacks[8][9] = 1
        attacks[5][8] = 1
        attacks[6][9] = 1
        attacks[5][6] = 1
        
        moves[7][7] = -1
        attacks[7][7] = -1
        
        super().__init__(name if name else 'Knight', color, moves, attacks, 4)
        
class King(Piece):
    def __init__(self, name, color, location):
        self.location = location
        self.isAttacked = False
        self.isChecked = False
        self.castleMap = np.ones((1,8))
        #centered at 7,7
        moves = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        attacks = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        
        moves[7][8] = 1
        moves[7][6] = 1
        moves[6][7] = 1
        moves[8][7] = 1
        moves[8][8] = 1
        moves[6][6] = 1
        moves[8][6] = 1
        moves[6][8] = 1
        
        attacks[7][8] = 1
        attacks[7][6] = 1
        attacks[6][7] = 1
        attacks[8][7] = 1
        attacks[8][8] = 1
        attacks[6][6] = 1
        attacks[8][6] = 1
        attacks[6][8] = 1
        
        self.castleMap[0,0] = 2
        self.castleMap[0,7] = 2
        
        moves[7][7] = -1
        attacks[7][7] = -1
        
        super().__init__(name if name else 'King', color, moves, attacks, 6)
        
class Queen(Piece):
    def __init__(self, name, color, location):
        self.location = location
        #centered at 7,7
        moves = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        attacks = np.zeros((15,15)) #[[0 for j in range(15)] for i in range(15)]
        moves[:,7] = 1
        attacks[:,7] = 1
        
        moves[7,:] = 1
        attacks[7,:] = 1
        
        np.fill_diagonal(np.fliplr(moves), 1)
        np.fill_diagonal(np.fliplr(attacks), 1)
        
        np.fill_diagonal(moves, 1)
        np.fill_diagonal(attacks, 1)

        moves[7][7] = -1
        attacks[7][7] = -1
        
        super().__init__(name if name else 'Queen', color, moves, attacks, 5)

PIECE_MAP = {0: Rook, 1: Knight, 2: Bishop, 3: King, 4: Queen, 5: Bishop, 6: Knight, 7: Rook}
PIECE_NAME = {0: 'Rook', 1: 'Knight', 2: 'Bishop', 3: 'King', 4: 'Queen', 5: 'Bishop', 6: 'Knight', 7: 'Rook'}

class Board:
    def __init__(self, width, height, customSetup = None):
        self.width = width
        self.height = height
        self.square = np.full((width , height), -1) #[[0 for j in range(height)] for i in range(width)]
        self.state = np.full((width,height), 0, dtype=object)
        self.whiteMoves = {}
        self.blackMoves = {}
        self.moveTurn = 0
        self.whitePieces = {}
        self.blackPieces = {}
        self.castle_Positions = [[0,1], [0,5], [7,1], [7,5]]
        if customSetup:
            customSetup(self)
        else:
            self.setupChess()
        self.getAllMoves(1)
        self.getAllMoves(2)
        
    def getSquare(x, y):
        return self.square.get(x).get(y)
        
    def setupChess(self):
        
        for i in range(8):
            self.state[1,i] = Pawn('Pawn'+str(i+1), 1, [1,i])
            self.square[1,i] = self.state[1,i].num
            
            self.state[6,i] = Pawn('Pawn'+str(i+1), 2, [6,i])
            self.square[6,i] = self.state[6,i].num
            
            self.whitePieces['Pawn'+str(i+1)] = self.state[1,i]
            self.blackPieces['Pawn'+str(i+1)] = self.state[6,i]
            
            if i < 5:
                self.state[0,i] = PIECE_MAP.get(i)(PIECE_NAME.get(i)+'1', 1, [0, i])
                self.square[0,i] = self.state[0,i].num
                
                self.state[7,i] = PIECE_MAP.get(i)(PIECE_NAME.get(i)+'1', 2, [7,i])
                self.square[7,i] = self.state[7,i].num
                
            
                self.whitePieces[PIECE_NAME.get(i)+'1'] = self.state[0,i]
                self.blackPieces[PIECE_NAME.get(i)+'1'] = self.state[7,i]
            else:
                self.state[0,i] = PIECE_MAP.get(i)(PIECE_NAME.get(i)+'2', 1, [0,i])
                self.square[0,i] = self.state[0,i].num
                
                self.state[7,i] = PIECE_MAP.get(i)(PIECE_NAME.get(i)+'2', 2, [7,i])
                self.square[7,i] = self.state[7,i].num
                
                self.whitePieces[PIECE_NAME.get(i)+'2'] = self.state[0,i]
                self.blackPieces[PIECE_NAME.get(i)+'2'] = self.state[7,i]
   
    
    def calculateMoves(self, piece, i, j, state = [], square = []):
        if len(state) == 0:
            state = self.state
        if len(square) == 0:
            square = self.square
        moves = np.zeros((8,8))
        attacks = np.zeros((8,8))
        if isinstance(piece, Pawn):
            if not piece.hasMoved:
                piece_moves = piece.first_move
            else:
                piece_moves = piece.moves
            
            moves = np.where(np.logical_and(np.logical_and(piece.attacks[7-i:15-i,7-j:15-j] == 1, state != piece), square != -1), 3, moves)
        else:
            piece_moves = piece.moves
            moves = np.where(np.logical_and(piece_moves[7-i:15-i,7-j:15-j] == 1, state != piece), 3, moves)
        
        moves = np.where(np.logical_and(piece_moves[7-i:15-i,7-j:15-j] == 1, state == piece), 2, moves)
        
        moves = np.where(np.logical_and(piece_moves[7-i:15-i,7-j:15-j] == 1, square == -1), 1, moves)
        
        moves, attacks = self.calculateMovesHelper(piece, i, j, moves, attacks)
        
        #cleanup attacks
        attacks = np.where(np.logical_and(piece.attacks[7-i:15-i,7-j:15-j] == 1, square == -1), 0, attacks)
        
        if isinstance(piece, Pawn) and piece.enPassant:
            print(attacks)
            if self.square[i,j+1] == 1 and self.state[i,j+1].color != piece.color:
                x = i+1 if piece.color == 1 else i-1
                y = j+1
                attacks[x,y] = 1
            if self.square[i,j-1] == 1 and self.state[i,j+1].color != piece.color:
                x = i+1 if piece.color == 1 else i-1
                y = j-1
                attacks[x,y] = 1
           
        #setDefenders
        defended_locations = np.array(np.where(moves == 2)).T
        for [i,j] in defended_locations:
            if isinstance(state[i,j], Piece):
                state[i,j].isDefended = True

        # Check Castle
        if not piece.hasMoved and isinstance(piece, King):
            row = 0 if piece.color == 1 else 7
            castle_moves = np.where(np.logical_and(square[row,:] == 2, piece.castleMap == 2), 2, moves[row,:])
            castle_moves = np.where(np.logical_and(square[row,:] == -1, piece.castleMap == 1), 1, castle_moves)
            #left
            castle_moves[0, 2::-1] = np.cumprod(castle_moves[0, 2::-1])
            #right
            castle_moves[0, 4::] = np.cumprod(castle_moves[0, 4::], 0)
            if piece.color == 1:
                if castle_moves[0,0] == 2 and not self.whitePieces.get('Rook1').hasMoved:
                    moves[0,1] = 1
                if castle_moves[0,7] == 2 and not self.whitePieces.get('Rook2').hasMoved:
                    moves[0,5] = 1
            if piece.color == 2:
                if castle_moves[0,0] == 2 and not self.blackPieces.get('Rook1').hasMoved:
                    moves[7,1] = 1
                if castle_moves[0,7] == 2 and not self.blackPieces.get('Rook2').hasMoved:
                    moves[7,5] = 1
       
        #cleanup Moves
        moves = np.where(moves > 1, 0, moves)
        
        return moves, attacks
        
        
    def calculateMovesHelper(self, piece, i, j, moves, attacks):  
        if isinstance(piece, Pawn):
            if piece.color == 1:
                #down
                moves[i+1:, j] = np.cumprod(moves[i+1:, j], 0)
            if piece.color == 2:
                #up
                moves[i-1::-1, j] = np.cumprod(moves[i-1::-1, j], 0)
        if isinstance(piece, Rook) or isinstance(piece, Queen) or isinstance(piece, Pawn) or isinstance(piece, King):
            if i < 7:
                #down
                moves[i+1:, j] = np.cumprod(moves[i+1:, j], 0)
            if i > 0:
                #up
                moves[i-1::-1, j] = np.cumprod(moves[i-1::-1, j], 0)
            if j < 7:
                #right
                moves[i, j+1:] = np.cumprod(moves[i, j+1:], 0)
            if j > 0:
                #left
                moves[i, j-1::-1] = np.cumprod(moves[i, j-1::-1], 0)
                    
        if isinstance(piece, Queen) or isinstance(piece, Bishop) or isinstance(piece, King):
            #bottom right
            if i < 7 and j < 7:
                diag_matrix = np.cumprod(moves[i+1:,j+1::1].diagonal())
                np.fill_diagonal(moves[i+1:,j+1::1], diag_matrix)
            #top right
            if i > 0 and j < 7:
                diag_matrix = np.cumprod(moves[i-1::-1,j+1::1].diagonal())
                np.fill_diagonal(moves[i-1::-1,j+1::1], diag_matrix)
            #top left
            if i > 0 and j > 0:
                diag_matrix = np.cumprod(moves[i-1::-1,j-1::-1].diagonal())
                np.fill_diagonal(moves[i-1::-1,j-1::-1], diag_matrix)
            #bottom left
            if i < 7 and j > 0:
                diag_matrix = np.cumprod(moves[i+1:,j-1::-1].diagonal())
                np.fill_diagonal(moves[i+1:,j-1::-1], diag_matrix)
        #setAttacks
        attacks = np.where(moves == 3, 1, attacks)
        
        return moves, attacks

    def getMoves(self, i, j, state = [], square = []):
        if len(state) == 0:
            state = self.state
        if len(square) == 0:
            square = self.square
        piece = state[i,j]
        
        if isinstance(piece, Piece):
            moves, attacks = self.calculateMoves(piece, i, j, state, square)
            return moves, attacks
        return 0
        
    
    def getAllMoves(self, color, state = [], square = [], future = False):
        if len(state) == 0:
            state = self.state
        if len(square) == 0:
            square = self.square
        curr_pieceMap = {}
        moves = [[]]
        attacks = [[]]
        for i in range(8):
            for j in range(8):
                piece = state[i,j]
                if isinstance(piece, Piece) and piece.color == color:
                    moves, attacks = self.getMoves(i, j, state, square)
                    allMoves = np.add(moves, attacks)
                    allMoves = np.array(np.where(allMoves == 1)).T
                    
                    if not future and len(allMoves) > 0:
                        allMoves = self.removeIllegalMoves(piece, allMoves)
                    curr_pieceMap[piece.name] = allMoves
        if not future:
            if color == 1:
                self.whiteMoves = curr_pieceMap
            if color == 2:
                self.blackMoves = curr_pieceMap
        if len(curr_pieceMap.values()) == 0:
            return 0
        return np.concatenate(list(curr_pieceMap.values()))

    def removeIllegalMoves(self, piece, allMoves):
        movesToDelete = []
        for [i,j] in allMoves:
            if isinstance(piece, King) and (isinstance(self.state[i,j], Piece) and self.state[i,j].isDefended):
                #King cannot attack a defended Piece
                movesToDelete.append([i,j])
            else:
                state_copy = self.state.copy()
                square_copy = self.square.copy()
                state_copy[piece.location[0], piece.location[1]] = 0
                state_copy[i, j] = piece
                
                square_copy[piece.location[0], piece.location[1]] = -1
                square_copy[i, j] = piece.num
                
                if isinstance(piece, King):
                    king_location = [i,j]
                else:
                    king_location = self.whitePieces.get('King1').location if piece.color == 1 else self.blackPieces.get('King1').location
                
                new_allAttacks = self.getAllMoves((piece.color%2) +1, state_copy, square_copy, True)
                
                if not piece.hasMoved and isinstance(piece, King):
                    if j == 1:
                        castle_Positions = [[0,1], [0,2]] if piece.color == 1 else [[7,1], [7,2]]
                        for i in castle_Positions:
                            if i in new_allAttacks.tolist():
                                movesToDelete.append([i,j])
                                break
                    if j == 7:
                        castle_Positions = [[0,4],[0,5]] if piece.color == 1 else [[7,4], [7,5]]
                        for i in castle_Positions:
                            if i in new_allAttacks.tolist():
                                movesToDelete.append([i,j])
                                break
                
                if isinstance(new_allAttacks, np.ndarray) and king_location in new_allAttacks.tolist():
                    movesToDelete.append([i,j])
        indexToDelete = []
        for i in range(len(allMoves)):
            if allMoves[i].tolist() in movesToDelete:
                indexToDelete.append(i)
        allMoves = np.delete(allMoves, indexToDelete, axis=0)
        return allMoves
        
    def checkEndGame(self, current_player, next_player):
        current_allMoves = self.getAllMoves(current_player)
        next_king = self.whitePieces.get('King1') if (self.moveTurn%2) == 0 else self.blackPieces.get('King1')
        if next_king.location in current_allMoves.tolist():
            next_king.isChecked = True
        next_allMoves = self.getAllMoves(next_player)
        nextPlayerMoveMap = self.whiteMoves if (self.moveTurn%2) == 0 else self.blackMoves
        currentPlayerMoveMap = self.whiteMoves if (self.moveTurn%2) == 1 else self.blackMoves
        nextPlayerKing = self.whitePieces.get('King1') if (self.moveTurn%2) == 0 else self.blackPieces.get('King1')
        if next_allMoves.size == 0:
            if nextPlayerKing.isChecked:
                print('Game Over - Check Mate')
                print('Result - ' + ('White' if (self.moveTurn%2) == 1 else 'Black') + ' Wins')
                return 0
            else:
                print('Game Over - Stale Mate')
                print('Result - Tie')
                return 0
    
        
    def endTurn(self):
        resetDefended(self.state)
        current_player = (self.moveTurn%2)+1
        self.moveTurn += 1
        next_player = (self.moveTurn%2)+1
        self.checkEndGame(current_player, next_player)
        print("Turn: " + str(self.moveTurn))
        
    def makeCastleMove(self, piece, rook, move):
        rook_i, rook_j = move[0], st.mean([piece.location[1], move[1]])
        
        self.state[rook.location[0], rook.location[1]] = 0
        self.state[rook_i, rook_j] = rook
        
        self.square[rook.location[0], rook.location[1]] = -1
        self.square[rook_i, rook_j] = rook.num
        
        rook.location = [rook_i, rook_j]
        rook.hasMoved = True
        
    def promotePawn(self, pawn, pieces):
        num = 3
        for i in range(8):
            if ('Queen'+str(num)) in pieces.keys():
                num += 1
            else:
                break
        queen = Queen('Queen'+str(num), pawn.color, pawn.location)
        
        self.state[pawn.location[0], pawn.location[1]] = queen
        
        self.square[pawn.location[0], pawn.location[1]] = queen.num
        
        del pieces[pawn.name]
        pieces[queen.name] = queen
        
        return queen
    
    def makeMove(self, piece, move):
        result = 0
        if isinstance(piece, Piece) and (piece.color - 1) == (self.moveTurn%2):
            currentMoves = self.whiteMoves if (self.moveTurn%2) == 0 else self.blackMoves
            currentPieces = self.whitePieces if (self.moveTurn%2) == 0 else self.whitePieces
            if move in currentMoves.get(piece.name).tolist():
                result = 1
                if not piece.hasMoved:
                    if isinstance(piece, King):
                        if move in self.castle_Positions:
                            rook = currentPieces.get('Rook1') if move[1] < 3 else currentPieces.get('Rook2')
                            self.makeCastleMove(piece, rook, move)
                            result = rook.name
                    if isinstance(piece, Pawn):
                        # Enable En Passant
                        if abs(move[0] - piece.location[0]) == 2:
                            if isinstance(self.state[move[0], move[1]+1], Pawn) and self.state[move[0], move[1]+1].color != piece.color:
                                self.state[move[0], move[1]+1].enPassant = True
                            if isinstance(self.state[move[0], move[1]-1], Pawn) and self.state[move[0], move[1]-1].color != piece.color:
                                self.state[move[0], move[1]-1].enPassant = True
            
                captured_piece = None
                if isinstance(piece, Pawn) and piece.enPassant:
                    if move[1] != piece.location[1]:
                        captured_piece = self.state[move[0]-1, move[1]]
                        result = 'En Passant'
                    piece.enPassant = False
                if captured_piece == None:
                    captured_piece = self.state[move[0], move[1]]
                if isinstance(captured_piece, Piece):
                    del currentPieces[captured_piece.name]
                self.state[piece.location[0], piece.location[1]] = 0
                self.state[move[0], move[1]] = piece
                
                self.square[piece.location[0], piece.location[1]] = -1
                self.square[move[0], move[1]] = piece.num
                
                piece.location = move
                piece.hasMoved = True
                
                #Pawn Promotion
                end_row = 7 if piece.color == 1 else 0
                if isinstance(piece, Pawn) and move[0] == end_row:
                    #pawn will promote
                    queen = self.promotePawn(piece, currentPieces)
                    result = 'Queen'
                
                self.endTurn()
                return result
            else:
                print("Invalid Move")
                return result
        else:
            print("Turn Error")
            return result
            
        

def testBoard(board):
    board.state[0,0] = King('King1', 2, [0,0])
    board.square[0,0] = board.state[0,0].num
    
    #board.state[0,1] = Rook('Rook1', 1, [0,1])
    #board.square[0,1] = board.state[0,1].num
    
    board.state[3,1] = Queen('Queen1', 1, [3,1])
    board.square[3,1] = board.state[3,1].num
    
    board.state[1,2] = King('King1', 1, [1,2])
    board.square[1,2] = board.state[1,2].num
    
    board.whitePieces['King1'] = board.state[1,2]
    board.whitePieces['Queen1'] = board.state[3,1]
    board.blackPieces['King1'] = board.state[0,0]
    

def main():
    b = Board(8,8)
