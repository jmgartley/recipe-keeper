import sqlite3

conn = sqlite3.connect("recipes.db")
conn.execute("ALTER TABLE recipes ADD COLUMN instructions TEXT")
conn.commit()
conn.close()
print("Added instructions column")