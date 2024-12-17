import random
import pygame
import json
import os
from time import sleep
from datetime import datetime

class Grid:
    def __init__(self, rows, cols, mines, difficulty):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.difficulty = difficulty
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]  # Initialize empty grid
        self.mines_placed = False  # Flag to check if mines are placed

    def generate_grid(self, first_click):
        """Génère une grille avec des mines, en s'assurant que la première case cliquée et ses adjacentes sont sûres."""
        # Convert first_click to tuple if it's a list
        if isinstance(first_click, list):
            first_click = tuple(first_click)
            
        if self.mines > self.rows * self.cols - len(self.get_adjacent_cells(first_click)):
            raise ValueError("Le nombre de mines dépasse la capacité de la grille après exclusion de la première case et de ses adjacents.")

        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        safe_positions = self.get_adjacent_cells(first_click) + [first_click]
        available_positions = list(set(all_positions) - set(safe_positions))
        mine_positions = random.sample(available_positions, self.mines)

        for r, c in mine_positions:
            self.grid[r][c] = 'M'

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for r, c in mine_positions:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != 'M':
                    self.grid[nr][nc] += 1

        self.mines_placed = True

    def get_adjacent_cells(self, position):
        """Retourne les coordonnées des cellules adjacentes à une position donnée."""
        # Convert position to tuple if it's a list
        if isinstance(position, list):
            position = tuple(position)
        
        r, c = position
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        adjacent = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                adjacent.append((nr, nc))
        return adjacent

    def get_grid(self):
        return self.grid

    def restart_game(self):
        """Redémarre le jeu avec une nouvelle grille."""
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.mines_placed = False
        self.display = DisplayGrid(self.rows, self.cols)
        self.display.display(self.grid)
        print("\nNouvelle partie !")
        sleep(2)

class DisplayGrid:
    def __init__(self, rows, cols):
        """Initialise la grille d'affichage avec des symboles '*'."""
        self.rows = rows
        self.cols = cols
        self.grid_display = self.create_display_grid()

    def create_display_grid(self):
        """Crée une grille d'affichage vide avec des symboles pour les cases non révélées."""
        return [['*' for _ in range(self.cols)] for _ in range(self.rows)]

    def display(self, game_grid):
        """Affiche la grille de jeu et la grille d'affichage côte à côte."""
        print("\n=== Grille de jeu ===               === Grille d'affichage ===")
        cell_width = 3
        for row_game, row_display in zip(game_grid, self.grid_display):
            row_game_str = ' '.join(f"{'💣' if cell == 'M' else str(cell):<{cell_width}}" for cell in row_game)
            row_display_str = ' '.join(f"{str(cell):<{cell_width}}" for cell in row_display)
            print(f"{row_game_str}   {row_display_str}")

class Game:
    def __init__(self):
        """Initialise le jeu avec les paramètres de difficulté et le jeu de la grille."""
        self.difficulty = ""
        self.rows = 0
        self.cols = 0
        self.mines = 0
        self.grid = None
        self.display = None
        self.player_name = ""  # Ensure player_name attribute exists
        self.first_click_pos = None  # Add this new attribute

    def start_game(self, screen):
        """Démarre la partie avec les paramètres déjà définis."""
        # Initialize the grid and display
        self.grid = Grid(self.rows, self.cols, self.mines, self.difficulty)
        self.display = DisplayGrid(self.rows, self.cols)
        
        # Remove the save_grid call from here
        self.run(screen)

    def run(self, screen):
        """Lance l'interface du jeu."""
        initial_revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        # Swap self.cols and self.rows to match the parameter order
        interface(self.cols, self.rows, self.grid.get_grid(), initial_revealed, self, screen)

    def load_grid(self, folder="saved_grid", filename=None):
        """Charge une grille et ses paramètres depuis un fichier JSON dans un dossier donné."""
        if filename:
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, 'r') as file:
                    data = json.load(file)
                if isinstance(data, dict):
                    print(f"Grille rechargée depuis {filename}")
                    revealed = data.get("revealed", [[False for _ in range(data["cols"])] for _ in range(data["rows"])])
                    first_click = data.get("first_click")
                    return data["grid"], data["rows"], data["cols"], data["mines"], data["difficulty"], revealed, first_click
                else:
                    raise ValueError("Le fichier JSON ne contient pas un dictionnaire.")
            except (json.JSONDecodeError, KeyError, FileNotFoundError, ValueError) as e:
                print(f"Erreur de lecture dans le fichier {filename}: {e}")
                return None, None, None, None, None, None, None
        else:
            grid_files = [f for f in os.listdir(folder) if f.startswith('grid') and f.endswith('.json')]
            if not grid_files:
                print("Aucune grille sauvegardée trouvée.")
                return None, None, None, None, None

            latest_file = max(
                grid_files,
                key=lambda f: os.path.getmtime(os.path.join(folder, f))
            )
            filepath = os.path.join(folder, latest_file)

            try:
                with open(filepath, 'r') as file:
                    data = json.load(file)
                if isinstance(data, dict):
                    print(f"Grille rechargée depuis {latest_file}")
                    revealed = data.get("revealed", [[False for _ in range(data["cols"])] for _ in range(data["rows"])])
                    first_click = data.get("first_click")
                    return data["grid"], data["rows"], data["cols"], data["mines"], data["difficulty"], revealed, first_click
                else:
                    raise ValueError("Le fichier JSON ne contient pas un dictionnaire.")
            except (json.JSONDecodeError, KeyError, FileNotFoundError, ValueError) as e:
                print(f"Erreur de lecture dans le fichier {latest_file}: {e}")
                return None, None, None, None, None, None, None

    def save_score(self, score, difficulty):
        scores_file = f"saved_grid/scores_{difficulty}.json"
        try:
            with open(scores_file, 'r') as file:
                scores = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []

        scores.append({"name": self.player_name, "score": score, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        with open(scores_file, 'w') as file:
            json.dump(scores, file)

    def save_grid(self, grid, difficulty, revealed=None):
        """Sauvegarde la grille avec les paramètres du jeu."""
        # Convert first_click_pos to tuple before saving
        first_click = tuple(self.first_click_pos) if self.first_click_pos else None
        
        grid_file = f"saved_grid/grid_{difficulty}_{int(datetime.now().timestamp())}.json"
        data = {
            "rows": self.rows,
            "cols": self.cols,
            "mines": self.mines,
            "difficulty": self.difficulty,
            "grid": grid,
            "revealed": revealed,
            "player_name": self.player_name,  # Add player name to saved data
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Add date for better display
            "first_click": first_click,  # Save as tuple
        }
        with open(grid_file, 'w') as file:
            json.dump(data, file)

    def end_game(self, score):
        self.save_score(score, self.difficulty)
        self.save_grid(self.grid.grid, self.difficulty)
        print("Game over! Your score has been saved.")

    def load_and_display_game(self, screen, game_file):
        game_instance = Game()
        loaded_grid, rows, cols, mines, difficulty, revealed, first_click = game_instance.load_grid(folder="saved_grid", filename=game_file)
        if loaded_grid:
            game_instance.rows = rows
            game_instance.cols = cols
            game_instance.mines = mines
            game_instance.difficulty = difficulty
            game_instance.grid = Grid(game_instance.rows, game_instance.cols, self.mines, self.difficulty)
            game_instance.grid.grid = loaded_grid
            game_instance.grid.mines_placed = True  # Indicate that mines are already placed
            game_instance.display = DisplayGrid(game_instance.rows, game_instance.cols)
            interface(game_instance.cols, game_instance.rows, loaded_grid, revealed, game_instance, screen)
        else:
            # Handle error if grid cannot be loaded
            error_font = pygame.font.SysFont('Arial', 30)
            error_text = error_font.render("Failed to load the selected game.", True, RED)
            screen.blit(error_text, (50, 200))
            pygame.display.flip()
            sleep(2)

def drawgrid(screen, table, revealed, blocksize, lost_mine=None, player_name=None):
    """Dessine la grille avec les mines et les cases révélées."""
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (200, 200, 200)
    GRAY = (150, 150, 150)

    nbline = len(table)
    nbcoln = len(table[0])

    for y in range(nbline):
        for x in range(nbcoln):
            rect = pygame.Rect(x * blocksize, y * blocksize, blocksize, blocksize)
            grid_x, grid_y = x, y  # Correct indexing

            if revealed[grid_y][grid_x]:
                cell_value = table[grid_y][grid_x]  # Swap indices here
                if cell_value == "M":
                    pygame.draw.rect(screen, RED, rect, 0)  # Fond rouge pour la mine
                    pygame.draw.circle(screen, BLACK, rect.center, blocksize // 4)  # Dessiner une mine
                elif cell_value == 0:
                    pygame.draw.rect(screen, GRAY, rect, 0)
                    if grid_y < len(table) - 1:
                        revealed[grid_y + 1][grid_x] = True
                    if grid_y > 0:
                        revealed[grid_y - 1][grid_x] = True
                    if grid_x < len(table[0]) - 1:
                        revealed[grid_y][grid_x + 1] = True
                    if grid_x > 0:
                        revealed[grid_y][grid_x - 1] = True
                    if grid_y < len(table) - 1 and grid_x < len(table[0]) - 1:
                        revealed[grid_y + 1][grid_x + 1] = True
                    if grid_y < len(table) - 1 and grid_x > 0:
                        revealed[grid_y + 1][grid_x - 1] = True
                    if grid_y > 0 and grid_x < len(table[0]) - 1:
                        revealed[grid_y - 1][grid_x + 1] = True
                    if grid_y > 0 and grid_x > 0:
                        revealed[grid_y - 1][grid_x - 1] = True
                else:
                    pygame.draw.rect(screen, GRAY, rect, 0)  # Case sans mine
                    if table[grid_y][grid_x] != 0:
                        font_size = max(12, blocksize // 2)
                        font = pygame.font.SysFont('Arial', font_size)

            pygame.draw.rect(screen, BLACK, rect, 2)  # Bordure

            if lost_mine and (grid_x, grid_y) == lost_mine:
                pygame.draw.rect(screen, RED, rect, 0)  # Fond rouge pour la mine
                pygame.draw.circle(screen, BLACK, rect.center, blocksize // 4)  # Dessiner une mine

    # Add player name at the top of the grid
    if player_name:
        font = pygame.font.SysFont('Arial', max(12, blocksize // 2))
        text = font.render(f"Player: {player_name}", True, WHITE)
        screen.blit(text, (10, 10))

def game_over_popup(screen, lost_message, WINDOW_WIDTH, WINDOW_HEIGHT):
    """Affiche un popup avec un message de défaite et les options de recommencer ou quitter."""
    font = pygame.font.SysFont('Arial', 30)
    text = font.render(lost_message, True, (255, 0, 0))
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 3))

    # Création des boutons
    restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2, 150, 50)
    quit_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 60, 150, 50)

    pygame.draw.rect(screen, (0, 255, 0), restart_button)  # Vert pour recommencer
    pygame.draw.rect(screen, (255, 0, 0), quit_button)  # Rouge pour quitter

    restart_text = font.render("Recommencer", True, (0, 0, 0))
    quit_text = font.render("Quitter", True, (0, 0, 0))

    screen.blit(restart_text, (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 10))
    screen.blit(quit_text, (WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 + 70))

    pygame.display.flip()

    return restart_button, quit_button

def interface(nbcoln, nbline, table, revealed, game_instance, screen):
    """Interface principale pour afficher le jeu et gérer la logique de la partie."""
    # Get the initial display resolution
    infoObject = pygame.display.Info()
    display_width, display_height = infoObject.current_w, infoObject.current_h

    # Calculate the maximum block size to fit the grid within the display
    # margin = 100  # Margin to ensure the window is not too close to the screen edges
    # max_window_width = display_width - margin
    # max_window_height = display_height - margin

    # blocksize_w = max_window_width // nbcoln
    # blocksize_h = max_window_height // nbline
    # blocksize = int(min(blocksize_w, blocksize_h, 30))  # Limit the block size to 30 for smaller grids
    blocksize = 30  # Initial fixed block size
    MIN_BLOCKSIZE = 10  # Minimum block size

    revealed = [[False for _ in range(nbcoln)] for _ in range(nbline)]
    lost_mine = None
    running = True
    first_click = True  # Flag to check if it's the first click

    while running:
        screen.fill((0, 0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                # Adjust the screen size
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

                # Recalculate blocksize based on new window size
                available_width = WINDOW_WIDTH
                available_height = WINDOW_HEIGHT
                new_blocksize_w = available_width // nbcoln
                new_blocksize_h = available_height // nbline
                blocksize = max(MIN_BLOCKSIZE, min(new_blocksize_w, new_blocksize_h))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    grid_x = x // blocksize
                    grid_y = y // blocksize

                    if 0 <= grid_x < nbcoln and 0 <= grid_y < nbline:
                        if first_click:
                            # Save first click position if it's a new game
                            if not game_instance.grid.mines_placed:
                                game_instance.first_click_pos = (grid_y, grid_x)
                                game_instance.grid.generate_grid((grid_y, grid_x))
                                game_instance.save_grid(table, game_instance.difficulty, revealed)
                            first_click = False
                            
                        # Reveal only the clicked cell and process its neighbors
                        revealed[grid_y][grid_x] = True
                        
                        # If clicked cell is 0, reveal adjacent cells
                        if table[grid_y][grid_x] == 0:
                            stack = [(grid_y, grid_x)]
                            while stack:
                                curr_y, curr_x = stack.pop()
                                for dy in [-1, 0, 1]:
                                    for dx in [-1, 0, 1]:
                                        ny, nx = curr_y + dy, curr_x + dx
                                        if (0 <= ny < nbline and 0 <= nx < nbcoln and 
                                            not revealed[ny][nx]):
                                            revealed[ny][nx] = True
                                            if table[ny][nx] == 0:
                                                stack.append((ny, nx))
                        # Si une mine est révélée, afficher la défaite
                        if table[grid_y][grid_x] == "M":
                            lost_mine = (grid_x, grid_y)  # Garder la position de la mine déclenchée

                            # Révéler toutes les mines après une défaite
                            for r in range(nbline):
                                for c in range(nbcoln):
                                    revealed[r][c] = True

                            # Afficher la grille complète avant de montrer le popup
                            drawgrid(screen, table, revealed, blocksize, lost_mine)
                            pygame.display.flip()

                            # Demander à l'utilisateur s'il veut recommencer
                            WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()  # Added line
                            restart_button, quit_button = game_over_popup(screen, "Vous avez perdu!", WINDOW_WIDTH, WINDOW_HEIGHT)

                            # Attendre l'action de l'utilisateur
                            waiting_for_action = True
                            while waiting_for_action:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        running = False
                                        waiting_for_action = False
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if event.button == 1:  # Clic gauche
                                            x, y = event.pos
                                            if restart_button.collidepoint(x, y):
                                                # Reset the game state without changing difficulty
                                                running = False
                                                game_instance.end_game(score=0)  # Save the game even if lost
                                                game_instance.start_game(screen)  # Restart the game with the same difficulty
                                                return
                                            elif quit_button.collidepoint(x, y):
                                                pygame.quit()
                                                exit()
                            return  # Exit the interface after handling game over

        # Draw the grid with the current blocksize
        drawgrid(screen, table, revealed, blocksize, lost_mine)

        pygame.display.flip()

def show_scores(screen, difficulty):
    scores_file = f"saved_grid/scores_{difficulty}.json"
    try:
        with open(scores_file, 'r') as file:
            scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('Arial', 30)
    y_offset = 50

    for score in scores:
        text = font.render(f"Name: {score['name']}, Score: {score['score']}, Date: {score['date']}", True, (255, 255, 255))
        screen.blit(text, (50, y_offset))
        y_offset += 40

    pygame.display.flip()
    sleep(5)  # Display the scores for 5 seconds

def hall_of_fame(screen):
    difficulties = ["facile", "moyen", "difficile"]
    for difficulty in difficulties:
        show_scores(screen, difficulty)
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Arial', 40)
        text = font.render(f"=== {difficulty.capitalize()} ===", True, (255, 255, 255))
        screen.blit(text, (50, 20))
        pygame.display.flip()
        sleep(2)  # Display the difficulty title for 2 seconds
        show_scores(screen, difficulty)
        screen.blit(text, (50, 20))



        pygame.display.flip()
        sleep(2)  # Display the difficulty title for 2 seconds
        show_scores(screen, difficulty)



        screen.blit(text, (50, 20))



        pygame.display.flip()
        sleep(2)  # Display the difficulty title for 2 seconds
        show_scores(screen, difficulty)



