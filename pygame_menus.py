import pygame
from pygame_grid import Grid, show_scores, hall_of_fame, Game, interface, DisplayGrid
import json
import os

# Define color constants globally
WHITE = (200, 200, 200)
RED = (255, 0, 0)

def startmenu():
    pygame.font.init()
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)  # Added RESIZABLE flag
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

        # Add "VIEW GAME" button
        text_view_game = my_font.render('VIEW GAME', False, WHITE)
        rect_view_game = pygame.Rect(100, 350, 200, 75)
        pygame.draw.rect(screen, WHITE, rect_view_game, 2)
        screen.blit(text_view_game, (120, 360))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Update the screen with the new size
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
                # Optionally, reposition buttons based on new size
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if rect_play.collidepoint(event.pos):
                        running = False
                        diffmenu(screen)
                    if rect_hall_of_fame.collidepoint(event.pos):
                        hall_of_fame(screen)
                    if rect_quit.collidepoint(event.pos):
                        running = False
                    if rect_view_game.collidepoint(event.pos):
                        running = False
                        view_game_menu(screen)

def diffmenu(screen):
    pygame.font.init()
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 400
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
            elif event.type == pygame.VIDEORESIZE:
                # Update the screen with the new size
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
                # Optionally, reposition buttons based on new size
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect_facile.collidepoint(event.pos):
                        running = False
                        game = Game()
                        game.difficulty = "facile"
                        game.rows, game.cols, game.mines = 9, 9, 10
                        game.player_name = get_player_name(screen)  # Prompt for nickname
                        # show_scores(screen, game.difficulty)
                        game.start_game(screen)

                    elif rect_moyen.collidepoint(event.pos):
                        running = False
                        game = Game()
                        game.difficulty = "moyen"
                        game.rows, game.cols, game.mines = 16, 16, 40
                        game.player_name = get_player_name(screen)  # Prompt for nickname
                        # show_scores(screen, game.difficulty)
                        game.start_game(screen)

                    elif rect_diff.collidepoint(event.pos):
                        running = False
                        difficulty = "difficile"
                        grid = Grid(30, 16, 99, difficulty)
                        grid.generate_grid()
                        interface(30, 16, grid.get_grid(), grid)
                        game = Game()
                        game.difficulty = "difficile"
                        game.rows, game.cols, game.mines = 16, 30, 99  # Corrected dimensions
                        game.player_name = get_player_name(screen)  # Prompt for nickname
                        # show_scores(screen, game.difficulty)
                        game.start_game(screen)

def get_player_name(screen):
    """Prompt the player to enter their nickname."""
    player_name = ""
    input_active = True
    while input_active:
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
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Arial', 30)
        prompt = font.render("Enter your nickname:", True, WHITE)
        name_display = font.render(player_name, True, WHITE)
        screen.blit(prompt, (50, 150))
        screen.blit(name_display, (50, 200))
        pygame.display.flip()
    return player_name

# Add the new view_game_menu function
def view_game_menu(screen):
    pygame.font.init()
    my_font = pygame.font.SysFont('Arial', 30)
    running = True

    # Retrieve list of saved games
    saved_games = [f for f in os.listdir('saved_grid') if f.startswith('grid') and f.endswith('.json')]

    while running:
        screen.fill((0, 0, 0))
        title = my_font.render('Select a Game to View', True, WHITE)
        screen.blit(title, (100, 50))

        # Display saved games as buttons
        buttons = []
        for index, game in enumerate(saved_games):
            rect = pygame.Rect(100, 100 + index * 50, 400, 40)  # Made wider to fit more text
            pygame.draw.rect(screen, WHITE, rect, 2)

            # Load game data to display more info
            try:
                with open(os.path.join('saved_grid', game), 'r') as file:
                    data = json.load(file)
                    display_text = f"{data.get('player_name', 'Unknown')} - {data.get('difficulty', '?')} - {data.get('date', '?')}"
            except:
                display_text = game

            text = my_font.render(display_text, True, WHITE)
            screen.blit(text, (110, 110 + index * 50))
            buttons.append((rect, game))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for rect, game in buttons:
                        if rect.collidepoint(event.pos):
                            running = False
                            load_and_display_game(screen, game)  # Pass the selected game file
                            break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

# Modify load_and_display_game to handle the additional game parameters
def load_and_display_game(screen, game_file):
    game_instance = Game()
    loaded_data = game_instance.load_grid(folder="saved_grid", filename=game_file)
    if loaded_data:
        loaded_grid, rows, cols, mines, difficulty, revealed, first_click = loaded_data
        game_instance.rows = rows
        game_instance.cols = cols
        game_instance.mines = mines
        game_instance.difficulty = difficulty
        game_instance.first_click_pos = first_click  # Store the first click position
        game_instance.grid = Grid(rows, cols, mines, difficulty)

        # If we have a first click position, use it to generate the grid
        if first_click:
            game_instance.grid.generate_grid(first_click)
            game_instance.grid.mines_placed = True
            # Reveal the first clicked cell
            revealed[first_click[0]][first_click[1]] = True

            # If it's a 0, reveal adjacent cells
            if loaded_grid[first_click[0]][first_click[1]] == 0:
                stack = [first_click]
                while stack:
                    curr_y, curr_x = stack.pop()
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            ny, nx = curr_y + dy, curr_x + dx
                            if (0 <= ny < rows and 0 <= nx < cols and
                                not revealed[ny][nx]):
                                revealed[ny][nx] = True
                                if loaded_grid[ny][nx] == 0:
                                    stack.append((ny, nx))

        game_instance.grid.grid = loaded_grid
        game_instance.display = DisplayGrid(rows, cols)
        interface(cols, rows, loaded_grid, revealed, game_instance, screen)
    else:
        # Handle error if grid cannot be loaded
        error_font = pygame.font.SysFont('Arial', 30)
        error_text = error_font.render("Failed to load the selected game.", True, RED)
        screen.blit(error_text, (50, 200))
        pygame.display.flip()
        sleep(2)

startmenu()
