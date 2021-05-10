import pygame
class enemy:
    def __init__(self, x, y, speed, pattern, image):
        self.x = x
        self.y = y
        self.speed= speed
        self.pattern = pattern
        self.image = pygame.image.load(image)
        self.down = True
        self.right = True


    def move(self, height, width):
        print(self.down)
        if self.pattern == 0:
            if self.down == True:
                if self.y >= height - 75:
                    self.down = False
                    self.y -= self.speed
                else:
                    self.y += self.speed
            if self.down == False:
                if self.y <= 0:
                    self.down = True
                    self.y += self.speed
                else:
                    self.y -= self.speed

        else:
            pass
        pygame.display.set_mode.blit(self.image, (self.x, self.y))

