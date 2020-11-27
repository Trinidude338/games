#
#   This is not Broforce
#
import curses
import math
import time
import random


def main():
    dead = False
    stdscr = curses.initscr()
    curses.raw()
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.curs_set(0)
    maxyx = stdscr.getmaxyx()
    bullets = []
    frame = 0
    seconds = 0
    direc = 0
    thrust = [0.0, 0.0, 0.0]
    playerPos = [math.trunc(maxyx[0]/2), 2]
    ThaBigG = 1
    terrain = genTerrain(stdscr)
    drawTitle(stdscr)
    drawControls(stdscr)
    while(dead!=True):
        if (frame>59):
            frame = 0
            seconds += 1
        else:
            frame += 1
        #draw frame
        drawTerrain(stdscr, terrain)
        drawPlayer(stdscr, playerPos, direc)
        drawBullets(stdscr, bullets)
        #keyboard input
        try:
            c = stdscr.getkey()
        except:
            c = 0
        #moving, quitting, and all that stuff
        if (c=='q'):
            gameover(stdscr)
            break
        if (c=='d'):
            thrust[2] = 3
            direc = 0
        if (c=='a'):
            thrust[1] = 3
            direc = 1
        if (c==' ' or c=='w'):
            thrust[0] = 4
        if (c=='j'):
            if (direc==0):
                bullets.append([playerPos[0]+3, playerPos[1]+12, 0, random.randrange(2)])
            else:
                bullets.append([playerPos[0]+3, playerPos[1]-1, 1, random.randrange(2)])
        if (c=='p'):
            while(stdscr.getch()==curses.ERR):
                stdscr.addstr(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-3), "PAUSED")
                stdscr.refresh()
                time.sleep(0.016)
        #game loop stuff
        for i in bullets:
            if (i[3]==0):
                if (random.randrange(20)==0):
                    i[0] += 1
            else:
                if (random.randrange(20)==0):
                    i[0] -= 1
        for j in terrain:
            for i in bullets:
                if (i[3]==0):
                    if (i[1]>=j[1] and i[1]+3<=j[1] and i[0]==j[0] and i[0]==j[0]):
                        try:
                            bullets.pop(bullets.index(i))
                            terrain.pop(terrain.index(j))
                        except:
                            pass
                else:
                    if (i[1]>=j[1] and i[1]-3<=j[1] and i[0]==j[0] and i[0]==j[0]):
                        try:
                            bullets.pop(bullets.index(i))
                            terrain.pop(terrain.index(j))
                        except:
                            pass
        for i in bullets:
            if (i[2]==0):
                i[1] += 3
            else:
                i[1] -= 3
        if (playerPos[1]<6):
            playerPos[1] = 6
            for i in terrain:
                i[1] += 1
        if (playerPos[1]>maxyx[1]-12):
            playerPos[1] = maxyx[1]-12
            for i in terrain:
                i[1] -= 1
        ThaBigG += 0.3
        if(thrust[0]>0):
            thrust[0] -= 0.1
        if(thrust[1]>0):
            thrust[1] -= 0.2
        if(thrust[2]>0):
            thrust[2] -= 0.2
        playerPos[0] -= math.trunc(thrust[0])
        for i in terrain:
            if(playerPos[0]<=i[0] and playerPos[0]+12>=i[0] and playerPos[1]<=i[1] and playerPos[1]+12>=i[1]):
                playerPos[0] += math.trunc(thrust[0])
        playerPos[0] += math.trunc(ThaBigG)
        for i in terrain:
            if(playerPos[0]<=i[0] and playerPos[0]+12>=i[0] and playerPos[1]<=i[1] and playerPos[1]+12>=i[1]):
                ThaBigG = 1
                playerPos[0] -= math.trunc(ThaBigG)
        playerPos[1] -= math.trunc(thrust[1])
        for i in terrain:
            if(playerPos[0]<=i[0] and playerPos[0]+12>=i[0] and playerPos[1]<=i[1] and playerPos[1]+12>=i[1]):
                playerPos[1] += math.trunc(thrust[1])
        playerPos[1] += math.trunc(thrust[2])
        for i in terrain:
            if(playerPos[0]<=i[0] and playerPos[0]+12>=i[0] and playerPos[1]<=i[1] and playerPos[1]+12>=i[1]):
                playerPos[1] -= math.trunc(thrust[2])
        #
        stdscr.refresh()
        time.sleep(0.016)
        stdscr.erase()
    curses.endwin()

def drawBullets(stdscr, bullets):
    maxyx = stdscr.getmaxyx()
    for i in bullets:
        try:
            stdscr.addch(i[0], i[1], '-')
        except:
            pass

def drawTerrain(stdscr, terrain):
    maxyx = stdscr.getmaxyx()
    for i in terrain:
        try:
            stdscr.addch(i[0], i[1], i[2])
        except:
            pass

def genTerrain(stdscr):
    maxyx = stdscr.getmaxyx()
    lst = []
    for x in range(-500, 1000):
        for y in range(maxyx[0]-random.randrange(6, 8), maxyx[0]+4):
            lst.append([y, x, chr(random.randrange(35, 38))])
    return lst


def drawPlayer(stdscr, playerPos, direc):
    maxyx = stdscr.getmaxyx()
    sprite0 = """ ###
#####
 ###
#-----------
#|/ | #|
 ###|  #\\_
  ##
  ##
  ##&
 ----
##  ##
##  ##
##  ##"""
    sprite1 = """        ###
       #####
        ###
-----------#
    |# | \\|#
  _/#  |###
        ##
        ##
        ##&
       ----
      ##  ##
      ##  ##
      ##  ##"""
    curs = [0, 0]
    count = 0
    curs[0] = int(playerPos[0])
    curs[1] = int(playerPos[1])
    if(direc==0):
        for i in sprite0.splitlines():
            for j in i:
                if(j==' '):
                    curs[1] += 1
                    count += 1
                else:
                    try:
                        stdscr.addch(curs[0], curs[1], j)
                    except:
                        pass
                    curs[1] += 1
                    count += 1
            curs[0] += 1
            curs[1] -= count
            count = 0
    else:
        for i in sprite1.splitlines():
            for j in i:
                if(j==' '):
                    curs[1] += 1
                    count += 1
                else:
                    try:
                        stdscr.addch(curs[0], curs[1], j)
                    except:
                        pass
                    curs[1] += 1
                    count += 1
            curs[0] += 1
            curs[1] -= count
            count = 0

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
    line4 = "p - Pause"
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
    title = "TINB"
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
    line0 = "You died"
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
