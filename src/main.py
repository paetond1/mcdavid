import pygame, sys, math
from enemy import enemy
from enemy import boss

# display player on the screen
def movePlayer(xyList):
    screen.blit(playerImg, (xyList[0], xyList[1]))

# reset player coordinates to starting position
def resetPlayer(xyList):
    xyList[0] = 0
    xyList[1] = height/2 - 45

# determine a collison
def isCollision(xyList, enemyX, enemyY):

    # get the distance between the centre of the player and the enemy
    distance = math.sqrt(math.pow(xyList[0] + 45 - (enemyX + 75 // 2), 2) + (math.pow(xyList[1] + 45  - (enemyY + 75 // 2), 2)))

    # if player is at starting position, no collision
    if ((xyList[0] == 0) and (xyList[1] == height/2 - 45)):
        return False
    # else if distance is too small between player and enemy, it is a collision
    elif distance < (90 // 2 + 75 // 2):
        return True
    # else no collision
    else:
        return False

def handlePause(gamePaused, width, height):
    pauseText = "Game Paused - Press P to Resume - Press Q to Quit"
    pauseX = width // 2 - font.size(pauseText)[0] // 2
    pauseY = height // 2
   
    while(gamePaused):
       
        # set background
        screen.blit(background, (0, 0))
        clock.tick(30)
        for event in pygame.event.get():

            # unpause event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    gamePaused = False
                if event.key == pygame.K_q:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            # quiting events
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        # update the display
        screen.blit(font.render(pauseText, True, OILER_BLUE), (pauseX, pauseY))
        pygame.display.update()

    return gamePaused

def handleWonGame(width, height, deaths):
    score = str(deaths) + " deaths"
    scoreX = width // 2 - titleFont.size(score)[0] // 2
    scoreY = height // 3

    wonText1 = "Congratulations, you have brought Connor great honor."
    wonText2 = "Press P to play again or Q to quit."
    wonX1 = width // 2 - font.size(wonText1)[0] // 2
    wonX2 = width // 2 - font.size(wonText2)[0] // 2
    wonY1 = height // 2
    wonY2 = height // 2 + 25
    playAgain = False
   
    while(playAgain == False):
       
        # set background
        screen.blit(background, (0, 0))
        clock.tick(30)
        for event in pygame.event.get():

            # determine if player wants to quit or play again
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    playAgain = True
                if event.key == pygame.K_q:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            # quiting events
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        # update the display
        screen.blit(titleFont.render(score, True, OILER_ORANGE), (scoreX, scoreY))
        screen.blit(font.render(wonText1, True, OILER_BLUE), (wonX1, wonY1))
        screen.blit(font.render(wonText2, True, OILER_BLUE), (wonX2, wonY2))
        pygame.display.update()


# initialize pygame
pygame.init()

# initialize font
OILER_BLUE = (4, 30, 66)
OILER_ORANGE = (252, 76, 2)
fontSize = 30
titleFontSize = 60
lineSpace = 5
font = pygame.font.SysFont(None, fontSize)
titleFont = pygame.font.SysFont(None, 60)

# initialize screen
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
screen.fill((255,255,255))  # screen color

# initialize game
gameName = "McDavid's Quest"
backgroundColor = (255, 255, 255)
playerSpeed = 10
playerImg = pygame.image.load("../resources/images/player.jpg")
cupImg = pygame.image.load("../resources/images/cup.png")
level = 0
gamePaused = False
deaths = 0
running = True

# initialize stanley cup
cupX = width - 58
cupY = height/2 - 45

# initialize player
playerXY = [0, height/2 - 45]
moveUp = False
moveDown = False
moveLeft = False
moveRight = False

# initialize enemies and enemy list
e1 = enemy(width//2, 0, 4, 0, "../resources/images/enemy1.jpg")
e2 = enemy(width//2 + 100, height - 75, 4, 0, "../resources/images/enemy2.jpg")
e3 = enemy(width//3, 0, 4, 1, "../resources/images/enemy3.jpg")
e4 = enemy(0, 0, 4, 2, "../resources/images/enemy4.jpg")
e5 = enemy(width - 75, height * 1/2 - 75//2, 4, 4, "../resources/images/enemy5.png")
e6 = enemy(width * 2, height * 2, 10, 5, "../resources/images/enemy6.png", e5)
e7 = enemy(width//4, height * 1/2 - 75//2, 4, 3, "../resources/images/enemy7.png")
e8 = enemy(width//3, height - 75, 4, 1, "../resources/images/enemy8.jpg")
e9 = enemy(width//2, 0, 2, 1, "../resources/images/enemy9.png")
e10 = enemy(width//2, height - 75, 2, 1, "../resources/images/enemy10.jpg")
boss1 = boss(0, 0, 6, "../resources/images/boss.jpg")

allEnemies = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, boss1]
enemyList = []

# initialize caption, icon, clock, background
pygame.display.set_caption(gameName)
icon = pygame.image.load("../resources/images/icon.png")      # 32x32 icons only
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
background = pygame.image.load("../resources/images/background.jpg")


# INTRO ----------------------------------------------------------------------

titleText = "McDAVID'S QUEST"
titleX = width // 2 - titleFont.size(titleText)[0] // 2
titleY = height // 4

introText = [   "Get Connor McDavid to the cup. Avoid the obstacles.",
                "Use the arrow keys to move Connor. Press P to pause.",
                "Press space to begin!"
            ]

# render background, cup, player
screen.blit(background, (0, 0))
screen.blit(cupImg, (cupX, cupY))
screen.blit(playerImg, (playerXY[0], playerXY[1]))

# render title
screen.blit(titleFont.render(titleText, True, OILER_ORANGE), (titleX, titleY))

# render intro directions
introTextY = height // 2 - (len(introText) * (fontSize + lineSpace) // 2)
for text in introText:
    screen.blit(font.render(text, True, OILER_BLUE), (width // 2 - font.size(text)[0] // 2, introTextY))
    introTextY += fontSize + lineSpace

# display all intro objects
pygame.display.update()

# wait for player to press space
waiting = True
while waiting:

    for event in pygame.event.get():
        # responses to keyboard inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting = False

        # quiting events
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()


# GAME LOOP ---------------------------------------------------------------------
while running:
    clock.tick(30)

    # render background
    screen.blit(background, (0, 0))

    # render game text counters
    gameText = "Level: " + str(level) + "    " + "Deaths: " + str(deaths)
    screen.blit(font.render(gameText, True, OILER_BLUE), (5,5))
    gamePaused = handlePause(gamePaused, width, height)
    
    for event in pygame.event.get():

        # responses to keyboard inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True
            if event.key == pygame.K_UP:
                moveUp = True
            if event.key == pygame.K_DOWN:
                moveDown = True
            if event.key == pygame.K_p:
                gamePaused = not gamePaused
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_RIGHT:
                moveRight = False
            if event.key == pygame.K_UP:
                moveUp = False
            if event.key == pygame.K_DOWN:
                moveDown = False

        # quiting events
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    # set next player position
    if moveLeft:
        playerXY[0] -= playerSpeed
    if moveRight:
        playerXY[0] += playerSpeed
    if moveDown:
        playerXY[1] += playerSpeed
    if moveUp:
        playerXY[1] -= playerSpeed

    # force that player is within screen boundaries
    if playerXY[0] > (width - 90):
        playerXY[0] = width - 90
    elif playerXY[0] < 0:
        playerXY[0] = 0
    if playerXY[1] > (height - 90):
        playerXY[1] = height - 90
    elif playerXY[1] < 0:
        playerXY[1] = 0

    # see if there is collision between player and enemy
    for i in enemyList:
        collision = isCollision(playerXY, i.x, i.y)
        if collision:
            resetPlayer(playerXY)
            deaths += 1

    # see if there is a collision with the stanley cup to beat the level
    if (playerXY[0] == (width - 90)):
        if playerXY[1] >= (height/2 - 90):
            if playerXY[1] <= (height/2):

                level += 1

                # see if player has won the entire game
                if (level > len(allEnemies)):

                    # check if player wants to play again
                    handleWonGame(width, height, deaths)
                    enemyList.clear()
                    level = 0
                    deaths = 0
                    resetPlayer(playerXY)
                    moveUp = False
                    moveDown = False
                    moveLeft = False
                    moveRight = False
                    continue

                # else there are more levels to play, set up next level
                else:
                    enemyList.append(allEnemies[level - 1])
                    resetPlayer(playerXY)
                    moveUp = False
                    moveDown = False
                    moveLeft = False
                    moveRight = False
                    for i in enemyList:
                        i.resetEnemy()
                    continue


    # move and render the player
    movePlayer(playerXY)

    # move and render the enemies
    for i in enemyList:
        i.moveEnemy(height, width)
        screen.blit(i.image, (i.x, i.y))

    # display the target
    screen.blit(cupImg, (cupX, cupY))

    # update the display
    pygame.display.update()

