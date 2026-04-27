# Projet2
fichiers du projet numéro 2

Avant l'utilisation du script nommé ETL.py, utiliser un environnement virtuel avec venv à travers un terminal en faisant : "python -m venv env" puis en l'activant avec : "source env/Scripts/activate"

Installer le fichier requirements.txt avec : "pip install -r requirements.txt"

Ensuite lancer le script.

Ce script est détaillé et notifié grâce à des # tout le long des lignes de code si besoin.

Il va interroger le site https://books.toscrape.com/index.html

Si le site répond et est fonctionnel, le script s'appliquera.

Ce script récupère toutes les catégories disponibles. Si des catégories se rajoutent, cela fonctionnera pour elles aussi.

Dans chaque catégorie, le script va récupérer, page par page, les infos de tous les livres : prix ht et ttc, upc, titre, résumé, lien du livre, lien de l'image, notation et nombre disponible et le mettre dans un fichier CSV nommé d'après la catégorie (ex: mystery.csv)

Il va aussi créer un dossier "images" contenant toutes les images de livres disponibles, en fonction de l'upc du livre, afin d'éviter les doublons.

Si des livres s'ajoutent et créent de nouvelles pages, le script fonctionnera également.

Script Bonus : Permet de récupérer une catégorie sélectionnée avec ses images incluses afin d'alléger le process.

Au lancement, le script demande de saisir le nom d'une catégorie.

Tapez 'exit' pour quitter.
