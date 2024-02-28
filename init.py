import sqlite3
import os

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

create_table='''
CREATE TABLE IF NOT EXISTS  mock (
    ID       INTEGER PRIMARY KEY AUTOINCREMENT
                     UNIQUE
                     NOT NULL,
    [regexp] TEXT    NOT NULL,
    action   TEXT    NOT NULL
);
'''
cursor.execute(create_table)

conn.commit()
conn.close()

os.system("uvicorn main:app --reload")