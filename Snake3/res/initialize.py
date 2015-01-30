#! /usr/bin/env python

# Handle basics - actually load images and sounds.
# Hold all the trivial pygame setup stuff
# Additionally, contains the basic methods like safe_exit


# --------------
# TODO:
#   - Audio
# --------------

try:
    from config import *
    import pygame
    from pygame.locals import *
    import sys
except ImportError:
    print "You need the config file and pygame to run this."
    sys.exit(0)


# -----------------------------
# Images and their identifiers
# -----------------------------
IMG_APL = 0
IMG_SN1 = 1
IMG_SN2 = 2

# load audio
def load_audio():
    pass


# load images
def load_images():
    snake_1 = pygame.transform.scale(pygame.image.load(P1),
                                     (BLOCK_SIZE, BLOCK_SIZE))
    snake_2 = pygame.transform.scale(pygame.image.load(P2),
                                     (BLOCK_SIZE, BLOCK_SIZE))
    apple   = pygame.transform.scale(pygame.image.load(APPLE),
                                     (BLOCK_SIZE, BLOCK_SIZE))
    return apple, snake_1, snake_2


# load fonts
def load_fonts():
    font_1 = pygame.font.SysFont(FONT_S[0], FONT_S[1],
                                 FONT_S[2])
    font_2 = pygame.font.SysFont(FONT_M[0], FONT_M[1],
                                 FONT_M[2])
    font_3 = pygame.font.SysFont(FONT_L[0], FONT_L[1],
                                 FONT_L[2])
    return font_1, font_2, font_3

# initialize
def init():
    ''' Initialize pygame.
        Return the display, clock, images, fonts and audio.
    '''
    pygame.init()
    gameDisplay = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(CAPTION)
    clock   = pygame.time.Clock()
    images  = load_images()
    icon    = pygame.transform.scale(images[IMG_APL], (32, 32))
    pygame.display.set_icon(icon)
    fonts   = load_fonts()
    audio   = load_audio()
    return gameDisplay, clock, images, fonts, audio


def msg_to_screen(display, msg, font, color, location, antialias=True):
    text_surface     = font.render(msg, antialias, color)
    text_rect        = text_surface.get_rect()
    text_rect.center = location
    display.blit(text_surface, text_rect)
    return


def safe_exit():
    pygame.display.quit()
    sys.exit(0)


def check_quit(event):
    if (event.type == pygame.QUIT) or \
       ((event.type == pygame.KEYUP) and (event.key == K_ESCAPE)):
        return True
    return False
