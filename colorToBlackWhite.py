import cv2
import sys
import os

# Vérifier si un argument est donné
if len(sys.argv) < 2:
    print("Usage: python script.py <chemin_image>")
    exit()

# Récupérer l'image depuis les arguments
image_path = sys.argv[1]

# Charger l'image en niveaux de gris
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Vérifier si l'image a été chargée correctement
if image is None:
    print(f"❌ Erreur : Impossible de charger l'image à {image_path}. Vérifie le chemin.")
    exit()

# Appliquer le seuillage binaire
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# Créer le dossier output s'il n'existe pas
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Générer le nom du fichier de sortie
filename = os.path.basename(image_path)  # Récupère "Bob1.png"
filename_without_ext, ext = os.path.splitext(filename)  # Sépare "Bob1" et ".png"
output_path = os.path.join(output_dir, f"{filename_without_ext}_bw{ext}")

# Sauvegarder l'image en noir et blanc
cv2.imwrite(output_path, binary_image)

print(f"✅ Image enregistrée sous : {output_path}")
