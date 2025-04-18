import os
import sys
import cv2
import numpy as np

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python splitImage.py <chemin_image> <nombre_de_classes>")
        exit()

    image_path = sys.argv[1]
    level = int(sys.argv[2])

    output_dir = "output/cells"
    num_pieces = 60 * level

    image = cv2.imread(image_path)
    if image is None:
        print("Erreur : Impossible de charger l'image.")
        exit()

    height, width, _ = image.shape

    # Calcul de la grille en fonction du ratio
    aspect_ratio = width / height
    cols = int(np.sqrt(num_pieces * aspect_ratio))
    rows = int(np.ceil(num_pieces / cols))

    cell_width = width // cols
    cell_height = height // rows
    fixed_size = (cell_width, cell_height)

    os.makedirs(output_dir, exist_ok=True)

    count = 0
    for i in range(rows):
        for j in range(cols):
            x_start = j * cell_width
            y_start = i * cell_height
            x_end = min(x_start + cell_width, width)
            y_end = min(y_start + cell_height, height)

            cell = image[y_start:y_end, x_start:x_end]
            h, w, _ = cell.shape

            if (h, w) != fixed_size:
                padded_cell = np.ones((cell_height, cell_width, 3), dtype=np.uint8) * 255
                padded_cell[:h, :w] = cell
            else:
                padded_cell = cell

            output_path = os.path.join(output_dir, f"cell_{count}.png")
            cv2.imwrite(output_path, padded_cell)
            count += 1

    print(f"✅ Grille générée : {rows} lignes x {cols} colonnes ({rows * cols} cellules)")
