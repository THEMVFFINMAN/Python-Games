import math
import pygame

pygame.init()

# Initializing some colors for cleaner looks throughout
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 80, 0)
RED = (255, 0, 0)
LIGHTBLUE = (0, 255, 255)

# I've tried to program this in it's entirety based on these variables so that they can be changed
# and still work at any time, will do more testing on this later
gameWidth = 1024
gameHeight = 850
boardWidth = 960
boardHeight = 720
boardX = 32
boardY = 100
gameSpeed = 100
blockWidth = 64
blockHeight = 48

# Some initialization stuff
font = pygame.font.Font(None, 36)
size = (gameWidth, gameHeight)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PYTRON")
clock = pygame.time.Clock()
move = pygame.USEREVENT + 1
reset = pygame.USEREVENT + 2
pygame.time.set_timer(move, gameSpeed)

up, right, down, left = (False,)*4

board = [[0 for k in range(0, blockWidth)] for j in range(0, blockHeight)]
userTrail = []

def draw_board():
    # This just draws the grid lines that make up the board
    for k in range(0, blockWidth + 1):
        pygame.draw.line(screen, GREEN, (boardX - 1 + (k* 15), boardY - 1), (31 + (k* 15), boardHeight + boardY - 1), 2)
        
    for k in range(0, blockHeight + 1):
        pygame.draw.line(screen, GREEN, (boardX - 1, boardY - 1 + (k* 15)), (boardWidth + boardX - 1, boardY - 1 + (k* 15)), 2)

class Overseer(object):
    # Maintains score, reset, stuff like that

    def __init__(self):
        self.userScore = 0
        self.CPScore = 0
        self.reset = False

class Brick(object):
    # Brick class for both user and CP bricks
    def __init__(self, x, y, outlinecolor, image):
        self.image = pygame.image.load(image).convert()
        self.outlinecolor = outlinecolor
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False

    def update_draw(self):
        # Determines if a line for an outline needs to be drawn and draws it 
        screen.blit(self.image, self.rect)
        if self.top == False:
            pygame.draw.line(screen, self.outlinecolor, (self.rect.left, self.rect.top), (self.rect.left + 14, self.rect.top), 1)
        if self.right == False:
            pygame.draw.line(screen, self.outlinecolor, (self.rect.left + 14, self.rect.top), (self.rect.left + 14, self.rect.top + 14), 1)
        if self.bottom == False:
            pygame.draw.line(screen, self.outlinecolor, (self.rect.left, self.rect.top + 14), (self.rect.left + 14, self.rect.top + 14), 1)
        if self.left == False:
            pygame.draw.line(screen, self.outlinecolor, (self.rect.left, self.rect.top), (self.rect.left, self.rect.top + 14), 1)

class User(object):

    def __init__(self, x, y, direction):
        self.image = pygame.image.load('tron.png').convert()
        self.rect = self.image.get_rect()
        self.rotated = False
        self.rect.left = x
        self.rect.top = y
        self.dir = direction

    def update_draw(self):
        screen.blit(self.image, self.rect)    

    # These will rotate the image to face the correct way and change the direction as well
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

def reset():
    global user, userTrail
    user = User(56*15 + boardX, 24 * 15 + boardY, 3)
    del userTrail[:]
    overseer.reset = False

    screen.fill(BLACK)
    draw_board()

    user.update_draw()
    pygame.display.flip() 
    
    

def update_board():
    # This is where the magic happens so to speak
    # I wanted to find a way to draw an outline around the blocks in the most efficient way possible
    # Because I had to loop through all the bricks to print them at least once, I added the check code
    # to determine if it needed an outline or not. For my purposes, it is fast and efficient
    screen.fill(BLACK)
    draw_board()

    newUserBrick = Brick(user.rect.left, user.rect.top, LIGHTBLUE, 'brick.png')

    hasReset = False

    for ibrick in userTrail:
        if pygame.sprite.collide_rect(user, ibrick):
            overseer.reset = True
            hasReset = True
            reset()
            break

        ibrick.update_draw()
        
        if newUserBrick.rect.top == ibrick.rect.top:
            if newUserBrick.rect.left == ibrick.rect.left - 15:
                newUserBrick.right = True
                ibrick.left = True
            if newUserBrick.rect.left == ibrick.rect.left + 15:
                newUserBrick.left = True
                ibrick.right = True
        if newUserBrick.rect.left == ibrick.rect.left:
            if newUserBrick.rect.top == ibrick.rect.top - 15 :
                newUserBrick.bottom = True
                ibrick.top = True
            if newUserBrick.rect.top == ibrick.rect.top + 15:
                newUserBrick.top = True
                ibrick.bottom = True     

    if not hasReset:
        userTrail.append(newUserBrick)
        
    user.update_draw()
    
    pygame.display.flip()      

def keyCheck():

    # This checks if a key has been pressed
    # Extra checks have been put in place due to how pygame handles pressed
    # It will only register the moment it has been pressed and no more, even if it is held down
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

# Initialize user and game
user = User(56*15 + boardX, 24 * 15 + boardY, 3)
gameOn = True
overseer = Overseer()

while gameOn:
    
    clock.tick(50)

    print overseer.reset
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False 
        if event.type == pygame.KEYDOWN:
            keyCheck()
        if event.type == move:
            user.move()
            update_board()

pygame.quit()
