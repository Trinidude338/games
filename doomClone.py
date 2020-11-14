#
#   Doom clone
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
    mapStr = []
    mapStr.append("############################################################")
    mapStr.append("#..............................#...........................#")
    mapStr.append("#..............................#...........................#")
    mapStr.append("#..............................#...........................#")
    mapStr.append("#..............................#...........................#")
    mapStr.append("#..............................#...........................#")
    mapStr.append("#..............................#...........................#")
    mapStr.append("#..............................#...........................#")
    mapStr.append("#..............................#...........................#")
    mapStr.append("#..............................#...........................#")
    mapStr.append("#..............................##################..........#")
    mapStr.append("#####################......................................#")
    mapStr.append("#...................#......................................#")
    mapStr.append("#...................#......................................#")
    mapStr.append("#...................#.......................################")
    mapStr.append("#...................#.......................#..............#")
    mapStr.append("#...................#.......................#..............#")
    mapStr.append("#..........................................................#")
    mapStr.append("############...............................................#")
    mapStr.append("#..........#................................#..............#")
    mapStr.append("#..........#................................#..............#")
    mapStr.append("#..........#................................#..............#")
    mapStr.append("#...........................................################")
    mapStr.append("#..........................................................#")
    mapStr.append("#..........#...............................................#")
    mapStr.append("#..........#...............................................#")
    mapStr.append("#..........#.............#..#..#..#..#..#..................#")
    mapStr.append("#..........#...............................................#")
    mapStr.append("#..........#.............#..#..#..#..#..#..................#")
    mapStr.append("############...............................................#")
    mapStr.append("#..........................................................#")
    mapStr.append("#...................###########............................#")
    mapStr.append("#...................###########............................#")
    mapStr.append("#...................###########............................#")
    mapStr.append("#...................###########............................#")
    mapStr.append("#...................###########............................#")
    mapStr.append("#...................###########............................#")
    mapStr.append("#...................###########............................#")
    mapStr.append("#...................###########............................#")
    mapStr.append("############################################################")
    frame = 0
    seconds = 0
    score = 0
    playerPos = [20.0, 20.0]
    playerA = 0.0
    playerFOV = 3.14159 / 1.75
    drawTitle(stdscr)
    drawControls(stdscr)
    elapsed = 0
    while(dead!=True):
        if (frame>59):
            frame = 0
            seconds += 1
        else:
            frame += 1
        #draw frame
        drawWalls(stdscr, mapStr, playerPos, playerA, playerFOV)
        #keyboard input
        try:
            c = stdscr.getkey()
        except:
            c = 0
        #moving, quitting, shooting, and all that stuff
        if (c == 'q'):
            gameover(stdscr)
            dead = True
        if (c == 'w'):
            playerPos[0] += math.sin(playerA)/3
            playerPos[1] += math.cos(playerA)/3
            if (mapStr[int(playerPos[1])][int(playerPos[0])]=='#'):
                playerPos[0] -= math.sin(playerA)/3
                playerPos[1] -= math.cos(playerA)/3
        if (c == 's'):
            playerPos[0] -= math.sin(playerA)/3
            playerPos[1] -= math.cos(playerA)/3
            if (mapStr[int(playerPos[1])][int(playerPos[0])]=='#'):
                playerPos[0] += math.sin(playerA)/3
                playerPos[1] += math.cos(playerA)/3
        if (c == 'a'):
            playerA -= 0.1 / 1
        if (c == 'd'):
            playerA += 0.1 / 1
        curses.flushinp()
        stdscr.refresh()
        stdscr.erase()
        time.sleep(0.016)
    curses.endwin()

def drawWalls(stdscr, mapStr, playerPos, playerA, playerFOV):
    maxyx = stdscr.getmaxyx()
    depth = 30.0
    curs = [0, 0]
    for curs[1] in range(maxyx[1]):
        rayAngle = (playerA - playerFOV / 2.0) + (curs[1] / maxyx[1]) * playerFOV
        distanceToWall = 0
        hitWall = False
        boundary = False
        eyePos = [math.sin(rayAngle), math.cos(rayAngle)]
        while(not hitWall and distanceToWall<depth):
            distanceToWall += 0.1
            testPos = [(playerPos[0] + eyePos[0] * distanceToWall), (playerPos[1] + eyePos[1] * distanceToWall)]
            if (testPos[0]<0 or testPos[0]>=len(mapStr[0]) or testPos[1]<0 or testPos[1]>=len(mapStr)):
                hitWall = True
                distanceToWall = depth
            else:
                if (mapStr[int(testPos[1])][int(testPos[0])]=='#'):
                    hitWall = True
        ceiling = (maxyx[0]/2) - maxyx[0] / distanceToWall
        floor = maxyx[0] - ceiling
        shade = ' '
        if (boundary):
            shade = '|'
        elif (distanceToWall<=depth/4.0):
            shade = '#'
        elif (distanceToWall<depth/3.0):
            shade = 'X'
        elif (distanceToWall<depth/2.0):
            shade = 'O'
        elif (distanceToWall<depth):
            shade = '.'
        else:
            shade = ' '
        for curs[0] in range(maxyx[0]):
            if (curs[0]<ceiling):
                try:
                    stdscr.addch(curs[0], curs[1], ' ')
                except:
                    pass
            elif (curs[0]>ceiling and curs[0]<=floor):
                try:
                    stdscr.addch(curs[0], curs[1], shade)
                except:
                    pass
            else:
                shade = ' '
                b = 1.0 - ((curs[0]-maxyx[0]/2.0)/(maxyx[0]/2.0))
                if (b < 0.25):
                    shade = '='
                elif (b < 0.5):
                    shade = '~'
                elif (b < 0.75):
                    shade = '-'
                elif (b < 0.9):
                    shade = '.'
                else:
                    shade = ' '
                try:
                    stdscr.addch(curs[0], curs[1], shade)
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
    line2 = "w, a, s, d - Move"
    line3 = "j - Shoot"
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


def drawTitle(stdscr):
    maxyx = stdscr.getmaxyx()
    title = "Doom"
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-math.trunc(len(title)/2)))
    stdscr.addstr(title)
    stdscr.refresh()
    time.sleep(1)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame < 60):
        frame += 1
        time.sleep(0.016)

def gameover(stdscr):
    maxyx = stdscr.getmaxyx()
    line0 = "You died."
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
