import json

import pymysql
import sqlite3

import pytube_engine

with open('conf.json') as f:
    config = json.load(f)


class connection_mysql:
    def __init__(self, drink=False):
        self.conn = pymysql.connect(host='localhost', user=config["SQL_ID"], passwd=config["SQL_PASSWORD"],
                                    db=config["DB"])

        if not drink:
            self.query_1 = '''
            CREATE TABLE IF NOT EXISTS nondrink(
            id INT PRIMARY KEY,
            title LONGTEXT NOT NULL,
            author VARCHAR(255) NOT NULL,
            `date` VARCHAR(255) NOT NULL,
            `length` int NOT NULL,
            keyword LONGTEXT)
            '''
            self.query_2 = "INSERT INTO nondrink(id, title, author, date, length, keyword) VALUES(%s,%s,%s,%s,%s,%s)"
        else:
            self.query_1 = '''
            CREATE TABLE IF NOT EXISTS drink(
            id INT PRIMARY KEY,
            title LONGTEXT NOT NULL,
            author VARCHAR(255) NOT NULL,
            `date` VARCHAR(255) NOT NULL,
            `length` int NOT NULL,
            keyword LONGTEXT)
            '''
            self.query_2 = "INSERT INTO drink(id, title, author, date, length, keyword) VALUES(%s,%s,%s,%s,%s,%s)"


class connection_sqlite:
    def __init__(self, drink=False):
        self.conn = sqlite3.connect("youtube.db")

        if not drink:
            self.query_1 = '''
            CREATE TABLE IF NOT EXISTS nondrink(
            id INT PRIMARY KEY,
            title LONGTEXT NOT NULL,
            author VARCHAR(255) NOT NULL,
            `date` VARCHAR(255) NOT NULL,
            `length` int NOT NULL,
            keyword LONGTEXT)
            '''
            self.query_2 = "INSERT INTO nondrink(id, title, author, date, length, keyword)  VALUES(?,?,?,?,?,?)"
        else:
            self.query_1 = '''
                CREATE TABLE IF NOT EXISTS drink(
                id INT PRIMARY KEY,
                title LONGTEXT NOT NULL,
                author VARCHAR(255) NOT NULL,
                `date` VARCHAR(255) NOT NULL,
                `length` int NOT NULL,
                keyword LONGTEXT)
                '''
            self.query_2 = "INSERT INTO drink(id, title, author, date, length, keyword) VALUES(?,?,?,?,?,?)"


def add(youtube, con_instance):
    conn = con_instance.conn
    curs = conn.cursor()

    id = pytube_engine.hashing(youtube.title)
    title = youtube.title
    author = youtube.author
    date = str(youtube.publish_date)
    length = youtube.length
    keyword = str(youtube.keywords)

    print(id, title, author, date, length, keyword)

    curs.execute(con_instance.query_1)
    conn.commit()

    curs.execute(con_instance.query_2, (id, title, author, date, length, keyword,))
    conn.commit()


def get(id, connection, dr):
    # type: (str, connection, str("drink" or "nondrink")) -> list
    con_instance = connection()
    conn = con_instance.conn
    curs = conn.cursor()

    query = "SELECT subject FROM {0} WHERE id == {1}".format(dr, str(id))

    curs.execute(query)
    conn.commit()

    result = curs.fetchone()

    conn.close()

    return result
