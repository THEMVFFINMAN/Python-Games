import math
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 80, 0)
RED = (255, 0, 0)
LIGHTBLUE = (0, 255, 255)

gameWidth = 1024
gameHeight = 850
boardWidth = 960
boardHeight = 720
boardX = 32
boardY = 100
gameSpeed = 100

font = pygame.font.Font(None, 36)
size = (gameWidth, gameHeight)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PYTRON")
clock = pygame.time.Clock()
move = pygame.USEREVENT + 1
pygame.time.set_timer(move, gameSpeed)

layout = []

blockWidth = 64
blockHeight = 48

up = False
right = False
down = False
left = False

board = [[0 for k in range(0, blockWidth)] for j in range(0, blockHeight)]
userTrail = []

def drawBoard():
    for k in range(0, blockWidth + 1):
        pygame.draw.line(screen, GREEN, (boardX - 1 + (k* 15), boardY - 1), (31 + (k* 15), boardHeight + boardY - 1), 2)
        
    for k in range(0, blockHeight + 1):
        pygame.draw.line(screen, GREEN, (boardX - 1, boardY - 1 + (k* 15)), (boardWidth + boardX - 1, boardY - 1 + (k* 15)), 2)

class userBrick(object):

    def __init__(self, x, y):
        self.image = pygame.image.load('brick.png').convert()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False

    def updateDraw(self):
        screen.blit(self.image, self.rect)
        if self.top == False:
            pygame.draw.line(screen, LIGHTBLUE, (self.rect.left, self.rect.top), (self.rect.left + 14, self.rect.top), 1)
        if self.right == False:
            pygame.draw.line(screen, LIGHTBLUE, (self.rect.left + 14, self.rect.top), (self.rect.left + 14, self.rect.top + 14), 1)
        if self.bottom == False:
            pygame.draw.line(screen, LIGHTBLUE, (self.rect.left, self.rect.top + 14), (self.rect.left + 14, self.rect.top + 14), 1)
        if self.left == False:
            pygame.draw.line(screen, LIGHTBLUE, (self.rect.left, self.rect.top), (self.rect.left, self.rect.top + 14), 1)

def addBrick():

    newBrick = userBrick(user.rect.left, user.rect.top)
    updateBrick(newBrick)
    userTrail.append(newBrick)
        
def updateBrick(newBrick):
    for brick in userTrail:
        if newBrick.rect.top == brick.rect.top + 15 and newBrick.rect.left == brick.rect.left:
            newBrick.top = True
            brick.bottom = True
        if newBrick.rect.top == brick.rect.top and newBrick.rect.left == brick.rect.left - 15:
            newBrick.right = True
            brick.left = True
        if newBrick.rect.top == brick.rect.top - 15 and newBrick.rect.left == brick.rect.left:
            newBrick.bottom = True
            brick.top = True
        if newBrick.rect.top == brick.rect.top and newBrick.rect.left == brick.rect.left + 15:
            newBrick.left = True
            brick.right = True

class User(object):

    def __init__(self, x, y, direction):
        self.image = pygame.image.load('tron.png').convert()
        self.rect = self.image.get_rect()
        self.rotated = False
        self.rect.left = x
        self.rect.top = y
        self.dir = direction

    def updateDraw(self):
        screen.blit(self.image, self.rect)    

    def up(self):
        if self.dir == 1:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir = 2
        elif self.dir == 3:
            self.image = pygame.transform.rotate(self.image, 270)
            self.dir = 2

    def right(self):
        if self.dir == 0:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir = 1
        elif self.dir == 2:
            self.image = pygame.transform.rotate(self.image, 270)
            self.dir = 1

    def down(self):
        if self.dir == 1:
            self.image = pygame.transform.rotate(self.image, 270)
            self.dir = 0
        elif self.dir == 3:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir = 0

    def left(self):
        if self.dir == 0:
            self.image = pygame.transform.rotate(self.image, 270)
            self.dir = 3
        elif self.dir == 2:
            self.image = pygame.transform.rotate(self.image, 90)
            self.dir = 3

    def move(self):
        if self.dir == 0:
            self.rect.top = self.rect.top + 15
        elif self.dir == 1:
            self.rect.left = self.rect.left + 15
        elif self.dir == 2:
            self.rect.top = self.rect.top - 15
        elif self.dir == 3:
            self.rect.left = self.rect.left - 15

def updateBoard():
    # This is where the magic happens so to speak
    # I wanted to find a way to draw an outline around the blocks in the most efficient way possible
    # Because I had to loop through all the bricks to print them at least once, I added the check code
    # to determine if it needed an outline or not. For my purposes, it is fast and efficient
    screen.fill(BLACK)
    drawBoard()

    newBrick = userBrick(user.rect.left, user.rect.top)

    for brick in userTrail:
        brick.updateDraw()
        if newBrick.rect.top == brick.rect.top + 15 and newBrick.rect.left == brick.rect.left:
            newBrick.top = True
            brick.bottom = True
        if newBrick.rect.top == brick.rect.top and newBrick.rect.left == brick.rect.left - 15:
            newBrick.right = True
            brick.left = True
        if newBrick.rect.top == brick.rect.top - 15 and newBrick.rect.left == brick.rect.left:
            newBrick.bottom = True
            brick.top = True
        if newBrick.rect.top == brick.rect.top and newBrick.rect.left == brick.rect.left + 15:
            newBrick.left = True
            brick.right = True

    userTrail.append(newBrick)
        
    user.updateDraw()
    
    pygame.display.flip()      

def keyCheck():
    global left, right, up, down
    
    if pygame.key.get_pressed()[pygame.K_UP] and not up:
        up = True
        user.up()
    else:
        up = False    
    if pygame.key.get_pressed()[pygame.K_RIGHT] and not right:
        right = True
        user.right()
    else:
        right = False
    if pygame.key.get_pressed()[pygame.K_DOWN] and not down:
        down = True
        user.down()
    else:
        down = False
    if pygame.key.get_pressed()[pygame.K_LEFT] and not left:
        left = True
        user.left()
    else:
        left = False

user = User(56*15 + boardX, 24 * 15 + boardY, 3)

gameOn = True

while gameOn:
    
    clock.tick(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False 
        if event.type == pygame.KEYDOWN:
            keyCheck()
        if event.type == move:
            addBrick()
            user.move()
            updateBoard()
    
pygame.quit()
