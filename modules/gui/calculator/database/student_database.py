import os
import sqlite3
from .database import Database
from .file_reader import FileReader
from .keywords.keywords import students_keywords
from .keywords.keywords import training_programs_keywords
from .keywords.keywords import students_banned_keywords


class StudentsDatabase(Database):
    def __init__(self, path):
        super().__init__()
        self.path = path
        init_command = """
            CREATE TABLE IF NOT EXISTS "student" (
                "fio"	TEXT NOT NULL,
                "status"	INTEGER,
                "emails"	TEXT,
                "numbers"	TEXT,
                "dislocation"	TEXT,
                "school"	TEXT,
                "post"	TEXT,
                "how_know"	TEXT,
                "educational_program"	TEXT,
                "list_of_courses"	TEXT,
                "mentions"	TEXT
            );
        """
        self.init_db(path, init_command)

    @staticmethod
    def delete_db(path):
        try:
            os.remove(path)
        except Exception:
            pass

    def __get_cursor_and_connection(self, is_dict = False):
        connection = self.connect(self.path)
        connection.row_factory = sqlite3.Row if is_dict else None
        cur = self.get_cursor(connection)
        return cur, connection

    def save_student(self, student):
        try:
            cur, connection = self.__get_cursor_and_connection()
        except Exception:
            return False
        self.execute(cur, self.student_to_sql(student))
        self.commit(connection)

    @staticmethod
    def student_to_sql(student):
        return f'INSERT INTO student VALUES {student.to_sql()}'

    def get_all(self):
        cur, connection = self.__get_cursor_and_connection(is_dict=True)
        self.execute(cur, "SELECT * FROM student")
        return self.fetchall(cur)

    @staticmethod
    def save_data(excel_path, save_path):
        fr = FileReader(excel_path, students_keywords, training_programs_keywords,
                        students_banned_keywords)
        slovar = {}
        a = fr.read_workbook(excel_path, slovar)
        fr.join_repetitions(a)
        StudentsDatabase.delete_db(save_path)

        sdb = StudentsDatabase(save_path)

        for i in a:
            sdb.save_student(a[i][0])
