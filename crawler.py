import requests
from bs4 import BeautifulSoup


def get_artists(url):
    ret = []
    r = requests.get(url)
    body = r.content
    soup = BeautifulSoup(body, features="html.parser")
    tracklist = soup.find("table", {"class": "tracklist"})
    links = tracklist.find_all("a")
    for i in links:
        ret.append((i.text, i["href"]))
    return ret


def get_songs(song_url):
    pass


def get_artists(artists_url):
    pass


def crawl():
    artists = get_artists("http://www.songlyrics.com/a/")
    for name, link in artists:
        print(name, "  :  ", link)


if __name__ == "__main__":
    crawl()
