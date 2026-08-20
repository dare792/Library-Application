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

    #look for matches to q parameter in database
    #sort matches by alphabetical order, numbers last
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
        # Read raw passwords and validate before hashing
        password_raw = request.form['password']
        confirm_password_raw = request.form['confirm_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        #check if raw passwords match befor hashing
        if password_raw == confirm_password_raw:
            password = generate_password_hash(password_raw)
            #add users information to database
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

        #check if email and password match
        if user_email and check_password_hash(user_email['password'], password):
            session['user_id'] = user_email['user_id']
            session['first_name'] = user_email['first_name']
            session['show_welcome'] = True
            return redirect('/')

        #check if username and password match
        if user_name and check_password_hash(user_name['password'], password):
            session['user_id'] = user_name['user_id']
            session['first_name'] = user_name['first_name']
            session['show_welcome'] = True
            return redirect('/')

        flash('Invalid credentials!')
    
    return render_template('login.html')

#settings route to change or delete users information
@app.route("/settings", methods=['GET', 'POST'])
#prevent acces to settings if user is not logged in
def settings():
    if 'user_id' not in session:
        flash('Log into your account to edit it')
        return redirect('/login')
    
    return render_template('settings.html')


#route to python for changing usernames
@app.route("/settings/edit", methods=['GET', 'POST'])

def change_username():
    if 'user_id' not in session:
        flash('Please log into your account to change your username')
        return redirect('/settings')
    
    if request.method == 'POST':
        action = request.form.get('action')
        user_id = session.get('user_id')

        #check which utility is needed
        if  action == 'username':
            username_new = request.form['username']

            # Check if username meets requirements
            if len(username_new) < 3:
                flash('Username must be at least three characters long')
                return redirect('/settings')


            #update username in database
            try:
                db = get_db()
                query_db('''UPDATE users
                            SET user_name = ?
                            WHERE user_id =?''',
                            (username_new, user_id))
                db.commit()
                flash('Username updated successfully')
                return redirect('/settings')
            #error handling for duplicate usernames
            except sqlite3.IntegrityError:
                flash('Username already exists!')

        #check which utility is needed
        if action == 'password':
            user_row = query_db('SELECT password FROM users WHERE user_id = ?', (user_id,), one=True)

            if not user_row:
                flash('User not found')
                return redirect('/settings')

            current_password = request.form.get('current_password')
            new_password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            #safefail for javascript not handling missing input
            if not current_password or not new_password or not confirm_password:
                flash('Please fill in all password fields')
                return redirect('/settings')

            #check users authentcity before changing password
            if not check_password_hash(user_row['password'], current_password):
                flash('Current password incorrect')
                return redirect('/settings')

            #failsafe for javascript not detecting mismatched passwords
            if new_password != confirm_password:
                flash('New passwords do not match')
                return redirect('/settings')

            #update password in database
            db = get_db()
            query_db('''UPDATE users
                        SET password = ?
                        WHERE user_id = ?''',
                        (generate_password_hash(new_password), user_id))
            db.commit()
            flash('Password updated successfully')
            return redirect('/settings')

    return redirect('/settings')


#App route to python deleting the account and (all) associated information
@app.route("/settings/delete-account", methods=['GET', 'POST'])

def delete_account():
    #check if usere is logged in before attempting to delete account
    if 'user_id' not in session:
        flash('Please log into your account to delete it.')
        return redirect('/settings')

    user_id = session.get('user_id')

    #delete user information from user table
    #previously created trigger deletes information from other tables
    db = get_db()
    query_db('''DELETE FROM users WHERE user_id = ?;''',
                (user_id,))
    db.commit()
    session.clear()
    return redirect('/')


#logout route
#not linked to an html
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
            

#error handling for error 404 (page not found)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error = '404')

if __name__ == '__main__':
    app.run(debug=True)