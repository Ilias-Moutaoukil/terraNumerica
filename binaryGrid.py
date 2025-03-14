import cv2
import numpy as np
import sys
import os

# Vérification des arguments
if len(sys.argv) < 2:
    print("Usage: python binary_grid.py <chemin_image>")
    exit()

image_path = sys.argv[1]

# Charger l'image en noir et blanc (binaire)
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    print(f"❌ Erreur : Impossible de charger {image_path}")
    exit()

# Vérifier que l'image est bien binaire (contient uniquement 0 et 255)
unique_values = np.unique(image)
if not np.array_equal(unique_values, [0, 255]) and not np.array_equal(unique_values, [0]) and not np.array_equal(unique_values, [255]):
    print("⚠️ Attention : L'image ne semble pas être strictement binaire (0 et 255 uniquement).")

# Convertir : noir (0) → 0, blanc (255) → 1
binary_matrix = (image == 0).astype(np.uint8)

# Définir la taille des cellules (pixels de la grille)
cell_size = 20  # Taille des cases

# Dimensions de l'image finale
grid_height = image.shape[0] * cell_size
grid_width = image.shape[1] * cell_size

# Créer une image blanche pour la grille
grid_image = np.ones((grid_height, grid_width), dtype=np.uint8) * 255  # Image en niveaux de gris

# Ajustement pour centrer le texte (légèrement décalé en bas à gauche)
text_offset_x = cell_size // 5  # Décalage vers la gauche
text_offset_y = cell_size // 1.2  # Décalage vers le bas

# Ajouter la grille et les nombres
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        value = binary_matrix[i, j]  # 0 ou 1

        # Position du texte légèrement décalée en bas à gauche
        text_position = (j * cell_size + text_offset_x, i * cell_size + int(text_offset_y))

        # Placer le texte en noir (0) sur fond blanc
        cv2.putText(grid_image, str(value), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 1, cv2.LINE_AA)

# Dessiner la grille (lignes noires)
for i in range(image.shape[0] + 1):
    cv2.line(grid_image, (0, i * cell_size), (grid_width, i * cell_size), 0, 1)

for j in range(image.shape[1] + 1):
    cv2.line(grid_image, (j * cell_size, 0), (j * cell_size, grid_height), 0, 1)

# Sauvegarde sous forme d'image
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

filename, ext = os.path.splitext(os.path.basename(image_path))
output_path = os.path.join(output_dir, f"{filename}_grid{ext}")

cv2.imwrite(output_path, grid_image)
print(f"✅ Image avec grille enregistrée sous : {output_path}")
