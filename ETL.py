# import pour les modules
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os # module pour interagir avec le systeme d'exploitation
os.makedirs("images", exist_ok=True) #crée un dossier images s'il n'existe pas déjà, mis au début car en dehors des boucles, un seul fichier suffit, même s'il détécte, ça encombre moins le calcul
os.makedirs("categories", exist_ok=True) #crée un dossier csv pour ranger les catégories

# on demande de parser la page Home en utilisant beautifulsoup
# on crée la variable soup qui contient le code html de la page Home
home = requests.get("https://books.toscrape.com/")
soup = BeautifulSoup(home.text, "html.parser")
# on trouve la balise ul qui a pour classe nav-list et on trouve la balise li à l'intérieur de cette balise
nav = soup.find("ul", class_="nav-list").find("ul")
liste_categories = nav.find_all("li")
# on crée les en-tetes de notre fichier csv
en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
           "number_available", "product_description", "category", "review_rating", "image_url"]
# on demande de trouver la categorie dans la variable categories
for categorie in liste_categories:
    # on récupère la balise a qui est dans la variable categorie (dans le li)
    a = categorie.find("a")
    # on récupère le texte du lien (la catégorie), le strip() enlève les espaces
    name = a.text.strip()
    # on crée la variable href qui récupère l'attribut href des balises a
    href = a["href"]
    # on demande ensuite de ne garder que le slug du l'url : exemple travel_2, etc.
    slug = href.replace("catalogue/category/books/", "").replace("/index.html", "")
    # on reconstruit l'url
    base_url = "https://books.toscrape.com/" + href

    # on crée la liste Links qui va garder les liens des livres de la catégorie
    Links = []
    # on initialise les numéros des pages
    i = 1
    # on lance maintenant la boucle pour scrapper les pages de chaque catégorie
    while True:
        # la page 1 est différente de la page 2 et 3.. donc on précise.
        if i == 1:
            url = f"https://books.toscrape.com/catalogue/category/books/{slug}/index.html"
        else:
            url = f"https://books.toscrape.com/catalogue/category/books/{slug}/page-{i}.html"
        # on télécharge la page, si le statut http n'est pas 200, la boucle s'arrête car le site ne fonctionne pas.
        page = requests.get(url)
        if not page.ok:
            break
        # on parse la page et on trouve les balises div qui ont pour classe image_container, c'est dans ces balises que se trouvent les liens des livres
        if page.ok:
            soup = BeautifulSoup(page.text, "html.parser")
            product_page_url = soup.find_all("div", class_="image_container")

            #on récupère les liens des livres product_page_url dans la variable product_page_url
            for container in product_page_url:
                # on crée la variable a qui contient les balises a qui sont dans la variable container
                a = container.find("a")
                # si a existe et que l'attribut href existe, on ajoute l'url dans la liste Links
                if a and "href" in a.attrs:
                    # on transforme l'url en url absolue en utilisant la fonction urljoin de la librairie urllib.parse'
                    Link = urljoin(url, a["href"])
                    # on fait une liste avec les urls des livres
                    Links.append(Link)
        # page suivante
        i += 1
    # fin de la boucle
    # on crée le nom du fichier en fonction du nom de la catégorie, on met tout en minuscule et on remplace les espaces par des underscores
    nom_fichier = f"categories/{name.lower().replace(' ', '_')}.csv"
    # on demande de créer un fichier catégories en utilisant la variable nom_fichier
    with open(nom_fichier, "w", newline="", encoding="utf-8") as fichier:
       # on ouvre le fichier
        writer = csv.writer(fichier)
       # on crée la liste en-tete
        writer.writerow(en_tete)

        # on scrape pour chaque livres de la liste Links
        for link in Links:
            page = requests.get(link)
            page.encoding = "utf-8"
            if page.ok:
                soup = BeautifulSoup(page.text, "html.parser")
                table = soup.find("table", class_="table table-striped")
                tds = table.find_all("td")

                universal_product_code = tds[0].text
                price_including_tax = tds[3].text
                price_excluding_tax = tds[2].text
                number_available = tds[5].text

                title = soup.find("h1").text

                description = soup.find("div", id="product_description")
                product_description = description.find_next("p").text if description else ""

                category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text

                review = soup.find("p", class_="star-rating")
                review_rating = review["class"][1] if review else ""

                image = soup.find("img")
                image_url = urljoin(link, image["src"]) #on crée l'url de l'image en utilisant la fonction urljoin de la librairie urllib.parse

                img = requests.get(image_url).content # on télécharge l'image en utilisant requests.get et on récupère le contenu binaire de l'image avec .content

                image_filename = f"images/{universal_product_code}.jpg" # on demande que le nom soit celui de l'upc du livre dans le dossier images pour éviter les doublons
                with open(image_filename, "wb") as titreimage: # on ouvre le fichier en mode binaire pour écrire l'image
                    titreimage.write(img) # on prend les octets de img, on les écrit dans titreimage
                # on écrit tout ça dans le fichier csv
                writer.writerow(
                    [link, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,
                     product_description, category, review_rating, image_url])
