import sys
import subprocess
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <chemin_image> <nombre_de_classes> [easy]")
        exit()

    image_path = sys.argv[1]
    level = sys.argv[2]
    easy = sys.argv[3] if (len(sys.argv) > 3 and sys.argv[3] == "true") else "false"

    if not os.path.exists(image_path):
        print(f"❌ Erreur : L'image '{image_path}' n'existe pas.")
        exit()

    # Récupérer le nom de base sans extension
    filename, ext = os.path.splitext(os.path.basename(image_path))

    print("🔹 Pixelisation de l'image...")
    subprocess.run(["python", "pixelize.py", image_path, level], check=True)

    # Définition des chemins des fichiers générés par pixelize.py
    pixelized_path = os.path.join("output", f"{filename}_pixelized{ext}")
    pixelized_small_path = os.path.join("output", f"{filename}_pixelized_small{ext}")

    # Vérification que les fichiers existent bien
    for path in [pixelized_path, pixelized_small_path]:
        if not os.path.exists(path):
            print(f"❌ Erreur : L'image pixelisée '{path}' n'a pas été trouvée.")
            exit()

    print("🔹 Conversion des images en noir et blanc...")

    # Appliquer la conversion noir et blanc aux deux versions
    subprocess.run(["python", "colorToBlackWhite.py", pixelized_path], check=True)
    subprocess.run(["python", "colorToBlackWhite.py", pixelized_small_path], check=True)

    # Définition des chemins des fichiers noir et blanc
    bw_path = os.path.join("output", f"{filename}_pixelized_bw{ext}")
    bw_small_path = os.path.join("output", f"{filename}_pixelized_small_bw{ext}")

    # Vérification que les fichiers noir et blanc ont bien été créés
    for path in [bw_path, bw_small_path]:
        if not os.path.exists(path):
            print(f"❌ Erreur : L'image noir & blanc '{path}' n'a pas été trouvée.")
            exit()

    print("🔹 Génération des cellules")
    subprocess.run(["python", "splitImage.py", bw_small_path, level], check=True)

    # Définition du chemin de l'image avec la grille
    cell_path = os.path.join("output/cells")

    if not os.path.exists(cell_path):
        print(f"❌ Erreur : Les cellules n'ont pas été trouvées.")
        exit()

    # Exécuter binaryGrid.py sur l'image
    subprocess.run(["python", "binaryGrid.py", cell_path, easy], check=True)

    # Vérifier que le dossier est bien créé
    grid_path = os.path.join("output/grid_cells")

    if not os.path.exists(grid_path):
        print(f"❌ Erreur : Les images avec grille '{grid_path}' n'ont pas été trouvées.")
        exit()

    print(f"✅ Processus terminé !")
    print(f"📂 Image pixelisée : {pixelized_path}")
    print(f"📂 Image pixelisée réduite : {pixelized_small_path}")
    print(f"📂 Image noir & blanc pixelisée : {bw_path}")
    print(f"📂 Image noir & blanc réduite : {bw_small_path}")
    print(f"📂 Image découpé : {cell_path}")
    print(f"📂 Images avec grille : {grid_path}")
