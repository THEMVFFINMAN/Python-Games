import math
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

gameWidth = 1024
gameHeight = 768

size = (gameWidth, gameHeight)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BREAKOUT")
clock = pygame.time.Clock()

paddleX = (gameWidth/2 - 45)
paddleY = 700
paddleWidth = 4
paddleLength = 100

ballX = (gameWidth/2 - 45)
ballY = 600
ballLength = 5
ballAngle = 0
ballSpeed = 1
ballDirection = "DR"
ballAngleX = 0
ballAngleY = 2

brickX = 200
brickY = 200
brickWidth = 200
brickLength = 200

bricks = []

class RegularBrick(object):
    def __init__(self, x, y, color, outline, length, width):
        self.image = pygame.image.load('brick.png').convert()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.rect.width = width
        self.rect.height = length
        self.color = color
        self.outline = outline
        self.length = length
        self.width = width
        pygame.draw.rect(screen, color, [x, y, length, width], 0)

    def updateDraw(self):
        screen.blit(self.image, self.rect)

class Paddle(object):

    def __init__(self, x, y, color, length, width):
        self.x = x
        self.y = y
        self.color = color
        self.length = length
        self.width = width
        pygame.draw.rect(screen, color, [x, y, length, width], 0)

    def updateDraw(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - paddle.length/2
        
        if (self.x > (gameWidth - paddle.length)):
            self.x = (gameWidth - paddle.length)
        elif (self.x < 0):
            self.x = 0

        pygame.draw.rect(screen, self.color, [self.x, self.y, self.length, self.width], 0)
    

class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, color, length, angle, speed, direction, angleX, angleY):
        self.image = pygame.image.load('ball.png').convert()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.angleX = angleX
        self.angleY = angleY
        self.rect.width = length
        self.rect.height = length
        self.color = color
        self.angle = angle
        self.speed = speed
        self.oldDirection = direction
        self.direction = direction
        self.collision = False
        self.changed = False
        self.hit = False
        screen.blit(self.image, self.rect)

    def updateDraw(self):

        self.oldDirection = self.direction
        
        if self.rect.left < 0 + self.rect.width/2:
            if self.direction == "UL":
                self.direction = "UR"
            elif self.direction == "DL":
                self.direction = "DR"
        elif self.rect.left > gameWidth - self.rect.width/2:
            if self.direction == "UR":
                self.direction = "UL"
            elif self.direction == "DR":
                self.direction = "DL"
        elif self.rect.top < 0 + self.rect.width/2:
            if self.direction == "UR":
                self.direction = "DR"
            elif self.direction == "UL":
                self.direction = "DL"
        elif (self.rect.top > gameHeight - self.rect.width/2) or ((self.rect.left > paddle.x - self.rect.width/2 - 1) and
                                                     (self.rect.left < paddle.x + paddle.length + self.rect.width/2 + 1)
                                                     and (self.rect.top > paddle.y - self.rect.width/2 - 1)
                                                     and (self.rect.top < paddle.y + paddle.width + self.rect.width/2)):
            if (self.rect.left < paddle.x + paddle.length):
                self.angle = 0
            if (self.rect.left > paddle.x + paddle.length - paddle.length):
                self.angle = 0
            if (self.rect.left < paddle.x + ((11 * paddle.length)/24)):
                self.angle = 1
            if (self.rect.left > paddle.x + paddle.length - ((11 * paddle.length)/24)):
                self.angle = 1
            if (self.rect.left < paddle.x + paddle.length/3):
                self.angle = 2
            if (self.rect.left > paddle.x + paddle.length - paddle.length/3):
                self.angle = 2
            if (self.rect.left < paddle.x + paddle.length/4):
                self.angle = 3
                if self.direction == "DR":
                    self.direction = "DL"
            if (self.rect.left > paddle.x + paddle.length - paddle.length/4):
                self.angle = 3
                if self.direction == "DL":
                    self.direction = "DR"
            if (self.rect.left < paddle.x + paddle.length/6):
                self.angle = 4
                if self.direction == "DR":
                    self.direction = "DL"
            if (self.rect.left > paddle.x + paddle.length - paddle.length/6):
                self.angle = 4
                if self.direction == "DL":
                    self.direction = "DR"
            if (self.rect.left < paddle.x + paddle.length/12):
                self.angle = 5
                if self.direction == "DR":
                    self.direction = "DL"
            if (self.rect.left > paddle.x + paddle.length - paddle.length/12):
                self.angle = 5
                if self.direction == "DL":
                    self.direction = "DR"
                    
            self.hit = True
                
            if self.direction == "DL":
                self.direction = "UL"
            elif self.direction == "DR":
                self.direction = "UR"

        if self.oldDirection != self.direction and self.hit:
            self.oldDirection = self.direction
            self.hit = False

            if self.angle == 5:
                self.angleX = 3
                self.angleY = 1
                if ball.speed < 4:
                    ball.speed = ball.speed + 1
            elif self.angle == 4:
                self.angleX = 3
                self.angleY = 2
                if ball.speed < 4:
                    ball.speed = ball.speed + 1
            elif self.angle == 3:
                self.angleX = 2
                self.angleY = 2
            elif self.angle == 2:
                self.angleX = 1
                self.angleY = 3
                if ball.speed > 1:
                    ball.speed = ball.speed - 1
            elif self.angle == 1:
                self.angleX = 1
                self.angleY = 2
                if ball.speed > 1:
                    ball.speed = ball.speed - 1
            elif self.angle == 0:
                self.angleX = 0
                self.angleY = 2
                if ball.speed > 1:
                    ball.speed = ball.speed - 1

        if self.direction == "DR":
            self.rect.left = self.rect.left + self.angleX * ball.speed
            self.rect.top = self.rect.top + self.angleY * ball.speed
        elif self.direction == "UR":
            self.rect.left = self.rect.left + self.angleX * ball.speed
            self.rect.top = self.rect.top - self.angleY * ball.speed
        elif self.direction == "UL":
            self.rect.left = self.rect.left - self.angleX * ball.speed
            self.rect.top = self.rect.top - self.angleY * ball.speed
        elif self.direction == "DL":
            self.rect.left = self.rect.left - self.angleX * ball.speed
            self.rect.top = self.rect.top + self.angleY * ball.speed
                
        screen.blit(self.image, self.rect)
 

ball = Ball(ballX, ballY, WHITE, ballLength, ballAngle, ballSpeed, ballDirection, ballAngleX, ballAngleY)
brick = RegularBrick(brickX, brickY, RED, GREEN, brickLength, brickWidth)
paddle = Paddle(paddleX, paddleY, WHITE, paddleLength, paddleWidth)


gameOn = True

# -------- Main Program Loop -----------
while gameOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            gameOn = False # Flag that we are done so we exit this loop
 
    # --- Game logic should go here
    

    # --- Drawing

    
    screen.fill(BLACK)
       
    brick.updateDraw()
    ball.updateDraw()
    paddle.updateDraw() 


    # --- Print Variables
    font = pygame.font.Font(None, 36)
    text = font.render(str(ball.angle), 1, (255, 255, 255))
    text2 = font.render(str(ball.rect.left), 1, (255, 255, 255))
    text3 = font.render(str(ball.rect.top), 1, (255, 255, 255))
    text4 = font.render(str(ball.direction), 1, (255, 255, 255))
    text5 = font.render(str(ball.collision), 1, (255, 255, 255))
    screen.blit(text, (900, 20))
    screen.blit(text2, (900, 60))
    screen.blit(text3, (900, 100))
    screen.blit(text4, (900, 140))
    screen.blit(text5, (900, 180))

 
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(90)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
