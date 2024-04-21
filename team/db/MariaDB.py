import os

import mariadb
from flask import g

from team.model.captain import Captain
from team.model.player import Player


class MariaDatabase:
    @staticmethod
    def __get_db():
        if 'db' not in g:
            g.db = mariadb.connect(
                user=os.getenv('MARIABD_USER', default='root'),
                password=os.getenv('MARIABD_PASSWD', default='mypass'),
                host=os.getenv('MARIABD_ADDR', default='localhost'),
                port=int(os.getenv('MARIABD_PORT', default=3306)),
                database=os.getenv('MARIABD_DBNAME', default='sys')
            )
        return g.db

    @staticmethod
    def close_db():
        if 'db' in g and (db := g.db) is not None:
            db.close()

    @staticmethod
    def init_db():
        db = MariaDatabase.__get_db()
        with db.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS player;')
            cursor.execute('DROP TABLE IF EXISTS player;')
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS player 
                (
                    id         INTEGER PRIMARY KEY AUTO_INCREMENT,
                    firstname  VARCHAR(25) NOT NULL,
                    lastname   VARCHAR(25) NOT NULL,
                    age        TINYINT UNSIGNED NOT NULL,
                    experience INT UNSIGNED NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS captain 
                (
                    id    INTEGER PRIMARY KEY,
                    grade INT UNSIGNED
                )
             """)
        db.commit()

    @staticmethod
    def reset():
        db = MariaDatabase.__get_db()
        with db.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE player')
            cursor.execute('TRUNCATE TABLE captain')
        db.commit()

    @staticmethod
    def get_record(id: int):
        db = MariaDatabase.__get_db()

        with db.cursor() as cursor:
            cursor.execute("""
            SELECT player.*, captain.grade FROM player
            LEFT JOIN captain
                ON player.id = captain.id
            WHERE player.id = ?
            """, (id,))
            record = cursor.fetchone()

        record = Player(**record[:5]) if record[5] is None else Captain(**record)
        return record

    @staticmethod
    def get_records():
        db = MariaDatabase.__get_db()
        cursor = db.cursor(dictionary=True)
        query = cursor.execute("""
            SELECT *, captain.grade FROM player
            LEFT JOIN captain
                ON player.id = captain.id
        """)
        records = []
        rows = cursor.fetchall()  # Получаем все строки результата запроса
        for row in rows:
            record = Player(**row[:5]) if row.get('grade') is None else Captain(**row)
            records.append(record)
        cursor.close()
        return records

    @staticmethod
    def add_record(item):
        db = MariaDatabase.__get_db()

        with db.cursor() as cursor:
            query = "INSERT INTO player(firstname, lastname, age, experience) VALUES (?,?,?,?)"
            if item.age:
                cursor.execute(query, (item.firstname, item.lastname, int(item.age), item.experience))
            else:
                cursor.execute(query, (item.firstname, item.lastname, 0, item.experience))
            item.id = cursor.lastrowid
            if type(item) == Captain:
                query = "INSERT INTO captain VALUES (?,?)"
                cursor.execute(query, (item.id, item.grade))
        db.commit()

    @staticmethod
    def edit_record(item):
        db = MariaDatabase.__get_db()

        with db.cursor() as cursor:
            query = """
            UPDATE player
            SET firstname = ?, lastname = ?, age = ?, experience = ?
            WHERE id = ?
        """
            cursor.execute(query, (item.firstname, item.lastname, item.age, item.experience, item.id))
            if type(item) == Captain:
                query = """
                UPDATE captain
                SET grade = ?
                WHERE id = ?
            """
                cursor.execute(query, (item.grade, item.id))

    @staticmethod
    def delete_record(id: int):
        db = MariaDatabase.__get_db()
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM player WHERE id = ?", (id,))
            cursor.execute("DELETE FROM captain WHERE id = ?", (id,))

        db.commit()
