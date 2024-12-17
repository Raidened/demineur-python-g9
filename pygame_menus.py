import pygame
from Grid_Generator import Grid  # Importation de la classe Grid

def startmenu():
    pygame.font.init()
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 400
    RED = (255, 0, 0)
    WHITE = (200, 200, 200)
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    my_font = pygame.font.SysFont('Arial', 50)
    text_jouer = my_font.render('JOUER', False, WHITE)

    while running:
        pygame.init()
        rect_play = pygame.Rect(100, 100, 200, 100)
        pygame.draw.rect(screen, WHITE, rect_play, 2)
        rect_quit = pygame.Rect(125, 225, 150, 70)
        pygame.draw.rect(screen, RED, rect_quit, 2)
        pygame.display.flip()
        screen.blit(text_jouer, (130, 120))
        my_font = pygame.font.SysFont('Arial', 30)
        text_quit = my_font.render('QUITTER', False, RED)
        screen.blit(text_quit, (145, 240))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button.
                    # Check if the rect collides with the mouse pos.
                    if rect_play.collidepoint(event.pos):
                        running = False
                        diffmenu()
                    if rect_quit.collidepoint(event.pos):
                        running = False

def diffmenu():
    from pygame_grid import interface
    pygame.init()
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 400
    RED = (255, 0, 0)
    WHITE = (200, 200, 200)
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    my_font = pygame.font.SysFont('Arial', 50)

    while running:
        pygame.init()
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
                if event.button == 1:  # Left mouse button.
                    # Check if the rect collides with the mouse pos.
                    if rect_facile.collidepoint(event.pos):
                        running = False
                        difficulty = "facile"  # Vous pouvez utiliser un nom pour la difficulté
                        grid = Grid(9, 9, 10, difficulty)  # Passer 'difficulty'
                        grid.generate_grid()  # Appeler la méthode de génération de la grille
                        interface(9, 9, grid.get_grid())  # Passer la grille à l'interface

                    if rect_moyen.collidepoint(event.pos):
                        running = False
                        difficulty = "moyen"  # Par exemple
                        grid = Grid(16, 16, 40, difficulty)  # Passer 'difficulty'
                        grid.generate_grid()
                        interface(16, 16, grid.get_grid())

                    if rect_diff.collidepoint(event.pos):
                        running = False
                        difficulty = "difficile"  # Par exemple
                        grid = Grid(30, 16, 99, difficulty)  # Passer 'difficulty'
                        grid.generate_grid()
                        interface(30, 16, grid.get_grid())

startmenu()
