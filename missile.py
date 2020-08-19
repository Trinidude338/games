#
#   Not much but cheating using python,
#   a game written in mostly a generic paradigm
#
import curses
import math
import time
import random


#global variables because f**k you logic
rocketSprite = [
        ['0','0','0','|','/','0','0','0','0'],
        ['|','/','0','|','0','/','0','0','0'],
        ['=','=','=','=','=','=','=','=','-'],
        ['|','\\','0','|','0','\\','0','0','0'],
        ['0','0','0','|','\\','0','0','0','0']
        ]
rocketxy = []
bullets = []
bullets1 = []

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
    rocketxy = [math.trunc(maxyx[0]/2),1]
    frame = 0
    seconds = 0
    score = 0
    clouds = []
    enemys = []
    stars = []
    health = 20
    ammo = 20
    prevscore = 0
    notshootingframe = 0
    drawTitle(stdscr, prevscore)
    drawControls(stdscr)
    for i in range(125):
        stars.append([random.randrange(3), random.randrange(maxyx[0]-1), random.randrange(maxyx[1]-1)])
    while(dead!=True):
        if (frame>59):
            frame = 0
            seconds += 1
        else:
            frame += 1
        #draw frame
        drawBG(stdscr, stars)
        drawClouds(stdscr, clouds)
        drawBullets(stdscr, bullets, bullets1)
        for i in enemys:
            drawEnemy(stdscr, i[0], i[1], i[2])
        drawRocket(stdscr, rocketxy)
        drawUI(stdscr, health, ammo)
        #keyboard input
        try:
            c = stdscr.getkey()
        except:
            c = 0
        #moving, quitting, shooting, and all that stuff
        if (c == 'q'):
            break
        if (c == 'w'):
            rocketxy[0] -= 2
        if (c == 's'):
            rocketxy[0] += 2
        if (c == 'd'):
            rocketxy[1] += 2
        if (c == 'a'):
            rocketxy[1] -= 2
        if (c == 'j' and frame%1==0 and ammo>0):
            bullets.append([rocketxy[0]-3, rocketxy[1]+6])
            bullets.append([rocketxy[0]-1, rocketxy[1]+6])
            stdscr.move(rocketxy[0]+2, rocketxy[1]+1)
            ammo -= 2
            stdscr.addstr("FIRE", curses.COLOR_GREEN)
            stdscr.refresh()
        elif (c == 'j' and frame%2!=0):
            stdscr.move(rocketxy[0]+2, rocketxy[1]+1)
            stdscr.addstr("Fail!", curses.COLOR_RED)
            stdscr.refresh()
        if (c == ' '):
            while(stdscr.getch()==curses.ERR):
                stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-3))
                stdscr.addstr("PAUSED")
                time.sleep(0.016)
        if (c != 'j'):
            notshootingframe += 1
        #keeping rocket in bounds
        if (rocketxy[0]<5):
            rocketxy[0] = 5
        elif (rocketxy[0]>(maxyx[0]-2)):
                rocketxy[0] = (maxyx[0]-2)
        elif (rocketxy[1]<15):
                rocketxy[1] = 15
        elif (rocketxy[1]>(maxyx[1]-12)):
                rocketxy[1] = (maxyx[1]-12)
        #make enemies fire
        if (frame%random.randrange(20, 40)==0):
            for i in enemys:
                j = random.randrange(100)
                if (j%2==0):
                    bullets1.append([i[1]-2, i[2]-2])
                j = random.randrange(100)
                if (j%2==0):
                    bullets1.append([i[1]-2, i[2]-2])
        #move all player bullets to the right once
        for i in bullets:
            i[1] += 1
        #move all enemy bullets to the left once
        for i in bullets1:
            i[1] -= 1
        #move clouds
        if (frame%3==0):
            for i in clouds:
                i[1] -= 1
        #check for bullets at edge of screen and clear them
        for i in bullets:
            if (i[1]>=maxyx[1]-5):
                bullets.pop(bullets.index(i))
        for i in bullets1:
            if (i[1]<5):
                bullets1.pop(bullets1.index(i))
        #generate new clouds
        if (seconds%random.randrange(1,5)==0 and frame==0):
            clouds.append([random.randrange(maxyx[0]-10), maxyx[1]-5])
        #delete clouds at edge
        for i in clouds:
            if (i[1]-5==0):
                clouds.pop(clouds.index(i))
        #add new enemies
        if (seconds%random.randrange(1, 5)==0 and frame==0):
            enemys.append([random.randrange(5), random.randrange(maxyx[0]), maxyx[1]-10])
        #move enemies
        if(frame%3==0):
            for i in enemys:
                if (i[1]>=math.trunc(maxyx[0]/2)):
                    i[1] += random.randrange(-2, 1)
                else:
                    i[1] += random.randrange(-1, 2)
                i[2] += random.randrange(-1, 0)
                if (i[1]>maxyx[0]-10):
                    i[1] = maxyx[0]-10
                if (i[1]<10):
                    i[1] = 10
                if (i[2]>maxyx[1]-10):
                    i[2] = maxyx[1]-10
                if (i[2]<20):
                    i[2] = 20
        #detect bullet collisions
        for i in bullets1:
            if (i[0]<rocketxy[0] and i[0]>rocketxy[0]-6 and i[1]<rocketxy[1] and i[1]>rocketxy[1]-10):
                bullets1.pop(bullets1.index(i))
                curses.flash()
                health -= 1
        for i in bullets:
            for j in enemys:
                if (j[1]>=i[0]-2 and j[2]>=i[1]-2 and j[1]<=i[0]+2 and j[2]<=i[1]+2 ):
                    bullets.pop(bullets.index(i))
                    enemys.pop(enemys.index(j))
                    score += 1
                    ammo += 2
        #add stars
        if (frame%random.randrange(20, 40)==0):
            stars.append([random.randrange(3), random.randrange(maxyx[0]-1), maxyx[1]-1])
        #move stars
        if (frame%10==0):
            for i in stars:
                i[2] -= 1
        #delete stars at edge
        for i in stars:
            if (i[2]<=4):
                stars.pop(stars.index(i))
        #replenish ammo
        if (notshootingframe%180==0):
            ammo += 2
            if ammo>20:
                ammo = 20
        #check if dead
        if (health<1):
            gameover(stdscr, score)
            dead = True
        stdscr.refresh()
        stdscr.erase()
        time.sleep(0.016)
    curses.endwin()

def drawBG(stdscr, stars):
    maxyx = stdscr.getmaxyx()
    #stars
    for i in stars:
        if (i[0]==0):
            star = "*"
        elif (i[0]==1):
            star = "-"
        elif (i[0]==2):
            star = "."
        stdscr.move(i[1], i[2])
        stdscr.addch(star)
    #moon
    moon = ".-.,=\"''\"=.    0'=/_       \\0 |  '=._    |0  \\     '=./`,0   '=.__.=' `='"
    count = 0
    curs = [10, maxyx[1]-20]
    for i in moon:
        if (i==' '):
            count += 1
            curs[1] += 1
            continue
        elif (i=='0'):
            curs[1] -= count
            curs[0] += 1
            count = 0
            continue
        else:
            stdscr.addch(curs[0], curs[1], i)
            curs[1] += 1
            count += 1

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
    time.sleep(4)
    controlsbox.clear()
    stdscr.clear()
    controlsbox.refresh()
    stdscr.refresh()


def drawTitle(stdscr, prevscore):
    maxyx = stdscr.getmaxyx()
    title = "Missile"
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-math.trunc(len(title)/2)))
    stdscr.addstr(title)
    stdscr.refresh()
    time.sleep(2)

def gameover(stdscr, score):
    #story or sum shiiid
    maxyx = stdscr.getmaxyx()
    line0 = "Your aircraft was shot down after you took out " + str(score) + " enemy fighter planes."
    line1 = "Your name will soon be forgotten. As with most of your comrades."
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2-1), math.trunc(maxyx[1]/2-math.trunc(len(line0)/2)))
    stdscr.addstr(line0)
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-math.trunc(len(line1)/2)))
    stdscr.addstr(line1)
    stdscr.refresh()
    time.sleep(2)
    curses.flushinp()
    while (stdscr.getch()==curses.ERR):
        time.sleep(0.016)

def drawUI(stdscr, health, ammo):
    stdscr.move(0, 0)
    stdscr.addstr("Health: [")
    while (health>0):
        stdscr.addch('#')
        health -= 1
    stdscr.move(0, 29)
    stdscr.addch(']')
    stdscr.move(0, 35)
    stdscr.addstr("Ammo: [")
    while ammo>0:
        stdscr.addch("-")
        ammo -= 1
    stdscr.move(0, 62)
    stdscr.addch("]")

def drawEnemy(stdscr, enemId, enemY, enemX):
    maxyx = stdscr.getmaxyx()
    enemys = [
            #format:
            #[
            #"x", <-sprite as a string, 0 anywhere in the string corresponds to newline (str)
            #y, <---How many characters per line (int)
            #z <----How many lines the sprite takes up (int)
            #]
            ["-O%",
            3,
            1],
            ["  /|0-===0  \\|",
            4,
            3],
            ["-(O)",
            4,
            1],
            ["fuck",
            4,
            1],
            ["--=0  O0--=",
            3,
            3]
            ]
    enemy = enemys[enemId]
    curs = [enemY, enemX]
    if (curs[0]<maxyx[0]-enemy[2] and curs[1]<maxyx[1]-enemy[1] and curs[0]>0 and curs[1]>0):
        count = 0
        for i in enemy[0]:
            if (i == ' '):
                count += 1
                curs[1] += 1
                continue
            elif (i == '0'):
                curs[1] -= count
                curs[0] += 1
                count = 0
            else:
                stdscr.move(curs[0], curs[1])
                stdscr.addch(i)
                curs[1] += 1
                count += 1

def drawClouds(stdscr, points):
    #I like clouds
    maxyx = stdscr.getmaxyx()
    cloud = "   ___   0  (   )  0(___)___)"
    for i in points:
        curs = [i[0],i[1]]
        if (curs[0]<maxyx[0]-5 and curs[1]<maxyx[1]-10 and curs[0]>0 and curs[1]>0):
            for j in cloud:
                count = 0
                if (j == ' '):
                    curs[1] += 1
                    count += 1
                    continue
                elif (j == '0'):
                    curs[1] -= count+9
                    count = 0
                    curs[0] += 1
                else:
                    stdscr.move(curs[0], curs[1])
                    stdscr.addch(j)
                    count += 1
                    curs[1] += 1

def drawBullets(stdscr, points, points1):
    #pew pew
    for i in points:
        stdscr.move(i[0], i[1])
        stdscr.addch("-")
    for i in points1:
        stdscr.move(i[0], i[1])
        stdscr.addch("-")

def drawRocket(stdscr, points):
    locy = 0
    locx = 0
    stdscr.move(points[0],points[1])
    for i in range(5):
            for j in range(9):
                    if (rocketSprite[i][j] == '0'):
                            tmp = stdscr.getyx()
                            locy = tmp[0]
                            locx = tmp[1]
                            stdscr.move(locy, locx+1)
                    else: 
                        stdscr.addch(rocketSprite[i][j])
            tmp = stdscr.getyx()
            locy = tmp[0]
            locx = tmp[1]
            stdscr.move(locy-1, locx-9)

if __name__ == '__main__':
    main()
