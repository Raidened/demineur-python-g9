import random
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

        try:
            with open(filepath, 'r') as file:
                grid = json.load(file)
            print(f"Grille rechargée depuis {latest_file}")
            return grid
        except json.JSONDecodeError:
            print(f"Erreur de lecture dans le fichier {latest_file}")
            return None

    def start_game(self):
        """Démarre la partie après avoir choisi la difficulté."""
        self.game_menu()
        self.grid = Grid(self.rows, self.cols, self.mines, self.difficulty)
        self.display = DisplayGrid(self.rows, self.cols)

        # Sauvegarde de la grille
        self.grid.save_grid()

        # Affichage de la grille d'affichage à côté de la grille de jeu
        self.display.display(self.grid.grid)

        # Attente d'un moment pour l'utilisateur avant de commencer la partie
        print("\nLa partie commence !")
        sleep(2)

    def run(self):
        """Lance l'interface du jeu."""
        self.start_game()  # Démarre la partie
        # Passez `self` comme `game_instance` à `interface`
        interface(self.rows, self.cols, self.grid.get_grid(), self)

def drawgrid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, table, revealed, flagged, lost_mine=None):
    """Dessine la grille avec les mines et les cases révélées."""
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

            if revealed[grid_y][grid_x]:
                if table[grid_x][grid_y] == "M":
                    pygame.draw.rect(screen, RED, rect, 0)  # Fond rouge pour la mine
                    pygame.draw.circle(screen, BLACK, rect.center, blocksize // 4)  # Dessiner une mine
                elif table[grid_x][grid_y] == 0:
                    pygame.draw.rect(screen, GRAY, rect, 0)
                    if grid_y < len(table[0]) - 1:
                        revealed[grid_y + 1][grid_x] = True
                    if grid_y > 0:
                        revealed[grid_y - 1][grid_x] = True
                    if grid_x < len(table) - 1:
                        revealed[grid_y][grid_x + 1] = True
                    if grid_x > 0:
                        revealed[grid_y][grid_x - 1] = True
                    if grid_y < len(table[0]) - 1 and grid_x < len(table) - 1:
                        revealed[grid_y + 1][grid_x + 1] = True
                    if grid_y < len(table[0]) - 1 and grid_x > 0:
                        revealed[grid_y + 1][grid_x - 1] = True
                    if grid_y > 0 and grid_x < len(table) - 1:
                        revealed[grid_y - 1][grid_x + 1] = True
                    if grid_y > 0 and grid_x > 0:
                        revealed[grid_y - 1][grid_x - 1] = True
                else:
                    pygame.draw.rect(screen, GRAY, rect, 0)  # Case sans mine
                    if table[grid_x][grid_y] != 0:
                        font = pygame.font.SysFont('Arial', 20)
                        text = font.render(str(table[grid_x][grid_y]), True, BLACK)
                        screen.blit(text, (y + 10, x + 5))
            elif flagged[grid_y][grid_x]:
                imp = pygame.image.load("images/flag.png").convert()
                imp = pygame.transform.scale(imp, (26, 26))
                screen.blit(imp, (grid_x * 30 + 2, grid_y * 30 + 2))
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


def interface(nbcoln, nbline, table, game_instance):
    """Interface principale pour afficher le jeu et gérer la logique de la partie."""
    WINDOW_HEIGHT = nbline * 30
    WINDOW_WIDTH = nbcoln * 30
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    revealed = [[False for _ in range(nbcoln)] for _ in range(nbline)]  # Cases révélées
    flagged = [[False for _ in range(nbcoln)] for _ in range(nbline)]
    lost_mine = None  # Variable pour stocker la position de la mine déclenchée
    running = True


    while running:


        screen.fill((0, 0, 0))

        # Affichage de la grille pendant la partie
        drawgrid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, table, revealed, flagged, lost_mine)

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

                    # Si une mine est révélée, afficher la défaite
                    if table[grid_x][grid_y] == "M":
                        lost_mine = (grid_x, grid_y)  # Garder la position de la mine déclenchée

                        # Révéler toutes les mines après une défaite
                        for r in range(nbline):
                            for c in range(nbcoln):
                                revealed[r][c] = True

                        # Afficher la grille complète avant de montrer le popup
                        drawgrid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, table, revealed, flagged, lost_mine)
                        pygame.display.flip()

                        # Demander à l'utilisateur s'il veut recommencer
                        restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2, 150, 50)
                        quit_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 60, 150, 50)

                        pygame.draw.rect(screen, (161, 242, 255), restart_button)
                        pygame.draw.rect(screen, (161, 255, 201), quit_button)

                        font = pygame.font.SysFont(None, 30)
                        restart_text = font.render("Recommencer", True, (0, 0, 0))
                        quit_text = font.render("Quitter", True, (0, 0, 0))

                        screen.blit(restart_text, (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 10))
                        screen.blit(quit_text, (WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 + 70))

                        pygame.display.flip()

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
                                            # Relancer le jeu en réinitialisant tout le processus
                                            running = False  # Quitter le jeu
                                            from pygame_menus import startmenu
                                            startmenu()  # Redémarre le jeu

                                            waiting_for_action = False
                                        elif quit_button.collidepoint(x, y):
                                            running = False  # Quitter le jeu
                                            waiting_for_action = False

                elif event.button == 3:
                    x, y = event.pos
                    grid_x = x // 30
                    grid_y = y // 30
                    if flagged[grid_y][grid_x]:
                        flagged[grid_y][grid_x] = False
                    elif not revealed[grid_y][grid_x]:
                        flagged[grid_y][grid_x] = True

                    break  # Quitter la boucle pour arrêter le jeu

        checkout = 0
        for r in range(nbline):
            for c in range(nbcoln):
                if revealed[r][c] or flagged[r][c]:
                    checkout += 1
        if checkout == nbcoln * nbline:
            # Demander à l'utilisateur s'il veut recommencer
            win = pygame.Rect(WINDOW_WIDTH /2 - 130, WINDOW_HEIGHT // 4, 260, 50)
            restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2, 150, 50)
            quit_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 60, 150, 50)

            pygame.draw.rect(screen, (222, 161, 255), win)
            pygame.draw.rect(screen, (195, 161, 255), restart_button)
            pygame.draw.rect(screen, (161, 177, 255), quit_button)

            font = pygame.font.SysFont(None, 30)

            win_text = font.render("GG BG t'as vu la rime", True, (0, 0, 0))
            restart_text = font.render("Recommencer", True, (0, 0, 0))
            quit_text = font.render("Quitter", True, (0, 0, 0))

            screen.blit(win_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 9 + 50))
            screen.blit(restart_text, (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 10))
            screen.blit(quit_text, (WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 + 70))

            pygame.display.flip()

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
                                # Relancer le jeu en réinitialisant tout le processus
                                running = False  # Quitter le jeu
                                from pygame_menus import startmenu
                                startmenu()  # Redémarre le jeu

                                waiting_for_action = False
                            elif quit_button.collidepoint(x, y):
                                running = False  # Quitter le jeu
                                waiting_for_action = False