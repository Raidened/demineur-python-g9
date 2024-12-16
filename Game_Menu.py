import random
import json
import os
from time import sleep

def generate_grid(rows, cols, mines):
    """Génère une grille avec des mines et les cases adjacentes contenant le nombre de mines."""
    if mines > rows * cols:
        raise ValueError("Le nombre de mines dépasse la capacité de la grille.")

    # Création de la grille vide (avec des chiffres et des mines)
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Placement des mines
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    mine_positions = random.sample(all_positions, mines)

    # Placer les mines sur la grille
    for r, c in mine_positions:
        grid[r][c] = 'M'

    # Mettre à jour les cases adjacentes aux mines
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r, c in mine_positions:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 'M':
                grid[nr][nc] += 1

    return grid


def create_display_grid(rows, cols):
    """Crée une grille d'affichage vide avec des symboles pour les cases non révélées."""
    return [['*' for _ in range(cols)] for _ in range(rows)]


def display_game(display_grid):
    """Affiche la grille d'affichage au joueur avec des cases révélées."""
    print("\n=== Grille du jeu ===")
    for row in display_grid:
        print(" ".join(str(cell) for cell in row))


def get_next_grid_number(folder="saved_grid"):
    """Retourne le prochain numéro de fichier pour les grilles sauvegardées."""
    if not os.path.exists(folder):
        os.makedirs(folder)

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


def save_grid(grid, difficulty, folder="saved_grid"):
    """Sauvegarde la grille dans un fichier JSON avec un numéro incrémenté et la difficulté dans un dossier donné."""
    grid_number = get_next_grid_number(folder)
    difficulty_name = difficulty.lower()
    filename = f"grid_{difficulty_name}_{grid_number}.json"
    filepath = os.path.join(folder, filename)

    with open(filepath, 'w') as file:
        json.dump(grid, file)
    print(f"Grille sauvegardée sous {filename}")


def load_grid(folder="saved_grid"):
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


def game_menu():
    """Le menu principal du jeu."""
    print("=== Bienvenue dans le jeu de Démineur ===")
    print("Choisissez une difficulté:")
    print("1. Facile (9x9, 10 mines)")
    print("2. Moyen (16x16, 40 mines)")
    print("3. Difficile (30x30, 100 mines)")

    choice = input("Entrez le numéro de la difficulté : ")
    if choice == '1':
        rows, cols, mines = 9, 9, 10
        difficulty = "facile"
    elif choice == '2':
        rows, cols, mines = 16, 16, 40
        difficulty = "moyen"
    elif choice == '3':
        rows, cols, mines = 30, 30, 100
        difficulty = "difficile"
    else:
        print("Choix invalide. La difficulté par défaut 'facile' a été sélectionnée.")
        rows, cols, mines = 9, 9, 10
        difficulty = "facile"

    grid = generate_grid(rows, cols, mines)

    # Créer la grille d'affichage
    display = create_display_grid(rows, cols)

    # Sauvegarde de la grille avec la difficulté
    save_grid(grid, difficulty)

    # Affichage du plateau de jeu
    display_game(display)

    # Attente d'un moment pour l'utilisateur avant de commencer la partie
    print("\nLa partie commence !")
    sleep(2)

    # Vous pouvez ajouter ici la logique pour le jeu : choix du joueur, révélations de cases, etc.

if __name__ == "__main__":
    game_menu()
