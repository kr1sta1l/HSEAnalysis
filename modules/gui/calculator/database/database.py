import sqlite3


class Database:
    def __init__(self):
        pass

    def init_db(self, path, init_command) -> bool:
        try:
            Database.execute(Database.get_cursor(Database.connect(path)), init_command)
        except Exception:
            return False
        return True

    @staticmethod
    def connect(path):
        return sqlite3.connect(path)

    @staticmethod
    def get_cursor(connection):
        return connection.cursor()

    @staticmethod
    def execute(cursor, command):
        return cursor.execute(command)

    @staticmethod
    def commit(connection):
        connection.commit()

    @staticmethod
    def close(connection):
        connection.close()

    @staticmethod
    def fetchall(cursor):
        return cursor.fetchall()
