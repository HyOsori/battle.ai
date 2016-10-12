import pygame
import random
import time

# Set up the constants
WIDTH = 128
HEIGHT = 92
paddingWIDTH = 64
paddingHEIGHT = 64
SIZE = 6
MARGIN1 = 1 # Left-side and Up-side
MARGIN2 = 0 # Right-side and Down-side
ScoreBarWidth = 36
NumOfColor = 6
SleepSecond = 0.0
SleepSecondGradation = 0.00

# Start at corner
StartingPoint1_X = 0
StartingPoint1_Y = 0
StartingPoint2_X = WIDTH - 1
StartingPoint2_Y = HEIGHT - 1

# Start at center

StartingPoint1_X = WIDTH / 2 - 1
StartingPoint1_Y = HEIGHT / 2 - 1
StartingPoint2_X = WIDTH - 1 - StartingPoint1_X
StartingPoint2_Y = HEIGHT - 1 - StartingPoint1_Y
# Example) When width and height are odd numbers
# WIDTH = 63 (0 ~ 62)
# HEIGHT = 63 (0 ~ 62)
# Center is (31, 31)
# StartingPoint1_X = WIDTH / 2 - 1 = 63/2 - 1 = integer(31.5) - 1 = 31 - 1 = 30
# StartingPoint1_Y = HEIGHT / 2 - 1 = 63/2 - 1 = integer(31.5) - 1 = 31 - 1 = 30
# StartingPoint2_X = WIDTH - 1 - StartingPoint1_X = 63 - 1 - 30 = 32
# StartingPoint2_Y = HEIGHT - 1 - StartingPoint1_Y  = 63 - 1 - 30 = 32
# StartingPoint1 = (30, 30)
# Center is (31, 31)
# StartingPoint2 = (32, 32)


# Start at quarter
"""
StartingPoint1_X = WIDTH / 4 - 1
StartingPoint1_Y = HEIGHT / 4 - 1
StartingPoint2_X = WIDTH - 1 - StartingPoint1_X
StartingPoint2_Y = HEIGHT - 1 - StartingPoint1_Y
# Example1) When width and height are not multiples of 4
# WIDTH = 61 (0 ~ 60)
# HEIGHT = 61 (0 ~ 60)
# StartingPoint1_X = WIDTH / 4 - 1 = 61/4 - 1 = integer(15.25) - 1 = 15 - 1 = 14
# StartingPoint1_Y = HEIGHT / 4 - 1 = 61/4 - 1 = integer(15.25) - 1 = 15 - 1 = 14
# StartingPoint2_X = WIDTH - 1 - StartingPoint1_X = 61 - 1 - 14 = 46
# StartingPoint2_Y = HEIGHT - 1 - StartingPoint1_Y = 61 - 1 - 14 = 46
# StartingPoint1 = (14, 14)
# 1/4 point is (15, 15)
# Center is (30, 30)
# 3/4 point is (45, 45)
# StartingPoint2 = (46, 46)
"""

screenWIDTH = paddingWIDTH * 2 + WIDTH * SIZE + ScoreBarWidth * 4
screenHEIGHT = paddingHEIGHT * 2 + HEIGHT * SIZE

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

Red1 = (255, 0, 0)
Red2 = (255, 99, 71)
Red3 = (255, 127, 80)
Red4 = (205, 92, 92)
Red5 = (240, 128, 128)
Red6 = (233, 150, 122)

Green1 = (0, 100, 0)
Green2 = (0, 128, 0)
Green3 = (34, 139, 34)
Green4 = (0, 255, 0)
Green5 = (50, 205, 50)
Green6 = (144, 238, 144)

# Set up the variables
# ColorArray = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]
ColorArray = [[0 in range(WIDTH)] in range(HEIGHT)]
ColorArrayCopy = [[0 in range(WIDTH)] in range(HEIGHT)] # For Gradation
ColorNumArray = [[0 in range(WIDTH)] in range(HEIGHT)]
ChosenColorNum = 0
ColorNum = 0
RulerArray = [[0 in range(WIDTH)] in range(HEIGHT)]
RulerArrayCopy = [[0 in range(WIDTH)] in range(HEIGHT)]
Ruler = 0
RuledBy1 = 0
RuledBy2 = 0
GameRepeat = True

#ColorCheck - Rainbow
def ColorCheck(colornum): # ColorNum -> Color
    if (colornum == 1): return RED
    elif (colornum == 2): return ORANGE
    elif (colornum == 3): return YELLOW
    elif (colornum == 4): return GREEN
    elif (colornum == 5): return BLUE
    elif (colornum == 6): return PURPLE
    else: return BLACK

#ColorCheck - Red
"""
def ColorCheck(colornum): # ColorNum -> Color
    if (colornum == 1): return Red1
    elif (colornum == 2): return Red2
    elif (colornum == 3): return Red3
    elif (colornum == 4): return Red4
    elif (colornum == 5): return Red5
    elif (colornum == 6): return Red6
    else: return BLACK
"""

#ColorCheck - Green
"""
def ColorCheck(colornum): # ColorNum -> Color
    if (colornum == 1): return Green1
    elif (colornum == 2): return Green2
    elif (colornum == 3): return Green3
    elif (colornum == 4): return Green4
    elif (colornum == 5): return Green5
    elif (colornum == 6): return Green6
    else: return BLACK
"""

def Absorbtion (ruler, chosencolornum):

    # Copy ColorArray # For Gradation

    for y in range(HEIGHT):
        for x in range(WIDTH):
            ColorArrayCopy[y][x] = ColorArray[y][x]

    # global ColorArrayCopy
    # ColorArrayCopy = ColorArray
    # This doesn't work.

    for y in range(HEIGHT): # Fill ruled area with chosen color
        for x in range(WIDTH):
            if (RulerArray[y][x] == ruler):
                ColorNumArray[y][x] = chosencolornum
                ColorArray[y][x] = ColorCheck(chosencolornum)

    AbsorbRepeat = True

    while (AbsorbRepeat): # For complete absorption
        for y in range(HEIGHT): # Copy RulerArray
            for x in range(WIDTH):
                RulerArrayCopy[y][x] = RulerArray[y][x]

        for y in range(HEIGHT): # Absorb
            for x in range(WIDTH):
                if (RulerArray[y][x] == 0 and ColorNumArray[y][x] == chosencolornum and (
                    # If the area isn't ruled and is filled with chosen color
                            (x > 0 and RulerArray[y][x-1] == ruler) or # Check left side
                            (x < (WIDTH - 1) and RulerArray[y][x+1] == ruler) or # Check right side
                            (y > 0 and RulerArray[y-1][x] == ruler) or # Check up side
                            (y < (HEIGHT - 1) and RulerArray[y+1][x] == ruler))): # Check down side
                    RulerArray[y][x] = ruler # Rule the area

        AbsorbRepeat = False
        for y in range(HEIGHT): # If Ruler == RulerCopy -> Finish absorbtion
            for x in range(WIDTH):
                if (RulerArray[y][x] != RulerArrayCopy[y][x]):
                    AbsorbRepeat = True;
                    y = HEIGHT
                    break

def CheckStatus (ruler):
    global RuledBy1
    global RuledBy2
    ruledby1 = 0
    ruledby2 = 0
    Finish = True
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (ruler[y][x] == 0):
                Finish = False
            elif (ruler[y][x] == 1):
                ruledby1 = ruledby1 + 1
            elif (ruler[y][x] == 2):
                ruledby2 = ruledby2 + 1
    RuledBy1 = ruledby1
    RuledBy2 = ruledby2
    return Finish

# Draw - Basic

def Draw(ruler):
    for y in range(HEIGHT): # Fill ruled area with chosen color
        for x in range(WIDTH):
            if (RulerArray[y][x] == ruler): # If set screen.fill(WHITE) before Draw() Delete this.
                pygame.draw.rect(screen, ColorArray[y][x], (paddingWIDTH + SIZE * x + MARGIN1, paddingHEIGHT + SIZE * y + MARGIN1, SIZE - MARGIN1 - MARGIN2, SIZE - MARGIN1 - MARGIN2), 0)


# Draw - Gradation
"""
def Draw(ruler):
    n = 10
    for i in range(n):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (RulerArray[y][x] == ruler): # If set screen.fill(WHITE) before Draw() Delete this.
                    ColorTemp = ( float(ColorArray[y][x][0] * i + ColorArrayCopy[y][x][0] * ((n-1) - i)) / float(n-1),
                                  float(ColorArray[y][x][1] * i + ColorArrayCopy[y][x][1] * ((n-1) - i)) / float(n-1),
                                  float(ColorArray[y][x][2] * i + ColorArrayCopy[y][x][2] * ((n-1) - i)) / float(n-1))
                    pygame.draw.rect(screen, ColorTemp, (paddingWIDTH + SIZE * x + MARGIN1, paddingHEIGHT + SIZE * y + MARGIN1, SIZE - MARGIN1 - MARGIN2, SIZE - MARGIN1 - MARGIN2), 0)
                    pygame.display.update()
        #time.sleep(SleepSecondGradation)
"""

def OpstructionTest1 ():
    for y in range(5):
        for x in range(5):
            RulerArray[y + 30][x + 30] = -1
            ColorNumArray[y + 30][x + 30] = -1
            ColorArray[y + 30][x + 30] = ColorCheck(ColorNumArray[y + 30][x + 30])
            pygame.draw.rect(screen, ColorArray[y + 30][x + 30], (
            paddingWIDTH + SIZE * (x + 30) + MARGIN1, paddingHEIGHT + SIZE * (y + 30) + MARGIN1,
            SIZE - MARGIN1 - MARGIN2, SIZE - MARGIN1 - MARGIN2), 0)

def DummyAi1 (ruler, colornumarray, exclusionnum):
    if (ruler == 1):
        mycolornum = colornumarray[StartingPoint1_Y][StartingPoint1_X]
    elif (ruler == 2):
        mycolornum = colornumarray[StartingPoint2_Y][StartingPoint2_X]
    returncolornum = random.randint(1, 6)
    while (returncolornum == exclusionnum or returncolornum == mycolornum):
        returncolornum = random.randint(1, 6)
    return returncolornum

def DummyAi2 (ruler, colornumarray, exclusionnum):
    if (ruler == 1):
        mycolornum = colornumarray[StartingPoint1_Y][StartingPoint1_X]
    elif (ruler == 2):
        mycolornum = colornumarray[StartingPoint2_Y][StartingPoint2_X]

    NumOfEachColor = [0 for i in range(NumOfColor+1)]

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (RulerArray[y][x] == 0 and (
                # If the area isn't ruled
                        (x > 0 and RulerArray[y][x - 1] == ruler) or  # Check left side
                        (x < (WIDTH - 1) and RulerArray[y][x + 1] == ruler) or  # Check right side
                        (y > 0 and RulerArray[y - 1][x] == ruler) or  # Check up side
                        (y < (HEIGHT - 1) and RulerArray[y + 1][x] == ruler))):  # Check down side
                NumOfEachColor[colornumarray[y][x]] = NumOfEachColor[colornumarray[y][x]] + 1 # We can rule the area

    max = 0
    returncolornum = random.randint(1, 6)
    while (returncolornum == exclusionnum or returncolornum == mycolornum):
        returncolornum = random.randint(1, 6)
    NumOfEachColor[0] = -1

    for i in range(NumOfColor + 1):
        if (NumOfEachColor[i] > max and i != mycolornum and i != exclusionnum):
            max = NumOfEachColor[i]
            returncolornum = i

    return returncolornum

# Set up the screen
pygame.init()
screen = pygame.display.set_mode((screenWIDTH, screenHEIGHT))
pygame.display.set_caption('Greedy Pixel')
screen.fill(WHITE)

# Set up the map
for y in range(HEIGHT):
    for x in range(WIDTH):
        ColorNumArray[y][x] = random.randint(1, NumOfColor)
        ColorArray[y][x] = ColorCheck(ColorNumArray[y][x])
        pygame.draw.rect(screen, ColorArray[y][x], (paddingWIDTH + SIZE * x + MARGIN1, paddingHEIGHT + SIZE * y + MARGIN1, SIZE - MARGIN1 - MARGIN2, SIZE - MARGIN1 - MARGIN2), 0)

#OpstructionTest1()

RulerArray[StartingPoint1_Y][StartingPoint1_X] = 1
RulerArray[StartingPoint2_Y][StartingPoint2_X] = 2
Absorbtion(1, ColorNumArray[StartingPoint1_Y][StartingPoint1_X])
Absorbtion(2, ColorNumArray[StartingPoint2_Y][StartingPoint2_X])


# Game Loop
GameTurn = 1;
while (GameRepeat):
    if (GameTurn % 2): # If GameTurn is odd number, It's Ruler1's turn.
        Ruler = 1
        ChosenColorNum = DummyAi1(Ruler, ColorNumArray, ColorNumArray[StartingPoint2_Y][StartingPoint2_X])
    else: # If GameTurn is even number, It's Ruler2's turn.
        Ruler = 2
        ChosenColorNum = DummyAi2(Ruler, ColorNumArray, ColorNumArray[StartingPoint1_Y][StartingPoint1_X])

    Absorbtion(Ruler, ChosenColorNum)

    if (CheckStatus(RulerArray)): # If CheckStatus return True, finish game.
        GameRepeat = False

    #screen.fill(WHITE)

    Draw(Ruler)

    # Score
    pygame.draw.rect(screen, WHITE, (paddingWIDTH + SIZE * WIDTH + ScoreBarWidth, paddingHEIGHT, ScoreBarWidth * 3, HEIGHT - paddingHEIGHT), 0)

    Ruler1Score = (float(RuledBy1) / (float(WIDTH) * HEIGHT)) * HEIGHT * SIZE
    pygame.draw.rect(screen, ColorArray[StartingPoint1_Y][StartingPoint1_X],
                    (paddingWIDTH + SIZE * WIDTH + ScoreBarWidth, paddingHEIGHT, ScoreBarWidth, Ruler1Score), 0)

    Ruler2Score = (float(RuledBy2) / (float(WIDTH) * HEIGHT)) * HEIGHT * SIZE
    pygame.draw.rect(screen, ColorArray[StartingPoint2_Y][StartingPoint2_X],
                    (paddingWIDTH + SIZE * WIDTH + ScoreBarWidth * 3, paddingHEIGHT, ScoreBarWidth, Ruler2Score), 0)

    print "********** Turn " + str(GameTurn) + " **********"
    print "Ruler1 Score :" + str(RuledBy1)
    print "Ruler2 Score :" + str(RuledBy2)



    pygame.display.update()
    #pygame.display.flip()

    time.sleep(SleepSecond)
    GameTurn = GameTurn + 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT :  # Check Quit
            GameRepeat = False

# Quit
running = True
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT :  # Check Quit
            running = False

pygame.quit()