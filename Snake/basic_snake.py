import pygame, sys, random, math, time
from pygame.locals import *

# Real simple, no imported config or whatever

RESOLUTION = (800, 600)
CAPTION = "Snake? Snake! SNAAAAAKE!"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 20, 21)
RED2 = (155, 50, 50)
GREEN = (20, 200, 50)
FPS = 7
BLOCK_SIZE = 40
START_SIZE = 3

pygame.init()
gameDisplay = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
defaultFont = pygame.font.SysFont("umeuigothic", 32, bold=True)
tinyFont = pygame.font.SysFont("umeuigothic", 20)
largeFont = pygame.font.SysFont("umeuigothic", 64)
snakeFace = pygame.image.load('snakehead.png')
snakeFaceResized = pygame.transform.scale(snakeFace,
                                          (BLOCK_SIZE,
                                           BLOCK_SIZE))
apple = pygame.image.load('apple.png')
appleResized = pygame.transform.scale(apple,
                                      (BLOCK_SIZE,
                                       BLOCK_SIZE))
pygame.display.set_icon(apple)


def game_intro():
    intro = True
    gameDisplay.fill(WHITE)
    msg_to_screen("SNAAAAAAAAAKE?!",
                  largeFont, GREEN,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 - largeFont.get_linesize()))
    msg_to_screen("Press any non-ludicrous button to start...",
                  defaultFont, BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + defaultFont.get_linesize()))
    pygame.display.update()
    # I should probably do this better; the logic is a carbon copy of
    # the game over screen.
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    sys.exit(0)
                else:
                    intro = False
                    return


        clock.tick(FPS)


def pause():
    paused = True
    msg_to_screen("Paused...",
                  largeFont, RED2,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 - largeFont.get_linesize()))
    msg_to_screen("Press P to continue or Q to quit...",
                  defaultFont, BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + defaultFont.get_linesize()))
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE or \
                   event.key == pygame.K_q:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    paused = False
                    return
        clock.tick(FPS)
                
    


def draw_score(score):
    msg_to_screen("SCORE: %s" % score,
                  tinyFont, BLACK,
                  tinyFont.size("SCORE"))

    
def draw_snake(snakeList, lead_x_change, lead_y_change):
    # pygame.draw.rect(gameDisplay, BLACK, (400, 300, 10, 10))
    # Can be graphics accelerated, so use fill.

    increment = 255 / len(snakeList)

    for x,y in snakeList[:-1]:
##        increment = 128 / len(snakeList)
##        alpha = (snakeList.index([x,y]) + 1) * increment
        # fug alpha, just white-gradient it
        curr_incr = increment * (len(snakeList) - (snakeList.index([x,y]) + 1))
        col = tuple(min(255, sum(pair)) for pair in zip(GREEN, (curr_incr, 0, curr_incr)))
        gameDisplay.fill(col, (x, y, BLOCK_SIZE, BLOCK_SIZE))
    
    if lead_x_change > 0:
        snakeFace = pygame.transform.rotate(snakeFaceResized, 270)
    elif lead_x_change < 0:
        snakeFace = pygame.transform.rotate(snakeFaceResized, 90)
    elif lead_y_change > 0:
        snakeFace = pygame.transform.rotate(snakeFaceResized, 180)
    else:
        snakeFace = snakeFaceResized
    gameDisplay.blit(snakeFace, snakeList[-1])


def draw_apple(apple_x, apple_y):
    # gameDisplay.fill(RED, (apple_x, apple_y, BLOCK_SIZE, BLOCK_SIZE))
    gameDisplay.blit(appleResized, (apple_x, apple_y))

def new_apple(snakeList):
    apple_x, apple_y = snakeList[-1]    
    while [apple_x, apple_y] in snakeList:
        apple_x, apple_y = (BLOCK_SIZE * random.randrange(0, RESOLUTION[0] / BLOCK_SIZE - 1),
                            BLOCK_SIZE * random.randrange(0, RESOLUTION[1] / BLOCK_SIZE - 1))

    return apple_x, apple_y


def msg_to_screen(msg, font, color, location, antialias=True):
    text_surface    = font.render(msg, antialias, color)
    text_rect       = text_surface.get_rect() 

    text_rect.center = location
    gameDisplay.blit(text_surface, text_rect)
    
    return

    
def main_loop():
    gameExit = False
    lead_x, lead_y = (BLOCK_SIZE * (RESOLUTION[0] / (BLOCK_SIZE * 2)),
                      BLOCK_SIZE * (RESOLUTION[1] / (BLOCK_SIZE * 2)))
    lead_x_change, lead_y_change = (BLOCK_SIZE, 0) # Start off moving right
    gameOver = False
    score = 0
    snakeHead = [lead_x, lead_y]
    snakeList = []

    for i in range(START_SIZE):
        snakeList.append([lead_x - (i * BLOCK_SIZE), lead_y])

    # TODO: Does not check for snake position yet
    apple_x, apple_y = new_apple(snakeList)
    
    while not gameExit:
        while gameOver:
            # Eh, wanna see the snake when you lose.
            # gameDisplay.fill(WHITE)
            msg_to_screen("Game Over, Asshole!",
                          largeFont, RED2,
                          (RESOLUTION[0] / 2,
                           RESOLUTION[1] / 2 - largeFont.get_linesize()))
            msg_to_screen("Press Q to quit or C to continue...",
                          defaultFont, BLACK,
                          (RESOLUTION[0] / 2,
                           RESOLUTION[1] / 2 + defaultFont.get_linesize()))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False # To drop the loop
                if event.type == pygame.KEYUP:
                    if event.key == K_ESCAPE:
                        gameOver = False
                        gameExit = True
                    elif event.key == K_c:
                        main_loop()
                    elif event.key == K_q:
                        gameOver = False
                        gameExit = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYUP:
                if event.key == K_ESCAPE:
                    gameExit = True
                elif event.key == K_p:
                    pause()
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    # lead_x_change = 0
                    pass # Want it to keep moving, 'cause snake
                elif event.key == K_UP or event.key == K_DOWN:
                    # lead_y_change = 0
                    pass
            elif event.type == pygame.KEYDOWN:
                # After each key, we wanna break from the loop
                # So it doesn't go do 2 things before
                # acting on the button press.
                if event.key == K_LEFT:
                    if lead_x_change == 0: lead_x_change = -BLOCK_SIZE # Don't allow returns in same dir
                    lead_y_change = 0 # Fuck diagonals >=o
                    break
                elif event.key == K_RIGHT:
                    if lead_x_change == 0: lead_x_change = BLOCK_SIZE
                    lead_y_change = 0
                    break
                elif event.key == K_UP:
                    if lead_y_change == 0: lead_y_change = -BLOCK_SIZE
                    lead_x_change = 0
                    break
                elif event.key == K_DOWN:
                    if lead_y_change == 0: lead_y_change = BLOCK_SIZE
                    lead_x_change = 0
                    break

        lead_x, lead_y = (lead_x + lead_x_change,
                          lead_y + lead_y_change)

        # Boundaries:   no wrap around
        #               no self-crashing
        if (lead_x >= RESOLUTION[0] or lead_x < 0 or \
           lead_y >= RESOLUTION[1] or lead_y < 0) or \
           ([lead_x, lead_y] in snakeList[1:]):

            gameOver = True

            


        snakeList.append([lead_x, lead_y])
        if len(snakeList) > (score + START_SIZE):
            snakeList.remove(snakeList[0])
        gameDisplay.fill(WHITE)
        draw_apple(apple_x, apple_y)
        draw_snake(snakeList, lead_x_change, lead_y_change)
        draw_score(score)

        # Apple eatin'
        if lead_x == apple_x and lead_y == apple_y:
            apple_x, apple_y = new_apple(snakeList)
            score += 1
            msg_to_screen("Om nom nom", tinyFont, BLACK,
                          (lead_x, lead_y))

        # Apple eatin' for apples not quite the same size
##        if (lead_x >= apple_x and lead_x <= apple_x + BLOCK_SIZE) \
##           and \
##           (lead_y >= apple_y and lead_y <= apple_y + BLOCK_SIZE):
##            apple_x, apple_y = new_apple(snakeList)
##            score += 1
##            

        pygame.display.update()
        clock.tick(FPS)


    pygame.display.quit()
    sys.exit(0)


if __name__ == "__main__":
    game_intro()
    main_loop()
