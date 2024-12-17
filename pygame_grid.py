import random

import pygame

import pygame
import json
import os
from time import sleep

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

    def save_grid(self, folder="saved_grid"):
        """Sauvegarde la grille dans un fichier JSON avec un numéro incrémenté et la difficulté dans un dossier donné."""
        if not os.path.exists(folder):
            os.makedirs(folder)

        grid_number = self.get_next_grid_number(folder)
        difficulty_name = self.difficulty.lower()  # Utilisation de l'attribut difficulty
        filename = f"grid_{difficulty_name}_{grid_number}.json"
        filepath = os.path.join(folder, filename)

        with open(filepath, 'w') as file:
            json.dump(self.grid, file)
        print(f"Grille sauvegardée sous {filename}")

    def get_next_grid_number(self, folder="saved_grid"):
        """Retourne le prochain numéro de fichier pour les grilles sauvegardées."""
        files = os.listdir(folder)
        grid_files = [f for f in files if f.startswith('grid') and f.endswith('.json')]

        grid_numbers = []
        for f in grid_files:
            try:
                parts = f.replace('grid_', '').replace('.json', '').split('_')
                if len(parts) == 2 and parts[1].isdigit():
                    grid_numbers.append(int(parts[1]))
            except ValueError:
                pass  # Ignore les erreurs si le format est incorrect

        if not grid_numbers:
            return 1

        return max(grid_numbers) + 1

class DisplayGrid:
    def __init__(self, rows, cols):
        """Initialise la grille d'affichage avec des symboles '*'."""
        self.rows = rows
        self.cols = cols
        self.grid_display = self.create_display_grid()  # Renommé display en grid_display

    def create_display_grid(self):
        """Crée une grille d'affichage vide avec des symboles pour les cases non révélées."""
        return [['*' for _ in range(self.cols)] for _ in range(self.rows)]

    def display(self, game_grid):
        """Affiche la grille de jeu et la grille d'affichage côte à côte."""
        print("\n=== Grille de jeu ===               === Grille d'affichage ===")
        cell_width = 3
        for row_game, row_display in zip(game_grid, self.grid_display):  # Utiliser grid_display ici
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

    def game_menu(self):
        """Le menu principal du jeu."""
        print("=== Bienvenue dans le jeu de Démineur ===")
        print("Choisissez une difficulté:")
        print("1. Facile (9x9, 10 mines)")
        print("2. Moyen (16x16, 40 mines)")
        print("3. Difficile (30x30, 100 mines)")

        choice = input("Entrez le numéro de la difficulté : ")
        if choice == '1':
            self.rows, self.cols, self.mines = 9, 9, 10
            self.difficulty = "facile"
        elif choice == '2':
            self.rows, self.cols, self.mines = 16, 16, 40
            self.difficulty = "moyen"
        elif choice == '3':
            self.rows, self.cols, self.mines = 30, 30, 100
            self.difficulty = "difficile"
        else:
            print("Choix invalide. La difficulté par défaut 'facile' a été sélectionnée.")
            self.rows, self.cols, self.mines = 9, 9, 10
            self.difficulty = "facile"



    def load_grid(self, folder="saved_grid"):
        """Charge une grille depuis un fichier JSON dans un dossier donné."""
        files = os.listdir(folder)
        grid_files = [f for f in files if f.startswith('grid') and f.endswith('.json')]

        if not grid_files:
            print("Aucune grille sauvegardée trouvée.")
            return None

        latest_file = max(grid_files, key=lambda f: int(f.replace('grid', '').replace('.json', '').split('_')[1]))
        filepath = os.path.join(folder, latest_file)

        with open(filepath, 'r') as file:
            grid = json.load(file)

        print(f"Grille rechargée depuis {latest_file}")
        return grid

    def start_game(self):
        """Démarre la partie après avoir choisi la difficulté."""
        self.game_menu()
        self.grid = Grid(self.rows, self.cols, self.mines)
        self.display = DisplayGrid(self.rows, self.cols)

        # Sauvegarde de la grille
        self.save_grid()

        # Affichage de la grille d'affichage à côté de la grille de jeu
        self.display.display(self.grid.grid)

        # Attente d'un moment pour l'utilisateur avant de commencer la partie
        print("\nLa partie commence !")
        sleep(2)


def drawgrid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, table, revealed):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (200, 200, 200)
    GRAY = (150, 150, 150)
    blocksize = 30

    for x in range(0, WINDOW_HEIGHT, blocksize):
        for y in range(0, WINDOW_WIDTH, blocksize):
            rect = pygame.Rect(y, x, blocksize, blocksize)
            grid_x = y // blocksize
            grid_y = x // blocksize

            # Case révélée ou non
            if revealed[grid_y][grid_x]:
                # Si c'est une mine
                if table[grid_x][grid_y] == "M":
                    pygame.draw.rect(screen, RED, rect, 0)
                elif table[grid_x][grid_y] == 0:
                    pygame.draw.rect(screen, GRAY, rect, 0)
                    if grid_y<len(table[0])-1:
                        revealed[grid_y + 1][grid_x] = True
                    if grid_y>0:
                        revealed[grid_y - 1][grid_x] = True
                    if grid_x < len(table) - 1:
                        revealed[grid_y][grid_x + 1] = True
                    if grid_x > 0:
                        revealed[grid_y][grid_x - 1] = True
                else:
                    pygame.draw.rect(screen, GRAY, rect, 0)  # Case sans mine
                    # Affiche la valeur si ce n'est pas vide
                    font = pygame.font.SysFont('Arial', 20)
                    text = font.render(str(table[grid_x][grid_y]), True, BLACK)
                    screen.blit(text, (y + 10, x + 5))
            else:
                pygame.draw.rect(screen, WHITE, rect, 0)

            pygame.draw.rect(screen, BLACK, rect, 2)  # Bordure


def interface(nbcoln, nbline, table):
    WINDOW_HEIGHT = nbline * 30
    WINDOW_WIDTH = nbcoln * 30
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    revealed = [[False for _ in range(nbcoln)] for _ in range(nbline)]  # Cases révélées

    while running:
        screen.fill((0, 0, 0))
        drawgrid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, table, revealed)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Gestion du clic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    x, y = event.pos
                    grid_x = x // 30
                    grid_y = y // 30

                    # Révélation de la case
                    revealed[grid_y][grid_x] = True



