import cv2
import numpy as np
import sys
import os

# Vérification des arguments
if len(sys.argv) < 2:
    print("Usage: python binary_grid.py <chemin_image_ou_dossier> [easy] [chemin_sortie] ")
    exit()

input_path = sys.argv[1]

#Définition de la difficulté (optionnel)
easy = True if (len(sys.argv) > 2 and sys.argv[2] == "true") else False

# Définir le dossier de sortie (optionnel)
output_dir = sys.argv[3] if len(sys.argv) > 3 else "output/grid_cells"

# Fonction pour traiter une seule image
def process_image(image_path, output_dir, easy):
    # Charger l'image en noir et blanc (binaire)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"❌ Erreur : Impossible de charger {image_path}")
        return

    os.makedirs(output_dir, exist_ok=True)  # Création du dossier si nécessaire

    # Vérifier que l'image est bien binaire (contient uniquement 0 et 255)
    unique_values = np.unique(image)
    if not np.array_equal(unique_values, [0, 255]) and not np.array_equal(unique_values, [0]) and not np.array_equal(unique_values, [255]):
        print(f"⚠️ Attention : L'image '{image_path}' ne semble pas être strictement binaire (0 et 255 uniquement).")

    # Convertir : noir (0) → 0, blanc (255) → 1
    binary_matrix = (image == 0).astype(np.uint8)

    # Définir la taille des cellules (pixels de la grille)
    cell_size = 20  # Taille des cases

    # Dimensions de l'image finale
    grid_height = image.shape[0] * cell_size + 1
    grid_width = image.shape[1] * cell_size + 1

    # Créer une image blanche pour la grille
    binary = np.ones((grid_height, grid_width), dtype=np.uint8) * 255  # Image en niveaux de gris
    if not easy: grid_image = np.ones((grid_height, grid_width), dtype=np.uint8) * 255

    # Ajustement pour centrer le texte (légèrement décalé en bas à gauche)
    text_offset_x = cell_size // 5  # Décalage vers la gauche
    text_offset_y = cell_size // 1.2  # Décalage vers le bas

    if easy:
        # Ajouter la grille et les nombres
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                value = binary_matrix[i, j]  # 0 ou 1

                # Position du texte légèrement décalée en bas à gauche
                text_position = (j * cell_size + text_offset_x, i * cell_size + int(text_offset_y))

                # Placer le texte en noir (0) sur fond blanc
                cv2.putText(binary, str(value), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 1, cv2.LINE_AA)

        # Dessiner la grille (lignes noires)
        for i in range(image.shape[0] + 1):
            y = i * cell_size
            cv2.line(binary, (0, y), (grid_width-1, y), 0, 1)

        for j in range(image.shape[1] + 1):
            x = j * cell_size
            cv2.line(binary, (x, 0), (x, grid_height-1), 0, 1)
    else:
        # Ajouter la grille et les nombres
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                value = binary_matrix[i, j]  # 0 ou 1

                # Position du texte légèrement décalée en bas à gauche
                text_position = (j * cell_size + text_offset_x, i * cell_size + int(text_offset_y))

                # Placer le texte en noir (0) sur fond blanc
                cv2.putText(binary, str(value), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 1, cv2.LINE_AA)

        # Dessiner la grille (lignes noires)
        for i in range(image.shape[0] + 1):
            y = i * cell_size
            cv2.line(grid_image, (0, y), (grid_width-1, y), 0, 1)

        for j in range(image.shape[1] + 1):
            x = j * cell_size
            cv2.line(grid_image, (x, 0), (x, grid_height-1), 0, 1)

        start_point = (10, grid_height - 5)
        end_point = (10, grid_height - 14)
        color = (0)
        thickness = 1
        tipLength = 0.5

        cv2.arrowedLine(grid_image, start_point, end_point, color, thickness, tipLength=tipLength)



    # Sauvegarde sous forme d'image
    filename, ext = os.path.splitext(os.path.basename(image_path))
    output_path = os.path.join(output_dir, f"{filename}_grid{ext}")

    if easy:
        # En mode easy, seule l'image "binary" est utilisée
        cv2.imwrite(output_path, binary)
    else:
        # En mode non-easy, on a créé "grid_image" et on sauvegarde également "binary"
        binary_output_path = os.path.join(output_dir, f"{filename}_binary{ext}")
        cv2.imwrite(output_path, grid_image)
        cv2.imwrite(binary_output_path, binary)

# Vérifier si le chemin est un fichier ou un dossier
if os.path.isfile(input_path):
    # Appliquer la méthode sur le fichier donné
    process_image(input_path, output_dir,easy)
elif os.path.isdir(input_path):
    # Appliquer la méthode sur toutes les images du dossier
    for file in os.listdir(input_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(input_path, file)
            process_image(file_path, output_dir,easy)
else:
    print(f"❌ Erreur : Le chemin '{input_path}' n'existe pas ou n'est ni un fichier ni un dossier.")
    exit()
