# Projet2
fichiers du projet numéro 2
Avant l'utilisation du script, utiliser ou non un environnement virtuel.
Installer le fichier requirements.txt avec : pip install -r requirements.txt
Ensuite lancer le script.
Ce script est détaillé et notifié grâce à des # tout le long des lignes de code.
Il va interroger le site https://books.toscrape.com/index.html
Si le site répond et est fonctionnel, le script s'appliquera.
Ce script récupère toutes les catégories disponibles. Si des catégories se rajoutent, cela fonctionnera pour elles aussi.
Dans chaque catégorie, le script va récupérer, page par page, les infos de tous les livres : prix ht et ttc, upc, titre, résumé, lien du livre, lien de l'image, notation et nombre disponible et le mettre dans un dossier nommé "catégories"
Il va aussi créer un dossier "images" contenant toutes les images de livres disponibles et les nommer avec l'upc du livre pour éviter les doublons.
