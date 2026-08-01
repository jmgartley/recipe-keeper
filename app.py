from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("recipes.db")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    recipes = conn.execute("SELECT * FROM recipes").fetchall()
    conn.close()
    return render_template("index.html", recipes=recipes)

@app.route("/add", methods=["POST"])
def add():
    conn = get_db()
    conn.execute(
        "INSERT INTO recipes (title, prep_time, cook_time,instructions, rating, source) VALUES (?, ?, ?, ?, ?, ?)",
        (
            request.form["title"],
            request.form.get("prep_time") or None,
            request.form.get("cook_time") or None,
            request.form.get("rating") or None,
            request.form.get("source") or None,
            request.form.get("instructions") or None
        )
    )
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)