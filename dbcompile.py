import sqlite3
import sys
import os

with open("temp/schema.sql", "r") as f:
    schem = f.read()

db_path = "temp/notdoingshit.db" 
try:
    with sqlite3.connect("temp/notdoingshit.db") as conn:
        cur = conn.cursor()
        if not os.path.exists(db_path):
            cur.executescript(schem)
        cur.execute("SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='compile_test'")
        r = cur.fetchall()
        if r[0][0] != 1:
            cur.executescript(schem)
        cur.execute("INSERT INTO compile_test VALUES (1 , 'loves you', 'bettylovesyou.com')")
        cur.execute("SELECT * FROM compile_test")
        r = cur.fetchall()
        print(r)
        cur.close()
finally:
    print("Goodbye")


