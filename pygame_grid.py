import pygame
import random


def drawgrid(screen,WINDOW_WIDTH,WINDOW_HEIGHT,table,difficulty):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (200, 200, 200)
    blocksize = 30
    if difficulty == "difficile":
        blocksize = 30
    for x in range(0, WINDOW_HEIGHT, blocksize):
        for y in range(0, WINDOW_WIDTH, blocksize):
            rect = pygame.Rect(y, x, blocksize, blocksize)
            if table[(x)//30][(y)//30]=="M":
                pygame.draw.rect(screen, RED, rect, 0)
                pygame.draw.rect(screen, BLACK, rect, 2)
            else :
                pygame.draw.rect(screen, WHITE, rect, 0)
                pygame.draw.rect(screen, BLACK, rect, 2)


def interface(nbcoln,nbline,tabal,diff):
    WINDOW_HEIGHT = nbline*30
    WINDOW_WIDTH = nbcoln*30
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    while running:
        pygame.init()
        drawgrid(screen,WINDOW_WIDTH,WINDOW_HEIGHT,tabal,diff)
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False




