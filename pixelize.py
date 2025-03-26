import cv2
import sys
import os

if __name__ == "__main__":
    # Vérifier si les arguments sont donnés
    if len(sys.argv) < 3:
        print("Usage: python pixelize.py <chemin_image> <nombre_de_classes>")
        exit()

    # Récupérer l'image depuis les arguments
    image_path = sys.argv[1]

    # Récupérer le nombre de classes
    level = int(sys.argv[2])

    # Charger l'image
    image = cv2.imread(image_path)

    # Vérifier si l'image a été chargée
    if image is None:
        print(f"Erreur : Impossible de charger l'image à {image_path}")
        exit()

    # Obtenir les dimensions originales
    original_height, original_width = image.shape[:2]

    # Calculer le nombre de pixels cible
    target_pixels = level * 10_000  # 10 000 pixels par niveau

    # Calculer le facteur de réduction
    scale_factor = (target_pixels / (original_width * original_height)) ** 0.5

    # Calculer les nouvelles dimensions (réduction)
    new_width = max(1, int(original_width * scale_factor))
    new_height = max(1, int(original_height * scale_factor))

    # Redimensionner l'image vers la petite version pixelisée
    small_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # Ré-agrandir à la taille originale en conservant l'effet pixelisé
    pixelated_image = cv2.resize(small_image, (original_width, original_height), interpolation=cv2.INTER_NEAREST)

    # Créer le dossier output s'il n'existe pas
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Nom du fichier de sortie
    filename = os.path.basename(image_path)
    filename_without_ext, ext = os.path.splitext(filename)

    # 🔹 Enregistrer l'image réduite (non upscalée)
    output_small_path = os.path.join(output_dir, f"{filename_without_ext}_pixelized_small{ext}")
    cv2.imwrite(output_small_path, small_image)
    print(f"Image réduite enregistrée sous : {output_small_path}")

    # 🔹 Enregistrer l'image pixelisée (upscalée)
    output_pixelized_path = os.path.join(output_dir, f"{filename_without_ext}_pixelized{ext}")
    cv2.imwrite(output_pixelized_path, pixelated_image)
    print(f"Image pixelisée enregistrée sous : {output_pixelized_path}")
