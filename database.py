import sqlite3
from object_prototye import Movie
from object_prototye import Link
import os


def db_connection_movies(db_func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('movies.db')
        c = conn.cursor()

        with conn:
            return db_func(c, *args, **kwargs)
    return wrapper


@db_connection_movies
def init(c):
    # Now Handle by decorator
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()

    c.execute(""" CREATE TABLE IF NOT EXISTS movies (avNum TEXT PRIMARY KEY , title TEXT, coverImgUrl TEXT, release DATE)""")
    c.execute(""" CREATE TABLE IF NOT EXISTS stars (avNum TEXT, name TEXT, UNIQUE (avNum, name))""")
    c.execute(""" CREATE TABLE IF NOT EXISTS magnets (avNum TEXT, url TEXT, size TEXT, UNIQUE(avNum, url))""")
    c.execute(""" CREATE TABLE IF NOT EXISTS images (avNum TEXT, imgUrl TEXT, UNIQUE(avNum, imgUrl))""")


@db_connection_movies
def insert_movie(c, movie):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()

    # with conn:
    c.execute("INSERT OR REPLACE INTO movies VALUES (:avNum, :title, :coverImgUrl, :release)",
              {'avNum': movie.avNum,
               'title': movie.title,
               'coverImgUrl': movie.cover_img,
                   'release': movie.release_date})


@db_connection_movies
def insert_star(c, star, num):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute ("INSERT OR REPLACE INTO stars VALUES (:avNum, :name)",
              {'avNum': num,
               'name': star})


@db_connection_movies
def insert_magnet(c, link):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT OR REPLACE INTO magnets VALUES (:avNum, :magnet, :size)",
              {'avNum': link.av_num,
               'magnet': link.magnet,
               'size': link.size})


@db_connection_movies
def insert_img(c, img, num):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("INSERT OR REPLACE INTO images VALUES (:avNum, :name)",
              {'avNum': num,
               'name': img})


@db_connection_movies
def check_existence(c, av_num):
    # conn = sqlite3.connect('movies.db')
    # c = conn.cursor()
    #
    # with conn:
    c.execute("SELECT 1 FROM movies WHERE avNum=:avNum",
              {'avNum': av_num})

    if c.fetchone() is not None:
        print('data exists')
        return True
    else:
        # print('not exists')
        return False

@db_connection_movies
def check_links(c, av_num):
    c.execute("SELECT * FROM magnets WHERE avNum=:avNum", {'avNum': av_num})


if __name__ == '__main__':
    init()
    mov_1 = Movie('test', 'test', 'test', 'test')
    insert_movie(mov_1)
    link_1 = Link('test', 'test', 'test')
    insert_star('test', 'test')
    insert_img('test', 'test')
    insert_magnet(link_1)
    check_existence('test')


