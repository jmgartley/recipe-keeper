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

@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    conn = get_db()
    recipe = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()

    ingredients = conn.execute("""
    SELECT ingredients.name, recipe_ingredients.quantity, recipe_ingredients.unit
    FROM recipe_ingredients
    JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id
    WHERE recipe_ingredients.recipe_id = ?
    """, (recipe_id,)).fetchall()

    tools = conn.execute("""
    SELECT tools.name
    FROM recipe_tools
    JOIN tools ON recipe_tools.tool_id = tools.id
    WHERE  recipe_tools.recipe_id = ?
    """, (recipe_id,)).fetchall()

    tags = conn.execute("""
    SELECT tags.name
    FROM recipe_tags
    JOIN tags ON recipe_tags.tag_id = tags.id
    WHERE recipe_tags.recipe_id = ?
    """, (recipe_id,)).fetchall()

    cook_log = conn.execute("""
    SELECT *
    FROM cook_log
    WHERE recipe_id = ?
    ORDER BY date_made DESC
    """, (recipe_id,)).fetchall()

    conn.close()
    return render_template("recipe_detail.html", recipe=recipe, ingredients=ingredients, tools=tools, tags=tags, cook_log=cook_log)

@app.route("/recipe/<int:recipe_id>/log", methods=["POST"])
def add_cook_log(recipe_id):
    conn = get_db()
    conn.execute(
        "INSERT INTO cook_log (recipe_id, date_made, notes) VALUES (?, ?, ?)", 
        (recipe_id, request.form.get("date_made") or None, request.form.get("notes") or None)
    )

    conn.commit()
    conn.close()
    return redirect(f"/recipe/{recipe_id}")

@app.route("/add", methods=["POST"])
def add():
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO recipes (title, prep_time, cook_time, rating, source, instructions) VALUES (?, ?, ?, ?, ?, ?)",
        (
            request.form["title"],
            request.form.get("prep_time") or None,
            request.form.get("cook_time") or None,
            request.form.get("rating") or None,
            request.form.get("source") or None,
            request.form.get("instructions") or None
        )
    )
    recipe_id = cursor.lastrowid

    quantities = request.form.getlist("ingredient_quantity")
    units = request.form.getlist("ingredient_unit")
    ingredients = request.form.getlist("ingredient_name")

    for qty, unit, ingr in zip(quantities, units, ingredients):
        if ingr.strip():
            ingredient_id = get_or_create(conn, "ingredients", ingr.strip())
            conn.execute(
                "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (?, ?, ?, ?)",
                (recipe_id, ingredient_id, qty or None, unit or None)
            )

    tools = request.form.getlist("tool_name")

    for tool in tools:
        if tool.strip():
            tool_id = get_or_create(conn, "tools", tool.strip())
            conn.execute(
                "INSERT INTO recipe_tools (recipe_id, tool_id) VALUES (?, ?)",
                (recipe_id, tool_id)
            )

    tags = request.form.getlist("tag_name")
    
    for tag in tags:
        if tag.strip():
            tag_id = get_or_create(conn, "tags", tag.strip())
            conn.execute(
                "INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)",
                (recipe_id, tag_id)
            )

    conn.commit()
    conn.close()
    return redirect("/")


def get_or_create(conn, table, name):
    row = conn.execute(f"SELECT id FROM {table} WHERE name = ?", (name,)).fetchone()
    if row:
        return row["id"]
    cursor = conn.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
    return cursor.lastrowid

if __name__ == "__main__":
    app.run(debug=True)