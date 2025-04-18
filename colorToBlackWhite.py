import cv2
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python colorToBlackWhite.py <chemin_image>")
        exit()

    image_path = sys.argv[1]
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"Erreur : Impossible de charger l'image à {image_path}. Vérifie le chemin.")
        exit()

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(image)

    # Binarisation avec méthode d'Otsu
    _, binary_image = cv2.threshold(enhanced_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.basename(image_path)
    filename_without_ext, ext = os.path.splitext(filename)
    output_path = os.path.join(output_dir, f"{filename_without_ext}_bw{ext}")

    cv2.imwrite(output_path, binary_image)
