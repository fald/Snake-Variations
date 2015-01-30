#! usr/bin/env python

import sys, random, math, copy

try:
    from config import *
    from pygame.locals import *
    import pygame
except ImportError:
    print "You need the config and pygame modules to run this file."
    sys.exit(0)

# --------------------
# TODO:
#   - Snake AI
#   - Ability to change controls
# --------------------

class Apple(object):
    def __init__(self, img, x=None, y=None):
        self.x = x
        self.y = y
        # Load images elsewhere.
        # self.img = transform.scale(image.load(img), (size, size))
        self.img = img


    def dist_to(self, other):
        # Coulda handled this with absolute values, buttfuckit.
        x_dist = max(self.x, other.x) - min(self.x, other.x)
        y_dist = max(self.y, other.y) - min(self.y, other.y)

        total_dist = math.sqrt((x_dist ** 2) + (y_dist ** 2))

        return total_dist
    

    def new_apple(self, snakes,
                  x_bounds=RESOLUTION[0],
                  y_bounds=RESOLUTION[1],
                  block_size=BLOCK_SIZE):
        # not making a new object because imaginary optimization!
        self.x, self.y = None, None
        apple_in_snake = False
        # Bah, can't test if x,y in all snakes in 1 line
        # I think thats a python3 thing.
        # x in i for i in y
        while (not self.x) or (not self.y) or \
              (apple_in_snake):
            self.x, self.y = (block_size * \
                              random.randrange(0, x_bounds / \
                                               block_size - 1),
                              block_size * \
                              random.randrange(0, y_bounds / \
                                               block_size - 1))
            for snake in snakes:
                if (self.x, self.y) in snake.body:
                    apple_in_snake = True
                    break

    def draw(self, display):
        display.blit(self.img, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))
                                               








class Snake(object):
    # --------------
    # Directions
    # --------------
    NORTH   = (0, -1)
    EAST    = (1, 0)
    SOUTH   = (0, 1)
    WEST    = (-1, 0)
    DIRECTIONS = (NORTH, EAST, SOUTH, WEST)

    # --------------
    # Control
    # --------------
    HUMAN   = 0
    AI_DUR  = 1
    AI_BSC  = 2
    AI_ADV  = 3
    AI_LRN  = 4

    # -----------------------------
    # Controling keys (for humans)
    # -----------------------------
    DEFAULT = {"Up":NORTH, "Down":SOUTH, "Left":WEST, "Right":EAST}
    DEFAULT_1 = {"Up":K_w, "Down":K_s, "Left":K_a, "Right":K_d}
    CUSTOM_1  = {"Up":K_w, "Down":K_s, "Left":K_a, "Right":K_d}
    DEFAULT_2 = {"Up":K_UP, "Down":K_DOWN, "Left":K_LEFT, "Right":K_RIGHT}
    CUSTOM_2  = {"Up":K_UP, "Down":K_DOWN, "Left":K_LEFT, "Right":K_RIGHT}
    
    def __init__(self, name, head_img, x, y, start_direction,
                 color, control=HUMAN, buttons=DEFAULT_1,
                 size=START_SIZE):
        self.score = 0
        self.name = name
        self.img = head_img
        # Suboptimal. Rotating the original each loop
        # versus just having the 4 images.
        self.orig_img = head_img
        self.x, self.y = x, y
        self.direction = start_direction
        self.control = control
        if self.control == Snake.HUMAN:
            self.buttons = buttons
        self.color = color
        self.size = size
        self.body = []
        # Go backwards, as we want the head to be at position -1
        for i in range(self.size - 1, 0, -1):
            self.body.append((self.x - BLOCK_SIZE * i * self.direction[0],
                              self.y - BLOCK_SIZE * i * self.direction[1]))
        self.body.append((self.x, self.y))
        return

    def __str__(self):
        return self.name
    
    def update_position(self):
        # No case where we wait for multiple loops to update
        # sooo skip that.
        movement = tuple(BLOCK_SIZE * x for x in self.direction)
        zipped_movement = zip(self.body[-1], movement)
        self.x, self.y = tuple(sum(pair) for pair in zipped_movement)
        self.body.append((self.x, self.y))
        if len(self.body) > self.size:
            self.body.pop(0)
        return
        
    
    def process_command(self, event):
        if event.type == KEYDOWN:
            if event.key == self.buttons["Up"]:
                if self.direction != Snake.SOUTH:
                    self.direction = Snake.NORTH
                return True
            elif event.key == self.buttons["Down"]:
                if self.direction != Snake.NORTH:
                    self.direction = Snake.SOUTH
                return True
            elif event.key == self.buttons["Left"]:
                if self.direction != Snake.EAST:
                    self.direction = Snake.WEST
                return True
            elif event.key == self.buttons["Right"]:
                if self.direction != Snake.WEST:
                    self.direction = Snake.EAST
                return True


    def collide_with(self, other):
        if self.body[-1] in other.body:
            return True
        return False


    def collide_self(self):
        ''' Requires new method because the head will always be in its own body. '''
        if self.body[-1] in self.body[:-1]:
            return True
        return False

        
    def collide_wall(self):
        if (self.body[-1][0] not in range(RESOLUTION[0])) or \
           (self.body[-1][1] not in range(RESOLUTION[1])):
            return True
        return False
            

    def will_collide(self, other):
        ''' Combine collision tests. '''
        return self.collide_with(other) or \
               self.collide_self() or \
               self.collide_wall()


    def eats_apple(self, apple):
        if self.body[-1] == (apple.x, apple.y):
            return True
        return False


    def increase_size(self):
        self.size += 1
        return


    def increase_score(self):
        self.score += 1
        return
    

    def set_score(self, value):
        self.score = value
        return

        
    # -------------
    # AI
    # -------------
    # TODO: AI
    # AI_DUR = Random
    # AI_BSC = Random, but don't crash
    # AI_ADV = When not crashing, move towards nearest apple
    # AI_LRN = Hopefully, learned mechanic, so potential for
    #          actual plays and traps and stuff.
    def determine_move(self, others, apples):
        # Greedy Algorithm AI - Don't look ahead more than
        # one move.
        
        if self.control == Snake.AI_DUR:
##            return random.choice((Snake.NORTH, Snake.EAST,
##                                 Snake.SOUTH, Snake.WEST))
            # self.direction so its weighted towards staying
            # the course
            direction = random.choice((Snake.NORTH, Snake.EAST,
                                       Snake.SOUTH, Snake.WEST,
                                       self.direction))
            aiEvent = pygame.event.Event(2, {'key':direction})
            return aiEvent


        if self.control == Snake.AI_BSC:
            pass


        if self.control == Snake.AI_ADV:
            closest_apple = None
            # Ensure the initial closest dist is impossibly far
            closest_dist  = RESOLUTION[0] * RESOLUTION[1]
            for apple in apples:
                dist_to_self = apple.dist_to(self)
                if dist_to_self < closest_dist:
                    closest_dist = dist_to_self
                    closest_apple = apple
            # To hold the 2 directions that'll get the snake
            # closer to an apple
            preferred_directions = []
            if self.x < closest_apple.x:
                preferred_directions.append(Snake.EAST)
            elif self.x > closest_apple.x:
                preferred_directions.append(Snake.WEST)
            if self.y < closest_apple.y:
                preferred_directions.append(Snake.SOUTH)
            elif self.y > closest_apple.y:
                preferred_directions.append(Snake.NORTH)
            possible_directions = []
            # If current head + each direction will crash
            # or will hit other snakes heads + direction,
            # don't include.
            # Don't worry about potential moves of enemy,
            # as this is just a basic level, only the dir
            # its currently moving in.
            # Otherwise, include.
            possible_directions = list(Snake.DIRECTIONS[:])
            if self.direction == Snake.NORTH:
                possible_directions.remove(Snake.SOUTH)
            elif self.direction == Snake.SOUTH:
                possible_directions.remove(Snake.NORTH)
            elif self.direction == Snake.EAST:
                possible_directions.remove(Snake.WEST)
            elif self.direction == Snake.WEST:
                possible_directions.remove(Snake.EAST)

            possible_copy = possible_directions[:]
            for direction in possible_directions:
                future_snake = copy.deepcopy(self)
                future_snake.direction = direction
                future_snake.update_position()
                for other in others:
                    if future_snake.will_collide(other):
                        possible_copy.remove(direction)

            possible_directions = possible_copy[:]

            # For preferred directions, if they're in
            # possible, just take 'em.
            # Don't worry about fairness of choice as
            # this is the basic AI.
            final_choices = []
            for direction in preferred_directions:
                if direction in possible_directions:
                    final_choices.append(direction)

            if len(final_choices) > 0:
                final_dir = random.choice(final_choices)
            elif len(possible_directions) > 0:
                final_dir = random.choice(possible_directions)
            else:
                final_dir = self.direction

            aiEvent = pygame.event.Event(2, {'key':final_dir})
            return aiEvent


        if self.control == Snake.AI_LRN:
            pass




    
    

    def draw(self, display):
        for x, y in self.body[:-1]:
            display.fill(self.color, (x, y, BLOCK_SIZE, BLOCK_SIZE))

        if self.direction[0] != 0:
            self.img = pygame.transform.rotate(self.orig_img,
                                               90 + ((self.direction[0] > 0) * 180))
        else:
            self.img = pygame.transform.rotate(self.orig_img,
                                               0 + ((self.direction[1] > 0) * 180))

        display.blit(self.img, self.body[-1] + (BLOCK_SIZE, BLOCK_SIZE))
        
                                               
            












