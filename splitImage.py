import cv2
import os
import sys
import numpy as np

def split_image_by_grid(image_path, virtual_width, virtual_height, factor):
    # Charger l'image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"❌ Erreur : Impossible de charger l'image '{image_path}'.")
        exit()

    # Dimensions réelles de l'image
    height, width = image.shape

    # Nombre total de cellules dans la grille
    total_cells = virtual_width * virtual_height

    # Nombre final de sous-images souhaitées
    target_cells = 60 * factor

    # Calcul du nombre de cellules par bloc pour obtenir `target_cells`
    cells_per_block = total_cells // target_cells
    block_width = virtual_width // int(virtual_width / (cells_per_block ** 0.5))
    block_height = virtual_height // int(virtual_height / (cells_per_block ** 0.5))

    # Taille des blocs en pixels (dans l'image réelle)
    pixel_block_width = width // (virtual_width // block_width)
    pixel_block_height = height // (virtual_height // block_height)

    # Créer le dossier de sortie
    output_dir = "output/cells"
    os.makedirs(output_dir, exist_ok=True)

    # Découpage de l'image
    count = 0
    for i in range(0, height, pixel_block_height):
        for j in range(0, width, pixel_block_width):
            if i + pixel_block_height <= height and j + pixel_block_width <= width:
                sub_image = image[i:i + pixel_block_height, j:j + pixel_block_width]
                output_path = os.path.join(output_dir, f"cell_{count}.png")
                cv2.imwrite(output_path, sub_image)
                count += 1
                if count >= target_cells:  # Stopper dès qu'on atteint le bon nombre d'images
                    break
        if count >= target_cells:
            break

    print(f"✅ Image divisée en {count} cellules enregistrées dans '{output_dir}'.")

# Vérifier les arguments
if len(sys.argv) < 5:
    print("Usage: python splitByGrid.py <image_grille> <virtual_width> <virtual_height> <facteur_division>")
    exit()

# Récupérer les arguments
image_path = sys.argv[1]
virtual_width = int(sys.argv[2])
virtual_height = int(sys.argv[3])
factor = int(sys.argv[4])

# Exécuter la fonction
split_image_by_grid(image_path, virtual_width, virtual_height, factor)
