import sys, random, math, time

try:
    from res import config
    from res.config import *
    import pygame
    from pygame.locals import *
    from res.classes import *
    from res.initialize import *
except ImportError:
    print "You need the config, initialize and classes modules to continue!"
    

def game_intro(gameDisplay, fonts, clock, images, audio):
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
                  "WASD for Green (P1), Arrow Keys for Blue (P2).",
                  fonts[1], BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + 3 * fonts[1].get_linesize()))
    msg_to_screen(gameDisplay,
                  "1 or 2 to start with that number of humans.",
                  fonts[1], BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + 4 * fonts[1].get_linesize()))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if check_quit(event):
                safe_exit()
            else:
##                if event.type == pygame.KEYUP and \
##                   event.key == pygame.K_SPACE:
##                    intro = False
                if event.type == pygame.KEYUP and \
                   event.key == pygame.K_1:
                    main_loop(1, gameDisplay, clock, fonts, images, audio)
                if event.type == pygame.KEYUP and \
                   event.key == pygame.K_2:
                    main_loop(2, gameDisplay, clock, fonts, images, audio)

                # Easter egg - computer plays with itself.
                if event.type == pygame.KEYUP and \
                   event.key == pygame.K_3:
                    intro = False
                    main_loop(gameDisplay, clock, fonts, images, audio)
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
                   event.key == pygame.K_p:
                    paused = False
        clock.tick(FPS)
    return


def game_over(gameDisplay, winner, fonts, clock):
    gameOver = False
    win_msg = "%s wins!" % winner
    msg_to_screen(gameDisplay, win_msg, fonts[2],
                  RED2, gameDisplay.get_rect().center)
    msg_to_screen(gameDisplay, "1 or 2 to continue, ESC to quit.",
                  fonts[1], BLACK,
                  (RESOLUTION[0] / 2, RESOLUTION[1] / 2 + 2 * fonts[2].get_linesize()))
    pygame.display.update()
    
    while not gameOver:
        for event in pygame.event.get():
            if check_quit(event):
                safe_exit()
            else:
                if event.type == pygame.KEYUP:
                    if event.key == K_1:
                        gameOver = True
                        main_loop(1, gameDisplay, clock, fonts, images, audio)
                    elif event.key == K_2:
                        gameOver = True
                        main_loop(2, gameDisplay, clock, fonts, images, audio)
                    elif event.key == K_0:
                        gameOver = True
                        main_loop(0, gameDisplay, clock, fonts, images, audio)

        clock.tick(FPS)
    return
            
    
def main_loop(num_humans, gameDisplay, clock, fonts, images, audio):
    gameExit = False
    gameOver = False
    paused   = False
    winner   = "No one"

    snake_g = Snake("Greenie", images[IMG_SN1], 0, 0,
                    Snake.EAST, GREEN, Snake.HUMAN)
    snake_b = Snake("Blueface", images[IMG_SN2],
                    RESOLUTION[0] - BLOCK_SIZE,
                    RESOLUTION[1] - BLOCK_SIZE,
                    Snake.WEST, BLUE,
                    buttons=Snake.DEFAULT_2)
    snakes = [snake_g, snake_b]
    for snake in snakes[num_humans:]:
        snake.control = AI_LEVEL
        snake.buttons = Snake.DEFAULT
    apples = [Apple(images[IMG_APL])]
    for apple in apples:
        apple.new_apple(snakes)
        

    while not gameExit:
        # -----------------------------
        # GAME OVER
        # -----------------------------
        while gameOver:
            game_over(gameDisplay, winner, fonts, clock)
            
        # -----------------------------
        # PAUSE
        # -----------------------------
        while paused:
            pause(gameDisplay, fonts, clock)

            
        # -------------------------------
        # EVENT HANDLING
        # -------------------------------
        
##        # Change once per loop, none of this glitchy shit
##        G_CHANGE = False
##        B_CHANGE = False
        direction_changes = [False]*len(snakes)
        for event in pygame.event.get():
            if check_quit(event):
                gameExit = True
                safe_exit()
            else:
                if direction_changes == [True]*len(snakes):
                    print "boop"
                    break
##                if G_CHANGE and B_CHANGE:
##                    break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        pause(gameDisplay, fonts, clock)
                elif event.type == pygame.KEYDOWN:
                    for snake in snakes:
                        if not direction_changes[snakes.index(snake)]:
                            if snake.process_command(event):
                                direction_changes[snakes.index(snake)] = True
                                break



        high_score = -1
        for snake in snakes:
            
            # Why am I even doing it this way, I
            # don't plan on having 3+ snakes...
            snakes_minus = snakes[:]
            snakes_minus.remove(snake)
            
            # ----------------------
            # AI PROCESSING
            # ----------------------
            if snake.control != Snake.HUMAN:
                snake.process_command(snake.determine_move(snakes_minus, apples))
            
        
            # ---------------------
            # MOVEMENT
            # ---------------------
            snake.update_position()
            
            # ---------------------
            # APPLE EATING
            # ---------------------
            for apple in apples:
                if snake.eats_apple(apple):
                    snake.increase_size()
                    snake.increase_score()
                    apple.new_apple(snakes)
            
            # ---------------------
            # COLLISION
            # ---------------------
            for snake_other in snakes_minus:
                if snake.will_collide(snake_other):
                    snake.set_score(-1)
                    gameOver = True
                    
            # ---------------------
            # WINNER UPDATE
            # ---------------------
            if snake.score > high_score:
                high_score = snake.score
                winner = snake
            elif snake.score == high_score:
                winner = "No one"


        # -----------------------
        # DRAWING
        # -----------------------
        gameDisplay.fill(WHITE)
        for snake in snakes:
            snake.draw(gameDisplay)
        for apple in apples:
            apple.draw(gameDisplay)
        
        # -----------------------
        # SCREEN UPDATE
        # -----------------------
        pygame.display.update()
        clock.tick(FPS)

    safe_exit(0)



if __name__ == "__main__":
##    gameDisplay, clock = basic_setup()
##    snake_g, snake_b, apple = load_images()
##    fonts = load_fonts()
##    game_intro(gameDisplay, fonts, clock)
##    main_loop(gameDisplay, clock, snake_g, snake_b, apple, fonts)
    
    gameDisplay, clock, images, fonts, audio = init()
    game_intro(gameDisplay, fonts, clock, images, audio)














    
