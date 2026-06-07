import sqlite3
from flask import Flask, g, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "database.db"

app = Flask(__name__)
app.secret_key = 'bzY4Ho9WtyCoxCyyBFzb'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
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
    if 'user_id' in session and session.pop('show_welcome', False):
        flash (f"Welcome, {session['first_name']}!")
    return render_template('home.html')


@app.route("/settings")

def settings():
    if 'user_id' not in session:
        return redirect('/login')



    return render_template('settings.html')


@app.route("/collection")

def collection():
    #implement other tables in the future
    sql = """SELECT item_id, item_name, image_url, description
        FROM items
        ORDER BY
            CASE
                WHEN item_name GLOB '[0-9]*' THEN 1
                ELSE 0
            END ASC,
            item_name ASC"""
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
    sql = """SELECT item_id, item_name, image_url, description
        FROM items
        WHERE type = 'book'
        ORDER BY
            CASE
                WHEN item_name GLOB '[0-9]*' THEN 1
                ELSE 0
            END ASC,
            item_name ASC"""
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
    
    results = query_db("""SELECT item_id, item_name, image_url, description FROM items WHERE item_name LIKE ?
                       ORDER BY
                        CASE
                        WHEN item_name GLOB '[0-9]*' THEN 1
                        ELSE 0
                        END ASC,
                        item_name ASC""", ('%' + term + '%',))

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
        password_confirmation = generate_password_hash(request.form['confirm_password'])
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        if request.form['password'] == request.form['confirm_password']:

            try:
                db = get_db()
                query_db('''INSERT INTO users (email, user_name, password, first_name, last_name) 
                            VALUES (?, ?, ?, ?, ?)''',
                            (email, username, password, first_name, last_name))
                db.commit()

                return redirect('/login')
            
            except sqlite3.IntegrityError:
                flash('Email or Username already exists!')
        
        else:
            flash('Passwords do not match!')
    
    return render_template('signup.html')


#login route
@app.route("/login", methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        email_or_username = request.form['email_or_username']
        password = request.form['password']

        user_email = query_db('SELECT * FROM users WHERE email = ?', (email_or_username,), one=True)
        user_name = query_db('SELECT * FROM users WHERE user_name = ?', (email_or_username,), one=True)

        if user_email and check_password_hash(user_email['password'], password):
            session['user_id'] = user_email['user_id']
            session['first_name'] = user_email['first_name']
            session['show_welcome'] = True
            return redirect('/dashboard')
        
        if user_name and check_password_hash(user_name['password'], password):
            session['user_id'] = user_name['user_id']
            session['first_name'] = user_name['first_name']
            session['show_welcome'] = True
            return redirect('/dashboard')

        flash('Invalid credentials!')
    
    return render_template('login.html')

#dashboard route
#The dashboard is an extended home route, after successful login
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return redirect('/')
    return f"Welcome, {session['first_name']}!"


#logout route
#not linked to an html
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
            


if __name__ == '__main__':
    app.run(debug=True)