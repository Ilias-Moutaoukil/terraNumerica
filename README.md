# Numeric'Art

## Prérequis

- Python 3.7 ou supérieur

## Installation

1. Clonez le projet :

```bash
git clone https://github.com/Ilias-Moutaoukil/terraNumerica.git
cd terraNumerica
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

```
python main.py <chemin_image> <nombre_de_classes> [easy]
```

### Paramètres :
- **<chemin_image>** : Chemin vers l'image à traiter (formats supportés : JPG, PNG).
- **<nombre_de_classes>** : Nombre de classes participant à l'atelier (une classe représente environ 20 élèves).
- **[easy]** (optionnel) : Si ce paramètre est spécifié avec la valeur true, le script génèrera des instructions simplifiées (grilles et instructions combinées) adaptées à de très jeunes élèves. Si omis ou mis à false, les instructions seront séparées des grilles.

### Sortie :
Tous les fichiers générés seront placés dans le dossier `output`.

- **<votre_fichier>_pixelized_bw.png** : aperçu de l’image transformée en noir et blanc.
- Si le paramètre `[easy]` est défini sur `true` :
    - Un seul fichier **grid.pdf** est généré : il contient les grilles **avec instructions intégrées**, à raison de 6 par page.
- Si le paramètre `[easy]` est omis ou mis à `false` :
    - Deux fichiers sont générés :
        - **grid.pdf** : contient uniquement les grilles (6 par page).
        - **instructions.pdf** : contient les instructions individuelles pour chaque élève.
- À la fin du processus, le terminal affiche également les dimensions de la grille (en cellules), par exemple :
```
✅ Grille générée : 10 lignes x 6 colonnes (60 cellules)
```


## Bonus :
Un dossier **ressources** est fourni pour tester le code sur quelques exemples.  
Pour vos propres images, il n’est pas nécessaire de les placer dans ce dossier : il suffit de spécifier le bon chemin en argument.
