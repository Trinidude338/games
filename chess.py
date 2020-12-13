import curses
import math
import time
import random


def main():
    stdscr = curses.initscr()
    curses.start_color()
    curses.raw()
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.curs_set(0)
    maxyx = stdscr.getmaxyx()
    if (maxyx[0]<60 or maxyx[1]<80):
        screenTooSmall(stdscr)
        curses.endwin()
        exit(1)
    chessPiece = [0, 0, 0]
    chessBoard = genChessBoard()
    moves = genMoves(chessBoard, chessPiece)
    frame = 0
    seconds = 0
    blink = 0
    offset = 30
    whosTurnIsIt = 0
    chessCurs = 35
    drawTitle(stdscr)
    drawControls(stdscr)
    while(1):
        if (frame>59):
            frame = 0
            seconds += 1
        else:
            frame += 1
        #draw frame
        drawBoard(stdscr, chessBoard, chessCurs, blink)
        drawUI(stdscr, whosTurnIsIt, chessPiece)
        #keyboard input
        try:
            c = stdscr.get_wch()
        except:
            c = 0
        #moving, quitting, and all that stuff
        if (c=='q'):
            gameover(stdscr, whosTurnIsIt)
            break
        elif(c==' ' and chessBoard[chessCurs][1]==whosTurnIsIt+1):
            chessPiece = [chessBoard[chessCurs][0], chessBoard[chessCurs][1], chessCurs]
        elif(not chessPiece==[0, 0, 0] and (c==chr(10) or c==chr(13)) and chessCurs in moves):
            if(whosTurnIsIt==0):
                whosTurnIsIt = 1
            else:
                whosTurnIsIt = 0
            chessBoard[chessPiece[2]] = [0, 0]
            chessBoard[chessCurs] = [chessPiece[0], chessPiece[1]]
            chessPiece = [0, 0, 0]
        elif(c==curses.KEY_UP):
            frame = 50
            if(chessCurs>7):
                chessCurs -= 8
        elif(c==curses.KEY_DOWN):
            frame = 50
            if(chessCurs<56):
                chessCurs += 8
        elif(c==curses.KEY_LEFT):
            frame = 50
            if(chessCurs>0):
                chessCurs -= 1
        elif(c==curses.KEY_RIGHT):
            frame = 50
            if(chessCurs<63):
                chessCurs += 1
        #game loop stuff
        if (frame<offset):
            blink = 1
        else:
            blink = 0
        moves = genMoves(chessBoard, chessPiece)
        if([6, 1] not in chessBoard):
            checkmate(stdscr, 1)
            break
        if([6, 2] not in chessBoard):
            checkmate(stdscr, 0)
            break
        #
        stdscr.refresh()
        time.sleep(0.016)
        stdscr.erase()
    curses.endwin()

def checkmate(stdscr, winner):
    maxyx = stdscr.getmaxyx()
    stdscr.erase()
    if (winner==0):
        line0 = "X won by Checkmate!(kinda)"
    else:
        line0 = "O won by Checkmate!(kinda)"
    stdscr.addstr(int(maxyx[0]/2), int(maxyx[1]/2-len(line0)/2), line0)
    stdscr.refresh()
    time.sleep(4)

def genMoves(chessBoard, chessPiece): 
    moves = []
    walls = [0, 8, 16, 32, 40, 48, 56, 7, 15, 23, 31, 39, 47, 55, 63]
    knightArr = [15, 17, 6, 10]
    kingArr = [1, 7, 8, 9]
    pawnArr = []
    for i in range(8, 16):
        pawnArr.append([i, i+16])
    for i in range(48, 56):
        pawnArr.append([i, i-16])
    if (chessPiece[1]==1):
        if(chessPiece[0]==1):
            if(chessBoard[chessPiece[2]-8]==[0, 0]):
                moves.append(chessPiece[2]-8)
            if(chessBoard[chessPiece[2]-7][1]==2):
                moves.append(chessPiece[2]-7)
            if(chessBoard[chessPiece[2]-9][1]==2):
                moves.append(chessPiece[2]-9)
            for i in pawnArr:
                if(chessPiece[2]==i[0]):
                    moves.append(i[1])
        elif(chessPiece[0]==2):
            for i in range(chessPiece[2]-8, -1, -8):
                if (chessBoard[i][1]==1):
                    break
                elif(chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+8, 64, 8):
                if (chessBoard[i][1]==1):
                    break
                elif(chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+1, chessPiece[2]+int(8)):
                if (i>63 or chessBoard[i][1]==1):
                    break
                elif (i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-1, chessPiece[2]-int(8), -1):
                if (i<0 or chessBoard[i][1]==1):
                    break
                elif (i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==3):
            for i in knightArr:
                if(chessPiece[2]-i>=0 and chessPiece[2]-i<=63 and chessBoard[chessPiece[2]-i][1]!=1):
                    moves.append(chessPiece[2]-i)
                if(chessPiece[2]+i>=0 and chessPiece[2]+i<=63 and chessBoard[chessPiece[2]+i][1]!=1):
                    moves.append(chessPiece[2]+i)
        elif(chessPiece[0]==4):
            for i in range(chessPiece[2]-7, -1, -7):
                if(i<0 or chessBoard[i][1]==1):
                    break
                elif(i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-9, -1, -9):
                if(i<0 or chessBoard[i][1]==1):
                    break
                elif(i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+7, 64, 7):
                if(i>63 or chessBoard[i][1]==1):
                    break
                elif(i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+9, 64, 9):
                if(i>63 or chessBoard[i][1]==1):
                    break
                elif(i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==5):
            for i in range(chessPiece[2]-8, -1, -8):
                if (chessBoard[i][1]==1):
                    break
                elif(chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+8, 64, 8):
                if (chessBoard[i][1]==1):
                    break
                elif(chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+1, chessPiece[2]+int(8)):
                if (i>63 or chessBoard[i][1]==1):
                    break
                elif (i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-1, chessPiece[2]-int(8), -1):
                if (i<0 or chessBoard[i][1]==1):
                    break
                elif (i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-7, -1, -7):
                if(i<0 or chessBoard[i][1]==1):
                    break
                elif(i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-9, -1, -9):
                if(i<0 or chessBoard[i][1]==1):
                    break
                elif(i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+7, 64, 7):
                if(i>63 or chessBoard[i][1]==1):
                    break
                elif(i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+9, 64, 9):
                if(i>63 or chessBoard[i][1]==1):
                    break
                elif(i in walls or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==6):
            for i in kingArr:
                if(chessPiece[2]-i>=0 and chessPiece[2]-i<=63 and chessBoard[chessPiece[2]-i][1]!=1):
                    moves.append(chessPiece[2]-i)
                if(chessPiece[2]+i>=0 and chessPiece[2]+i<=63 and chessBoard[chessPiece[2]+i][1]!=1):
                    moves.append(chessPiece[2]+i)
    elif (chessPiece[1]==2):
        if(chessPiece[0]==1):
            if(chessBoard[chessPiece[2]+8]==[0, 0]):
                moves.append(chessPiece[2]+8)
            if(chessBoard[chessPiece[2]+7][1]==1):
                moves.append(chessPiece[2]+7)
            if(chessBoard[chessPiece[2]+9][1]==1):
                moves.append(chessPiece[2]+9)
            for i in pawnArr:
                if(chessPiece[2]==i[0]):
                    moves.append(i[1])
        elif(chessPiece[0]==2):
            for i in range(chessPiece[2]-8, -1, -8):
                if (chessBoard[i][1]==2):
                    break
                elif(chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+8, 64, 8):
                if (chessBoard[i][1]==2):
                    break
                elif(chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+1, chessPiece[2]+int(8)):
                if (i>63 or chessBoard[i][1]==2):
                    break
                elif (i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-1, chessPiece[2]-int(8), -1):
                if (i<0 or chessBoard[i][1]==2):
                    break
                elif (i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==3):
            for i in knightArr:
                if(chessPiece[2]-i>=0 and chessPiece[2]-i<=63 and chessBoard[chessPiece[2]-i][1]!=2):
                    moves.append(chessPiece[2]-i)
                if(chessPiece[2]+i>=0 and chessPiece[2]+i<=63 and chessBoard[chessPiece[2]+i][1]!=2):
                    moves.append(chessPiece[2]+i)
        elif(chessPiece[0]==4):
            for i in range(chessPiece[2]-7, -1, -7):
                if(i<0 or chessBoard[i][1]==2):
                    break
                elif(i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-9, -1, -9):
                if(i<0 or chessBoard[i][1]==2):
                    break
                elif(i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+7, 64, 7):
                if(i>63 or chessBoard[i][1]==2):
                    break
                elif(i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+9, 64, 9):
                if(i>63 or chessBoard[i][1]==2):
                    break
                elif(i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==5):
            for i in range(chessPiece[2]-8, -1, -8):
                if (chessBoard[i][1]==2):
                    break
                elif(chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+8, 64, 8):
                if (chessBoard[i][1]==2):
                    break
                elif(chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+1, chessPiece[2]+int(8)):
                if (i>63 or chessBoard[i][1]==2):
                    break
                elif (i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-1, chessPiece[2]-int(8), -1):
                if (i<0 or chessBoard[i][1]==2):
                    break
                elif (i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-7, -1, -7):
                if(i<0 or chessBoard[i][1]==2):
                    break
                elif(i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-9, -1, -9):
                if(i<0 or chessBoard[i][1]==2):
                    break
                elif(i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+7, 64, 7):
                if(i>63 or chessBoard[i][1]==2):
                    break
                elif(i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+9, 64, 9):
                if(i>63 or chessBoard[i][1]==2):
                    break
                elif(i in walls or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==6):
            for i in kingArr:
                if(chessPiece[2]-i>=0 and chessPiece[2]-i<=63 and chessBoard[chessPiece[2]-i][1]!=2):
                    moves.append(chessPiece[2]-i)
                if(chessPiece[2]+i>=0 and chessPiece[2]+i<=63 and chessBoard[chessPiece[2]+i][1]!=2):
                    moves.append(chessPiece[2]+i)
    return moves

def drawUI(stdscr, turn, piece):
    if(turn==0):
        stdscr.addstr(1, 1, "X's turn to play")
    else:
        stdscr.addstr(1, 1, "O's turn to play")
    if(piece[0]==1):
        line0 = "Pawn"
    elif(piece[0]==2):
        line0 = "Rook"
    elif(piece[0]==3):
        line0 = "Knight"
    elif(piece[0]==4):
        line0 = "Bishop"
    elif(piece[0]==5):
        line0 = "Queen"
    elif(piece[0]==6):
        line0 = "King"
    else:
        line0 = "None"
    stdscr.addstr(3, 1, str("Selected Piece: "+line0))

def drawBoard(stdscr, chessBoard, chessCurs, ifBlinkOn):
    maxyx = stdscr.getmaxyx()
    topLeftCorner = [math.trunc(maxyx[0]/2-25), math.trunc(maxyx[1]/2-40)]
    curs = [topLeftCorner[0], topLeftCorner[1]]
    pieces0 = [["   /\\    ","   \\/    ","   XX    ","   XX    ","  XXXX   "],
            ["  X  X   ","  XXXX   ","   XX    ","   XX    ","  XXXX   "],
            ["   XX    ","  XXXX   ","  XX     ","   XX    ","  XXXX   "],
            ["   /.    ","   \\/    ","   /\\    ","   XX    ","  XXXX   "],
            ["  ____   ","  ||||   ","   XX    ","   XX    ","  XXXX   "],
            ["   ||    ","  =XX=   ","   ||    ","   XX    ","  XXXX   "]]
    pieces1 = [["   /\\    ","   \\/    ","   OO    ","   OO    ","  OOOO   "],
            ["  O  O   ","  OOOO   ","   OO    ","   OO    ","  OOOO   "],
            ["   OO    ","  OOOO   ","  OO     ","   OO    ","  OOOO   "],
            ["   /.    ","   \\/    ","   /\\    ","   OO    ","  OOOO   "],
            ["  ____   ","  ||||   ","   OO    ","   OO    ","  OOOO   "],
            ["   ||    ","  =OO=   ","   ||    ","   OO    ","  OOOO   "]]
    line0 = "+---------+---------+---------+---------+---------+---------+---------+---------+"
    line1 = "|         |         |         |         |         |         |         |         |"
    for x in range(8):
        stdscr.addstr(curs[0], curs[1], line0)
        curs[0] += 1
        for y in range(5):
            stdscr.addstr(curs[0], curs[1], line1)
            curs[0] += 1
    stdscr.addstr(curs[0], curs[1], line0)
    curs = [topLeftCorner[0], topLeftCorner[1]]
    for num, i in enumerate(chessBoard):
        curs = [math.trunc(topLeftCorner[0]+int(num/8)*6)+1, math.trunc(topLeftCorner[1]+(num%8)*10)+1]
        if (num==chessCurs and ifBlinkOn!=1):
            for j in range(5):
                for x in range(9):
                    stdscr.addch(curs[0], curs[1]+x, '#')
                curs[0] += 1
            curs = [math.trunc(topLeftCorner[0]+int(num/8)*6)+1, math.trunc(topLeftCorner[1]+(num%8)*10)+1]
        if (i[1]==0):
            pass
        elif (i[1]==1):
            for j in pieces0[i[0]-1]:
                for x, c in enumerate(j):
                    if (c==' '):
                        pass
                    else:
                        stdscr.addch(curs[0], curs[1]+x, c)
                curs[0] += 1
        else:
            for j in pieces1[i[0]-1]:
                for x, c in enumerate(j):
                    if (c==' '):
                        pass
                    else:
                        stdscr.addch(curs[0], curs[1]+x, c)
                curs[0] += 1

def screenTooSmall(stdscr):
    maxyx = stdscr.getmaxyx()
    stdscr.erase()
    line0 = "Your terminal window isn't big enough"
    stdscr.addstr(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-(len(line0)/2)), line0)
    stdscr.refresh()
    while(stdscr.getch()==curses.ERR):
        time.sleep(0.016)

def genChessBoard():
    lst = []
    #[[x, y] * 64]     :       x = type of piece   y = team of piece
    #                           0-7                 0-2
    for i in range(64):
        lst.append([0, 0])
    #pawns
    for i in range(8, 16):
        lst[i] = [1, 2]
    for i in range(48, 56):
        lst[i] = [1, 1]
    #rooks
    lst[0] = [2, 2]
    lst[7] = [2, 2]
    lst[56] = [2, 1]
    lst[63] = [2, 1]
    #knights
    lst[1] = [3, 2]
    lst[6] = [3, 2]
    lst[57] = [3, 1]
    lst[62] = [3, 1]
    #bishops
    lst[2] = [4, 2]
    lst[5] = [4, 2]
    lst[58] = [4, 1]
    lst[61] = [4, 1]
    #queens
    lst[3] = [5, 2]
    lst[59] = [5, 1]
    #kings
    lst[4] = [6, 2]
    lst[60] = [6, 1]
    return lst

def drawControls(stdscr):
    maxyx = stdscr.getmaxyx()
    stdscr.clear()
    controlsbox = curses.newwin(math.trunc(maxyx[0]*3/5), math.trunc(maxyx[1]/3), math.trunc(maxyx[0]/5), math.trunc(maxyx[1]/3))
    curses.raw()
    curses.noecho()
    curses.cbreak()
    controlsbox.nodelay(True)
    controlsbox.keypad(True)
    maxyx1 = controlsbox.getmaxyx()
    controlsbox.border()
    line0 = "Controls:"
    line1 = "q - Quit"
    line2 = "Arrow Keys - Move Cursor"
    line3 = "Space - Select Piece"
    line4 = "Enter - Move Piece"
    controlsbox.move(math.trunc(maxyx1[0]/2)-5, math.trunc(maxyx1[1]/2-len(line0)/2))
    controlsbox.addstr(line0)
    controlsbox.move(math.trunc(maxyx1[0]/2)-1, math.trunc(maxyx1[1]/2-len(line1)/2))
    controlsbox.addstr(line1)
    controlsbox.move(math.trunc(maxyx1[0]/2)+1, math.trunc(maxyx1[1]/2-len(line2)/2))
    controlsbox.addstr(line2)
    controlsbox.move(math.trunc(maxyx1[0]/2)+3, math.trunc(maxyx1[1]/2-len(line3)/2))
    controlsbox.addstr(line3)
    controlsbox.move(math.trunc(maxyx1[0]/2)+5, math.trunc(maxyx1[1]/2-len(line4)/2))
    controlsbox.addstr(line4)
    stdscr.refresh()
    controlsbox.refresh()
    time.sleep(1)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame < 600):
        frame += 1
        time.sleep(0.016)
    controlsbox.clear()
    stdscr.clear()
    controlsbox.refresh()
    stdscr.refresh()


def drawTitle(stdscr):
    maxyx = stdscr.getmaxyx()
    title = "Chess"
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-math.trunc(len(title)/2)))
    stdscr.addstr(title)
    stdscr.refresh()
    time.sleep(1)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame < 60):
        frame += 1
        time.sleep(0.016)

def gameover(stdscr, turn):
    maxyx = stdscr.getmaxyx()
    if(turn==0):
        line0 = "Quit during X's turn"
    else:
        line0 = "Quit during O's turn"
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2-1), math.trunc(maxyx[1]/2-math.trunc(len(line0)/2)))
    stdscr.addstr(line0)
    stdscr.refresh()
    time.sleep(2)
    curses.flushinp()
    frame = 0
    while (stdscr.getch()==curses.ERR and frame < 600):
        time.sleep(0.016)
        frame += 1

if __name__ == '__main__':
    main()
