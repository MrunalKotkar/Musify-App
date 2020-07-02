from flask import Flask, render_template, request, redirect, session
import mysql.connector
import pymysql
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)


db = pymysql.connect("localhost","testuser","test123","TESTDB" )

cursor = db.cursor()


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/login')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    db = pymysql.connect("localhost", "testuser", "test123", "TESTDB")
    cursor = db.cursor()

    cursor.execute("""INSERT INTO users (NAME, EMAIL, PASSWORD) VALUES
    ('{}', '{}', '{}')""".format(name, email, password))

    db.commit()
    db.close()
    return "Data Added"


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




if __name__ == '__main__':
    app.run(debug=True)
