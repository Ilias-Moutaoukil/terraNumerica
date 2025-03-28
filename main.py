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
    easy = sys.argv[3] if (len(sys.argv) > 3 and sys.argv[3] == "true") else "false"

    if not os.path.exists(image_path):
        print(f"❌ Erreur : L'image '{image_path}' n'existe pas.")
        exit()

    # Vider l'output
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
    subprocess.run(["python", "binaryGrid.py", cell_path, easy], check=True)

    # Vérifier que le dossier est bien créé
    grid_path = os.path.join("output/grid_cells")

    if not os.path.exists(grid_path):
        print(f"❌ Erreur : Les images avec grille '{grid_path}' n'ont pas été trouvées.")
        exit()

    output_pdf = "output/output.pdf"
    images_folder = grid_path  # Ton dossier d’images
    logo_path = "ressources/logo.png"  # Logo en haut
    pdfmetrics.registerFont(TTFont("DejaVu", "ressources/DejaVuSans.ttf"))
    page_width, page_height = A4
    margin = 50  # Marge haute et basse réduite

    # Taille max de l'image principale (légèrement réduite)
    max_img_width = page_width - 2 * margin
    max_img_height = page_height - 350  # Plus de place pour logo + texte

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

    # Récupération des images
    image_files = sorted([
        f for f in os.listdir(images_folder)
        if f.lower().endswith('binary.png')
    ])

    # Création du PDF
    c = canvas.Canvas(output_pdf, pagesize=A4)

    for page_num, image_name in enumerate(image_files, start=1):
        image_path = os.path.join(images_folder, image_name)

        y_cursor = page_height - margin  # On commence depuis le haut

        # Logo
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path)
            logo_ratio = logo_img.width / logo_img.height
            logo_width = logo_height * logo_ratio
            c.drawImage(logo_path, (page_width - logo_width) / 2, y_cursor - logo_height, width=logo_width,
                        height=logo_height)
            y_cursor -= logo_height + 60  # espace vide sous le logo

        # Texte
        c.setFont("DejaVu", 12)
        line_height = 16
        for line in text_lines:
            c.drawCentredString(page_width / 2, y_cursor, line)
            y_cursor -= line_height
        y_cursor -= 60  # espace après le texte

        # Image principale
        img = Image.open(image_path)
        img_width, img_height = img.size
        ratio = min(max_img_width / img_width, max_img_height / img_height)
        new_width = img_width * ratio * 0.8
        new_height = img_height * ratio * 0.8

        x = (page_width - new_width) / 2
        y = y_cursor - new_height
        c.drawImage(image_path, x, y, width=new_width, height=new_height)

        # Numéro de page en bas
        c.setFont("Helvetica", 12)
        c.drawCentredString(page_width / 2, margin / 2, f"Page {page_num}")

        c.showPage()

    c.save()
    print("✅ PDF généré :", output_pdf)

    print(f"✅ Processus terminé !")
    print(f"📂 Image pixelisée : {pixelized_path}")
    print(f"📂 Image pixelisée réduite : {pixelized_small_path}")
    print(f"📂 Image noir & blanc pixelisée : {bw_path}")
    print(f"📂 Image noir & blanc réduite : {bw_small_path}")
    print(f"📂 Image découpé : {cell_path}")
    print(f"📂 Images avec grille : {grid_path}")
