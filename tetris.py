import curses
import time
import random
import math

Tets = ["XXXX",
        "X0X0X0X",
        "XXXX",
        "X0X0X0X",
        "X0XXX",
        "XX0X0X",
        "XXX0  X",
        " X0 X0XX",
        "  X0XXX",
        "X0X0XX",
        "XXX0X",
        "XX0 X0 X",
        "XX0XX",
        "XX0XX",
        "XX0XX",
        "XX0XX",
        " XX0XX",
        "X0XX0 X",
        " XX0XX",
        "X0XX0 X",
        " X0XXX",
        "X0XX0X",
        "XXX0 X",
        " X0XX0 X",
        "XX0 XX",
        " X0XX0X",
        "XX0 XX",
        " X0XX0X",]

def main():
    global maxyx
    global curs
    global curtet
    global curtetcount
    global dead
    global Tet
    global Tets
    global score
    global deadTets
    frame = 0
    deadTets = []
    score = 0
    stdscr = curses.initscr()
    curses.raw()
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)
    dead = False
    maxyx = stdscr.getmaxyx()
    initTet = [5, math.trunc(maxyx[1]/2)]
    Tet = [initTet[0], initTet[1]]
    curtet = random.randrange(0, len(Tets))
    drawTitle(stdscr)
    while(not dead):
        if (frame>60):
            frame = 0
        frame += 1
        drawBin(stdscr)
        drawTetrominos(stdscr)
        drawFallingTet(stdscr, frame)
        checkBounds(stdscr)
        if (hasToSet()):
            Tet[0] -= 1
            Set(Tet, curtet, deadTets, initTet)
            curtet = random.randrange(0, len(Tets)-1)
            Tet = [initTet[0], initTet[1]]
        try:
            c = stdscr.getkey()
        except:
            c = -1
        if (c == 'q'):
            break
        if (c == 'a'):
            Tet[1] -= 1
        if (c == 'd'):
            Tet[1] += 1
        if (c == 'w'):
            curtet = rotate(curtet)
        if (c == 's'):
            frame = 29
        if (c == ' '):
            while (stdscr.getch()==curses.ERR):
                stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-3))
                stdscr.addstr("PAUSED")
                time.sleep(0.016)
        stdscr.refresh()
        stdscr.erase()
        time.sleep(0.016)
    gameover(stdscr)
    time.sleep(2)
    curses.flushinp()
    while(stdscr.getch()==curses.ERR):
        time.sleep(0.016)
    curses.endwin()

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
    line2 = "w - Rotate"
    line3 = "a, d - Move"
    line4 = "Space - Pause"
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
    time.sleep(4)
    controlsbox.clear()
    stdscr.clear()
    controlsbox.refresh()
    stdscr.refresh()

def checkBounds(stdscr):
    if (Tet[1] > math.trunc(maxyx[1]*2/3-3)):
        Tet[1] -= 1
    elif (Tet[1] < math.trunc(maxyx[1]/3+1)):
        Tet[1] += 1

def hasToSet():
    curs = [Tet[0], Tet[1]]
    count = 0
    for i in Tets[curtet]:
        if (i == '0'):
            curs = [curs[0]+1, curs[1]-count]
            count = 0
            continue
        elif (i == ' '):
            count += 1
            curs[1] += 1
            continue
        else:
            count += 1
            for j in deadTets:
                if (j[0] == curs[0] and j[1] == curs[1]):
                    return True
            curs[1] += 1
    count = 0
    for i in Tets[curtet]:
        if (i == '0'):
            count += 1
    if (Tet[0] > maxyx[0]-3-count):
        return True
    return False

def Set(Tet, curtet, deadTets, initTet):
    count = 0
    curs = [Tet[0], Tet[1]]
    for i in Tets[curtet]:
        if (i == ' '):
            curs[1] += 1
            count += 1
        elif (i == '0'):
            curs = [curs[0]+1, curs[1]-count]
            count = 0
        else:
            deadTets.append([curs[0], curs[1]])
            count += 1
            curs[1] += 1

def rotate(curtet):
    if ((curtet+1)%4==0):
        curtet -= 4
    curtet += 1
    return curtet

def drawTitle(stdscr):
    title = "Tetris"
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-len(title)/2))
    stdscr.addstr(title)
    stdscr.refresh()
    time.sleep(3)

def gameover(stdscr):
    end = "Score: " + str(score)
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-len(end)/2))
    stdscr.addstr(end)
    stdscr.refresh()

def drawBin(stdscr):
    curs = [0, math.trunc(maxyx[1]/3)]
    stdscr.move(curs[0], curs[1])
    while(curs[0]<maxyx[0]-2):
        stdscr.addch("#")
        curs[0] += 1
        stdscr.move(curs[0], curs[1])
    while(curs[1]<math.trunc(maxyx[1]*2/3)):
        stdscr.addch("#")
        curs[1] += 1
    while(curs[0]>0):
        stdscr.addstr("#")
        curs[0] -= 1
        stdscr.move(curs[0], curs[1])
    stdscr.addch("#")

def drawTetrominos(stdscr):
    for i in (deadTets):
        stdscr.move(i[0], i[1])
        stdscr.addch("X")

def drawFallingTet(stdscr, frame):
    curs = [Tet[0], Tet[1]]
    stdscr.move(curs[0], curs[1])
    count = 0
    for i in Tets[curtet]:
        if (i == '0'):
            curs = [curs[0]+1, curs[1]-count]
            stdscr.move(curs[0], curs[1])
            count = 0
        else:
            stdscr.addch(i)
            curs[1] += 1
            count += 1
    if (frame%30==0):
        Tet[0] += 1


if __name__ == '__main__':
    main()
