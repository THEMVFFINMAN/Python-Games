import math
import pygame
import random

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
game_speed = 50
block_width = 64
block_height = 48
fill_limit = 500

user_start_x = 56 * 15 + board_x
user_start_y = 24 * 15 + board_y
user_dir = 3
user_image = 'tron.png'
user_color = LIGHTBLUE
user_brick = 'brick.png'


enemy1_start_x = 7 * 15 + board_x
enemy1_start_y = 24 * 15 + board_y
enemy1_dir = 1
enemy1_image = 'cp.png'
enemy1_color = RED
enemy1_brick = 'brick2.png'

# Some initialization stuff
font = pygame.font.Font(None, 36)
size = (game_width, game_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PYTRON")
clock = pygame.time.Clock()
move = pygame.USEREVENT + 1
pygame.time.set_timer(move, game_speed)

up, right, down, left = (False,)*4

def flood_fill(x, y, new_board, direction):
    toFill = set()
    filled = []
    filled.append((x, y))
    toFill.add((x, y))
    fill = 0

    if direction == 0:
        filled.append((x, y + 1))
    elif direction == 1:
        filled.append((x - 1, y))
    elif direction == 2:
        filled.append((x, y - 1))
    elif direction == 3:
        filled.append((x + 1, y))

    while toFill:
        (x,y) = toFill.pop()
        filled.append((x, y))
        
        if new_board[y][x] != 0:
            continue

        fill += 1

        if fill >= fill_limit:
            return fill
        
        if (x - 1, y) not in filled:
            toFill.add((x - 1,y))
        if (x + 1,y) not in filled:
            toFill.add((x + 1,y))
        if (x,y - 1) not in filled:
            toFill.add((x,y - 1))
        if (x,y + 1) not in filled:
            toFill.add((x,y + 1))
        
    return fill
    
def draw_board():
    # This just draws the grid lines that make up the board
    for k in range(0, block_width + 1):
        pygame.draw.line(screen, GREEN, (board_x - 1 + (k * 15), board_y - 1),
                         (31 + (k * 15), board_height + board_y - 1), 2)

    for k in range(0, block_height + 1):
        pygame.draw.line(screen, GREEN, (board_x - 1, board_y - 1 + (k * 15)),
                         (board_width + board_x - 1, board_y - 1 + (k * 15)), 2)

class Graph(object):
    def __init__(self, graph_list):
        self.graph_dict = self.generate(graph_list)

    def generate(cls, graph_list):
        graph_dict = {}
        i = 1
        for row in graph_list[:-1]:
            j = 1
            for value in row[:-1]:
                graph_dict[(i, j)] = []
                if i + 1 < len(graph_list) - 1:
                    graph_dict[(i, j)].append((i + 1, j))
                if i - 1 >= 1:
                    graph_dict[(i, j)].append((i - 1, j))
                if j + 1 < len (row) - 1:
                    graph_dict[(i, j)].append((i, j + 1))
                if j - 1 >= 1:
                    graph_dict[(i, j)].append((i, j - 1))
                j += 1
            i += 1
        return graph_dict

    def get_path_size(cls, x, y):
        path = set()
        checked = []
        path.add((x, y))
        checked.append((x, y))

        while checked:
            coord = checked.pop()
            for element in cls.graph_dict[coord]:
                if element not in path:
                    path.add(element)
                    checked.append(element)          
        
        return len(path)
    def remove_node(cls, x, y):
        for coord in cls.graph_dict[(x, y)]:
            cls.graph_dict[coord].remove((x, y))

class Overseer(object):
    # Maintains score, reset, stuff like that

    def __init__(self):
        self.user_score = 0
        self.cp_score = 0


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
            cls.dir = 0
        elif cls.dir == 3:
            cls.image = pygame.transform.rotate(cls.image, 270)
            cls.dir = 0

    def right(cls):
        if cls.dir == 0:
            cls.image = pygame.transform.rotate(cls.image, 270)
            cls.dir = 1
        elif cls.dir == 2:
            cls.image = pygame.transform.rotate(cls.image, 90)
            cls.dir = 1

    def down(cls):
        if cls.dir == 1:
            cls.image = pygame.transform.rotate(cls.image, 270)
            cls.dir = 2
        elif cls.dir == 3:
            cls.image = pygame.transform.rotate(cls.image, 90)
            cls.dir = 2

    def left(cls):
        if cls.dir == 0:
            cls.image = pygame.transform.rotate(cls.image, 90)
            cls.dir = 3
        elif cls.dir == 2:
            cls.image = pygame.transform.rotate(cls.image, 270)
            cls.dir = 3

    def move(cls):
        if cls.dir == 0:
            cls.rect.top = cls.rect.top - 15
        elif cls.dir == 1:
            cls.rect.left = cls.rect.left + 15
        elif cls.dir == 2:
            cls.rect.top = cls.rect.top + 15
        elif cls.dir == 3:
            cls.rect.left = cls.rect.left - 15

    def reset(cls, x, y, direction, image):
        cls.image = pygame.image.load(image).convert()
        cls.rect = cls.image.get_rect()
        cls.rotated = False
        cls.rect.left = x
        cls.rect.top = y
        cls.dir = direction

def getNewBoard():
    board = [[0 for k in range(0, block_width + 2)] for j in range(0, block_height + 2)]

    for i in range(0, block_width + 2):
        board[0][i] = 2
        board[block_height + 1][i] = 2

    for i in range(0, block_height + 1):
        board[i][0] = 2
        board[i][block_width + 1] = 2

    return board


def reset(drivers, overseer):
    
    drivers[0].reset(user_start_x, user_start_y, user_dir, user_image)
    drivers[1].reset(enemy1_start_x, enemy1_start_y, enemy1_dir, enemy1_image)

    for driver in drivers:
        del driver.driver_trail[:]

def normalize_x(x):
    return ((x - board_x) / 15) + 1

def normalize_y(y):
    return ((y - board_y) / 15) + 1

def makeBrick(driver):
    # This is where the magic happens so to speak
    # I wanted to find a way to draw an outline around the blocks in the most efficient way possible
    # Because I had to loop through all the bricks to print them at least once, I added the check code
    # to determine if it needed an outline or not. For my purposes, it is fast and efficient
    
    new_brick = Brick(driver.rect.left, driver.rect.top, driver.color, driver.brickimage)
    driver_trail = driver.driver_trail
    
    for ibrick in driver_trail:
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

    return (normalize_x(new_brick.rect.left), normalize_y(new_brick.rect.top))


def update_board(drivers, overseer, board, g):
    
    screen.fill(BLACK)
    draw_board()

    for driver in drivers:
        
        best_up, best_right, best_down, best_left, wall_up, wall_right, wall_down, wall_left = (False,) * 8

        for driver2 in drivers:
            if driver2 != driver:
                if pygame.sprite.collide_rect(driver, driver2):
                    reset(drivers, overseer)
                    return getNewBoard()

        update_driver_y = normalize_y(driver.rect.top)
        update_driver_x = normalize_x(driver.rect.left)

        if board[update_driver_y][update_driver_x] != 0:
            reset(drivers, overseer)
            return getNewBoard()

        if drivers[0] != driver:
            
            new_board = list(board)
            
            flood_up = flood_fill(update_driver_x, update_driver_y - 1, new_board, driver.dir)
            flood_right = flood_fill(update_driver_x + 1, update_driver_y, new_board, driver.dir)
            flood_down = flood_fill(update_driver_x, update_driver_y + 1, new_board, driver.dir)
            flood_left = flood_fill(update_driver_x - 1, update_driver_y, new_board, driver.dir)

            if board[update_driver_y - 1][update_driver_x] != 0:
                wall_up = True
            if board[update_driver_y][update_driver_x + 1] != 0:
                wall_right = True
            if board[update_driver_y + 1][update_driver_x] != 0:
                wall_down = True
            if board[update_driver_y][update_driver_x - 1] != 0:
                wall_left = True

            if wall_up and driver.dir == 0:
                
                if wall_left:
                    print "upleft"
                    driver.right()
                elif wall_right:
                    print "upright"
                    driver.left()
                else:
                    print "up"
                    if bool(random.getrandbits(1)):
                        driver.right()
                    else:
                        driver.left()
                        
            if wall_right and driver.dir == 1:
                
                if wall_up:
                    print "rightup"
                    driver.down()
                elif wall_down:
                    print "rightdown"
                    driver.up()
                else:
                    print "right"
                    if bool(random.getrandbits(1)):
                        driver.down()
                    else:
                        driver.up()
                        
            if wall_down and driver.dir == 2:
                
                if wall_left:
                    print "downleft"
                    driver.right()
                elif wall_right:
                    print "downright"
                    driver.left()
                else:
                    print "down"
                    if bool(random.getrandbits(1)):
                        driver.right()
                    else:
                        driver.left()
                        
            if wall_left and driver.dir == 3:
                
                if wall_up:
                    print "leftup"
                    driver.down()
                elif wall_down:
                    print "leftdown"
                    driver.up()
                else:
                    print "left"
                    if bool(random.getrandbits(1)):
                        driver.down()
                    else:
                        driver.up()
                                    
        makeBrick(driver)

        if driver.color == LIGHTBLUE:
            board[update_driver_y][update_driver_x] = 1
        else:
            board[update_driver_y][update_driver_x] = 3
        
        driver.update_draw()           

    pygame.display.flip()

    return board


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
    user = Driver(user_start_x, user_start_y, user_dir, user_image, user_color, user_brick)
    enemy1 = Driver(enemy1_start_x, enemy1_start_y, enemy1_dir, enemy1_image, enemy1_color, enemy1_brick)
    
    drivers = []
    gameOn = True
    overseer = Overseer()

    # Initiate drivers
    drivers.append(user)
    drivers.append(enemy1)

    # Make board (For collision purposes mainly for user)
    # Make graph (For AI purposes)
    board = getNewBoard()
    g = Graph(board)

    while gameOn:
        clock.tick(50)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False 
            if event.type == pygame.KEYDOWN:
                keyCheck(user)
            if event.type == move:
                for driver in drivers:
                    driver.move()
                board = update_board(drivers, overseer, board, g)

    pygame.quit()

if __name__ == "__main__":
    main()
