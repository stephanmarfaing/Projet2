import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

index_url = "https://books.toscrape.com/index.html"
page = requests.get(index_url)
soup = BeautifulSoup(page.text, "html.parser")
categories = {}
for a in soup.select("ul.nav-list ul a"):
    nom = a.text.strip().lower()
    lien = a["href"]  # ex: "catalogue/category/books/mystery_3/index.html"
    # On extrait la partie utile : "mystery_3"
    url_category_slug = lien.split("/")[-2]
    categories[nom] = url_category_slug
name_category = input("\nEntrez le nom de la catégorie : ").strip().lower()
if name_category not in categories:
    raise ValueError(f"Catégorie '{name_category}' inconnue ou invalide.")
os.makedirs(f"{name_category}/images", exist_ok=True)

url_category = categories[name_category]
Links = []
i = 1
while True:
    if i == 1:
        url = "https://books.toscrape.com/catalogue/category/books/" + url_category + "/index.html"
    else:
        url = f"https://books.toscrape.com/catalogue/category/books/{url_category}/page-{i}.html"
    page = requests.get(url)
    if not page.ok:
        break

    if page.ok:
        soup = BeautifulSoup(page.text, "html.parser")

        product_page_url = soup.find_all("div", class_="image_container")

        for container in product_page_url:
            a = container.find("a")
            if a and "href" in a.attrs:
                Link = urljoin(url, a["href"])
                Links.append(Link)


    i += 1
en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
           "number_available", "product_description", "category", "review_rating", "image_url"]
with open(f"{name_category}.csv", "w", newline="", encoding="utf-8") as fichierEtape2:
    writer = csv.writer(fichierEtape2, delimiter=",")
    writer.writerow(en_tete)

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
            image_url = urljoin(link, image["src"])

            img = requests.get(image_url).content

            image_filename = f"{name_category}/images/{universal_product_code}.jpg"  # on demande que le nom soit celui de l'upc du livre dans le dossier images pour éviter les doublons
            with open(image_filename, "wb") as titreimage:  # on ouvre le fichier en mode binaire pour écrire l'image
                titreimage.write(img)  # on prend les octets de img, on les écrit dans titreimage

            writer.writerow([link, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])

