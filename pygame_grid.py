import random
import pygame
import json
import os
from time import sleep, time_ns
import datetime




class Grid:
    def __init__(self, rows, cols, mines, difficulty):
        self.player_name = "Anonyme"
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.difficulty = difficulty
        self.grid = self.generate_grid()
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Ajout de revealed
        self.score = None


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

    def save_game(self,save_dir):
        """Sauvegarde l'état du jeu dans un fichier JSON dans le dossier 'saved_grid'."""
        # Créer le dossier 'saved_grid' si nécessaire
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        # Trouver un numéro de fichier libre
        file_number = 1
        while True:
            filename = f"{save_dir}/grid{file_number}_{self.difficulty}.json"
            if not os.path.exists(filename):
                break
            file_number += 1
        # Sauvegarder l'état du jeu dans le fichier
        datenow = datetime.datetime.now()
        with open(filename, 'w') as f:
            json.dump(self.grid, f)
        game_state = {
            'rows': self.rows,
            'cols': self.cols,
            'mines': self.mines,
            'difficulty': self.difficulty,
            'grid': self.grid,
            'revealed': self.revealed,  # Ajout de l'état des cases révélées
            'name':self.player_name,
            'date': str(datenow)[:-4],
            'score': self.score
        }
        with open(filename, 'w') as f:
            json.dump(game_state, f)
        print(f"Partie sauvegardée sous {filename}!")



class Game:
    def __init__(self):
        """Initialise le jeu avec les paramètres de difficulté et le jeu de la grille."""
        self.difficulty = ""
        self.rows = 0
        self.cols = 0
        self.mines = 0
        self.grid = None
        self.display = None

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
                    return data["rows"], data["cols"], data["mines"], data[
                        "difficulty"], data["grid"], revealed, first_click
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
                    return data["grid"], data["rows"], data["cols"], data["mines"], data[
                        "difficulty"], revealed, first_click
                else:
                    raise ValueError("Le fichier JSON ne contient pas un dictionnaire.")
            except (json.JSONDecodeError, KeyError, FileNotFoundError, ValueError) as e:
                print(f"Erreur de lecture dans le fichier {latest_file}: {e}")
                return None, None, None, None, None, None, None

def drawgrid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, table, revealed, flagged, lost_mine=None):
    """Dessine la grille avec les mines et les cases révélées."""

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    blocksize = 30

    for x in range(0, WINDOW_HEIGHT, blocksize):
        for y in range(0, WINDOW_WIDTH, blocksize):
            rect = pygame.Rect(y, x, blocksize, blocksize)
            grid_x = y // blocksize
            grid_y = x // blocksize
            gridxmax = WINDOW_HEIGHT // blocksize
            gridymax = WINDOW_WIDTH // blocksize
            truc= grid_y * (gridymax//15) *5
            truc2 = grid_x * (gridxmax//15) *5
            WHITE = (0 + truc , 0, 104 + truc2)
            GRAY = (100 + truc2 , 100, 255 - truc)

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
                pygame.draw.rect(screen, WHITE, rect, 0)
                imp = pygame.image.load("images/flag.png").convert_alpha()
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


def interface(nbcoln, nbline, table, game_instance, isfirst):
    """Interface principale pour afficher le jeu et gérer la logique de la partie."""
    WINDOW_HEIGHT = nbline * 30
    WINDOW_WIDTH = nbcoln * 30
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    revealed = [[False for _ in range(nbcoln)] for _ in range(nbline)]  # Cases révélées
    flagged = [[False for _ in range(nbcoln)] for _ in range(nbline)]
    lost_mine = None  # Variable pour stocker la position de la mine déclenchée
    running = True
    score_start = time_ns()//1000000
    lose=False
    print(score_start)


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
                    if isfirst:
                        while table[grid_x][grid_y] != 0:
                            game_instance.grid = game_instance.generate_grid()
                            table=game_instance.grid
                    isfirst = False
                    # Révélation de la case
                    revealed[grid_y][grid_x] = True

                    # Si une mine est révélée, afficher la défaite
                    if table[grid_x][grid_y] == "M":
                        lose = True

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

                        pygame.draw.rect(screen, (195, 161, 255), restart_button)
                        pygame.draw.rect(screen, (161, 177, 255), quit_button)

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

            # Sauvegarder la partie
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Touche S pour sauvegarder
                    if isinstance(game_instance, Grid):  # Vérifiez si game_instance est bien une instance de Grid
                        game_instance.save_game('saved_grid')  # Sauvegarder le jeu
                    else:
                        print ("Erreur")

                break  # Quitter la boucle pour arrêter le jeu

        checkout = 0
        for r in range(nbline):
            for c in range(nbcoln):
                if revealed[r][c]:
                    checkout += 1
                elif flagged[r][c]:
                    if table[c][r] == "M":
                        checkout += 1
        if checkout >= nbcoln * nbline and not lose:

            score_end = time_ns() // 1000000
            score=score_end - score_start
            game_instance.score = score
            game_instance.save_game('hof/'+game_instance.difficulty)
            scoresec = "GG fini en " + str((score // 1000) % 60) + "." + str(score % 1000)
            if score%60000>1 :
                scoresec= "GG fini en "+str(score//100000)+":"+str((score//1000)%60)+"."+str(score%1000)

            drawgrid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, table, revealed, flagged, lost_mine)
            # Demander à l'utilisateur s'il veut recommencer
            win = pygame.Rect(WINDOW_WIDTH /2 - 130, WINDOW_HEIGHT // 2 - 100, 260, 50)
            restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2, 150, 50)
            quit_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 60, 150, 50)

            pygame.draw.rect(screen, (222, 161, 255), win)
            pygame.draw.rect(screen, (195, 161, 255), restart_button)
            pygame.draw.rect(screen, (161, 177, 255), quit_button)

            font = pygame.font.SysFont(None, 30)

            win_text = font.render(scoresec, True, (0, 0, 0))
            restart_text = font.render("Recommencer", True, (0, 0, 0))
            quit_text = font.render("Quitter", True, (0, 0, 0))

            screen.blit(win_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 85))
            screen.blit(restart_text, (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 10))
            screen.blit(quit_text, (WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 + 70))

            pygame.display.flip()

            # Attendre l'action de l'utilisateur
            waiting_for_action = True
            while waiting_for_action:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
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