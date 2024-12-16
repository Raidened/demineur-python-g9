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
    print("3. Difficile : 16x30 avec 99 mines")


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
            return (16, 30, 99, "difficile")  # Ajout du nom de la difficulté
        else:
            print("\nOption non valide. Veuillez choisir une difficulté parmi les options disponibles.")


def start_game():
    """Démarre la partie après avoir choisi la difficulté."""
    from Grid_Generator import generate_grid, display_grid, save_grid, create_display_grid  # Importer les fonctions nécessaires
    from pygame_grid import interface,drawgrid

    rows, cols, mines, difficulty = select_difficulty()  # On récupère aussi le nom de la difficulté
    grid = generate_grid(rows, cols, mines)

    # Créer la grille d'affichage (initialement avec des '*')
    display = create_display_grid(rows, cols)

    # Affichage de la grille de jeu et de la grille d'affichage côte à côte
    print(f"\nLa partie commence avec un plateau de {rows}x{cols} et {mines} mines.")
    display_grid(grid, display)

    interface(cols, rows, grid, difficulty)

    # Sauvegarde de la grille avec la difficulté sélectionnée dans le nom du fichier
    save_grid(grid, difficulty)





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
