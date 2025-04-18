import sys
import subprocess
import os
import shutil
import re
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
    easy = len(sys.argv) > 3 and sys.argv[3] == "true"

    if not os.path.exists(image_path):
        print(f"❌ Image '{image_path}' non trouvée.")
        exit()

    if os.path.exists("./output"):
        shutil.rmtree("./output")
    os.makedirs("output", exist_ok=True)

    filename, ext = os.path.splitext(os.path.basename(image_path))

    # Gestion des formats JPG/PNG et transparence
    if ext.lower() in ['.jpg', '.jpeg']:
        img = Image.open(image_path)
        image_path = os.path.join("output", f"{filename}.png")
        img.save(image_path, "PNG")
    elif ext.lower() == '.png':
        img = Image.open(image_path)
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            background = Image.new("RGB", img.size, (255, 255, 255))
            alpha = img.split()[3] if img.mode == "RGBA" else img.split()[1]
            background.paste(img, mask=alpha)
            image_path = os.path.join("output", f"{filename}_whitebg.png")
            background.save(image_path, "PNG")
        else:
            image_path = os.path.join("output", os.path.basename(image_path))
            img.save(image_path)

    filename, ext = os.path.splitext(os.path.basename(image_path))

    # Étape 1 : Pixeliser l'image
    subprocess.run(["python", "pixelize.py", image_path, level], check=True)

    pixelized_path = os.path.join("output", f"{filename}_pixelized{ext}")
    pixelized_small_path = os.path.join("output", f"{filename}_pixelized_small{ext}")

    for path in [pixelized_path, pixelized_small_path]:
        if not os.path.exists(path):
            print(f"❌ Image manquante : {path}")
            exit()

    # Étape 2 : Convertir l'image pixelisée en noir et blanc
    subprocess.run(["python", "colorToBlackWhite.py", pixelized_path], check=True)
    subprocess.run(["python", "colorToBlackWhite.py", pixelized_small_path], check=True)

    bw_path = os.path.join("output", f"{filename}_pixelized_bw{ext}")
    bw_small_path = os.path.join("output", f"{filename}_pixelized_small_bw{ext}")

    for path in [bw_path, bw_small_path]:
        if not os.path.exists(path):
            print(f"❌ Image manquante : {path}")
            exit()

    # Étape 3 : Découper l'image en cellules individuelles
    subprocess.run(["python", "splitImage.py", bw_small_path, level], check=True)

    cell_path = os.path.join("output/cells")
    if not os.path.exists(cell_path):
        print("❌ Cellules non générées.")
        exit()

    # Étape 4 : Transformer les cellules en valeurs binaires
    subprocess.run(["python", "binaryGrid.py", cell_path, "true" if easy else "false"], check=True)

    if not os.path.exists(cell_path):
        print("❌ Cellules avec grille non trouvées.")
        exit()

    # Étape 5 : Génération du premier PDF (instructions)
    output_pdf = "output/instructions.pdf"
    images_folder = "output/grid_cells"
    logo_path = "ressources/logo.png"
    pdfmetrics.registerFont(TTFont("DejaVu", "ressources/DejaVuSans.ttf"))
    page_width, page_height = A4
    margin = 50

    if not easy:
        logo_height = 60
        text_lines = [
            "Agent secret, votre mission commence maintenant !",
            "",
            "Une organisation mystérieuse vous a envoyé un message codé…",
            "Pour le déchiffrer, suivez les instructions :",
            "",
            "■ Coloriez en noir les cases marquées avec un 1",
            "□ Laissez vides celles marquées avec un 0",
            "",
            "Une fois toutes les cases coloriées, un message secret apparaîtra !",
            "",
            "Saurez-vous découvrir ce qui se cache derrière cette énigme informatique?"
        ]

        binary_images = {
            int(m.group(1)): f
            for f in os.listdir(images_folder)
            if (m := re.match(r'cell_(\d+)_binary\.png$', f, re.IGNORECASE))
        }

        if not binary_images:
            print("⚠️ Aucune image 'binary.png' trouvée.")
            exit()

        c = canvas.Canvas(output_pdf, pagesize=A4)

        for page in sorted(binary_images):
            path = os.path.join(images_folder, binary_images[page])
            y = page_height - margin

            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_ratio = logo_img.width / logo_img.height
                logo_width = logo_height * logo_ratio
                c.drawImage(logo_path, (page_width - logo_width) / 2, y - logo_height,
                            width=logo_width, height=logo_height)
                y -= logo_height + 60

            c.setFont("DejaVu", 12)
            for line in text_lines:
                c.drawCentredString(page_width / 2, y, line)
                y -= 16
            y -= 40

            img = Image.open(path)
            ratio = min((page_width - 2 * margin) / img.width, (page_height - 350) / img.height)
            new_w, new_h = img.width * ratio * 0.8, img.height * ratio * 0.8
            c.drawImage(path, (page_width - new_w) / 2, y - new_h, width=new_w, height=new_h)

            c.setFont("Helvetica", 12)
            c.drawCentredString(page_width / 2, margin / 2, f"Page {page}")
            c.drawCentredString(page_width / 2, margin / 2 + 14, "Reportez ce numéro au dos.")

            c.showPage()

        c.save()
        print("✅ PDF généré :", output_pdf)

    # Étape 6 : Génération du second PDF (6 grilles par page pour impression)
    grid_files = sorted([f for f in os.listdir(images_folder) if f.lower().endswith('grid.png')])
    if not grid_files:
        print("⚠️ Aucune image 'grid.png' pour le PDF secondaire.")
    else:
        output_pdf_grid = "output/grid.pdf"
        c_grid = canvas.Canvas(output_pdf_grid, pagesize=A4)

        num_columns, num_rows = 2, 3
        cell_w = (page_width - 2 * margin) / num_columns
        cell_h = (page_height - 2 * margin) / num_rows

        for i, name in enumerate(grid_files):
            if i % 6 == 0 and i > 0:
                c_grid.showPage()

            col = (i % 6) % num_columns
            row = (i % 6) // num_columns
            x = margin + col * cell_w
            y = page_height - margin - (row + 1) * cell_h

            path = os.path.join(images_folder, name)
            try:
                with Image.open(path) as img:
                    scale = min((cell_w - 2) / img.width, (cell_h - 2) / img.height)
                    w, h = img.width * scale, img.height * scale
                    c_grid.drawImage(path, x + (cell_w - w) / 2, y + (cell_h - h) / 2,
                                     width=w, height=h)
            except Exception as e:
                print(f"❌ Erreur avec {path}: {e}")

        c_grid.save()
        print("✅ PDF des grilles généré :", output_pdf_grid)

    print("✅ Processus terminé !")
