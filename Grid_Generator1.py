

# AFFICHAGE AVEC LES NUMEROS ET LES MINES VISIBLES



import random
import json
import os

def generate_grid(rows, cols, mines):
    """Génère une grille avec des mines et les cases adjacentes contenant le nombre de mines."""
    if mines > rows * cols:
        raise ValueError("Le nombre de mines dépasse la capacité de la grille.")

    # Création de la grille vide
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


def display_grid(grid):
    """Affiche la grille de manière propre."""
    print("\n=== Grille de jeu ===")
    for row in grid:
        print(" ".join(str(cell) for cell in row))


def get_next_grid_number(folder="saved_grid"):
    """Retourne le prochain numéro de fichier pour les grilles sauvegardées."""
    # Crée le dossier si nécessaire
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Récupère les fichiers existants dans le dossier
    files = os.listdir(folder)

    # Filtrer uniquement les fichiers qui commencent par 'grid' et se terminent par '.json'
    grid_files = [f for f in files if f.startswith('grid') and f.endswith('.json')]

    # Extraire les numéros de fichier et calculer le prochain numéro
    grid_numbers = []
    for f in grid_files:
        # Tenter d'extraire le numéro de la grille en évitant les erreurs de format
        try:
            # On extrait le numéro de grille de la forme "grid_<difficulté>_<numéro>.json"
            parts = f.replace('grid_', '').replace('.json', '').split('_')
            if len(parts) == 2 and parts[1].isdigit():
                grid_numbers.append(int(parts[1]))
        except ValueError:
            pass  # Ignore les erreurs si le format est incorrect

    # Si aucun fichier n'existe, on commence avec 1
    if not grid_numbers:
        return 1

    # Retourne le prochain numéro
    return max(grid_numbers) + 1


def save_grid(grid, difficulty, folder="saved_grid"):
    """Sauvegarde la grille dans un fichier JSON avec un numéro incrémenté et la difficulté dans un dossier donné."""
    # Déterminer le nom du fichier basé sur le nombre de grilles existantes et la difficulté
    grid_number = get_next_grid_number(folder)
    difficulty_name = difficulty.lower()  # Convertir la difficulté en minuscule
    filename = f"grid_{difficulty_name}_{grid_number}.json"
    filepath = os.path.join(folder, filename)

    # Sauvegarder la grille dans le fichier
    with open(filepath, 'w') as file:
        json.dump(grid, file)
    print(f"Grille sauvegardée sous {filename}")


def load_grid(folder="saved_grid"):
    """Charge une grille depuis un fichier JSON dans un dossier donné."""
    # Liste tous les fichiers et trie par nom pour obtenir le plus récent
    files = os.listdir(folder)
    grid_files = [f for f in files if f.startswith('grid') and f.endswith('.json')]

    if not grid_files:
        print("Aucune grille sauvegardée trouvée.")
        return None

    # Récupérer le dernier fichier (le plus grand numéro)
    latest_file = max(grid_files, key=lambda f: int(f.replace('grid', '').replace('.json', '').split('_')[1]))
    filepath = os.path.join(folder, latest_file)

    # Charger la grille depuis le fichier
    with open(filepath, 'r') as file:
        grid = json.load(file)

    print(f"Grille rechargée depuis {latest_file}")
    return grid


# Exemple d'utilisation
if __name__ == "__main__":
    rows, cols, mines = 9, 9, 10
    grid = generate_grid(rows, cols, mines)

    # Difficuté choisie
    difficulty = "facile"  # Vous pouvez aussi demander à l'utilisateur de choisir la difficulté

    # Affichage de la grille générée
    display_grid(grid)

    # Sauvegarde de la grille avec la difficulté incluse dans le nom
    save_grid(grid, difficulty)

    # Pour recharger la grille
    reloaded_grid = load_grid()
    if reloaded_grid:
        print("\nGrille rechargée depuis le fichier :")
        display_grid(reloaded_grid)
