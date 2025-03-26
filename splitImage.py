import os
import sys
import cv2
import numpy as np

if __name__ == "__main__":
    # Vérifier si les arguments sont donnés
    if len(sys.argv) < 3:
        print("Usage: python splitImage.py <chemin_image> <nombre_de_classes>")
        exit()

    # Récupérer l'image depuis les arguments
    image_path = sys.argv[1]

    # Récupérer le nombre de classes
    level = int(sys.argv[2])

    output_dir = "output/cells"
    num_pieces = 60 * level

    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        print("Erreur : Impossible de charger l'image.")
        exit()

    # Récupérer les dimensions de l'image
    height, width, _ = image.shape

    # Calculer la grille approximative
    aspect_ratio = width / height
    cols = int(np.sqrt(num_pieces * aspect_ratio))
    rows = int(np.ceil(num_pieces / cols))  # Utiliser ceil pour s'assurer d'avoir assez de lignes

    cell_width = width // cols
    cell_height = height // rows

    # Taille fixe de sortie (ajustée au cas où certaines cellules seraient plus petites)
    fixed_size = (cell_width, cell_height)

    # Créer le dossier de sortie
    os.makedirs(output_dir, exist_ok=True)

    count = 0
    for i in range(rows):
        for j in range(cols):
            x_start = j * cell_width
            y_start = i * cell_height

            # Gérer les cas où la cellule est en bout de ligne ou colonne
            x_end = min(x_start + cell_width, width)
            y_end = min(y_start + cell_height, height)

            # Extraire la sous-image
            cell = image[y_start:y_end, x_start:x_end]

            # Vérifier si la cellule est plus petite que la taille cible
            h, w, _ = cell.shape
            if (h, w) != fixed_size:
                # Créer une image blanche de la taille cible
                padded_cell = np.ones((cell_height, cell_width, 3), dtype=np.uint8) * 255
                padded_cell[:h, :w] = cell  # Placer l'image d'origine en haut à gauche
            else:
                padded_cell = cell

            # Enregistrer la sous-image
            output_path = os.path.join(output_dir, f"cell_{count}.png")
            cv2.imwrite(output_path, padded_cell)
            count += 1

    print(f"{count} sous-images enregistrées dans {output_dir}")
