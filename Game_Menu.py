from Grid_Generator import Grid, DisplayGrid, Game  # Importation des nouvelles classes
from time import sleep

def display_menu():
    """Affiche le menu principal."""
    print("\n=== Menu Principal ===")
    print("1. Démarrer une partie")
    print("2. Quitter")

def display_difficulty_menu():
    """Affiche le menu des difficultés."""
    print("\n=== Choix de la Difficulté ===")
    print("1. Facile : 9x9 avec 10 mines")
    print("2. Moyen : 16x16 avec 40 mines")
    print("3. Difficile : 30x16 avec 99 mines")

def select_difficulty():
    """Permet de choisir la difficulté du jeu."""
    while True:
        display_difficulty_menu()
        difficulty = input("Veuillez choisir une difficulté (1, 2 ou 3) : ")
        if difficulty == "1":
            print("\nDifficulté sélectionnée : Facile")
            return (9, 9, 10, "facile")  # Ajout du nom de la difficulté
        elif difficulty == "2":
            print("\nDifficulté sélectionnée : Moyen")
            return (16, 16, 40, "moyenne")  # Ajout du nom de la difficulté
        elif difficulty == "3":
            print("\nDifficulté sélectionnée : Difficile")
            return (30, 16, 99, "difficile")  # Ajout du nom de la difficulté
        else:
            print("\nOption non valide. Veuillez choisir une difficulté parmi les options disponibles.")

def start_game():
    """Démarre la partie après avoir choisi la difficulté."""
    rows, cols, mines, difficulty = select_difficulty()  # On récupère aussi le nom de la difficulté

    # Création de l'objet Grid avec la difficulté
    game_grid = Grid(rows, cols, mines, difficulty)  # Passer la difficulté ici
    display_grid = DisplayGrid(rows, cols)

    # Sauvegarde de la grille avec la difficulté sélectionnée dans le nom du fichier
    game_grid.save_grid()  # Utilisation de la méthode save_grid de la classe Grid

    # Affichage de la grille d'affichage à côté de la grille de jeu
    display_grid.display(game_grid.grid)

    print(f"\nLa partie commence avec un plateau de {rows}x{cols} et {mines} mines.")
    # Attente d'un moment pour l'utilisateur avant de commencer la partie
    print("\nLa partie commence !")
    sleep(2)


def handle_invalid_option():
    """Gère une option invalide."""
    print("\nOption non valide. Veuillez choisir une option parmi celles du menu.")

def main():
    """Point d'entrée principal de l'application."""
    while True:
        display_menu()
        choice = input("Veuillez sélectionner une option (1 ou 2) : ")

        if choice == "1":
            start_game()
        elif choice == "2":
            print("\nMerci d'avoir utilisé l'application. Au revoir !")
            break
        else:
            handle_invalid_option()

if __name__ == "__main__":
    main()
