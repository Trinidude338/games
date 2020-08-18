import curses
import time
import math
import random

def main():
    global offset
    global curs
    global previouscurs
    global head
    global maxyx
    global dead
    stdscr = curses.initscr()
    curses.raw()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    curses.curs_set(0)
    maxyx = stdscr.getmaxyx()
    drawTitle(stdscr)
    stdscr.clear()
    foody = random.randrange(5, maxyx[0]-5)
    foodx = random.randrange(5, maxyx[0]-5)
    dead = False
    offset = list([2,2,2,2,2])
    score = len(offset)
    default = 2
    curs = [math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2)]
    head = [math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2)]
    while (dead==False and isOutofBounds()==False):
        drawLength(stdscr)
        drawFood(stdscr, foody, foodx)
        try:
            drawSnake(stdscr)
        except:
            dead = True
        stdscr.refresh()
        try:
            c = stdscr.getkey()
        except:
            c = -1
        if (c == 'q'):
            break
        if (c == ' '):
            stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-3))
            stdscr.addstr("PAUSED")
            while (stdscr.getch()==curses.ERR):
                time.sleep(0.0016)
        elif (c == 'w' and default != 1):
            shift()
            offset.append(0)
            default = 0
            head[0] -= 1
        elif (c == 's' and default != 0):
            shift()
            offset.append(1)
            default = 1
            head[0] += 1
        elif (c == 'a' and default != 3):
            shift()
            offset.append(2)
            default = 2
            head[1] -= 1
        elif (c == 'd' and default != 2):
            shift()
            offset.append(3)
            default = 3
            head[1] += 1
        elif (c == -1):
            shift()
            offset.append(default)
            if (default == 0):
                head[0] -= 1
            elif (default == 1):
                head[0] += 1
            elif (default == 2):
                head[1] -= 1
            elif (default == 3):
                head[1] += 1
        stdscr.move(head[0], head[1])
        if(head[0] == foody and head[1] == foodx):
            foody = random.randrange(5, maxyx[0]-5)
            foodx = random.randrange(5, maxyx[0]-5)
            grow(stdscr, default)
            grow(stdscr, default)
            grow(stdscr, default)
        stdscr.move(head[0], head[1])
        curs = [head[0], head[1]]
        for i in range(-1, (len(offset)*-1)-1, -1):
            if (offset[i] == 0):
                curs[0] += 1
            elif (offset[i] == 1):
                curs[0] -= 1
            elif (offset[i] == 2):
                curs[1] += 1
            elif (offset[i] == 3):
                curs[1] -= 1
            if (head[0] == curs[0] and head[1] == curs[1]):
                dead = True
                break
        time.sleep(0.16)
        stdscr.refresh()
        stdscr.clear()
    curses.flash()
    gameover(stdscr)
    curses.endwin()

def drawTitle(stdscr):
    try:
        with open(".snakeyHighScore.txt", "r") as f:
            prevscore = "High Score: " + str(f.read())
    except:
        prevscore = ""
        with open(".snakeyHighScore.txt", "w+") as f:
            f.write("5")
    title = "Snakey"
    controls0 = "Use WASD to move."
    controls1 = "Press SPACE to pause the game."
    controls2 = "At any point, press 'Q' to quit the game"
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-math.trunc(len(title)/2)))
    stdscr.addstr(title)
    stdscr.move(math.trunc(maxyx[0]/2+1), math.trunc(maxyx[1]/2-math.trunc(len(prevscore)/2)))
    stdscr.addstr(prevscore)
    stdscr.move(math.trunc(maxyx[0]/2+2), math.trunc(maxyx[1]/2-math.trunc(len(controls0)/2)))
    stdscr.addstr(controls0)
    stdscr.move(math.trunc(maxyx[0]/2+3), math.trunc(maxyx[1]/2-math.trunc(len(controls1)/2)))
    stdscr.addstr(controls1)
    stdscr.move(math.trunc(maxyx[0]/2+4), math.trunc(maxyx[1]/2-math.trunc(len(controls2)/2)))
    stdscr.addstr(controls2)
    stdscr.refresh()
    time.sleep(3)

def drawLength(stdscr):
    length = "Length: " + str(len(offset))
    stdscr.addstr(length)

def gameover(stdscr):
    msg0 = "You were " + str(len(offset)) + " X's long when you met your demise."
    msg1 = "Less X's than the lines of code in this python script. :("
    msg2 = "More X's than the lines of code in this python script. :)"
    with open(".snakeyHighScore.txt", "r+") as f:
        c = str(f.read())
    msg3 = "High Score: " + str(c)
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-math.trunc(len(msg0)/2)))
    stdscr.addstr(msg0)
    stdscr.move(math.trunc(maxyx[0]/2+1), math.trunc(maxyx[1]/2-math.trunc(len(msg1)/2)))
    count = 206
    if (len(offset)<count):
        stdscr.addstr(msg1)
    else:
        stdscr.addstr(msg2)
    stdscr.move(math.trunc(maxyx[0]/2+3), math.trunc(maxyx[1]/2-math.trunc(len(msg3)/2)))
    stdscr.addstr(msg3)
    stdscr.refresh()
    time.sleep(3)
    while (stdscr.getch()==curses.ERR):
        time.sleep(0.0016)

def grow(stdscr, default):
    offset.insert(0, default)
    curses.flash()
    with open(".snakeyHighScore.txt", "r+") as f:
        c = f.read()
        if (int(c) < int(len(offset))):
            f.seek(0)
            f.write(str(len(offset)))



def shift():
    offset.pop(0)
    return offset

def isOutofBounds():
    if (head[0]==maxyx[0]-1 or head[0]==0 or head[1]==maxyx[1]-1 or head[1]==0):
        return True
    else:
        return False

def drawFood(stdscr, foody, foodx):
    stdscr.move(foody, foodx)
    stdscr.addch('o')

def drawSnake(stdscr):
    curs = [head[0],head[1]]
    stdscr.move(head[0], head[1])
    stdscr.addch('%')
    n = -1
    while (n > len(offset)*-1):
        if (offset[n] == 0):
            curs[0] += 1
        elif (offset[n] == 1):
            curs[0] -= 1
        elif (offset[n] == 2):
            curs[1] += 1
        elif (offset[n] == 3):
            curs[1] -= 1
        stdscr.move(curs[0], curs[1])
        stdscr.addch('X')
        n -= 1
    return 0

if __name__ == '__main__':
    main()
