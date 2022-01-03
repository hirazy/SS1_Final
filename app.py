from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

todoList = [
    {'id': 1, 'description': 'Test 1', 'status': 'Done'},
    {'id': 2, 'description': 'Test 2', 'status': 'Doing'}
]

conn = sqlite3.connect('database.db')

conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print("Table created successfully")
conn.close()

@app.route('/')
@app.route('/index')
def index():
    return 'Hello world'

@app.route('/list', methods = ['GET'])
def getList():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    return []

@app.route('/add', methods = ['POST'])
def add():

    return []

@app.route('/update?id=<id>', methods = [])
def update(id):

    return []

@app.route('/delete?id=<id>', methods = [])
def delete(id):

    return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
