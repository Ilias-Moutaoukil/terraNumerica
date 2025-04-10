import sys
import subprocess
import os
import shutil
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <chemin_image> <nombre_de_classes> [easy]")
        exit()

    image_path = sys.argv[1]
    level = sys.argv[2]
    easy = True if (len(sys.argv) > 3 and sys.argv[3] == "true") else False

    if not os.path.exists(image_path):
        print(f"❌ Erreur : L'image '{image_path}' n'existe pas.")
        exit()

    # Vider le dossier output
    if os.path.exists("./output"):
        shutil.rmtree("./output")

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
    subprocess.run(["python", "binaryGrid.py", cell_path, "true" if easy else "false"], check=True)

    if not os.path.exists(cell_path):
        print(f"❌ Erreur : Les images avec grille '{cell_path}' n'ont pas été trouvées.")
        exit()

    #########################################################################
    # Première partie : Génération du PDF avec les images se terminant par binary.png
    #########################################################################
    output_pdf = "output/output.pdf"
    images_folder = "output/grid_cells"  # Dossier contenant les images générées par binaryGrid.py
    logo_path = "ressources/logo.png"  # Chemin du logo
    pdfmetrics.registerFont(TTFont("DejaVu", "ressources/DejaVuSans.ttf"))
    page_width, page_height = A4
    margin = 50  # Marge haute et basse

    # Taille max de l'image principale (légèrement réduite)
    max_img_width = page_width - 2 * margin
    max_img_height = page_height - 350  # Plus de place pour le logo et le texte

    if not easy:
        # Logo dimensions
        logo_height = 60

        # Texte à insérer sous le logo
        text_lines = [
            "Agent secret, votre mission commence maintenant !",
            " ",
            "Une organisation mystérieuse vous a envoyé un message codé…",
            "Pour le déchiffrer, suivez les instructions :",
            " ",
            "■ Coloriez en noir les cases marquées avec un 1",
            "□ Laissez vides celles marquées avec un 0",
            " ",
            "Une fois toutes les cases coloriées, un message secret apparaîtra !",
            " ",
            "Saurez-vous découvrir ce qui se cache derrière cette énigme informatique?"
        ]

        # Récupération des images se terminant par binary.png
        binary_image_files = sorted([
            f for f in os.listdir(images_folder)
            if f.lower().endswith('binary.png')
        ])

        if not binary_image_files:
            print("⚠️ Aucune image se terminant par 'binary.png' n'a été trouvée pour le second PDF.")
            exit()

        # Création du PDF
        c = canvas.Canvas(output_pdf, pagesize=A4)

        for page_num, image_name in enumerate(binary_image_files, start=1):
            image_path_full = os.path.join(images_folder, image_name)
            y_cursor = page_height - margin  # Commencer depuis le haut de la page

            # Logo
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_ratio = logo_img.width / logo_img.height
                logo_width = logo_height * logo_ratio
                c.drawImage(logo_path, (page_width - logo_width) / 2, y_cursor - logo_height, width=logo_width,
                            height=logo_height)
                y_cursor -= logo_height + 60  # Espace après le logo

            # Texte
            c.setFont("DejaVu", 12)
            line_height = 16
            for line in text_lines:
                c.drawCentredString(page_width / 2, y_cursor, line)
                y_cursor -= line_height
            y_cursor -= 40  # Espace après le texte

            # Image principale
            img = Image.open(image_path_full)
            img_width, img_height = img.size
            ratio = min(max_img_width / img_width, max_img_height / img_height)
            new_width = img_width * ratio * 0.8
            new_height = img_height * ratio * 0.8

            x = (page_width - new_width) / 2
            y = y_cursor - new_height
            c.drawImage(image_path_full, x, y, width=new_width, height=new_height)

            # Numéro de page en bas
            c.setFont("Helvetica", 12)
            c.drawCentredString(page_width / 2, margin / 2, f"Page {page_num}")
            c.drawCentredString(page_width / 2, margin / 2 + 14, f"(Pensez à reporter le numéro de page au dos de votre grille)")

            c.showPage()

        c.save()
        print("✅ PDF généré :", output_pdf)

    #########################################################################
    # Deuxième partie : Génération d'un second PDF avec 6 images par page,
    # disposées en 2 colonnes et 3 lignes, avec un espace entre chaque image.
    #########################################################################
    # Récupérer les images se terminant par grid.png
    grid_image_files = sorted([
        f for f in os.listdir(images_folder)
        if f.lower().endswith('grid.png')
    ])

    if not grid_image_files:
        print("⚠️ Aucune image se terminant par 'grid.png' n'a été trouvée pour le second PDF.")
    else:
        output_pdf_grid = "output/grid_images.pdf"
        c_grid = canvas.Canvas(output_pdf_grid, pagesize=A4)

        # Nouvelle organisation : 2 colonnes et 3 lignes (6 images par page)
        num_columns = 2
        num_rows = 3

        # Définir un espacement interne (padding) dans chaque cellule
        #padding = 10  # en points

        # Calculer la taille de chaque cellule en fonction de la marge
        cell_width = (page_width - 2 * margin) / num_columns
        cell_height = (page_height - 2 * margin) / num_rows

        for i, image_name in enumerate(grid_image_files):
            # À chaque 6 images, on démarre une nouvelle page
            if i % 6 == 0 and i > 0:
                c_grid.showPage()

            idx_in_page = i % 6
            # Pour 2 colonnes :
            # - Le premier et le deuxième élément de chaque ligne sont respectivement à la colonne 0 et 1
            # - Le row index est déterminé par la division entière de l'indice par 2
            col_idx = idx_in_page % num_columns
            row_idx = idx_in_page // num_columns

            # Calcul de la position de la cellule
            x_cell = margin + col_idx * cell_width
            # La coordonnée y : on part du haut de la page (page_height - margin) et on descend d'une cellule complète pour chaque row.
            cell_bottom_y = page_height - margin - (row_idx + 1) * cell_height

            # L'espace utile dans la cellule après application du padding
            available_width = cell_width - 2 #* padding
            available_height = cell_height - 2 #* padding

            image_path_grid = os.path.join(images_folder, image_name)
            try:
                with Image.open(image_path_grid) as img:
                    img_width, img_height = img.size
            except Exception as e:
                print(f"❌ Erreur lors de l'ouverture de l'image {image_path_grid}: {e}")
                continue

            # Calculer le facteur d'échelle pour que l'image tienne dans la zone disponible
            scale = min(available_width / img_width, available_height / img_height)
            new_img_width = img_width * scale
            new_img_height = img_height * scale

            # Centrer l'image dans la zone de la cellule, en tenant compte du padding
            x_img = x_cell + (available_width - new_img_width) / 2 #+ padding
            y_img = cell_bottom_y + (available_height - new_img_height) / 2 #+ padding

            c_grid.drawImage(image_path_grid, x_img, y_img, width=new_img_width, height=new_img_height)

        c_grid.save()
        print("✅ PDF des grid images généré :", output_pdf_grid)

    print("✅ Processus terminé !")
