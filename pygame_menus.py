import pygame
from pygame_grid import Grid  # Importation de la classe Grid

def startmenu():
    print("Welcome to pygame menu")
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
                if event.button == 1:  # Left mouse button
                    # Check if the rect collides with the mouse pos
                    if rect_play.collidepoint(event.pos):
                        running = False
                        diffmenu()  # Ouvrir le menu de difficulté
                    if rect_quit.collidepoint(event.pos):
                        running = False

def diffmenu():
    from pygame_grid import interface
    pygame.font.init()
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 400
    RED = (255, 0, 0)
    WHITE = (200, 200, 200)
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    my_font = pygame.font.SysFont('Arial', 50)

    while running:
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
                if event.button == 1:  # Left mouse button
                    # Vérifiez si le rectangle de difficulté est cliqué
                    if rect_facile.collidepoint(event.pos):
                        running = False
                        difficulty = "facile"
                        grid = Grid(9, 9, 10, difficulty)
                        grid.generate_grid()
                        interface(9, 9, grid.get_grid(), grid)  # Passez grid à l'interface

                    if rect_moyen.collidepoint(event.pos):
                        running = False
                        difficulty = "moyen"
                        grid = Grid(16, 16, 40, difficulty)
                        grid.generate_grid()
                        interface(16, 16, grid.get_grid(), grid)

                    if rect_diff.collidepoint(event.pos):
                        running = False
                        difficulty = "difficile"
                        grid = Grid(30, 16, 99, difficulty)
                        grid.generate_grid()
                        interface(30, 16, grid.get_grid(), grid)
startmenu()
