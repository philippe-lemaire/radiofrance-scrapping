from bs4 import BeautifulSoup
import requests
import os
import sys
from string import punctuation

BASE_URL = "https://www.radiofrance.fr"


def get_soup(url):
    """From a given full url, return the soup"""
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="lxml")
    return soup


def get_mp3(href, folder, name):
    """From a relative uri, find the mp3 link and download it in folder"""
    url = BASE_URL + href

    soup = get_soup(url)
    scripts = soup.find_all("script", {"type": "application/ld+json"})
    script = scripts[1]
    script = eval(script.string)

    content_url = script["@graph"][0]["mainEntity"]["contentUrl"]
    print(f"downloading from {content_url}")
    target_folder = f"{os.path.expanduser('~')}/Téléchargements/{folder}"
    os.makedirs(target_folder, exist_ok=True)
    name = f"{name.replace(' ', '_')}.mp3"
    # nettoyage du nom du fichier pour éviter les caractères génants comme | ou /
    for punc in punctuation:
        name = name.replace(punc, "_")
    os.system(f"wget {content_url} -O {target_folder}/{name}")


def main():
    if len(sys.argv) == 1:
        print(
            "Indiquez l’url de la page du podcast à télécharger, par exemple\npython radiofrancescrapping.py https://www.radiofrance.fr/franceculture/podcasts/lectures-d-enfance"
        )
        return None
    url = sys.argv[1]

    if BASE_URL not in url:
        print(
            "commande mal formée, exemple \npython radiofrancescrapping.py https://www.radiofrance.fr/franceculture/podcasts/lectures-d-enfance"
        )
        return None

    folder = url.split("/")[-1]
    soup = get_soup(url)
    links = soup.find_all("a", {"class": "CardTitle-text qg-st4 svelte-1pxl00z"})

    for num, link in enumerate(links, start=1):
        href = link["href"]
        name = f"{num}_{link.text}"
        get_mp3(href, folder, name)


if __name__ == "__main__":
    main()
