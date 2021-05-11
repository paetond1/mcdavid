import pygame, math
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

    # reset the enemy upon winning the level
    def resetEnemy(self):
        self.x = self.initialX
        self.y = self.initialY
        self.down = True
        self.right = True
        self.radians = math.pi

