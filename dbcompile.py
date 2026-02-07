# import datetime
# import sqlite3
# import sys
# import os
# import textual
from textual.app import App
from textual.widgets import Footer, Header
import rich._unicode_data.unicode17-0-0

# with open("temp/schema.sql", "r") as f:
#     schem = f.read()

# db_path = "temp/notdoingshit.db" 
# try:
#     with sqlite3.connect("temp/notdoingshit.db") as conn:
#         cur = conn.cursor()
#         if not os.path.exists(db_path):
#             print("making db")
#             cur.executescript(schem)
#         cur.execute("SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='compile_test')")
#         r = cur.fetchall()
#         print((r[0][0]))
#         if r[0][0] != 1:
#             cur.executescript(schem)
#         cur.execute("INSERT INTO compile_test (description, imageURL) VALUES ('loves you', 'bettylovesyou.com')")
#         cur.execute("SELECT * FROM compile_test")
#         r = cur.fetchall()
#         print(r)
#         cur.close()
# finally:
#     print("Goodbye")


class CompileTest(App):
    def compose(self):
        yield Header()
        yield Footer()

if __name__ == "__main__":
    app = CompileTest()
    app.run()