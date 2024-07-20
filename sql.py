import sqlite3
from sqlite3 import Error
from faker import Faker
import random


def create_connection(db_file):
    """ Create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established")
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created")
    except Error as e:
        print(e)


def insert_data(conn, student):
    """ Insert a new student into the STUDENT table """
    sql = ''' INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()
    return cur.lastrowid


def main():
    database = "studentt.db"

    sql_create_student_table = """
    CREATE TABLE IF NOT EXISTS STUDENT (
        NAME TEXT NOT NULL,
        CLASS TEXT NOT NULL,
        SECTION TEXT NOT NULL,
        MARKS INTEGER NOT NULL
    );"""

    # Initialize Faker
    fake = Faker()

    # Sample data
    classes = ['Data Science', 'DEVOPS', 'Computer Science', 'Information Technology', 'Mathematics']
    sections = ['A', 'B', 'C', 'D']
    marks_range = (0, 100)

    students = []

    # Generate random student data
    for _ in range(100):  # Adjust the range for the desired number of records
        name = fake.name()
        student_class = random.choice(classes)
        section = random.choice(sections)
        marks = random.randint(*marks_range)
        students.append((name, student_class, section, marks))

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_student_table)

        for student in students:
            insert_data(conn, student)

        print("The inserted records are:")
        cur = conn.cursor()
        cur.execute("SELECT * FROM STUDENT")

        rows = cur.fetchall()
        for row in rows:
            print(row)

        conn.close()
    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()
