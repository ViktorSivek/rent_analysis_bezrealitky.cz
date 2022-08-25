from bs4 import BeautifulSoup
import requests
from csv import writer
import re

# Postupně vyhledává na každé page
for page in range(1, 201):
    # url = "https://www.bezrealitky.cz/vypis/nabidka-pronajem/byt"
    url = "https://www.bezrealitky.cz/vypis/nabidka-pronajem/byt?page={page}".format(page=page)
    print(url)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    lists = soup.find_all('article', class_="propertyCard")

    # Generuje csv soubor
    with open('pronajmy.csv', 'a', encoding='utf8', newline='') as f:
        thewriter = writer(f)
        # header = ['Lokace', 'Velikost', 'Metry2', 'Cena', 'Sluzby']
        # thewriter.writerow(header)

        # Vyhledává informace
        for list in lists:
            title = list.find('span', class_="PropertyCard_propertyCardAddress__yzOdb").text
            title = str(title).replace(",", "")
            size2 = list.find('ul', class_="FeaturesList_featuresList__W4KSP featuresList mt-3").text
            size2 = str(size2).replace("kk", "k").replace("Garsoniéra", "Gar")
            size = size2[0:3].replace("k", "kk").replace("Gar", "Garsoniéra")
            metres2 = size2[3:].replace("m²", "")
            price2 = list.find('p', class_="propertyPrice").text
            price = str(price2).replace("\xa0", "").split(" ")[0].replace("Kč", "")
            try:
                services = str(price2).replace("\xa0", "").split(" ")[1].replace("Kč", "")
            except:
                services = "0"

            info = [title, size, metres2, price, services]
            thewriter.writerow(info)

            print(info)
