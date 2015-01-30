import pygame, sys, random, math, time
from pygame.locals import *

try:
    from res import config
    from res.config import *
except ImportError:
    print "You need the config module to continue!"


def load_images():
    greenSnake = pygame.transform.scale(pygame.image.load(P1),
                                        (BLOCK_SIZE,
                                         BLOCK_SIZE))
    blueSnake = pygame.transform.scale(pygame.image.load(P2),
                                        (BLOCK_SIZE,
                                         BLOCK_SIZE))
    apple = pygame.transform.scale(pygame.image.load(APPLE),
                                        (BLOCK_SIZE,
                                         BLOCK_SIZE))

    return greenSnake, blueSnake, apple


def load_fonts():
    defaultFont = pygame.font.SysFont(FONT_M[0], FONT_M[1], FONT_M[2])
    tinyFont = pygame.font.SysFont(FONT_S[0], FONT_S[1], FONT_S[2])
    largeFont = pygame.font.SysFont(FONT_L[0], FONT_L[1], FONT_L[2])

    return tinyFont, defaultFont, largeFont


def basic_setup():
    pygame.init()
    gameDisplay = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()

    icon = pygame.transform.scale(pygame.image.load(ICON),
                                        (32, 32))
    pygame.display.set_icon(icon)

    return gameDisplay, clock


def safe_exit():
    pygame.display.quit()
    sys.exit(0)


def check_quit(event):
    if (event.type == pygame.QUIT) or \
       (event.type == pygame.KEYUP and \
        event.key == pygame.K_ESCAPE):
        return True
    else:
        return False
    
    
def msg_to_screen(gameDisplay, msg, font,
                  color, location, antialias=True):
    text_surface    = font.render(msg, antialias, color)
    text_rect       = text_surface.get_rect() 

    text_rect.center = location
    gameDisplay.blit(text_surface, text_rect)
    return

def draw_apple(gameDisplay, apple_img, apple_x, apple_y):
    gameDisplay.blit(apple, (apple_x, apple_y))

def new_apple(snakeList_g, snakeList_b):
    apple_x, apple_y = snakeList_g[-1]
    while [apple_x, apple_y] in snakeList_g or \
          [apple_x, apple_y] in snakeList_b:
        apple_x, apple_y = (BLOCK_SIZE * random.randrange(0, RESOLUTION[0] / BLOCK_SIZE - 1),
                            BLOCK_SIZE * random.randrange(0, RESOLUTION[1] / BLOCK_SIZE - 1))
    return apple_x, apple_y


def draw_snakes(gameDisplay,
                snakeList_g, snake_g_x_change, snake_g_y_change,
                snakeList_b, snake_b_x_change, snake_b_y_change):


    increment_b = min(25, 255 / len(snakeList_b))
    increment_g = min(25, 255 / len(snakeList_g))
    for x, y in snakeList_b[:-1]:
        col = increment_b * (len(snakeList_b) - (snakeList_b.index([x,y])))
        col = tuple(min(255, sum(pair)) for pair in zip(BLUE, (col,)*3))
        gameDisplay.fill(col, (x, y, BLOCK_SIZE, BLOCK_SIZE))
    for x, y in snakeList_g[:-1]:
        col = increment_g * (len(snakeList_g) - (snakeList_g.index([x,y])))
        col = tuple(min(255, sum(pair)) for pair in zip(GREEN, (col,)*3))
        gameDisplay.fill(col, (x, y, BLOCK_SIZE, BLOCK_SIZE))

        
    if snake_g_x_change != 0:
        snake_g_face = pygame.transform.rotate(snake_g,
                                               90 + ((snake_g_x_change > 0) * 180))
    else:
        snake_g_face = pygame.transform.rotate(snake_g,
                                               0 + ((snake_g_y_change > 0) * 180))
    gameDisplay.blit(snake_g_face, snakeList_g[-1])

    if snake_b_x_change != 0:
        snake_b_face = pygame.transform.rotate(snake_b,
                                               90 + ((snake_b_x_change > 0) * 180))
    else:
        snake_b_face = pygame.transform.rotate(snake_b,
                                               0 + ((snake_b_y_change > 0) * 180))
    gameDisplay.blit(snake_b_face, snakeList_b[-1])

    return

    
def game_intro(gameDisplay, fonts, clock):
    intro = True
    gameDisplay.fill(WHITE)
    msg_to_screen(gameDisplay,
                  "2 MANY SNAKES",
                  fonts[2], GREEN,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 - fonts[2].get_linesize()))
    msg_to_screen(gameDisplay,
                  "The objective of the game is to not die first.",
                  fonts[1], BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + fonts[1].get_linesize()))
    msg_to_screen(gameDisplay,
                  "Collect apples to grow longer. Help or hindrance?",
                  fonts[1], BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + 2 * fonts[1].get_linesize()))
    msg_to_screen(gameDisplay,
                  "WASD for Green, Arrow Keys for Blue.",
                  fonts[1], BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + 3 * fonts[1].get_linesize()))
    msg_to_screen(gameDisplay,
                  "Space to start...",
                  fonts[1], BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + 4 * fonts[1].get_linesize()))

    pygame.display.update()

    while intro:
        for event in pygame.event.get():
            if check_quit(event):
                safe_exit()
            else:
                if event.type == pygame.KEYUP and \
                   event.key == pygame.K_SPACE:
                    intro = False
        clock.tick(FPS)
    return
                

def pause(gameDisplay, fonts, clock):
    paused = True
    msg_to_screen(gameDisplay, "PAUSED...",
                  fonts[2], RED2,
                  gameDisplay.get_rect().center)
    msg_to_screen("Press P to continue",
                  fonts[1], BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + 2 * fonts[1].get_linesize()))
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if check_quit(event):
                safe_exit()
            else:
                if event.type == pygame.KEYUP and \
                   event.key == pygame.K_SPACE:
                    paused = False
        clock.tick(FPS)
    return
                   
    
def main_loop(gameDisplay, clock, snake_g, snake_b, apple, fonts):
    gameExit = False
    gameOver = False
    snake_g_x, snake_g_y = [0, 0]
    snake_g_x_change, snake_g_y_change = (BLOCK_SIZE, 0) # Start off moving right
    snake_b_x, snake_b_y = [RESOLUTION[0] - BLOCK_SIZE,
                            RESOLUTION[1] - BLOCK_SIZE]
    snake_b_x_change, snake_b_y_change = (-BLOCK_SIZE, 0)
    score_b = 0
    score_g = 0
    snakeHead_g = [snake_g_x, snake_g_y]
    snakeHead_b = [snake_b_x, snake_b_y]
    snakeList_b = []
    snakeList_g = []
    winner = None
        # Fuck this, assume start size 1 for now..
##    for i in range(START_SIZE):
##        snakeList_b.appemd(


    for i in range(START_SIZE - 1, 0, -1):
            snakeList_b.append([snake_b_x + BLOCK_SIZE * i,
                                snake_b_y])
            snakeList_g.append([snake_g_x - BLOCK_SIZE * i,
                                snake_g_y])

    snakeList_b.append(snakeHead_b)
    snakeList_g.append(snakeHead_g)
    # First apple is centered, more or less
    # Nah
    apple_x, apple_y = new_apple(snakeList_b, snakeList_g)

    

    while not gameExit:
        # -----------------------------
        # GAME OVER
        # -----------------------------
        # Probably shoulda put it in a function like
        # everything the fuck else.
        while gameOver:
            msg_to_screen(gameDisplay,
                          "%s wins!" % winner,
                          fonts[2], RED2,
                          gameDisplay.get_rect().center)
            msg_to_screen(gameDisplay,
                          "Space to continue, ESC to quit.",
                          fonts[1], BLACK,
                          (RESOLUTION[0] / 2,
                           RESOLUTION[1] / 2 + 2 * fonts[2].get_linesize()))
            pygame.display.update()
            for event in pygame.event.get():
                if check_quit(event):
                    gameExit, gameOver = True, False
                    safe_exit()
                else:
                    if event.type == pygame.KEYUP and \
                       event.key == pygame.K_SPACE:
                        main_loop(gameDisplay, clock, snake_g,
                                  snake_b, apple, fonts)
            clock.tick(FPS)

        # -------------------------------
        # EVENT HANDLING
        # -------------------------------
        
        # Change once per loop, none of this glitchy shit
        G_CHANGE = False
        B_CHANGE = False
        for event in pygame.event.get():
            if check_quit(event):
                gameExit = True
                safe_exit()
            else:
                if G_CHANGE and B_CHANGE:
                    break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        pause(gameDisplay, fonts, clock)
                elif event.type == pygame.KEYDOWN:
                    # GREEN
                    if not G_CHANGE:
                        if event.key == pygame.K_a:
                            if snake_g_x_change == 0: snake_g_x_change = -BLOCK_SIZE
                            snake_g_y_change = 0
                            G_CHANGE = True
                        elif event.key == pygame.K_d:
                            if snake_g_x_change == 0: snake_g_x_change = BLOCK_SIZE
                            snake_g_y_change = 0
                            G_CHANGE = True
                        elif event.key == pygame.K_w:
                            if snake_g_y_change == 0: snake_g_y_change = -BLOCK_SIZE
                            snake_g_x_change = 0
                            G_CHANGE = True
                        elif event.key == pygame.K_s:
                            if snake_g_y_change == 0: snake_g_y_change = BLOCK_SIZE
                            snake_g_x_change = 0
                            G_CHANGE = True

                    # BLUE
                    if not B_CHANGE:
                        if event.key == pygame.K_LEFT:
                            if snake_b_x_change == 0: snake_b_x_change = -BLOCK_SIZE
                            snake_b_y_change = 0
                            B_CHANGE = True 
                        elif event.key == pygame.K_RIGHT:
                            if snake_b_x_change == 0: snake_b_x_change = BLOCK_SIZE
                            snake_b_y_change = 0
                            B_CHANGE = True
                        elif event.key == pygame.K_UP:
                            if snake_b_y_change == 0: snake_b_y_change = -BLOCK_SIZE
                            snake_b_x_change = 0
                            B_CHANGE = True
                        elif event.key == pygame.K_DOWN:
                            if snake_b_y_change == 0: snake_b_y_change = BLOCK_SIZE
                            snake_b_x_change = 0
                            B_CHANGE = True


        # -------------------
        # MOVEMENT
        # -------------------
        snake_g_x, snake_g_y = (snake_g_x + snake_g_x_change,
                                snake_g_y + snake_g_y_change)
        snake_b_x, snake_b_y = (snake_b_x + snake_b_x_change,
                                snake_b_y + snake_b_y_change)



        # ------------------------
        # Snakelist updating
        # ------------------------
        snakeList_b.append([snake_b_x, snake_b_y])
        snakeList_g.append([snake_g_x, snake_g_y])
        if len(snakeList_b) > score_b + START_SIZE:
            snakeList_b.remove(snakeList_b[0])
        if len(snakeList_g) > score_g + START_SIZE:
            snakeList_g.remove(snakeList_g[0])



        # --------------------
        # BOUNDARIES
        # --------------------
        if (snake_g_x >= RESOLUTION[0] or snake_g_x < 0 or \
            snake_g_y >= RESOLUTION[1] or snake_g_y < 0 or \
            ([snake_g_x, snake_g_y] in snakeList_g[:-1]) or \
            ([snake_g_x, snake_g_y] in snakeList_b)):
            gameOver = True
            winner = "Blue"
        if (snake_b_x >= RESOLUTION[0] or snake_b_x < 0 or \
            snake_b_y >= RESOLUTION[1] or snake_b_y < 0 or \
            ([snake_b_x, snake_b_y] in snakeList_b[:-1]) or \
            ([snake_b_x, snake_b_y] in snakeList_g)):
            gameOver = True
            if winner == "Blue":
                winner = "FUCKING NOBODY" # Draw
            else:
                winner = "Green"
                


        

        # -----------------------
        # APPLE EATING
        # -----------------------
        if snake_b_y == apple_y and snake_b_x == apple_x:
            apple_x, apple_y = new_apple(snakeList_g, snakeList_b)
            score_b += 1
        elif snake_g_y == apple_y and snake_g_x == apple_x:
            apple_x, apple_y = new_apple(snakeList_g, snakeList_b)
            score_g += 1

            
        # -----------------------
        # DRAWING
        # -----------------------
        gameDisplay.fill(WHITE)
        draw_apple(gameDisplay, apple, apple_x, apple_y)
        draw_snakes(gameDisplay, snakeList_g, snake_g_x_change,
                    snake_g_y_change, snakeList_b,
                    snake_b_x_change, snake_b_y_change)
        
        
        # -----------------------
        # SCREEN UPDATE
        # -----------------------
        pygame.display.update()
        clock.tick(FPS)

    safe_exit(0)




if __name__ == "__main__":
    gameDisplay, clock = basic_setup()
    snake_g, snake_b, apple = load_images()
    fonts = load_fonts()
    game_intro(gameDisplay, fonts, clock)
    main_loop(gameDisplay, clock, snake_g, snake_b, apple, fonts)

