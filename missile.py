#
#   Not much but cheating using python,
#   a game written in mostly a generic paradigm
#
import curses
import math
import time
import random


def main():
    dead = False
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
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
    half = 0
    playerCols = []
    enemCols = []
    ufoCols = []
    clouds = []
    enemys = []
    stars = []
    bullets = []
    bullets1 = []
    ufos = []    
    rocketSprite = [
            ['0','0','0','|','/','0','0','0','0'],
            ['|','/','0','|','0','/','0','0','0'],
            ['=','=','=','=','=','=','=','=','-'],
            ['|','\\','0','|','0','\\','0','0','0'],
            ['0','0','0','|','\\','0','0','0','0']
    ]
    ufosSpriteList = ["    .---.   0  _/_____\_  0 (_________) 0             ",
            "    .---.   0  _/_____\_  0 (_________) 0   /      \\  ",
            "    .---.   0  _/_____\_  0 (_________) 0  /        \\ "]
    enemysSpriteList = [
            #format:
            #[
            #"x","y" <----  sprite as two strings, 0 anywhere in the string corresponds to newline (str)
            #y, <---------  How many characters per line (int)
            #z <----------  How many lines the sprite takes up (int)
            #]
            ["-OK", "-O ",
            3,
            1],
            ["  /|0-===0  \\|", "  /K0-===0  \\K",
            4,
            3],
            ["-(O)", "-(X)",
            4,
            1], 
            ["--=0  O0--=", "--=0  X0--=",
            3,
            3],
            ["   /  0 -=<=-<0   \\  ", "   /- 0 -=<=-K0   \\- ",
            6,
            3],
            [" /| 0< | 0 \| ", " /|_0< |_0 \| ",
            4,
            3]
            ]
    spriteNum = int(len(enemysSpriteList))
    health = 10
    ammo = 30
    prevscore = 0
    notshootingframe = 0
    drawTitle(stdscr, prevscore)
    drawControls(stdscr)
    for i in range(125):
        stars.append([random.randrange(3), random.randrange(maxyx[0]-1), random.randrange(maxyx[1]-1), random.randrange(2, 4)])
    nonplayable = True
    while(nonplayable):
        drawBG(stdscr, stars)
        drawRocket(stdscr, rocketxy, rocketSprite)
        if (rocketxy[1]<math.trunc(maxyx[1]/2)):
            rocketxy[1] += 2
            stdscr.refresh()
            stdscr.erase()
            time.sleep(0.016)
        else:
            nonplayable = False
    curses.flushinp()
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
            drawEnemy(stdscr, enemysSpriteList, i[0], i[1], i[2], i[3], half)
        drawUfos(stdscr, ufos, frame, ufosSpriteList, ufoCols)
        drawRocket(stdscr, rocketxy, rocketSprite)
        drawUI(stdscr, health, ammo)
        #keyboard input
        try:
            c = stdscr.getkey()
        except:
            c = 0
        #moving, quitting, shooting, and all that stuff
        if (c == 'q'):
            gameover(stdscr, score, rocketxy, rocketSprite)
            dead = True
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
        elif (rocketxy[0]>(maxyx[0]-4)):
                rocketxy[0] = (maxyx[0]-4)
        elif (rocketxy[1]<10):
                rocketxy[1] = 10
        elif (rocketxy[1]>(maxyx[1]-12)):
                rocketxy[1] = (maxyx[1]-12)
        #make enemies fire
        if (frame%random.randrange(20, 40)==0):
            for i in enemys:
                j = random.randrange(100)
                if (j%2==0):
                    bullets1.append([i[1]-2, i[2]-3])
                j = random.randrange(100)
                if (j%2==0):
                    bullets1.append([i[1]-2, i[2]-3])
        if (frame%18>=9):
            for i in ufos:
                bullets1.append([i[0],i[1]])
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
            enemys.append([random.randrange(spriteNum), random.randrange(maxyx[0]), maxyx[1]-10, random.randrange(2, 6)])
        if (seconds%15==0 and frame==0):
            ufos.append([random.randrange(10, maxyx[0]-10), random.randrange(math.trunc(maxyx[1]/2), maxyx[1]), 0, random.randrange(2, 6)])
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
        if(frame%54==0):
            ufocount = len(ufos)
            for i in range(ufocount):
                 ufos[i] = [random.randrange(10, maxyx[0]-10), random.randrange(math.trunc(maxyx[1]/2), maxyx[1]), ufos[i][2], ufos[i][3]]
        #detect bullet collisions
        y = 0
        x = 0
        playerCols = []
        for i in rocketSprite:
            for j in i:
                if(j=='0'):
                    x += 1
                else:
                    playerCols.append([rocketxy[0]-y, rocketxy[1]+x])
                    x += 1
            y += 1
            x = 0
        enemCols = []
        for num, i in enumerate(enemys):
            y = 0
            x = 0
            for j in enemysSpriteList[i[0]]:
                if(j=='0'):
                    y += 1
                    x = 0
                elif(j==' '):
                    x += 1
                else:
                    enemCols.append([i[1]+y, i[2]+x, num])
                    x += 1
        ufoCols = []
        for num, i in enumerate(ufos):
            y = 0
            x = 0
            if(frame%9+1<=3):
                ufosind = 0
            elif(frame%9+1>=4 and frame%9+1<=6):
                ufosind = 1
            else:
                ufosind = 2
            for j in ufosSpriteList[ufosind]:
                if(j=='0'):
                    y += 1
                    x = 0
                elif(j==' '):
                    x += 1
                else:
                    ufoCols.append([i[0]+y, i[1]+x, num])
                    x += 1
        for i in bullets1:
            if(i in playerCols):
                bullets1.pop(bullets1.index(i))
                health -= 1
                curses.flash()
        for i in bullets1:
            for num, j in enumerate(enemys):
                if([i[0], i[1], num] in enemCols):
                    enemys.pop(num)
                    num -= 1
                    bullets1.pop(bullets1.index(i))
        for num, i in enumerate(bullets):
            for j in enemCols:
                if(i[0]==j[0] and i[1]==j[1]):
                    enemys.pop(j[2])
                    bullets.pop(num)
                    num -= 1
                    score += 1
                    health += 1
                    if (health>10):
                        health = 10
                    ammo += 2
                    if ammo>30:
                        ammo = 30
        for num, i in enumerate(bullets):
            for j in ufoCols:
                if(i[0]==j[0] and i[1]==j[1]):
                    if(ufos[j[2]][2]<2):
                        bullets.pop(num)
                        ufos[j[2]][2] += 1
                        num -= 1
                        score += 1
                        health += 1
                        if (health>10):
                            health = 10
                        ammo += 2
                        if ammo>30:
                            ammo = 30
                    else:
                        ufos.pop(j[2])
                        bullets.pop(num)
                        num -= 1
                        score += 1
                        health += 1
                        if (health>10):
                            health = 10
                        ammo += 2
                        if ammo>30:
                            ammo = 30

        #add stars
        if (frame%random.randrange(20, 40)==0):
            stars.append([random.randrange(3), random.randrange(maxyx[0]-1), maxyx[1]-1, random.randrange(2, 4)])
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
            if ammo>30:
                ammo = 30
        #weird misc stuff
        if (frame%30<15):
            half = 0
        else:
            half = 1
        #check if dead
        if (health<1):
            gameover(stdscr, score, rocketxy, rocketSprite)
            dead = True
        stdscr.refresh()
        stdscr.erase()
        time.sleep(0.016)
    curses.endwin()

def drawUfos(stdscr, ufos, frame, ufosSpriteList, ufoCols):
    maxyx = stdscr.getmaxyx()
    curs = []
    for ufo in ufos:
        spritenum = frame%9+1
        curs = [ufo[0], ufo[1]]
        count = 0
        if (spritenum <= 3):
            for i in ufosSpriteList[0]:
                if (i==' '):
                    count += 1
                    curs[1] += 1
                elif (i=='0'):
                    curs[1] -= count
                    curs[0] += 1
                    count = 0
                else:
                    if (curs[0]>0 and curs[0]<maxyx[0] and curs[1]>0 and curs[1]<maxyx[1]):
                        stdscr.addch(curs[0], curs[1], i, curses.color_pair(ufo[3]))
                    curs[1] += 1
                    count += 1
        elif (spritenum >= 4 and spritenum <= 6):
            for i in ufosSpriteList[1]:
                 if (i==' '):
                    count += 1
                    curs[1] += 1
                 elif (i=='0'):
                    curs[1] -= count
                    curs[0] += 1
                    count = 0
                 else:
                    if (curs[0]>0 and curs[0]<maxyx[0] and curs[1]>0 and curs[1]<maxyx[1]):
                        stdscr.addch(curs[0], curs[1], i, curses.color_pair(ufo[3]))
                    curs[1] += 1
                    count += 1
        elif (spritenum >= 7):
            for i in ufosSpriteList[2]:
                if (i==' '):
                    count += 1
                    curs[1] += 1
                elif (i=='0'):
                    curs[1] -= count
                    curs[0] += 1
                    count = 0
                else:
                    if (curs[0]>0 and curs[0]<maxyx[0] and curs[1]>0 and curs[1]<maxyx[1]):
                        stdscr.addch(curs[0], curs[1], i, curses.color_pair(ufo[3]))
                    curs[1] += 1
                    count += 1

    

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
        stdscr.addch(star, curses.color_pair(i[3]))
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
            stdscr.addch(curs[0], curs[1], i, curses.color_pair(2))
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
    title = ["    ___                       ___           ___                                     ___ ", "    /__/\        ___          /  /\         /  /\        ___                        /  /\ ", "    |  |::\      /  /\        /  /:/_       /  /:/_      /  /\                      /  /:/_ ", "     |  |:|:\    /  /:/       /  /:/ /\     /  /:/ /\    /  /:/      ___     ___    /  /:/ /\ ", "   __|__|:|\:\  /__/::\      /  /:/ /::\   /  /:/ /::\  /__/::\     /__/\   /  /\  /  /:/ /:/_ ", "  /__/::::| \:\ \__\/\:\__  /__/:/ /:/\:\ /__/:/ /:/\:\ \__\/\:\__  \  \:\ /  /:/ /__/:/ /:/ /\\", "   \  \:\~~\__\/    \  \:\/\ \  \:\/:/~/:/ \  \:\/:/~/:/    \  \:\/\  \  \:\  /:/  \  \:\/:/ /:/ ", "   \  \:\           \__\::/  \  \::/ /:/   \  \::/ /:/      \__\::/   \  \:\/:/    \  \::/ /:/ ", "   \  \:\          /__/:/    \__\/ /:/     \__\/ /:/       /__/:/     \  \::/      \  \:\/:/ ", "    \  \:\         \__\/       /__/:/        /__/:/        \__\/       \__\/        \  \::/ ", "     \__\/                     \__\/         \__\/                                   \__\/ "]
    for num, i in enumerate(range(int(0-len(title)/2), int(len(title)/2))):
        try:
            stdscr.move(math.trunc(maxyx[0]/2+i), math.trunc(maxyx[1]/2-math.trunc(len(title[num])/2)))
            stdscr.addstr(title[num], curses.color_pair(2))
        except:
            pass
    stdscr.refresh()
    time.sleep(1)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame < 60):
        frame += 1
        time.sleep(0.016)

def gameover(stdscr, score, rocketxy, sprite):
    #story or sum shiiid
    maxyx = stdscr.getmaxyx()
    line0 = "Your aircraft was shot down after you took out " + str(score) + " enemies."
    line1 = "Your name will soon be forgotten. As with most of your comrades."
    drawDeadRocket(stdscr, rocketxy, sprite)
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2-1), math.trunc(maxyx[1]/2-math.trunc(len(line0)/2)))
    stdscr.addstr(line0, curses.color_pair(1))
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-math.trunc(len(line1)/2)))
    stdscr.addstr(line1, curses.color_pair(1))
    stdscr.refresh()
    time.sleep(2)
    curses.flushinp()
    frame = 0
    while (stdscr.getch()==curses.ERR and frame < 600):
        time.sleep(0.016)
        frame += 1

def drawUI(stdscr, health, ammo):
    stdscr.move(0, 0)
    stdscr.addstr("Health: [", curses.color_pair(2))
    while (health>0):
        stdscr.addch('#', curses.color_pair(1))
        health -= 1
    stdscr.move(0, 19)
    stdscr.addch(']', curses.color_pair(2))
    stdscr.move(0, 25)
    stdscr.addstr("Ammo: [", curses.color_pair(2))
    while ammo>0:
        stdscr.addch("-", curses.color_pair(5))
        ammo -= 1
    stdscr.move(0, 62)
    stdscr.addch("]", curses.color_pair(2))

def drawEnemy(stdscr, enemys, enemId, enemY, enemX, enemCol, sprite):
    maxyx = stdscr.getmaxyx()
    enemy = enemys[enemId]
    curs = [enemY, enemX]
    if (curs[0]<maxyx[0]-enemy[3] and curs[1]<maxyx[1]-enemy[2] and curs[0]>0 and curs[1]>0):
        count = 0
        for i in enemy[sprite]:
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
                stdscr.addch(i, curses.color_pair(enemCol))
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
        stdscr.addch("-", curses.color_pair(5))
    for i in points1:
        stdscr.move(i[0], i[1])
        stdscr.addch("-", curses.color_pair(1))

def drawRocket(stdscr, points, sprite):
    locy = 0
    locx = 0
    stdscr.move(points[0],points[1])
    for i in range(5):
            for j in range(9):
                    if (sprite[i][j] == '0'):
                            tmp = stdscr.getyx()
                            locy = tmp[0]
                            locx = tmp[1]
                            stdscr.move(locy, locx+1)
                    elif (sprite[i][j] == ' '):
                        stdscr.addch(' ', curses.color_pair(1))
                    else: 
                        stdscr.addch(sprite[i][j], curses.color_pair(2))
            tmp = stdscr.getyx()
            locy = tmp[0]
            locx = tmp[1]
            stdscr.move(locy-1, locx-9)

def drawDeadRocket(stdscr, points, sprite):
    curses.flash()
    locy = 0
    locx = 0
    stdscr.move(points[0],points[1])
    for i in range(5):
            for j in range(9):
                    if (sprite[i][j] == '0'):
                            tmp = stdscr.getyx()
                            locy = tmp[0]
                            locx = tmp[1]
                            stdscr.move(locy, locx+1)
                    elif (sprite[i][j] == ' '):
                        stdscr.addch(' ', curses.color_pair(1))
                    else: 
                        if (random.randrange(10) % 3 != 0):
                            stdscr.addch(sprite[i][j], curses.color_pair(2))
                        else:
                            stdscr.addch(' ')
            tmp = stdscr.getyx()
            locy = tmp[0]
            locx = tmp[1]
            stdscr.move(locy-1, locx-9)
    stdscr.refresh()
    time.sleep(2)
    curses.flash()


if __name__ == '__main__':
    main()
