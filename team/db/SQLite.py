import sqlite3
from pathlib import Path

from flask import g

from team.model.captain import Captain
from team.model.player import Player


class SQLiteDatabase:
    @staticmethod
    def __get_db():
        if 'db' not in g:
            g.db = sqlite3.connect('storage/sqlite.db')
        return g.db

    @staticmethod
    def init_db():
        db = SQLiteDatabase.__get_db()
        print(Path(__file__).with_suffix('.db'))
        with open(Path(__file__).with_name('scheme.sql'), 'r') as f:
            db.executescript(f.read())
        db.commit()

    @staticmethod
    def close_db():
        if 'db' in g and (db := g.db) is not None:
            db.close()

    @staticmethod
    def reset():
        db = SQLiteDatabase.__get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM player")
        cursor.execute("DELETE FROM captain")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='player'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='captain'")
        cursor.close()
        db.commit()

    @staticmethod
    def get_record(id: int):
        db = SQLiteDatabase.__get_db()
        cursor = db.cursor()
        query = cursor.execute("""
            SELECT player.*, captain.grade FROM player
            LEFT JOIN captain
                ON player.id == captain.id
            WHERE player.id = ?
        """, (id,))
        record = query.fetchone()
        record = Player(*record[:5]) if record[5] is None else Captain(*record)
        cursor.close()
        return record

    @staticmethod
    def get_records():
        db = SQLiteDatabase.__get_db()
        cursor = db.cursor()
        query = cursor.execute("""
            SELECT player.*, captain.grade FROM player
            LEFT JOIN captain
                ON player.id == captain.id
        """)
        records = []
        for record in query:
            record = Player(*record[:5]) if record[5] is None else Captain(*record)
            records.append(record)
        cursor.close()
        return records

    @staticmethod
    def add_record(item):
        db = SQLiteDatabase.__get_db()
        cursor = db.cursor()
        query = "INSERT INTO player(firstname, lastname, age, experience) VALUES (?,?,?,?)"
        cursor.execute(query, (item.firstname, item.lastname, item.age, item.experience))
        item.id = cursor.lastrowid
        if type(item) == Captain:
            query = "INSERT INTO captain VALUES (?,?)"
            cursor.execute(query, (item.id, item.grade))
        cursor.close()
        db.commit()

    @staticmethod
    def edit_record(item):
        db = SQLiteDatabase.__get_db()
        cursor = db.cursor()
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
        cursor.close()
        db.commit()

    @staticmethod
    def delete_record(id: int):
        db = SQLiteDatabase.__get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM player WHERE id = ?", (id,))
        cursor.execute("DELETE FROM captain WHERE id = ?", (id,))
        cursor.close()
        db.commit()
