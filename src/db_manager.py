# Manage a database of manga??? Not sure what I'm doing
from os import stat
import sqlite3

db_path = "data\manga_library.db"

def create_database():
    """First time running the program create the database"""
    try:
        with sqlite3.connect(db_path) as conn:
            libraries_table = """CREATE TABLE IF NOT EXISTS libraries (
                                    library_id INTEGER PRIMARY KEY,
                                    library_name TEXT UNIQUE,
                                    path_name TEXT);

                """
            create_table(conn, libraries_table)

            manga_table = """CREATE TABLE IF NOT EXISTS manga_series (
                                id INTEGER PRIMARY KEY,
                                local_title TEXT NOT NULL,
                                site_title TEXT,
                                site_id INTEGER,
                                my_volumes INTEGER NOT NULL,
                                eng_volumes INTEGER,
                                eng_status TEXT,
                                source_volumes INTEGER,
                                source_status TEXT,
                                has_match TEXT);
                """
            create_table(conn, manga_table)

            junction = """CREATE TABLE IF NOT EXISTS library_manga (
                            library_id INTEGER,
                            manga_id INTEGER,
                            FOREIGN KEY(library_id) REFERENCES libraries(library_id),
                            FOREIGN KEY(manga_id) REFERENCES manga(id));
                """
            create_table(conn, junction)
            
            print("Database created successfully.")
    except sqlite3.Error as e:
        print(e)


def create_table(conn, statement):
    """Creates a table for a library of manga"""

    try:
        c = conn.cursor()
        c.execute(statement)
    except sqlite3.Error as e:
        print(e)


def create_connection():
    """Connects to database or creates it if not found"""

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def insert_library(name, path):
    try:
        with create_connection() as conn:
            statement = """INSERT INTO libraries (library_name, path_name) VALUES (?, ?);"""

            cur = conn.cursor()
            cur.execute(statement, (name, path))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print("Library already exists. Moving on...")
        return False


def insert_manga(manga_list, library_name):
    with create_connection() as conn:
        cur = conn.cursor()
        find_library = """SELECT library_id from libraries WHERE library_name = ?;"""
        cur.execute(find_library, [library_name])
        library_id = cur.fetchall()[0][0]

        for manga in manga_list:
            statement = """INSERT INTO manga_series (local_title,site_title,site_id,my_volumes,
                                eng_volumes,eng_status,source_volumes,source_status,has_match) 
                                
                                VALUES (?,?,?,?,?,?,?,?,?);"""

            data = (manga.local_title,manga.site_title,manga.site_id,manga.my_volumes,
                    manga.eng_volumes,manga.eng_status,manga.source_volumes, manga.source_status,
                    manga.has_match)
            cur.execute(statement, data)
            
            cur.execute("select last_insert_rowid();")
            last_manga_id = cur.fetchall()[0][0]

            junction = """INSERT INTO library_manga (library_id, manga_id) VALUES (?,?);"""
            cur.execute(junction, (library_id, last_manga_id))

            conn.commit()


def get_libraries():
    try:
        with create_connection() as conn:
            cur = conn.cursor()
            cur.execute("""SELECT library_id, library_name from libraries""")

            return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Error in getting libraries ---> {e}")