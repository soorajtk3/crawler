import requests
import os
import wget
from bs4 import BeautifulSoup
header = {
    'User-Agent': 'Mozilla/5.0 (MacintoshIntel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def get_image(site_url):
    ret = []
    r = requests.get(url=site_url, headers=header)
    soup = BeautifulSoup(r.content, features="html.parser")
    gallery = soup.find(
        "div", {"class": "GalleryItems-module__searchContent___DbMmK"})
    link = gallery.find_all("a")
    for i in link:
        ret.append((i.text, i['href']))
    return ret


def image_download(url):
    ret = []
    r = requests.get(url=url, headers=header)
    soup = BeautifulSoup(r.content, features="html.parser")
    image_div = soup.find("img", {"class": "AssetCard-module__image___dams4"})
    x = image_div['src']
    print(x, "\n")
    return x


def main():
    links = get_image("https://www.gettyimages.in/photos/aamir-khan-actor")
    head = "https://www.gettyimages.in"
    os.mkdir("images")

    for name, link in links:
        wget.download(image_download(head+link))


if __name__ == "__main__":
    main()
