import math
import pygame

pygame.init()

# Initializing some colors for cleaner looks throughout
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 80, 0)
RED = (255, 0, 0)
LIGHTBLUE = (0, 255, 255)

# I've tried to program this in it's entirety based
# on these variables so that they can be changed
# and still work at any time, will do more testing on this later
game_width = 1024
game_height = 850
board_width = 960
board_height = 720
board_x = 32
board_y = 100
game_speed = 100
block_width = 64
block_height = 48

# Some initialization stuff
font = pygame.font.Font(None, 36)
size = (game_width, game_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PYTRON")
clock = pygame.time.Clock()
move = pygame.USEREVENT + 1
reset = pygame.USEREVENT + 2
pygame.time.set_timer(move, game_speed)

up, right, down, left = (False,)*4

board = [[0 for k in range(0, block_width)] for j in range(0, block_height)]

def draw_board():
    # This just draws the grid lines that make up the board
    for k in range(0, block_width + 1):
        pygame.draw.line(screen, GREEN, (board_x - 1 + (k * 15), board_y - 1),
                         (31 + (k * 15), board_height + board_y - 1), 2)

    for k in range(0, block_height + 1):
        pygame.draw.line(screen, GREEN, (board_x - 1, board_y - 1 + (k * 15)),
                         (board_width + board_x - 1, board_y - 1 + (k * 15)), 2)


class Overseer(object):
    # Maintains score, reset, stuff like that

    def __init__(self):
        self.user_score = 0
        self.cp_score = 0
        self.reset = False
        self.walls = []


class Wall(object):
    # The invisible walls

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)


class Brick(object):
    # Brick class for both user and CP bricks
    def __init__(self, x, y, outline_color, image):
        self.image = pygame.image.load(image).convert()
        self.outline_color = outline_color
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False

    def update_draw(cls):
        # Determines if a line for an outline needs to be drawn and draws it 
        screen.blit(cls.image, cls.rect)
        if cls.top is False:
            pygame.draw.line(screen, cls.outline_color, (cls.rect.left, cls.rect.top), 
            (cls.rect.left + 14, cls.rect.top), 1)
        if cls.right is False:
            pygame.draw.line(screen, cls.outline_color, (cls.rect.left + 14, cls.rect.top), 
            (cls.rect.left + 14, cls.rect.top + 14), 1)
        if cls.bottom is False:
            pygame.draw.line(screen, cls.outline_color, (cls.rect.left, cls.rect.top + 14), 
            (cls.rect.left + 14, cls.rect.top + 14), 1)
        if cls.left is False:
            pygame.draw.line(screen, cls.outline_color, (cls.rect.left, cls.rect.top), 
            (cls.rect.left, cls.rect.top + 14), 1)


class User(object):

    def __init__(self, x, y, direction):
        self.image = pygame.image.load('tron.png').convert()
        self.rect = self.image.get_rect()
        self.rotated = False
        self.rect.left = x
        self.rect.top = y
        self.dir = direction

    def update_draw(cls):
        screen.blit(cls.image, cls.rect)    

    # These will rotate the image to face the correct way and change the direction as well
    def up(cls):
        if cls.dir == 1:
            cls.image = pygame.transform.rotate(cls.image, 90)
            cls.dir = 2
        elif cls.dir == 3:
            cls.image = pygame.transform.rotate(cls.image, 270)
            cls.dir = 2

    def right(cls):
        if cls.dir == 0:
            cls.image = pygame.transform.rotate(cls.image, 90)
            cls.dir = 1
        elif cls.dir == 2:
            cls.image = pygame.transform.rotate(cls.image, 270)
            cls.dir = 1

    def down(cls):
        if cls.dir == 1:
            cls.image = pygame.transform.rotate(cls.image, 270)
            cls.dir = 0
        elif cls.dir == 3:
            cls.image = pygame.transform.rotate(cls.image, 90)
            cls.dir = 0

    def left(cls):
        if cls.dir == 0:
            cls.image = pygame.transform.rotate(cls.image, 270)
            cls.dir = 3
        elif cls.dir == 2:
            cls.image = pygame.transform.rotate(cls.image, 90)
            cls.dir = 3

    def move(cls):
        if cls.dir == 0:
            cls.rect.top = cls.rect.top + 15
        elif cls.dir == 1:
            cls.rect.left = cls.rect.left + 15
        elif cls.dir == 2:
            cls.rect.top = cls.rect.top - 15
        elif cls.dir == 3:
            cls.rect.left = cls.rect.left - 15


def reset(overseer, user, user_trail):
    user.rect.left = 56*15 + board_x
    user.rect.top = 24 * 15 + board_y
    user.dir = 3
    user.image = pygame.image.load('tron.png').convert()
    del user_trail[:]
    overseer.reset = False
    
    screen.fill(BLACK)
    draw_board()

    user.update_draw()
    pygame.display.flip() 


def update_board(user, overseer, user_trail):
    # This is where the magic happens so to speak
    # I wanted to find a way to draw an outline around the blocks in the most efficient way possible
    # Because I had to loop through all the bricks to print them at least once, I added the check code
    # to determine if it needed an outline or not. For my purposes, it is fast and efficient
    screen.fill(BLACK)
    draw_board()

    new_user_brick = Brick(user.rect.left, user.rect.top, LIGHTBLUE, 'brick.png')

    has_reset = False

    for ibrick in user_trail:
        if pygame.sprite.collide_rect(user, ibrick):
            overseer.reset = True
            has_reset = True
            reset(overseer, user, user_trail)
            break

        ibrick.update_draw()
        
        if new_user_brick.rect.top == ibrick.rect.top:
            if new_user_brick.rect.left == ibrick.rect.left - 15:
                new_user_brick.right = True
                ibrick.left = True
            if new_user_brick.rect.left == ibrick.rect.left + 15:
                new_user_brick.left = True
                ibrick.right = True
        if new_user_brick.rect.left == ibrick.rect.left:
            if new_user_brick.rect.top == ibrick.rect.top - 15:
                new_user_brick.bottom = True
                ibrick.top = True
            if new_user_brick.rect.top == ibrick.rect.top + 15:
                new_user_brick.top = True
                ibrick.bottom = True

    for wall in overseer.walls:
        print wall.rect.left, wall.rect.top, wall.rect.width, wall.rect.height
        if pygame.sprite.collide_rect(user, wall):
            overseer.reset = True
            has_reset = True
            reset(overseer, user, user_trail)
            break

    if not has_reset:
        user_trail.append(new_user_brick)
        
    user.update_draw()
    
    pygame.display.flip()      


def keyCheck(user):

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


def main():

    # Initialize user and game
    user = User(56*15 + board_x, 24 * 15 + board_y, 3)
    user_trail = []
    gameOn = True
    overseer = Overseer()
    
    # Place the invisible walls
    topwall = Wall(board_x, board_y - 1, board_width, 1)
    rightwall = Wall(board_x + board_width + 1, board_y, 1, board_height)
    bottomwall = Wall(board_x, board_y + board_height + 1, board_width, 1)
    leftwall = Wall(board_x - 1, board_y, 1, board_height)

    overseer.walls.append(topwall)
    overseer.walls.append(rightwall)
    overseer.walls.append(bottomwall)
    overseer.walls.append(leftwall)

    while gameOn:
        clock.tick(50)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False 
            if event.type == pygame.KEYDOWN:
                keyCheck(user)
            if event.type == move:
                user.move()
                update_board(user, overseer, user_trail)

    pygame.quit()

if __name__ == "__main__":
    main()
