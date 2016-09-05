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


class Driver(object):

    def __init__(self, x, y, direction, image, color, brickimage):
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rotated = False
        self.rect.left = x
        self.rect.top = y
        self.dir = direction
        self.color = color
        self.brickimage = brickimage
        self.driver_trail = []

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

    def reset(cls, x, y, direction, image):
        cls.image = pygame.image.load(image).convert()
        cls.rect = cls.image.get_rect()
        cls.rotated = False
        cls.rect.left = x
        cls.rect.top = y
        cls.dir = direction


def reset(drivers, overseer):
    
    drivers[0].reset(56*15 + board_x, 24 * 15 + board_y, 3, 'tron.png')
    drivers[1].reset(8*15 + board_x, 24 * 15 + board_y, 1, 'cp.png')

    for driver in drivers:
        del driver.driver_trail[:]

    overseer.reset = False
    
    screen.fill(BLACK)
    draw_board()

    pygame.display.flip()

def makeBrick(driver):
    new_brick = Brick(driver.rect.left, driver.rect.top, driver.color, driver.brickimage)
    driver_trail = driver.driver_trail
    for ibrick in driver_trail:
        if pygame.sprite.collide_rect(driver, ibrick):
            return False

        ibrick.update_draw()
        
        if new_brick.rect.top == ibrick.rect.top:
            if new_brick.rect.left == ibrick.rect.left - 15:
                new_brick.right = True
                ibrick.left = True
            if new_brick.rect.left == ibrick.rect.left + 15:
                new_brick.left = True
                ibrick.right = True
        if new_brick.rect.left == ibrick.rect.left:
            if new_brick.rect.top == ibrick.rect.top - 15:
                new_brick.bottom = True
                ibrick.top = True
            if new_brick.rect.top == ibrick.rect.top + 15:
                new_brick.top = True
                ibrick.bottom = True

    driver_trail.append(new_brick)

    return False


def update_board(drivers, overseer):
    # This is where the magic happens so to speak
    # I wanted to find a way to draw an outline around the blocks in the most efficient way possible
    # Because I had to loop through all the bricks to print them at least once, I added the check code
    # to determine if it needed an outline or not. For my purposes, it is fast and efficient
    screen.fill(BLACK)
    draw_board()

    has_reset = False

    for driver in drivers:
        has_reset = makeBrick(driver)

    for wall in overseer.walls:
        for driver in drivers:
            if pygame.sprite.collide_rect(driver, wall):
                overseer.reset = True
                has_reset = True
                reset(drivers, overseer)
                break

    if has_reset:
        reset(drivers, overseer)

    for driver in drivers:
        driver.update_draw()
    
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
    user = Driver(56*15 + board_x, 24 * 15 + board_y, 3, 'tron.png', LIGHTBLUE, 'brick.png')
    enemy1 = Driver(6*15 + board_x, 24 * 15 + board_y, 1, 'cp.png', RED, 'brick2.png')
    drivers = []
    gameOn = True
    overseer = Overseer()

    # Initiate drivers
    drivers.append(user)
    drivers.append(enemy1)
    
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
                enemy1.move()
                update_board(drivers, overseer)

    pygame.quit()

if __name__ == "__main__":
    main()
