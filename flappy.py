#
#   flappy bird
#
import curses
import math
import time
import random


def main():
    dead = False
    stdscr = curses.initscr()
    curses.start_color()
    curses.raw()
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.curs_set(0)
    maxyx = stdscr.getmaxyx()
    frame = 0
    seconds = 0
    score = 0
    prevscore = 0
    accelerationFlappy = 1
    upthrustFlappy = 0
    tubes = genTubes(stdscr)
    flappyPos = [math.trunc(maxyx[0]/2)-20, math.trunc(maxyx[1]/2)]
    drawTitle(stdscr, prevscore)
    drawControls(stdscr)
    while(dead!=True):
        if (frame>59):
            frame = 0
            seconds += 1
        else:
            frame += 1
            upthrustFlappy -= 0.1
        #draw frame
        drawFlappy(stdscr, flappyPos)
        drawTubes(stdscr, tubes)
        drawUI(stdscr, score)
        #keyboard input
        try:
            c = stdscr.getkey()
        except:
            c = 0
        #moving, quitting, and all that stuff
        if (c=='q'):
            gameover(stdscr, score)
            break
        elif (c==' '):
            upthrustFlappy += 3
        elif (c=='p'):
            while(stdscr.getch()==curses.ERR):
                drawFlappy(stdscr, flappyPos)
                drawTubes(stdscr, tubes)
                drawUI(stdscr, score)
                stdscr.addstr(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-3), "PAUSED")
                stdscr.refresh()
                time.sleep(0.016)
        #game loop stuff
        flappyPos[0] -= math.trunc(accelerationFlappy*upthrustFlappy)
        if (frame%2==0):
            flappyPos[0] += accelerationFlappy
        if (frame%3==0):
            for i in tubes:
                i[0][1] -= 2
                i[1][1] -= 2
        if (flappyPos[0]<0):
            flappyPos[0] = 0
            upthrustFlappy /= 2
        for i in tubes:
            if (flappyPos[0]<i[0][0] and flappyPos[1]+6>=i[0][1]-9 and flappyPos[1]+6<=i[0][1]+9 or flappyPos[0]+8>i[1][0] and flappyPos[1]+6>=i[1][1]-9 and flappyPos[1]+6<=i[1][1]+9):
                time.sleep(3)
                curses.flash()
                gameover(stdscr, score)
                dead = True
        score = 0
        for i in tubes:
            if (flappyPos[1]>i[0][1]):
                score += 1
        if (flappyPos[0]>maxyx[0]):
            time.sleep(3)
            curses.flash()
            gameover(stdscr, score)
            dead = True
        #
        stdscr.refresh()
        time.sleep(0.016)
        stdscr.erase()
    curses.endwin()

def drawUI(stdscr, score):
    maxyx = stdscr.getmaxyx()
    stdscr.move(0, 0)
    stdscr.addstr("Score: ")
    stdscr.addstr(str(score))

def genTubes(stdscr):
    maxyx = stdscr.getmaxyx()
    lst = []
    for i in range(80, 8000, 80):
        x = random.randrange(maxyx[0]-30)
        lst.append([[x, i+maxyx[1]],[x+30, i+maxyx[1]]])
    return lst

def drawTubes(stdscr, tubes):
    maxyx = stdscr.getmaxyx()
    curs = [0, 0]
    for i in tubes:
        #top
        curs[0] = i[0][0]
        curs[1] = i[0][1]-7
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_LLCORNER)
            except:
                pass
        curs[1] += 1
        for j in range(13):
            if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                try:
                        stdscr.addch(curs[0], curs[1], curses.ACS_HLINE)
                except:
                    pass
            curs[1] += 1
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_LRCORNER)
            except:
                pass
        curs[1] += 1
        curs[0] = i[0][0]-1
        curs[1] = i[0][1]-7
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                    stdscr.addch(curs[0], curs[1], curses.ACS_ULCORNER)
            except:
                pass
        curs[1] += 1
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_LRCORNER)
            except:
                pass
        curs[1] += 1
        for j in range(11):
            if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                try:
                        stdscr.addch(curs[0], curs[1], ' ')
                except:
                    pass
            curs[1] += 1
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_LLCORNER)
            except:
                pass
        curs[1] += 1
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_URCORNER)
            except:
                pass
        curs[1] += 1
        for j in range(i[0][0]-2, 0, -1):
            curs[0] = j
            curs[1] = i[0][1]-6
            if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                try:
                    stdscr.addch(curs[0], curs[1], curses.ACS_VLINE)
                except:
                    pass
            curs[1] += 1
            for x in range(11):
                if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                    try:
                        stdscr.addch(curs[0], curs[1], ' ')
                    except:
                            pass
                curs[1] += 1
            if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                try:
                    stdscr.addch(curs[0], curs[1], curses.ACS_VLINE)
                except:
                    pass
            curs[1] += 1
        #bottom
        curs[0] = i[1][0]-2
        curs[1] = i[1][1]-7
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_ULCORNER)
            except:
                pass
        curs[1] += 1
        for j in range(13):
            if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                try:
                    stdscr.addch(curs[0], curs[1], curses.ACS_HLINE)
                except:
                    pass
            curs[1] += 1
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                    stdscr.addch(curs[0], curs[1], curses.ACS_URCORNER)
            except:
                pass
        curs[1] += 1
        curs[0] = i[1][0]-1
        curs[1] = i[1][1]-7
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_LLCORNER)
            except:
                pass
        curs[1] += 1
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_URCORNER)
            except:
                pass
        curs[1] += 1
        for j in range(11):
            if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                try:
                    stdscr.addch(curs[0], curs[1], ' ')
                except:
                    pass
            curs[1] += 1
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_ULCORNER)
            except:
                pass
        curs[1] += 1
        if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
            try:
                stdscr.addch(curs[0], curs[1], curses.ACS_LRCORNER)
            except:
                    pass
        curs[1] += 1
        for j in range(i[1][0], maxyx[0]-1, 1):
            curs[0] = j
            curs[1] = i[1][1]-6
            if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                try:
                    stdscr.addch(curs[0], curs[1], curses.ACS_VLINE)
                except:
                    pass
            curs[1] += 1
            for x in range(11):
                if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                    try:
                        stdscr.addch(curs[0], curs[1], ' ')
                    except:
                        pass
                curs[1] += 1
            if (curs[0]<maxyx[0] and curs[1]<maxyx[1]):
                try:
                    stdscr.addch(curs[0], curs[1], curses.ACS_VLINE)
                except:
                    pass
            curs[1] += 1

def drawFlappy(stdscr, pos):
    maxyx = stdscr.getmaxyx()
    curs = [pos[0], pos[1]]
    #stdscr.addch(curs[0], curs[1], 'X')
    count = 0
    sprite = "   _=======___\n  _=000000=000=\n _======00=0@0=\n=0000000=0=___=\n=0000000=000======\n =======000=______=\n  =000000000=____=\n   ========="
    for i in sprite:
        if (i==' '):
            curs[1] += 1
            count += 1
        elif (i=='0'):
            curs[1] += 1
            count += 1
            if (curs[0]<maxyx[0]-1 and curs[1]<maxyx[1]-1):
                try:
                    stdscr.addch(curs[0], curs[1], ' ')
                except:
                    pass
        elif (i=='\n'):
            curs[0] += 1
            curs[1] -= count
            count = 0
        else:
            curs[1] += 1
            count += 1
            if (curs[0]<maxyx[0]-1 and curs[1]<maxyx[1]-1):
                try:
                    stdscr.addch(curs[0], curs[1], i)
                except:
                    pass


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
    line2 = "Space - Move"
    line3 = "p - Pause"
    controlsbox.move(math.trunc(maxyx1[0]/2)-5, math.trunc(maxyx1[1]/2-len(line0)/2))
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
    while(stdscr.getch()==curses.ERR and frame < 300):
        frame += 1
        time.sleep(0.016)
    controlsbox.clear()
    stdscr.clear()
    controlsbox.refresh()
    stdscr.refresh()


def drawTitle(stdscr, prevscore):
    maxyx = stdscr.getmaxyx()
    title = "Flappy"
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-math.trunc(len(title)/2)))
    stdscr.addstr(title)
    stdscr.refresh()
    time.sleep(1)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame < 60):
        frame += 1
        time.sleep(0.016)

def gameover(stdscr, score):
    maxyx = stdscr.getmaxyx()
    line0 = "You died"
    line1 = "Score : " + str(score)
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2-1), math.trunc(maxyx[1]/2-math.trunc(len(line0)/2)))
    stdscr.addstr(line0)
    stdscr.move(math.trunc(maxyx[0]/2+1), math.trunc(maxyx[1]/2-math.trunc(len(line1)/2)))
    stdscr.addstr(line1)
    stdscr.refresh()
    time.sleep(2)
    curses.flushinp()
    frame = 0
    while (stdscr.getch()==curses.ERR and frame < 600):
        time.sleep(0.016)
        frame += 1

if __name__ == '__main__':
    main()
