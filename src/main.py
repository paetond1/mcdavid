import pygame, sys, math
from enemy import enemy

# display player on the screen
def movePlayer(xyList):
    screen.blit(playerImg, (xyList[0], xyList[1]))

# reset player coordinates to starting position
def resetPlayer(xyList):
    xyList[0] = 0
    xyList[1] = height/2 - 45

# determine a collison
def isCollision(xyList, enemyX, enemyY):
    distance = math.sqrt(math.pow(xyList[0] - enemyX, 2) + (math.pow(xyList[1] - enemyY, 2)))
    if distance < 50:
        return True
    else:
        return False

def handlePause(gamePaused, width, height):
    pauseText = "Game Paused - Press P to Resume"
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

            # quiting events
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        # update the display
        screen.blit(font.render(pauseText, True, (0, 0, 0)), (pauseX, pauseY))
        pygame.display.update()

    return gamePaused


# initialize pygame
pygame.init()
font = pygame.font.SysFont(None, 30)

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
lastLevelWon = False

# initialize position of stanley cup
cupX = width - 58
cupY = height/2 - 45

# initialize position and movements of player
playerXY = [0, height/2 - 45]
moveUp = False
moveDown = False
moveLeft = False
moveRight = False

# initialize enemies and enemy list
e0 = enemy(width//2, 0, 5, 0, "../resources/images/enemy1.jpg")
e1 = enemy(width//2 + 100, height - 75, 5, 0, "../resources/images/enemy1.jpg")
e2 = enemy(width//3, 0, 5, 1, "../resources/images/enemy2.jpg")
e3 = enemy(0, 0, 5, 2, "../resources/images/enemy3.jpg")
e4 = enemy(width//4, height * 1/2 - 75//2, 5, 3, "../resources/images/enemy4.jpg")
e5 = enemy(width - 75, height * 1/2 - 75//2, 5, 4, "../resources/images/enemy5.png")
e6 = enemy(width * 2, height * 2, 10, 5, "../resources/images/enemy6.png", e5)

allEnemies = [e0, e1, e2, e3, e4, e5, e6]
enemyList = []

# initialize caption, icon, clock, background
pygame.display.set_caption(gameName)
icon = pygame.image.load("../resources/images/icon.png")      # 32x32 icons only
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
background = pygame.image.load("../resources/images/background.jpg")

# game loop
while running:
    clock.tick(30)

    # render background
    screen.blit(background, (0, 0))

    # render game text counters
    gameText = "Level: " + str(level) + "    " + "Deaths: " + str(deaths)
    screen.blit(font.render(gameText, True, (0, 0, 0)), (5,5))
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

    # see if there is a winning collision with the stanley cup
    if (playerXY[0] == (width - 90)):
        if playerXY[1] >= (height/2 - 60):
            if playerXY[1] <= (height/2 - 30):

                # player has won
                enemyList.append(allEnemies[level])
                level += 1
                resetPlayer(playerXY)
                lastLevelWon = True
                for i in enemyList:
                    i.resetEnemy()


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

