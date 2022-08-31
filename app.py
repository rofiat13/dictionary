from flask import Flask, render_template, url_for, request, flash
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
import MySQLdb as mdb
import mysql.connector
import json



app = Flask(__name__)
app.secret_key = 'secret key'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_DB']='dictionary'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='rofiat13'

mysql = MySQL(app)

@app.route('/', methods= ['GET', 'POST'])
def home():
    user_response = ''
    if request.method == 'POST':
        user_input = request.form['word']
        if user_input == '':
            user_response = 'You did not input a valid word'
        else:
            # conn = mysql.get_db()
            cur = mysql.connection.cursor(mdb.cursors.DictCursor)
            # cur = conn.cursor()
            select_script = 'SELECT meaning FROM words where word=(%s)'
            select_value = {user_input}
            cur.execute(select_script, select_value)
            # cur.execute('''select meaning from words where word='Python';''')
            mysql.connection.commit()
            rv = cur.fetchall()
            if(len(rv)>0):
                user_response = rv[0]['meaning']
            else:
                user_response = 'The word you inputed cannot be found in this dictionary, please try again with another word'
        
    return render_template("index.html", user_response = user_response)

@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor(mdb.cursors.DictCursor) 
    cur.execute('select * from words')
    mysql.connection.commit()
    rv = cur.fetchall()
    for item in rv:
        print(item)
    
    return render_template("Dashboard.html", words=rv)

@app.route('/word', methods=['POST'])
def add_new_word():
    req = request.get_json()
    word = req['word']
    meaning = req['meaning']
    if word == '' or meaning == '':
        flash('Please fill in all fields to add a new word')
    else:
        cur = mysql.connection.cursor(mdb.cursors.DictCursor)
        # select_script = 'SELECT meaning FROM words where word=(%s)'
        # select_value = {user_input}
        cur.execute('insert into words(word, meaning) VALUES (%s, %s)', (word, meaning))
        mysql.connection.commit()
        cur.close()

    return json.dumps('success')

@app.route('/word/<id>/delete', methods=['POST'])
def delete_word(id):
    word_id = id
    cur = mysql.connection.cursor(mdb.cursors.DictCursor)
    cur.execute('delete from words where id=%s', (word_id))
    mysql.connection.commit()
    cur.close()

    return json.dumps('success') 

@app.route('/word/<id>/edit', methods=['POST'])
def edit_word(id):
    word_id = id
    req = request.get_json()
    word = req['word']
    meaning = req['meaning']
    if word == '' or meaning == '':
        flash('Please fill in all fields to add a new word')
    else:
        cur = mysql.connection.cursor(mdb.cursors.DictCursor)
        cur.execute('update words set word=%s, meaning=%s where id=%s', (word, meaning, word_id))
        mysql.connection.commit()
        cur.close()

    return json.dumps('success')

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
