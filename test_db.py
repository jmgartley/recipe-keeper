import sqlite3

conn = sqlite3.connect("recipes.db")
conn.executescript(open("schema.sql").read())

cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

conn.close()