from flask import Flask, render_template, request, redirect, session
import pymysql
import os
from Spotify_client import SpotifyAPI

client_id = "a7c2cecdaf4d47219b4383f75a3be0d6"
client_secret = "75656d3dae404952a35f611bb7bbaf09"
spotify = SpotifyAPI(client_id, client_secret)

app = Flask(__name__)
app.secret_key = os.urandom(24)

app = Flask(__name__)

db = pymysql.connect("127.0.0.1","testuser","test123","TESTDB" )

cursor = db.cursor()


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('search.html')

@app.route('/track_data', methods=['POST'])
def track_data():
    query = request.form.get('trackname')
    print(query)
    option = request.form.get('topology')
    print(option)
    data = spotify.search({"track": query}, search_type=option)

    search_string = option.lower() + "s"
    print(search_string)
    r = data[search_string]['items']
    print(len(r))
    return render_template('home2.html', data=r, length=len(r), search_string=search_string)


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    random_tracks = spotify.get_random_tracks()
    length = len(random_tracks)
    if 'user_id' in session:
        return render_template('home.html', random_tracks=random_tracks, length = length)
    else:
        return redirect('/login')

@app.route('/add_user', methods=['POST'])
def add_user():
    random_tracks = spotify.get_random_tracks()
    length = len(random_tracks)

    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    db = pymysql.connect("localhost", "testuser", "test123", "TESTDB")
    cursor = db.cursor()

    cursor.execute("""INSERT INTO users (NAME, EMAIL, PASSWORD) VALUES
    ('{}', '{}', '{}')""".format(name, email, password))

    db.commit()
    db.close()
    return render_template('home.html', random_tracks=random_tracks, length = length)

@app.route('/profile', methods=['POST'])
def profile():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    return render_template('profile.html', name=name, email=email, password=password)





@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    db = pymysql.connect("localhost", "testuser", "test123", "TESTDB")
    cursor = db.cursor()

    cursor.execute(""" SELECT * FROM users WHERE EMAIL LIKE '{}' AND PASSWORD LIKE '{}' """
                   .format(email, password))
    users = cursor.fetchall()
    print(users)
    db.close()

    if len(users)>0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
