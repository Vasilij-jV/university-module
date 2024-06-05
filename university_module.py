# -*- config: utf8 -*-
import sqlite3
from prettytable import PrettyTable


class University:

    def __init__(self, name_u, db_path):
        self.name_u = name_u
        self.conn = sqlite3.connect(db_path)
        self.curs = self.conn.cursor()

        self.curs.execute('''
            CREATE TABLE IF NOT EXISTS students(
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        ''')
        self.conn.commit()

        self.curs.execute('''
            CREATE TABLE IF NOT EXISTS grades(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                grade REAL NOT NULL,
                student_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            );
        ''')
        self.conn.commit()

    def add_student(self, name, age):
        query = 'INSERT INTO students(name, age) VALUES(?, ?)'
        self.curs.execute(query, (name, age))
        self.conn.commit()

    def add_grade(self, subject, grade, student_id):
        query = 'INSERT INTO grades(subject, grade, student_id) VALUES(?, ?, ?)'
        self.curs.execute(query, (subject, grade, student_id))
        self.conn.commit()

    def get_students(self, subject=None):
        self.curs.execute('''
                        SELECT DISTINCT students.name, students.age, grades.subject, grades.grade
                        FROM students JOIN grades ON students.student_id = grades.student_id
                    ''')
        results = self.curs.fetchall()
        self.conn.commit()

        if subject is None:
            return results
        else:
            for item_tuple in results:
                if subject in item_tuple:
                    list_tuple = [item_tuple]
                    return list_tuple


u1 = University('Urban', 'student_grade.db')
# u1.add_directly()

u1.add_student('Ivan', 26)  # id - 1
u1.add_student('Ilya', 24)
u1.add_student('Jhon', 18)  # id - 1
u1.add_student('Stive', 18)
# id - 2

u1.add_grade('Python', 4.8, 1)
u1.add_grade('PHP', 4.3, 2)
u1.add_grade('JS', 4.1, 3)
u1.add_grade('C++', 4.7, 4)

print(u1.get_students())
print(u1.get_students('Python'))
