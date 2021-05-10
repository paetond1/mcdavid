import pygame, sys, math 

class enemy:
    def __init__(self, x, y, speed, patternIndex, image, shootingEnemy=None):
        self.initialX = x           # for resetting
        self.initialY = y           # for resetting
        self.x = x           
        self.y = y
        self.speed= speed
        self.pattern = patternIndex # for choosing a movement patterns
        self.image = pygame.image.load(image)
        self.down = True
        self.right = True
        self.fire = False
        self.radians = math.pi
        self.shootingEnemy = shootingEnemy

        # list of movement patterns
        self.options = [self.upDown,
                        self.diagonal,
                        self.perimeter,
                        self.circle,
                        self.semiCircle,
                        self.leftRightObj]

    # pattern to move an enemy up and down
    def upDown(self, height, width):

        # determine y coordinate
        if self.down == True:
            if self.y >= height - 75:
                self.down = False
                self.y -= self.speed
            else:
                self.y += self.speed
        else:
            if self.y <= 0:
                self.down = True
                self.y += self.speed
            else:
                self.y -= self.speed

    # pattern to move enemy diagonally
    def diagonal(self, height, width):

        # determine y coordinate
        if self.down == True:
            if self.y >= height - 75:
                self.down = False
                self.y -= self.speed
            else:
                self.y += self.speed
        else:
            if self.y <= 0:
                self.down = True
                self.y += self.speed
            else:
                self.y -= self.speed

        # determine x coordinate
        if self.right == True:
            if self.x >= width - 75:
                self.right = False
                self.x -= self.speed
            else:
                self.x += self.speed
        else:
            if self.x <= 0:
                self.right = True
                self.x += self.speed
            else:
                self.x -= self.speed

    # pattern to move enemy along perimeter of screen in clockwise
    def perimeter(self, height, width):
        # movement along top wall
        if self.down == True and self.right == True:
            self.x += self.speed
            if self.x > width - 75:
                self.x = width - 75
                self.right = False
        # movement along right wall
        elif self.down == True and self.right == False:
            self.y += self.speed
            if self.y > height - 75:
                self.y = height - 75
                self.down = False
        # movement along bottom wall
        elif self.down == False and self.right == False:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
                self.right = True
        # movement along left wall
        else:
            self.y -= self.speed
            if self.y < 0:
                self.y = 0
                self.down = True


    # pattern to move enemy in a clockwise circle
    def circle(self, height, width):
        radius = min(width, height) // 4
        circleSpeed = self.speed * 0.01
        self.radians += circleSpeed

        # determine x and y
        self.x = radius * math.sin(self.radians) + self.initialX
        self.y = radius * math.cos(self.radians) + self.initialY
    
    # pattern to move enemy vertically in a semi-circle (goalie)
    def semiCircle(self, height, width):
        radius = min(width, height) // 3
        circleSpeed = self.speed * 0.01

        # calculate radians if moving downward
        if self.down == True:
            self.radians += circleSpeed
            #print(self.radians > (2 * math.pi))
            if self.radians > (2 * math.pi):
                self.down = False
                self.radians == 2 * math.pi
        # calculate radians if moving upward
        else:
            self.radians -= circleSpeed
            if self.radians < math.pi:
                self.down = True
                self.radians == math.pi

        # determine x and y
        self.x = radius * math.sin(self.radians) + self.initialX
        self.y = radius * math.cos(self.radians) + self.initialY

    def leftRightObj(self, height, width):
        if self.shootingEnemy.x > width - 74:
            self.x = width - 75*2
            self.y = self.shootingEnemy.y
        else:
            self.x -= self.speed

    # get the movement pattern and move the enemy
    def moveEnemy(self, height, width):
        self.options[self.pattern](height, width)
        screen.blit(self.image, (self.x, self.y))

    # reset the enemy upon winning the level
    def resetEnemy(self):
        self.x = self.initialX
        self.y = self.initialY
        self.down = True
        self.right = True
        self.radians = math.pi

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


# initialize pygame
pygame.init()

# main info you can change around
gameName = "McDavid"
backgroundColor = (255, 255, 255)
playerSpeed = 10
width = 1000
height = 600
playerImg = pygame.image.load("images/player.jpg")
cupImg = pygame.image.load("images/cup.png")
level = 0

# caption, icon, clock
pygame.display.set_caption(gameName)
icon = pygame.image.load("images/icon.png")      # 32x32 icons only
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# create screen
screen = pygame.display.set_mode((width, height))
screen.fill((255,255,255))                       # screen color
pygame.display.update()

# set position of stanley cup
cupX = width - 58
cupY = height/2 - 45

# set position of player
playerXY = [0, height/2 - 45]

# initialize enemies and enemy list
e0 = enemy(width//2, 0, 5, 0, "images/enemy1.jpg")
e1 = enemy(width//2 + 100, height - 75, 5, 0, "images/enemy1.jpg")
e2 = enemy(width//3, 0, 5, 1, "images/enemy2.jpg")
e3 = enemy(0, 0, 5, 2, "images/enemy3.jpg")
e4 = enemy(width//4, height * 1/2 - 75//2, 5, 3, "images/enemy4.jpg")
e5 = enemy(width - 75, height * 1/2 - 75//2, 5, 4, "images/enemy5.png")

# this enemy fires a goalie stick
e6 = enemy(width * 2, height * 2, 10, 5, "images/enemy6.jpg", e5)

allEnemies = [e0, e1, e2, e3, e4, e5, e6]
enemyList = []

# arrow moves
moveUp = False
moveDown = False
moveLeft = False
moveRight = False

# game loop
running = True
while running:
    clock.tick(30)
    screen.fill(backgroundColor)
    
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

    # set boundaries
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

    # set winning conditions
    if (playerXY[0] == (width - 90)):
        if playerXY[1] >= (height/2 - 60):
            if playerXY[1] <= (height/2 - 30):
                enemyList.append(allEnemies[level])
                level += 1
                resetPlayer(playerXY)
                for i in enemyList:
                    i.resetEnemy()


    # move the player
    movePlayer(playerXY)

    # move the enemies
    for i in enemyList:
        i.moveEnemy(height, width)

    # display the target
    screen.blit(cupImg, (cupX, cupY))

    # update the display
    pygame.display.update()

