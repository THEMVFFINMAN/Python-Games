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
ballRadius = 4
ballAngle = 0
ballSpeed = 1
ballDirection = "DR"

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
    

class Ball(object):

    def __init__(self, x, y, color, radius, angle, speed, direction):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.angle = angle
        self.speed = speed
        self.direction = direction
        pygame.draw.circle(screen, color, (x, y), radius, 0)

    def updateDraw(self):

        if self.x < 0 + self.radius:
            if self.direction == "UL":
                self.direction = "UR"
            elif self.direction == "DL":
                self.direction = "DR"
        elif self.x > gameWidth - self.radius:
            if self.direction == "UR":
                self.direction = "UL"
            elif self.direction == "DR":
                self.direction = "DL"
        elif self.y < 0 + self.radius:
            if self.direction == "UR":
                self.direction = "DR"
            elif self.direction == "UL":
                self.direction = "DL"
        elif (self.y > gameHeight - self.radius) or ((self.x > paddle.x - self.radius - 1) and
                                                     (self.x < paddle.x + paddle.length + self.radius + 1)
                                                     and (self.y > paddle.y - self.radius - 1)
                                                     and (self.y < paddle.y + paddle.width + self.radius)):
            if (self.x < paddle.x + paddle.length):
                self.angle = 0
            if (self.x > paddle.x + paddle.length - paddle.length):
                self.angle = 0
            if (self.x < paddle.x + ((11 * paddle.length)/24)):
                self.angle = 1
            if (self.x > paddle.x + paddle.length - ((11 * paddle.length)/24)):
                self.angle = 1
            if (self.x < paddle.x + paddle.length/3):
                self.angle = 2
            if (self.x > paddle.x + paddle.length - paddle.length/3):
                self.angle = 2
            if (self.x < paddle.x + paddle.length/4):
                self.angle = 3
                if self.direction == "DR":
                    self.direction = "DL"
            if (self.x > paddle.x + paddle.length - paddle.length/4):
                self.angle = 3
                if self.direction == "DL":
                    self.direction = "DR"
            if (self.x < paddle.x + paddle.length/6):
                self.angle = 4
                if self.direction == "DR":
                    self.direction = "DL"
            if (self.x > paddle.x + paddle.length - paddle.length/6):
                self.angle = 4
                if self.direction == "DL":
                    self.direction = "DR"
            if (self.x < paddle.x + paddle.length/12):
                self.angle = 5
                if self.direction == "DR":
                    self.direction = "DL"
            if (self.x > paddle.x + paddle.length - paddle.length/12):
                self.angle = 5
                if self.direction == "DL":
                    self.direction = "DR"
                
            if self.direction == "DL":
                self.direction = "UL"
            elif self.direction == "DR":
                self.direction = "UR"

        if self.angle == 5:
            angleX = 3
            angleY = 1
            if ball.speed < 3:
                ball.speed = ball.speed + 1
        elif self.angle == 4:
            angleX = 3
            angleY = 2
            if ball.speed < 3:
                ball.speed = ball.speed + 1
        elif self.angle == 3:
            angleX = 2
            angleY = 2
        elif self.angle == 2:
            angleX = 1
            angleY = 3
            if ball.speed > 1:
                ball.speed = ball.speed - 1
        elif self.angle == 1:
            angleX = 1
            angleY = 2
            ball.speed = 1
        elif self.angle == 0:
            ball.speed = 1
            angleX = 0
            angleY = 1

        if self.direction == "DR":
            self.x = self.x + angleX * ball.speed
            self.y = self.y + angleY * ball.speed
        elif self.direction == "UR":
            self.x = self.x + angleX * ball.speed
            self.y = self.y - angleY * ball.speed
        elif self.direction == "UL":
            self.x = self.x - angleX * ball.speed
            self.y = self.y - angleY * ball.speed
        elif self.direction == "DL":
            self.x = self.x - angleX * ball.speed
            self.y = self.y + angleY * ball.speed
                
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)
 

ball = Ball(ballX, ballY, WHITE, ballRadius, ballAngle, ballSpeed, ballDirection)
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
    paddle.updateDraw()    
    
    ball.updateDraw()


    # --- Print Variables
    font = pygame.font.Font(None, 36)
    text = font.render(str(ball.angle), 1, (255, 255, 255))
    text2 = font.render(str(ball.x), 1, (255, 255, 255))
    text3 = font.render(str(ball.y), 1, (255, 255, 255))
    text4 = font.render(str(ball.direction), 1, (255, 255, 255))
    screen.blit(text, (900, 20))
    screen.blit(text2, (900, 60))
    screen.blit(text3, (900, 100))
    screen.blit(text4, (900, 140))

 
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(90)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
