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
        self.grid = self.generate_grid()

    def generate_grid(self):
        """Génère une grille avec des mines et les cases adjacentes contenant le nombre de mines."""
        if self.mines > self.rows * self.cols:
            raise ValueError("Le nombre de mines dépasse la capacité de la grille.")

        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # Placement des mines
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mine_positions = random.sample(all_positions, self.mines)

        for r, c in mine_positions:
            grid[r][c] = 'M'

        # Mettre à jour les cases adjacentes aux mines
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for r, c in mine_positions:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and grid[nr][nc] != 'M':
                    grid[nr][nc] += 1

        return grid

    def get_grid(self):
        return self.grid

    def restart_game(self):
        """Redémarre le jeu avec une nouvelle grille."""
        self.grid = Grid(self.rows, self.cols, self.mines, self.difficulty)  # Créer une nouvelle instance de Grid
        self.display = DisplayGrid(self.rows, self.cols)
        self.display.display(self.grid.grid)
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
            row_game_str = ' '.join(f"{str(cell):<{cell_width}}" for cell in row_game)
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
        self.player_name = ""

    def start_game(self, screen):
        """Démarre la partie avec les paramètres déjà définis."""
        # Initialize the grid and display
        self.grid = Grid(self.rows, self.cols, self.mines, self.difficulty)
        self.display = DisplayGrid(self.rows, self.cols)

        # Fix the call to save the grid
        self.save_grid(self.grid.grid, self.difficulty)

        # Start the game interface
        self.run(screen)

    def run(self, screen):
        """Lance l'interface du jeu."""
        # Swap self.cols and self.rows to match the parameter order
        interface(self.cols, self.rows, self.grid.get_grid(), self, screen)

    def load_grid(self, folder="saved_grid"):
        """Charge une grille depuis un fichier JSON dans un dossier donné."""
        files = os.listdir(folder)
        grid_files = [f for f in files if f.startswith('grid') and f.endswith('.json')]

        if not grid_files:
            print("Aucune grille sauvegardée trouvée.")
            return None

        latest_file = max(grid_files, key=lambda f: int(f.replace('grid', '').replace('.json', '').split('_')[1]))
        filepath = os.path.join(folder, latest_file)

        try:
            with open(filepath, 'r') as file:
                grid = json.load(file)
            print(f"Grille rechargée depuis {latest_file}")
            return grid
        except json.JSONDecodeError:
            print(f"Erreur de lecture dans le fichier {latest_file}")
            return None

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

    def save_grid(self, grid, difficulty):
        grid_file = f"saved_grid/grid_{difficulty}.json"
        with open(grid_file, 'w') as file:
            json.dump(grid, file)

    def end_game(self, score):
        self.save_score(score, self.difficulty)
        self.save_grid(self.grid.grid, self.difficulty)
        print("Game over! Your score has been saved.")

def drawgrid(screen, table, revealed, blocksize, lost_mine=None):
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
                    if table[grid_x][grid_y] != 0:
                        font_size = max(12, blocksize // 2)
                        font = pygame.font.SysFont('Arial', font_size)
                        text = font.render(str(table[grid_x][grid_y]), True, BLACK)
                        screen.blit(text, (x * blocksize + 10, y * blocksize + 5))
            else:
                pygame.draw.rect(screen, WHITE, rect, 0)  # Case non révélée

            pygame.draw.rect(screen, BLACK, rect, 2)  # Bordure

            if lost_mine and (grid_x, grid_y) == lost_mine:
                pygame.draw.rect(screen, RED, rect, 0)  # Fond rouge pour la mine
                pygame.draw.circle(screen, BLACK, rect.center, blocksize // 4)  # Dessiner une mine

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

def interface(nbcoln, nbline, table, game_instance, screen):
    """Interface principale pour afficher le jeu et gérer la logique de la partie."""
    # Get the display resolution
    infoObject = pygame.display.Info()
    display_width, display_height = infoObject.current_w, infoObject.current_h

    # Calculate the maximum block size to fit the grid within the display
    margin = 100  # Margin to ensure the window is not too close to the screen edges
    max_window_width = display_width - margin
    max_window_height = display_height - margin

    blocksize_w = max_window_width // nbcoln
    blocksize_h = max_window_height // nbline
    blocksize = int(min(blocksize_w, blocksize_h, 30))  # Limit the block size to 30 for smaller grids

    WINDOW_WIDTH = blocksize * nbcoln
    WINDOW_HEIGHT = blocksize * nbline

    # Adjust the screen size
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    revealed = [[False for _ in range(nbcoln)] for _ in range(nbline)]
    lost_mine = None
    running = True

    while running:
        screen.fill((0, 0, 0))

        # Pass the dynamic blocksize to drawgrid
        drawgrid(screen, table, revealed, blocksize, lost_mine)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Gestion du clic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    x, y = event.pos
                    grid_x = x // blocksize
                    grid_y = y // blocksize

                    # Révélation de la case
                    revealed[grid_y][grid_x] = True

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
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Arial', 40)
        text = font.render(f"=== {difficulty.capitalize()} ===", True, (255, 255, 255))
        screen.blit(text, (50, 20))
        pygame.display.flip()
        sleep(2)  # Display the difficulty title for 2 seconds
        show_scores(screen, difficulty)


