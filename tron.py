import curses
import math
import time
import random

def main():
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.nodelay(True)
    curses.raw()            
    stdscr.keypad(True)
    curses.curs_set(0)      
    maxyx = stdscr.getmaxyx()
    drawTitle(stdscr)
    drawControls(stdscr)
    player1yx = [math.trunc(maxyx[0]/2), 2]
    player2yx = [math.trunc(maxyx[0]/2), math.trunc(maxyx[1])-2]
    p1dir = 1
    p2dir = 3
    p1trail = list()
    p2trail = list()
    dead = False
    while(not dead):
        stdscr.box()
        drawPlayerTrail(stdscr, p1trail, 0)
        drawPlayerTrail(stdscr, p2trail, 1)
        drawPlayers(stdscr, player1yx, player2yx)
        #Main Loop here
        try:
            c = stdscr.getch()
        except:
            c = -1
        if (c==ord('q')):
            dead = True
        if (c==ord(' ')):
            while (stdscr.getch()==curses.ERR):
                stdscr.addstr(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2)-3, "PAUSED")
                time.sleep(0.016)
        if (c==ord('w')):
            p1dir = 0
        elif (c==ord('d')):
            p1dir = 1
        elif (c==ord('s')):
            p1dir = 2
        elif (c==ord('a')):
            p1dir = 3
        if (c==ord('u')):
            p2dir = 0
        elif (c==ord('k')):
            p2dir = 1
        elif (c==ord('j')):
            p2dir = 2
        elif (c==ord('h')):
            p2dir = 3
        if (p1dir==0):
            player1yx[0] -= 1
        elif (p1dir==1):
            player1yx[1] += 1
        elif (p1dir==2):
            player1yx[0] += 1
        elif (p1dir==3):
            player1yx[1] -= 1
        if (p2dir==0):
            player2yx[0] -= 1
        elif (p2dir==1):
            player2yx[1] += 1
        elif (p2dir==2):
            player2yx[0] += 1
        elif (p2dir==3):
            player2yx[1] -= 1
        if (player1yx[0]==0 or player1yx[0]==maxyx[0]-1 or player1yx[1]==0 or player1yx[1]==maxyx[1]-1):
            dead = True
            winner = 1
        if (player2yx[0]==0 or player2yx[0]==maxyx[0]-1 or player2yx[1]==0 or player2yx[1]==maxyx[1]-1):
            dead = True
            winner = 0
        p1trail.append([player1yx[0], player1yx[1]])
        p2trail.append([player2yx[0], player2yx[1]])
        for i in p1trail:
            if (player2yx[0]==i[0] and player2yx[1]==i[1]):
                dead = True
                winner = 0
        for i in p2trail:
            if (player1yx[0]==i[0] and player1yx[1]==i[1]):
                dead = True
                winner = 1
        #
        stdscr.refresh()
        stdscr.erase()
        time.sleep(0.08)
    gameover(stdscr, winner)
    stdscr.refresh()
    curses.endwin()
    exit(0)

def gameover(stdscr, winner):
    maxyx = stdscr.getmaxyx()
    time.sleep(2)
    if (winner == 0):
        line = "X won"
    else:
        line = "O won"
    stdscr.addstr(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-len(line)/2), line)
    stdscr.refresh()
    time.sleep(2)
    curses.flushinp()
    frame = 0
    stdscr.erase()
    stdscr.addstr(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-len(line)/2), line)
    stdscr.refresh()
    while (stdscr.getch()==curses.ERR and frame < 120):
        frame += 1
        time.sleep(0.016)

def drawPlayers(stdscr, yx1, yx2):
    maxyx = stdscr.getmaxyx()
    stdscr.addch(yx1[0],yx1[1],curses.ACS_BLOCK)
    stdscr.addch(yx2[0],yx2[1],curses.ACS_BLOCK)

def drawPlayerTrail(stdscr, trail, player):
    for i in trail:
        if (player == 0):
            stdscr.addch(i[0], i[1], 'X')
        else:
            stdscr.addch(i[0], i[1], 'O')

def drawTitle(stdscr):
    maxyx = stdscr.getmaxyx()
    title = "Tron"
    stdscr.addstr(math.trunc(maxyx[0]/2),math.trunc(maxyx[1]/2-len(title)/2), title)
    stdscr.refresh()
    time.sleep(1)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame<60):
        frame += 1
        time.sleep(0.016)
    stdscr.erase()
    stdscr.refresh()

def drawControls(stdscr):
    maxyx = stdscr.getmaxyx()
    stdscr.erase()
    stdscr.refresh()
    line0 = "Quit - q"
    line1 = "Pause - Space"
    line2 = "Player 1 - w,a,s,d"
    line3 = "Player 2 - u,h,j,k"
    controlsbox = curses.newwin(math.trunc(maxyx[0]*3/5), math.trunc(maxyx[1]/3), math.trunc(maxyx[0]/5), math.trunc(maxyx[1]/3))
    curses.raw()
    curses.noecho()
    curses.cbreak()
    controlsbox.nodelay(True)
    controlsbox.keypad(True)
    maxyx1 = controlsbox.getmaxyx()
    controlsbox.border()
    controlsbox.move(math.trunc(maxyx1[0]/2)-3, math.trunc(maxyx1[1]/2-len(line0)/2))
    controlsbox.addstr(line0)
    controlsbox.move(math.trunc(maxyx1[0]/2)-1, math.trunc(maxyx1[1]/2-len(line1)/2))
    controlsbox.addstr(line1)
    controlsbox.move(math.trunc(maxyx1[0]/2)+1, math.trunc(maxyx1[1]/2-len(line2)/2))
    controlsbox.addstr(line2)
    controlsbox.move(math.trunc(maxyx1[0]/2)+3, math.trunc(maxyx1[1]/2-len(line3)/2))
    controlsbox.addstr(line3)
    stdscr.refresh()
    controlsbox.refresh()
    time.sleep(1)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame<300):
        frame += 1
        time.sleep(0.016)
    controlsbox.clear()
    stdscr.clear()
    controlsbox.refresh()
    stdscr.refresh()

if __name__ == '__main__':
    main()
