import curses
import time
import random
import math


def main():
    Tets = ["AAAA",
            "A0A0A0A", 
            "AAAA", 
            "A0A0A0A", 
            "B0BBB", 
            "BB0B0B", 
            "BBB0  B", 
            " B0 B0BB", 
            "  C0CCC", 
            "C0C0CC", 
            "CCC0C", 
            "CC0 C0 C", 
            "DD0DD", 
            "DD0DD", 
            "DD0DD", 
            "DD0DD", 
            " EE0EE", 
            "E0EE0 E", 
            " EE0EE", 
            "E0EE0 E", 
            " F0FFF", 
            "F0FF0F", 
            "FFF0 F", 
            " F0FF0 F", 
            "GG0 GG", 
            " G0GG0G", 
            "GG0 GG", 
            " G0GG0G"]
    frame = 0
    deadTets = []
    cols = []
    score = 0
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.raw()
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)
    dead = False
    maxyx = stdscr.getmaxyx()
    initTet = [5, math.trunc(maxyx[1]/2)]
    Tet = [initTet[0], initTet[1]]
    curtet = random.choice(range(0, len(Tets), 4))
    nextet = random.choice(range(0, len(Tets), 4))
    drawTitle(stdscr)
    drawControls(stdscr)
    curses.flushinp()
    while(not dead):
        if (frame>60):
            frame = 0
        frame += 1
        drawBin(stdscr)
        drawTetrominos(stdscr, deadTets)
        drawFallingTet(stdscr, frame, Tet, curtet, Tets)
        drawUI(stdscr, Tets, nextet, score)
        checkBounds(stdscr, cols, Tet)
        if (hasToSet(stdscr, Tet, deadTets, curtet, Tets, cols)):
            Set(Tet, curtet, deadTets, initTet, Tets)
            curtet = nextet
            nextet = random.choice(range(0, len(Tets), 4))
            Tet = [initTet[0], initTet[1]]
        try:
            c = stdscr.get_wch()
        except:
            c = -1
        if (c=='q'):
            break
        if (c=='a' or c==curses.KEY_LEFT):
            Tet[1] -= 1
        if (c=='d' or c==curses.KEY_RIGHT):
            Tet[1] += 1
        if (c=='w' or c==curses.KEY_UP):
            curtet = rotate(curtet)
        if (c=='s' or c==curses.KEY_DOWN):
            frame = 59
        if (c==' '):
            while (stdscr.getch()==curses.ERR):
                stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-3))
                stdscr.addstr("PAUSED")
                time.sleep(0.016)
        #game loop stuff
        cols = []
        count = 0
        y, x = Tet[0], Tet[1]
        for i in Tets[curtet]:
            if(i=='0'):
                x -= count
                count = 0
                y += 1
            elif(i==' '):
                x += 1
                count += 1
            else:
                cols.append([y, x])
                x += 1
                count += 1
        for y in range(0, int(maxyx[0])):
            shiftnum = 0
            for x in range(int(maxyx[1]/2-12), int(maxyx[1]/2+12)):
                for c in range(65, 72):
                    if([y, x, chr(c)] in deadTets):
                        shiftnum += 1
            if(shiftnum>=19):
                toPop = []
                for i in deadTets:
                    if(i[0]==y or i[0]==int(maxyx[0]*2/3+1)):
                        toPop.append(i)
                for i in toPop:
                    deadTets.remove(i)
                for i in deadTets:
                    if(i[0]<y):
                        i[0] += 1
                score += 1
                shiftnum = 0
                curses.flash()
        #
        stdscr.refresh()
        stdscr.erase()
        time.sleep(0.016)
    gameover(stdscr, score)
    time.sleep(2)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame < 600):
        time.sleep(0.016)
        frame += 1
    curses.endwin()

def drawUI(stdscr, Tets, nextet, score):
    maxyx = stdscr.getmaxyx()
    line0 = "Next Piece: "
    line1 = "Score: "
    stdscr.addstr(5, int(maxyx[1]/2-30), line0)
    stdscr.addstr(5, int(maxyx[1]/2+15), line1)
    count = 0
    curs = [5, int(maxyx[1]/2-30+len(line0))]
    for i in Tets[nextet]:
        if(i=='0'):
            curs[1] -= count
            count = 0
            curs[0] += 1
        elif(i==' '):
            count += 1
            curs[1] += 1
        else:
            count += 1
            curs[1] += 1
            stdscr.addch(curs[0], curs[1], i, curses.color_pair(int(nextet/4)+1))
    curs = [5, int(maxyx[1]/2+15+len(line1))]
    stdscr.addstr(curs[0], curs[1], str(score))


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
    frame = 0
    curses.flushinp()
    while(stdscr.getch()==curses.ERR and frame < 300):
        frame += 1
        time.sleep(0.016)
    controlsbox.clear()
    stdscr.clear()
    controlsbox.refresh()
    stdscr.refresh()

def checkBounds(stdscr, cols, Tet):
    maxyx = stdscr.getmaxyx()
    walls0 = []
    walls1 = []
    for i in range(5, int(maxyx[0]-1)):
        walls0.append([i, int(maxyx[1]/2-10)])
    for i in range(5, int(maxyx[0]-1)):
        walls1.append([i, int(maxyx[1]/2+10)])
    for i in cols:
        if (i in walls1):
            Tet[1] -= 1
            break
        if (i in walls0):
            Tet[1] += 1
            break

def hasToSet(stdscr, Tet, deadTets, curtet, Tets, cols):
    maxyx = stdscr.getmaxyx()
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
                    Tet[0] -= 1
                    return True
            curs[1] += 1
    count = 0
    for i in Tets[curtet]:
        if (i == '0'):
            count += 1
    ground0 = []
    for i in range(int(maxyx[1]/2-12), int(maxyx[1]/2+12)):
        ground0.append([int(maxyx[0]*2/3)+1, i])
    for i in cols:
        if(i in ground0):
            Tet[0] -= 1
            return True
    return False

def Set(Tet, curtet, deadTets, initTet, Tets):
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
            deadTets.append([curs[0], curs[1], Tets[curtet][-1], int(curtet/4)+1])
            count += 1
            curs[1] += 1

def rotate(curtet):
    if (curtet%4==3):
        curtet -= 3
    else:
        curtet += 1
    return curtet

def drawTitle(stdscr):
    maxyx = stdscr.getmaxyx()
    title = ["ooooooooooooo               .             o8o          ", "8'   888   `8             .o8             `\"'          ", "     888       .ooooo.  .o888oo oooo d8b oooo   .oooo.o", "     888      d88' `88b   888   `888\"\"8P `888  d88(  \"8", "     888      888ooo888   888    888      888  `\"Y88b.", "     888      888    .o   888 .  888      888  o.  )88b", "    o888o     `Y8bod8P'   \"888\" d888b    o888o 8\"\"888P'"]
    stdscr.clear()
    for num, i in enumerate(range(int(0-len(title)/2), int(len(title)/2+1))):
        try:
            stdscr.move(math.trunc(maxyx[0]/2+i), math.trunc(maxyx[1]/2-len(title[num])/2))
            stdscr.addstr(title[num], curses.color_pair(9))
        except:
            pass
    stdscr.refresh()
    time.sleep(3)

def gameover(stdscr, score):
    maxyx = stdscr.getmaxyx()
    end = "Score: " + str(score)
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-len(end)/2))
    stdscr.addstr(end)
    stdscr.refresh()

def drawBin(stdscr):
    maxyx = stdscr.getmaxyx()
    curs = [5, math.trunc(maxyx[1]/2-10)]
    stdscr.move(curs[0], curs[1])
    while(curs[0]<maxyx[0]*2/3):
        stdscr.addch("#", curses.color_pair(8))
        curs[0] += 1
        stdscr.move(curs[0], curs[1])
    while(curs[1]<math.trunc(maxyx[1]/2+10)):
        stdscr.addch("#", curses.color_pair(8))
        curs[1] += 1
    while(curs[0]>5):
        stdscr.addstr("#", curses.color_pair(8))
        curs[0] -= 1
        stdscr.move(curs[0], curs[1])
    stdscr.addch("#", curses.color_pair(8))

def drawTetrominos(stdscr, deadTets):
    for i in (deadTets):
        stdscr.move(i[0], i[1])
        stdscr.addch(i[2], curses.color_pair(i[3]))

def drawFallingTet(stdscr, frame, Tet, curtet, Tets):
    curs = [Tet[0], Tet[1]]
    count = 0
    for i in Tets[curtet]:
        if (i == '0'):
            curs = [curs[0]+1, curs[1]-count]
            count = 0
        elif(i==' '):
            curs[1] += 1
            count += 1
        else:
            stdscr.addch(curs[0], curs[1], i, curses.color_pair(int(curtet/4)+1))
            curs[1] += 1
            count += 1
    if (frame%30==0):
        Tet[0] += 1


if __name__ == '__main__':
    main()
