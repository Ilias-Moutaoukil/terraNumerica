import cv2
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pixelize.py <chemin_image> <nombre_de_classes>")
        exit()

    image_path = sys.argv[1]
    level = int(sys.argv[2])

    image = cv2.imread(image_path)
    if image is None:
        print(f"Erreur : Impossible de charger l'image à {image_path}")
        exit()

    original_height, original_width = image.shape[:2]
    target_pixels = level * 10_000
    scale_factor = (target_pixels / (original_width * original_height)) ** 0.5

    new_width = max(1, int(original_width * scale_factor))
    new_height = max(1, int(original_height * scale_factor))

    small_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    pixelated_image = cv2.resize(small_image, (original_width, original_height), interpolation=cv2.INTER_NEAREST)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.basename(image_path)
    filename_without_ext, ext = os.path.splitext(filename)

    output_small_path = os.path.join(output_dir, f"{filename_without_ext}_pixelized_small{ext}")
    cv2.imwrite(output_small_path, small_image)

    output_pixelized_path = os.path.join(output_dir, f"{filename_without_ext}_pixelized{ext}")
    cv2.imwrite(output_pixelized_path, pixelated_image)
