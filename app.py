from flask import Flask, g, render_template
import sqlite3

DATABASE = "database.db"

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")

def home():
    return render_template('home.html')


@app.route("/collection")

def collection():
    #sql = "SELECT book_id, book_name, image_url FROM books;"
    sql = """SELECT book_id, book_name, image_url, description
        FROM books
        ORDER BY
            CASE
                WHEN book_name GLOB '[0-9]*' THEN 1
                ELSE 0
            END ASC,
            book_name ASC"""
    results = query_db(sql)
    
    #Listing all Letters from A-Z to be used in HTML
    letters = []
    for result in results:
        letter = result[1][0]
        if letter not in letters:
            letter = letter.upper()
            letters.append(letter)
        else:
            pass
    letters.sort(key=lambda x: (x.isdigit(), x))

    #return str(results)
    return render_template('collection.html', results=results, letters=letters)


@app.route("/<int:id>")

def item(id):
    
    return render_template("item")


if __name__ == '__main__':
    app.run(debug=True)