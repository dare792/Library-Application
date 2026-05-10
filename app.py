import sqlite3
from flask import Flask, g, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "database.db"

app = Flask(__name__)
app.config['PASSWORD_ENCRYPTION'] = 'u19qYPA72Y98CwGtRj1Z'

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
    db = get_db
    cur = get_db().execute(query, args)
    db.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")

def home():
    if 'user_id' in session:
        return redirect('/dashboard')
        
    return render_template('home.html')


@app.route("/collection")

def collection():
    #implement other tables in the future
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
    return render_template('collection.html', results=results, letters=letters)


@app.route("/<int:id>")

def item(id):
    
    return render_template("item.html")


@app.route("/books")

def books():
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
    return render_template('collection.html', results=results, letters=letters)


#search route
@app.route("/search")

def search():
    term = request.args.get("q") #get q parameter from url
    
    results = query_db("""SELECT book_id, book_name, image_url, description FROM books WHERE book_name LIKE ?
                       ORDER BY
                        CASE
                        WHEN book_name GLOB '[0-9]*' THEN 1
                        ELSE 0
                        END ASC,
                        book_name ASC""", ('%' + term + '%',))

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

    return render_template("search.html", results=results, letters=letters, term=term)


#signup route
@app.route("/signup", methods=['GET', 'POST'])

def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        # Hash the password for security
        password = generate_password_hash(request.form['password'])
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        try:
            query_db('''INSERT INTO users (email, username, password, first_name, last_name) 
                        VALUES (?, ?, ?, ?, ?)''',
                    (email, username, password, first_name, last_name))
            return redirect('/login')
        
        except sqlite3.IntegrityError:
            flash('Email or Username already exists!')
    
    return render_template('signup.html')


#login route
@app.route("/login", methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = query_db('SELECT * FROM users WHERE email = ?', one=True)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['first_name'] = user['first_name']
            return redirect('/dashboard')
        
        flash('Invalid credentials')
    
    return render_template('login.html')

#dashboard route
#Tha dashboard is an extended home route, after successful login
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    return f"Welcome, {session['first_name']}!"


#logout route
#not linked to an html
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
            


if __name__ == '__main__':
    app.run(debug=True)