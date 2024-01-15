import tkinter as tk
from chess import *
import numpy as np

logic_board = Board(8,8)

class moveDot:
    def __init__(self, canvas, image, x=0, y=0):
        self.canvas = canvas
        self.image = image
        self.id = self.canvas.create_image(x, y, image=self.image, anchor='nw')
        self.canvas.itemconfig(self.id, state='hidden')
    
    def show(self):
        self.canvas.itemconfig(self.id, state='normal')
        return self
    
    def hide(self):
        self.canvas.itemconfig(self.id, state='hidden')

class DraggablePiece:
    def __init__(self, canvas, color, image, location, x=0, y=0):
        self.location = location
        self.canvas = canvas
        self.image = image
        self.color = color
        self.id = self.canvas.create_image(x, y, image=self.image, anchor='nw')
        self.canvas.tag_bind(self.id, '<ButtonPress-1>', self.click)
        self.canvas.tag_bind(self.id, '<Button1-Motion>', self.drag)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.drop)

    def click(self, event):
        board.hideDots()
        if self.color == 1:
            moves = logic_board.whiteMoves.get(logic_board.state[self.location[0],self.location[1]].name)
        elif self.color == 2:
            moves = logic_board.blackMoves.get(logic_board.state[self.location[0],self.location[1]].name)
        board.showDots(moves)
        
    def drag(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.id, x, y)
    
    def hide(self):
        self.canvas.itemconfig(self.id, state='hidden')

    def drop(self, event):
        x, y = event.x - event.x % 100, event.y - event.y % 100
        j, i = int(x/100), int(y/100)
        if [i,j] == self.location:
            self.canvas.coords(self.id, j*100, i*100)
            print('no move')
        else:
            result = logic_board.makeMove(logic_board.state[self.location[0],self.location[1]], [i,j])
            if result:
                self.canvas.coords(self.id, x, y)
                if isinstance(board.pieces[i,j], DraggablePiece):
                    board.pieces[i,j].hide()
                board.pieces[self.location[0], self.location[1]] = 0
                board.pieces[i,j] = self
                self.location = [i,j]
                if result == 'Rook1':
                    board.movePiece(board.pieces[i,0], location=[i,2])
                elif result == 'Rook2':
                    board.movePiece(board.pieces[i,7], location=[i,4])
                elif result == 'Queen':
                    board.promotePawn(board.pieces[i,j])
                elif result == 'En Passant':
                    if self.color == 1:
                        board.pieces[i-1,j].hide()
                    else:
                        board.pieces[i+1,j].hide()
            else:
                self.canvas.coords(self.id, self.location[1]*100, self.location[0]*100)
            board.hideDots()

class ChessBoard:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack()
        self.pieces = np.full((8,8), 0, dtype=object)
        self.dots = np.full((8,8), 0, dtype=object)
        self.displayedDots = []
        self.dot_image = tk.PhotoImage(file='images/dot.png')
        self.draw_board()
        self.add_pieces()

    def draw_board(self):
        color = "aquamarine2"
        for i in range(8):
            color = "aquamarine2" if color == "green" else "green"
            for j in range(8):
                x1 = j * 100
                y1 = i * 100
                x2 = x1 + 100
                y2 = y1 + 100
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                self.dots[i, j] = moveDot(self.canvas, self.dot_image, x1, y1)
                color = "aquamarine2" if color == "green" else "green"
        #self.dots[2,0].show()
    
    def showDots(self, locations):
        for [i,j] in locations:
            self.displayedDots.append(self.dots[i,j].show())
    
    def hideDots(self):
        for i in self.displayedDots:
            i.hide()
            
    def movePiece(self, piece, location):
        i,j = location[0], location[1]
        self.canvas.coords(piece.id, j*100, i*100)
        if isinstance(self.pieces[i,j], DraggablePiece):
            board.pieces[i,j].hide()
        self.pieces[piece.location[0], piece.location[1]] = 0
        self.pieces[i, j] = piece
        piece.location = [i,j]
        
    def promotePawn(self, pawn):
        i,j = pawn.location[0], pawn.location[1]
        board.pieces[i,j].hide()
        board.createQueen(i, j, pawn.color)
    
    def createQueen(self, i, j, color):
        image = self.white_queen if color == 1 else self.black_queen
        self.pieces[i,j] = DraggablePiece(self.canvas, 1, image, [i,j], j * 100, i * 100)
        

    def add_pieces(self):
        # Load the images
        self.white_pawn = tk.PhotoImage(file='images/WP.png')
        self.black_pawn = tk.PhotoImage(file='images/BP.png')
        self.white_rook = tk.PhotoImage(file='images/WR.png')
        self.black_rook = tk.PhotoImage(file='images/BR.png')
        self.white_knight = tk.PhotoImage(file='images/WN.png')
        self.black_knight = tk.PhotoImage(file='images/BN.png')
        self.white_bishop = tk.PhotoImage(file='images/WB.png')
        self.black_bishop = tk.PhotoImage(file='images/BB.png')
        self.white_queen = tk.PhotoImage(file='images/WQ.png')
        self.black_queen = tk.PhotoImage(file='images/BQ.png')
        self.white_king = tk.PhotoImage(file='images/WK.png')
        self.black_king = tk.PhotoImage(file='images/BK.png')
        # Add the images to the board
        
        for i in range(8):
            self.pieces[1,i] = DraggablePiece(self.canvas, 1, self.white_pawn, [1,i], i * 100, 100)
            self.pieces[6,i] = DraggablePiece(self.canvas, 2, self.black_pawn, [6,i], i * 100, 600)
            
            match i:
                case 0:
                    self.pieces[0,i] = DraggablePiece(self.canvas, 1, self.white_rook, [0,i], i * 100, 0)
                    self.pieces[7,i] = DraggablePiece(self.canvas, 2, self.black_rook, [7,i], i * 100, 700)
                case 1:
                    self.pieces[0,i] = DraggablePiece(self.canvas, 1, self.white_knight, [0,i], i * 100, 0)
                    self.pieces[7,i] = DraggablePiece(self.canvas, 2, self.black_knight, [7,i], i * 100, 700)
                case 2:
                    self.pieces[0,i] = DraggablePiece(self.canvas, 1, self.white_bishop, [0,i], i * 100, 0)
                    self.pieces[7,i] = DraggablePiece(self.canvas, 2, self.black_bishop, [7,i], i * 100, 700)
                case 3:
                    self.pieces[0,i] = DraggablePiece(self.canvas, 1, self.white_king, [0,i], i * 100, 0)
                    self.pieces[7,i] = DraggablePiece(self.canvas, 2, self.black_king, [7,i], i * 100, 700)
                case 4:
                    self.pieces[0,i] = DraggablePiece(self.canvas, 1, self.white_queen, [0,i], i * 100, 0)
                    self.pieces[7,i] = DraggablePiece(self.canvas, 2, self.black_queen, [7,i], i * 100, 700)
                case 5:
                    self.pieces[0,i] = DraggablePiece(self.canvas, 1, self.white_bishop, [0,i], i * 100, 0)
                    self.pieces[7,i] = DraggablePiece(self.canvas, 2, self.black_bishop, [7,i], i * 100, 700)
                case 6:
                    self.pieces[0,i] = DraggablePiece(self.canvas, 1, self.white_knight, [0,i], i * 100, 0)
                    self.pieces[7,i] = DraggablePiece(self.canvas, 2, self.black_knight, [7,i], i * 100, 700)
                case 7:
                    self.pieces[0,i] = DraggablePiece(self.canvas, 1, self.white_rook, [0,i], i * 100, 0)
                    self.pieces[7,i] = DraggablePiece(self.canvas, 2, self.black_rook, [7,i], i * 100, 700)

root = tk.Tk()
board = ChessBoard(root)
root.mainloop()
