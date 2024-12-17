import pygame
import random


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
                if table[grid_y][grid_x] == "M":
                    pygame.draw.rect(screen, RED, rect, 0)
                else:
                    pygame.draw.rect(screen, GRAY, rect, 0)  # Case sans mine
                    # Affiche la valeur si ce n'est pas vide
                    font = pygame.font.SysFont('Arial', 20)
                    text = font.render(str(table[grid_y][grid_x]), True, BLACK)
                    screen.blit(text, (y + 10, x + 5))
            else:
                pygame.draw.rect(screen, WHITE, rect, 0)

            pygame.draw.rect(screen, BLACK, rect, 2)  # Bordure


def generate_grid(nbline, nbcoln, nb_mines):
    """ Génère une grille avec des mines aléatoires et des numéros autour """
    grid = [['0' for _ in range(nbcoln)] for _ in range(nbline)]
    mines = set()

    # Placement des mines
    while len(mines) < nb_mines:
        x = random.randint(0, nbcoln - 1)
        y = random.randint(0, nbline - 1)
        if (y, x) not in mines:
            mines.add((y, x))
            grid[y][x] = "M"

    # Mise à jour des numéros autour des mines
    for y, x in mines:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < nbline and 0 <= nx < nbcoln and grid[ny][nx] != "M":
                    grid[ny][nx] = str(int(grid[ny][nx]) + 1)

    return grid


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



