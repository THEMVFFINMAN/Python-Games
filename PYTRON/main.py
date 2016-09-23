import copy
import math
import pygame
import random
import sys

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
fill_limit = 750

#user_start_x = 40 * 15 + board_x
#user_start_y = 23 * 15 + board_y
#user_dir = 1
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

# Some more initialization stuff
font = pygame.font.Font(None, 36)
size = (game_width, game_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PYTRON")
clock = pygame.time.Clock()
move = pygame.USEREVENT + 1
pygame.time.set_timer(move, game_speed)


def draw_board():
    # This just draws the grid lines that make up the board
    for k in range(0, block_width + 1):
        pygame.draw.line(screen, GREEN, (board_x - 1 + (k * 15), board_y - 1),
                         (31 + (k * 15), board_height + board_y - 1), 2)

    for k in range(0, block_height + 1):
        pygame.draw.line(screen, GREEN, (board_x - 1, board_y - 1 + (k * 15)),
                         (board_width + board_x - 1, board_y - 1 + (k * 15)), 2)


class Graph(object):
    # The graph is a dict where the key is a tuple of coordinates and the values are the
    # active neighbor coordinates in the form of a tuple
    def __init__(self):
        self.graph_dict = {}
        self.future_graph = {}
        self.generate_new_graph()

    def generate_new_graph(cls):
        # This will generate the graph of coordinates
        graph_dict = {}
        for row in range(0, block_height):
            for column in range(0, block_width):
                graph_dict[(row, column)] = []
                if row + 1 < block_height:
                    graph_dict[(row, column)].append((row + 1, column))
                if row - 1 >= 0:
                    graph_dict[(row, column)].append((row - 1, column))
                if column + 1 < block_width:
                    graph_dict[(row, column)].append((row, column + 1))
                if column - 1 >= 0:
                    graph_dict[(row, column)].append((row, column - 1))
        cls.graph_dict = graph_dict
    
    def get_path_size(cls, x, y):
        # This is the floodfill at work
        if ((x, y)) in cls.future_graph:
            # If the coordinate is in the dict, as in if it isn't a driver wall
            # Then it runs, otherwise it returns 0
            path = set()
            checked = []
            path.add((x, y))
            checked.append((x, y))

            # Instead of recursion, I just continually add things to the queue and then pop them as I go
            while checked:
                coord = checked.pop()
                for element in cls.future_graph[coord]:
                    # I use a set and check the set because checking if it's in a set is constant time
                    # This also prevents me from adding the same coordinates infinite times
                    if element not in path:
                        path.add(element)
                        checked.append(element)

            return len(path)

        return 0

    def copy_graph(cls):
        cls.future_graph = copy.deepcopy(cls.graph_dict)

    def print_graph(cls):
        # This was an invaluable tool when making the future_graph to visibly see it
        
        arrayify = [[0 for x in range(0, block_width)] for y in range(0, block_height)]
        for i in range(0, block_width):
            for j in range(0, block_height):
                if (j, i) in cls.future_graph:
                    arrayify[j][i] = 1

        for row in arrayify:
            print row

        arrayify = [[0 for x in range(0, block_width)] for y in range(0, block_height)]
        for i in range(0, block_width):
            for j in range(0, block_height):
                if (j, i) in cls.graph_dict:
                    arrayify[j][i] = 1

        for row in arrayify:
            print row

    def remove_node(cls, x, y):
        # First it checks all its neighbors (keys) and removes the edges to itself (values)
        # Then it removes itself (key) from the graph
        for coord in cls.graph_dict[(x, y)]:
            cls.graph_dict[coord].remove((x, y))

        cls.graph_dict.pop((x, y), None)

    def remove_future_node(cls, x, y):

        if (x, y) in cls.future_graph:
            for coord in cls.future_graph[(x, y)]:
                cls.future_graph[coord].remove((x, y))

            cls.future_graph.pop((x, y), None)

            return True
        else:
            return False


class Overseer(object):
    # Maintains score, reset, stuff like that

    # TODO Implement score

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
        # This section is what makes the driver's tail stick together
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
    # Driver class for both user and enemies
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
        elif cls.dir == 3:
            cls.image = pygame.transform.rotate(cls.image, 270)

        cls.dir = 0

    def right(cls):
        if cls.dir == 0:
            cls.image = pygame.transform.rotate(cls.image, 270)
        elif cls.dir == 2:
            cls.image = pygame.transform.rotate(cls.image, 90)

        cls.dir = 1

    def down(cls):
        if cls.dir == 1:
            cls.image = pygame.transform.rotate(cls.image, 270)
        elif cls.dir == 3:
            cls.image = pygame.transform.rotate(cls.image, 90)

        cls.dir = 2

    def left(cls):
        if cls.dir == 0:
            cls.image = pygame.transform.rotate(cls.image, 90)
        elif cls.dir == 2:
            cls.image = pygame.transform.rotate(cls.image, 270)

        cls.dir = 3

    def move(cls):
        # Just moves the little rectangle around
        if cls.dir == 0:
            cls.rect.top = cls.rect.top - 15
        elif cls.dir == 1:
            cls.rect.left = cls.rect.left + 15
        elif cls.dir == 2:
            cls.rect.top = cls.rect.top + 15
        elif cls.dir == 3:
            cls.rect.left = cls.rect.left - 15

    def reset(cls, x, y, direction, image):
        # Resets the driver, used after crashes and the like
        cls.image = pygame.image.load(image).convert()
        cls.rect = cls.image.get_rect()
        cls.rotated = False
        cls.rect.left = x
        cls.rect.top = y
        cls.dir = direction


def getNewBoard():
    # This gets you a brand new board on reset and initial start

    board = [[0 for k in range(0, block_width + 2)] for j in range(0, block_height + 2)]

    for i in range(0, block_width + 2):
        board[0][i] = 2
        board[block_height + 1][i] = 2

    for i in range(0, block_height + 1):
        board[i][0] = 2
        board[i][block_width + 1] = 2

    return board


def reset(drivers, overseer):
    # Reset function for crashes and the like
    drivers[0].reset(user_start_x, user_start_y, user_dir, user_image)
    drivers[1].reset(enemy1_start_x, enemy1_start_y, enemy1_dir, enemy1_image)

    for driver in drivers:
        del driver.driver_trail[:]

    raw_input()


def normalize_x(x):
    # This gets an x pixel value and finds its corresponding value in the array
    return ((x - board_x) / 15)


def normalize_y(y):
    # This gets a y pixel value and finds its corresponding value in the array
    return ((y - board_y) / 15)


def makeBrick(driver):
    # This adds the tail behind the driver
    # Every time, it checks this brick with its neighbors' bricks
    # In order to update them to say they now have a block side or not
    # This is where the logic comes in for making the driver's tail stick together

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

    # After checking if the new brick is touching any others, it adds it to the tail
    driver_trail.append(new_brick)

    # It also returns its normalized location to remove it from the graph
    return normalize_x(new_brick.rect.left), normalize_y(new_brick.rect.top)


def update_board(drivers, overseer, g):
    # Start with a clear screen
    
    screen.fill(BLACK)
    draw_board()

    for driver in drivers:

        wall_up, wall_right, wall_down, wall_left = (False,) * 4

        # Checks if the drivers hit each other, it will score as a tie
        for driver2 in drivers:
            if driver2 != driver:
                if pygame.sprite.collide_rect(driver, driver2):
                    reset(drivers, overseer)
                    return False

        # Gets its normalized location for the graph
        update_driver_y = normalize_y(driver.rect.top)
        update_driver_x = normalize_x(driver.rect.left)

        # If the node has been removed (meaning it's a wall)
        # Then the driver crashes and the game resets
        if (update_driver_y, update_driver_x) not in g.graph_dict:
            print driver.color
            g.print_graph()
            reset(drivers, overseer)
            return False

        # Adds the brick and removes it from the graph
        added_brick_x, added_brick_y = makeBrick(driver)
        g.remove_node(added_brick_y, added_brick_x)

        # If the driver isn't the user, then add some ai
        if drivers[0] != driver:

            g.copy_graph()
            

            if  drivers[0].dir == 3 and driver.rect.top != drivers[0].rect.top:
                free_left = True
                future_x = normalize_x(drivers[0].rect.left)
                future_y = normalize_y(drivers[0].rect.top)
                while free_left:
                    future_x -= 1
                    free_left = g.remove_future_node(future_y, future_x)

            # Checks which sides have walls on them
            if (update_driver_y - 1, update_driver_x) not in g.future_graph:
                wall_up = True
            if (update_driver_y, update_driver_x + 1) not in g.future_graph:
                wall_right = True
            if (update_driver_y + 1, update_driver_x) not in g.future_graph:
                wall_down = True
            if (update_driver_y, update_driver_x - 1) not in g.future_graph:
                wall_left = True
                
            # The flood variables initialized
            flood_up, flood_right, flood_down, flood_left = (0,)*4

            # Checks how many open spaces are on each side of the driver
            if not wall_up:
                flood_up = g.get_path_size(update_driver_y - 1, update_driver_x)
            if not wall_right:
                flood_right = g.get_path_size(update_driver_y, update_driver_x + 1)
            if not wall_down:
                flood_down = g.get_path_size(update_driver_y + 1, update_driver_x)
            if not wall_left:
                flood_left = g.get_path_size(update_driver_y, update_driver_x - 1)

            print flood_up, flood_right, flood_down, flood_left

            # Finds the most efficient turn and walls up the other sides
            if flood_up > flood_right and flood_up > flood_left:
                wall_left = True
                wall_right = True
                if flood_up > flood_down:
                    wall_down = True
            if flood_down > flood_right and flood_down > flood_left:
                wall_left = True
                wall_right = True
                if flood_down > flood_up:
                    wall_up = True
            if flood_left > flood_down and flood_left > flood_up:
                wall_up = True
                wall_down = True
                if flood_left > flood_right:
                    wall_right = True
            if flood_right > flood_down and flood_right > flood_up:
                wall_up = True
                wall_down = True
                if flood_right > flood_left:
                    wall_left = True
            
            # Moves the enemy drivers
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

        driver.update_draw()

    pygame.display.flip()

    return True


def keyCheck(key_pressed, user):

    # This checks if a key has been pressed
    # It then adds the required function to a queue
    # When the timing of the clock is right, it pops the next move off

    if key_pressed == 273 and user.dir != 2:
        return user.up
    if key_pressed == 275 and user.dir != 3:
        return user.right
    if key_pressed == 274 and user.dir != 0:
        return user.down
    if key_pressed == 276 and user.dir != 1:
        return user.left

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

    # Make graph of board
    g = Graph()

    # Allows you to press keys in sequence faster than the game ticks
    # So that it will pop the next command when needed
    keys_pressed = []

    while gameOn:
        clock.tick(50)

        # The actual while loop that runs the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False
            if event.type == pygame.KEYDOWN:
                key_checked = keyCheck(event.key, user)
                if key_checked:
                    keys_pressed.insert(0, key_checked)
            if event.type == move:
                
                # If there are any keys added to the queue, it pops them and then runs them
                if keys_pressed:
                    keys_pressed.pop()()
                    
                for driver in drivers:
                    driver.move()
                if not update_board(drivers, overseer, g):
                    g.generate_new_graph()

    pygame.quit()

if __name__ == "__main__":
    main()
