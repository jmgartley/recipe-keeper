# A Recipe Tracker

A Full-Stack Recipe Manager with a relational database structure.  Built to demonstrate knowledge of SQL and Schema-Design Skills

## Features
- Add recipes with prep/cook time, rating, source, and instructions
- Track ingredients (with quantity and unit), required tools, and multiple tags per recipe (e.g. a recipe can be both a "Main" and "Vegetarian")
- Log each time you've made a recipe, with notes per instance
- View a full recipe detail page pulling together ingredients, tools, tags, instructions, and cook history
- Print a clean, distraction-free version of any recipe
- Select multiple recipes and generate a combined, aggregated grocery list.  Matching ingredients of the same units are summed, while mismatched units are kept as seperate lines
- Server-side validation throughout, including a constrained unit dropdown (with a write-in option)

## Database Design
Built around a normalized, multi-table SQL schema:
- `recipes`, `ingredients`, `tools`, and `tags` - core entities
- `recipe-ingredients` - a many-to-many junction table that also carries data unique to that pairing (i.e. quantity and unit)
- `recipe-tools` and `recipe-tags` - pure many-to-many junction tables
- `cook-log` - a one-to-many table tracking comments when making a recipe

Foreign key constraints enforce referential integrity between tables.

## Built with
- Python / Flask
- SQLite
- Jinja2 Templating
- HTML / CSS
- A small amount of Javascript (conditional fields / print trigger)

## Usage
1. Clone the repo and set up a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Create the database: `python test_db.py`
4. Run the App: `python app.py` (use `python3 app.py` on Mac/Linux)
5. Open `http://127.0.0.1:5000` in your browser

## Possible Future Additions
- Edit or delete existing recipes
- Fuzzy matching for ingredient names (Currently 'Apple' != 'Apples')
- Deployment to a Live URL
- Stylize with consistent CSS