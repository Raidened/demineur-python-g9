import json
import os

import pygame
from pygame_grid import Grid,  Game, interface  # Importation de la classe Grid

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
        screen.fill((30,20,50))
        rect_play = pygame.Rect(WINDOW_WIDTH/4, WINDOW_HEIGHT//4, WINDOW_WIDTH//2, WINDOW_WIDTH//4)
        pygame.draw.rect(screen, WHITE, rect_play, 2)
        rect_quit = pygame.Rect(10, 320, 90, 70)
        pygame.draw.rect(screen, RED, rect_quit, 2)
        rect_load = pygame.Rect(25, 225, 150, 70)
        pygame.draw.rect(screen, WHITE, rect_load, 2)
        rect_hoff = pygame.Rect(210, 245, 150, 40)
        pygame.draw.rect(screen, WHITE, rect_hoff, 2)
        rect_hofm = pygame.Rect(210, 295, 150, 40)
        pygame.draw.rect(screen, WHITE, rect_hofm, 2)
        rect_hofd = pygame.Rect(210, 345, 150, 40)
        pygame.draw.rect(screen, WHITE, rect_hofd, 2)
        screen.blit(text_jouer, (WINDOW_WIDTH/3.1, WINDOW_HEIGHT/3.3))
        text_load = my_font.render('LOAD', False, WHITE)
        screen.blit(text_load, (65, 240))
        text_hof = my_font.render('HALL OF FAME', False, WHITE)
        screen.blit(text_hof, (200, 210))
        text_hoff = my_font.render('FACILE', False, WHITE)
        screen.blit(text_hoff, (240, 245))
        text_hoff = my_font.render('MOYEN', False, WHITE)
        screen.blit(text_hoff, (240, 295))
        text_hoff = my_font.render('DIFFICILE', False, WHITE)
        screen.blit(text_hoff, (225, 345))
        my_font = pygame.font.SysFont('Arial', 30)
        text_quit = my_font.render('QUIT', False, RED)
        screen.blit(text_quit, (25, 335))

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
                    if rect_load.collidepoint(event.pos):
                        running = False
                        view_game_menu()
                    if rect_hoff.collidepoint(event.pos):
                        running = False
                        hall_of_fame('facile')
                    if rect_hofm.collidepoint(event.pos):
                        running = False
                        hall_of_fame('moyen')
                    if rect_hofd.collidepoint(event.pos):
                        running = False
                        hall_of_fame('difficile')
        pygame.display.flip()

def diffmenu():
    pygame.font.init()
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 400
    RED = (255, 0, 0)
    WHITE = (200, 200, 200)
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    my_font = pygame.font.SysFont('Arial', 50)

    while running:
        screen.fill((60, 40, 100))
        text_facile = my_font.render('FACILE', False, WHITE)
        rect_facile = pygame.Rect(100, 50, 200, 75)
        pygame.draw.rect(screen, WHITE, rect_facile, 2)
        screen.blit(text_facile, (155, 70))

        text_moyen = my_font.render('MOYEN', False, WHITE)
        rect_moyen = pygame.Rect(100, 150, 200, 75)
        pygame.draw.rect(screen, WHITE, rect_moyen, 2)
        screen.blit(text_moyen, (155, 170))

        text_diff = my_font.render('DIFFICILE', False, WHITE)
        rect_diff = pygame.Rect(100, 250, 200, 75)
        pygame.draw.rect(screen, WHITE, rect_diff, 2)
        screen.blit(text_diff, (145, 270))

        my_font = pygame.font.SysFont('Arial', 30)
        text_back = my_font.render('BACK', False, RED)
        rect_back = pygame.Rect(10, 10, 80, 40)
        pygame.draw.rect(screen, RED, rect_back, 2)
        screen.blit(text_back, (15, 13))

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
                        grid.player_name = get_player_name(screen)
                        interface(9, 9, grid.grid, grid, True)  # Passez grid à l'interface

                    if rect_moyen.collidepoint(event.pos):
                        running = False
                        difficulty = "moyen"
                        grid = Grid(16, 16, 40, difficulty)
                        grid.generate_grid()
                        grid.player_name = get_player_name(screen)
                        interface(16, 16, grid.grid, grid,True)

                    if rect_diff.collidepoint(event.pos):
                        running = False
                        difficulty = "difficile"
                        grid = Grid(30, 16, 99, difficulty)
                        grid.generate_grid()
                        grid.player_name = get_player_name(screen)
                        interface(30, 16, grid.grid, grid,True)

                    if rect_back.collidepoint(event.pos):
                        running = False
                        startmenu()


def get_player_name(screen):
    """Prompt the player to enter their nickname."""
    player_name = ""
    input_active = True
    while input_active:
        screen.fill((120, 80, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        font = pygame.font.SysFont('Arial', 30)
        prompt = font.render("Enter your nickname:", True, (255,255,255))
        name_display = font.render(player_name, True, (255,255,255))
        screen.blit(prompt, (50, 150))
        screen.blit(name_display, (50, 200))
        pygame.display.flip()
    return player_name




def view_game_menu():
    screen = pygame.display.set_mode((600, 400))
    game_instance = Game()
    pygame.font.init()
    my_font = pygame.font.SysFont('Arial', 30)
    running = True
    # Retrieve list of saved games
    saved_games = [f for f in os.listdir('saved_grid') if f.startswith('grid') and f.endswith('.json')]
    while running:
        screen.fill((60,40,100))
        title = my_font.render('Select a Game to View', True, (255,255,255))
        screen.blit(title, (100, 50))
        # Display saved games as buttons
        buttons = []
        for index, game in enumerate(saved_games):
            rect = pygame.Rect(10, 110 + index * 50, 580, 40)  # Made wider to fit more text
            pygame.draw.rect(screen, (255,255,255), rect, 2)

            # Load game data to display more info
            try:
                with open(os.path.join('saved_grid', game), 'r') as file:
                    data = json.load(file)
                    display_text = f"{data.get('name', 'Unknown')} - {data.get('difficulty', '?')} - {data.get('date', '?')}"
            except:
                display_text = game

            text = my_font.render(display_text, True, (255,255,255))
            screen.blit(text, (20, 110 + index * 50))
            buttons.append((rect, game))
        my_font = pygame.font.SysFont('Arial', 30)
        text_back = my_font.render('BACK', False, (255, 0, 0))
        rect_back = pygame.Rect(10, 10, 80, 40)
        pygame.draw.rect(screen, (255, 0, 0), rect_back, 2)
        screen.blit(text_back, (15, 13))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect_back.collidepoint(event.pos):
                        running = False
                        startmenu()
                    for rect, game in buttons:
                        if rect.collidepoint(event.pos):
                            loadgrid = game_instance.load_grid(folder="saved_grid", filename=game)
                            rows, cols, mines, difficulty, grid, revealed, firstclick = loadgrid
                            print(rows, cols, difficulty, grid, mines, revealed, firstclick)
                            newgrid = Grid(rows, cols, mines, difficulty)
                            newgrid.grid = grid
                            newgrid.revealed = revealed
                            running = False
                            interface(rows, cols, newgrid.grid, newgrid, False)  # Pass the selected game file
                            break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def hall_of_fame(diff):
    screen = pygame.display.set_mode((600, 400))
    game_instance = Game()
    pygame.font.init()
    my_font = pygame.font.SysFont('Arial', 30)
    running = True
    # Retrieve list of saved games
    saved_games = [f for f in os.listdir('hof/'+diff) if f.startswith('grid') and f.endswith('.json')]

    while running:
        screen.fill((60,40,100))
        title = my_font.render('Select a Game to View', True, (255,255,255))
        screen.blit(title, (100, 50))
        # Display saved games as buttons
        buttons = []
        for index, game in enumerate(saved_games):
            rect = pygame.Rect(10, 110 + index * 50, 580, 40)  # Made wider to fit more text
            pygame.draw.rect(screen, (255,255,255), rect, 2)

            # Load game data to display more info
            try:
                with open(os.path.join('hof/'+diff, game), 'r') as file:
                    data = json.load(file)
                    display_text = f"{data.get('name', 'Unknown')} - {data.get('score', 'NO SCORE')} - {data.get('date', '?')}"
            except:
                display_text = game
            text = my_font.render(display_text, True, (255,255,255))
            screen.blit(text, (20, 110 + index * 50))
            buttons.append((rect, game))
        my_font = pygame.font.SysFont('Arial', 30)
        text_back = my_font.render('BACK', False, (255, 0, 0))
        rect_back = pygame.Rect(10, 10, 80, 40)
        pygame.draw.rect(screen, (255, 0, 0), rect_back, 2)
        screen.blit(text_back, (15, 13))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect_back.collidepoint(event.pos):
                        running = False
                        startmenu()
                    for rect, game in buttons:
                        if rect.collidepoint(event.pos):
                            loadgrid = game_instance.load_grid(folder='hof/'+diff, filename=game)
                            rows, cols, mines, difficulty, grid, revealed, firstclick = loadgrid
                            print(rows, cols, difficulty, grid, mines, revealed, firstclick)
                            newgrid = Grid(rows, cols, mines, difficulty)
                            newgrid.grid = grid
                            newgrid.revealed = revealed
                            running = False
                            interface(cols, rows, newgrid.grid, newgrid, False)  # Pass the selected game file
                            break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
startmenu()