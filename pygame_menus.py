import pygame
from pygame_grid import Grid, show_scores, hall_of_fame, Game, interface
import json

def startmenu():
    pygame.font.init()
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    RED = (255, 0, 0)
    WHITE = (200, 200, 200)
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    my_font = pygame.font.SysFont('Arial', 50)
    text_jouer = my_font.render('JOUER', False, WHITE)
    text_hall_of_fame = my_font.render('HALL OF FAME', False, WHITE)

    while running:
        screen.fill((0, 0, 0))
        rect_play = pygame.Rect(100, 100, 200, 100)
        pygame.draw.rect(screen, WHITE, rect_play, 2)
        rect_hall_of_fame = pygame.Rect(100, 250, 200, 100)
        pygame.draw.rect(screen, WHITE, rect_hall_of_fame, 2)
        rect_quit = pygame.Rect(125, 375, 150, 70)
        pygame.draw.rect(screen, RED, rect_quit, 2)
        
        screen.blit(text_jouer, (130, 120))
        screen.blit(text_hall_of_fame, (80, 270))
        my_font = pygame.font.SysFont('Arial', 30)
        text_quit = my_font.render('QUITTER', False, RED)
        screen.blit(text_quit, (145, 390))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if rect_play.collidepoint(event.pos):
                        running = False
                        diffmenu(screen)
                    if rect_hall_of_fame.collidepoint(event.pos):
                        hall_of_fame(screen)
                    if rect_quit.collidepoint(event.pos):
                        running = False

def diffmenu(screen):
    pygame.font.init()
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 400
    RED = (255, 0, 0)
    WHITE = (200, 200, 200)
    running = True
    my_font = pygame.font.SysFont('Arial', 50)

    while running:
        screen.fill((0, 0, 0))
        text_facile = my_font.render('FACILE', False, WHITE)
        rect_facile = pygame.Rect(100, 50, 200, 75)
        pygame.draw.rect(screen, WHITE, rect_facile, 2)
        screen.blit(text_facile, (130, 60))

        text_moyen = my_font.render('MOYEN', False, WHITE)
        rect_moyen = pygame.Rect(100, 150, 200, 75)
        pygame.draw.rect(screen, WHITE, rect_moyen, 2)
        screen.blit(text_moyen, (125, 160))

        text_diff = my_font.render('DIFFICILE', False, WHITE)
        rect_diff = pygame.Rect(100, 250, 200, 75)
        pygame.draw.rect(screen, WHITE, rect_diff, 2)
        screen.blit(text_diff, (103, 260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect_facile.collidepoint(event.pos):
                        running = False
                        game = Game()
                        game.difficulty = "facile"
                        game.rows, game.cols, game.mines = 9, 9, 10
                        show_scores(screen, game.difficulty)
                        game.start_game(screen)

                    elif rect_moyen.collidepoint(event.pos):
                        running = False
                        game = Game()
                        game.difficulty = "moyen"
                        game.rows, game.cols, game.mines = 16, 16, 40
                        show_scores(screen, game.difficulty)
                        game.start_game(screen)

                    elif rect_diff.collidepoint(event.pos):
                        running = False
                        game = Game()
                        game.difficulty = "difficile"
                        game.rows, game.cols, game.mines = 16, 30, 99  # Corrected dimensions
                        show_scores(screen, game.difficulty)
                        game.start_game(screen)

startmenu()
