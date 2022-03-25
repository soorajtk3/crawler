import requests
import os
from bs4 import BeautifulSoup
import psycopg2


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


def get_songs(artist_url):
    songs = []
    r = requests.get(artist_url)
    body = r.content
    soup = BeautifulSoup(body, features="html.parser")
    tracklist = soup.find("table", {"class": "tracklist"})
    links = tracklist.find_all("a")
    for i in links:
        songs.append((i.text, i["href"]))
    return songs


def get_lyrics(song_url):
    r = requests.get(song_url)
    body = r.content
    soup = BeautifulSoup(body, features="html.parser")
    lyrics_div = soup.find("p", {"id": "songLyricsDiv"})
    lyrics = lyrics_div.text
    return lyrics


def crawl():

    artists = get_artists("https://www.songlyrics.com/a/")
    conn = psycopg2.connect("dbname=music")
    cur = conn.cursor()
    for name, link in artists[:10]:
        cur.execute("INSERT INTO artist(name) VALUES(%s)", (name,))
        print(name)

        songs = get_songs(link)
        for song, song_link in songs[:10]:
            lyrics = get_lyrics(song_link)
            cur.execute(
                "INSERT INTO song (artist, name, lyrics) VALUES ((SELECT id from artist WHERE name=%s),%s,%s);", (name, song, lyrics,))

    conn.commit()
    conn = cur.close()
    print("DONE")


if __name__ == "__main__":
    crawl()
