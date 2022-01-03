import os
import sqlite3 as sql
import json

from flask_cors import CORS

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import redirect

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    list = []

    # Check DB exist
    if os.path.isfile('todoList.db'):
        con = sql.connect("todoList.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM todo")
        # Get all Item
        rows = cur.fetchall()
        for row in rows:
            list.append({'id': row['id'],
                         'description': row['description'],
                         'status': row['status']})
    else:
        # Create DB todoList
        con = sql.connect("todoList.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        sqlQueryCreate = "CREATE TABLE todo (id INTEGER PRIMARY KEY, description TEXT NOT NULL, status TEXT NOT NULL)"
        cur.execute(sqlQueryCreate)
        con.commit()

    return render_template('index.html', todoList=list)


@app.route('/add', methods=['POST'])
def add():
    description = request.form.get("itemDescription")

    with sql.connect("todoList.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO todo (description, status) values (?,?)", (description, 'Doing'))
        con.commit()

    return redirect('/')


@app.route('/edit', methods=['POST'])
def update():
    itemID = request.form.get("itemID")

    print(itemID)

    if request.form["clickBtn"] == 'update':

        description = request.form["itemDescription"]
        status = "Doing"

        if request.form.get('itemStatus'):
            status = "Done"

        # Update
        with sql.connect("todoList.db") as con:
            cur = con.cursor()
            sqlQuery = "UPDATE todo SET description = ? , status = ? where id = ?"
            cur.execute(sqlQuery, (description, status, itemID))
            con.commit()

    elif request.form["clickBtn"] == 'delete':
        # Delete
        with sql.connect("todoList.db") as con:
            cur = con.cursor()
            sqlQuery = "DELETE FROM todo WHERE id = " + itemID
            cur.execute(sqlQuery)
            con.commit()

    return redirect('/')


@app.route('/api/list')
def getListAPI():
    list = []

    if os.path.isfile('todoList.db'):
        con = sql.connect("todoList.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM todo")
        rows = cur.fetchall()
        for row in rows:
            list.append({'id': row['id'],
                         'description': row['description'],
                         'status': row['status']})  # or simply data.append(list(row))

    else:
        # Create DB todoList
        con = sql.connect("todoList.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        sqlQueryCreate = "CREATE TABLE todo (id INTEGER PRIMARY KEY, description TEXT NOT NULL, status TEXT NOT NULL)"
        cur.execute(sqlQueryCreate)
        con.commit()

    return jsonify(list)


@app.route('/api/add', methods=['POST'])
def addAPI():
    item = json.loads(request.data)
    print(item)
    description = item['itemDescription']

    with sql.connect("todoList.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO todo (description, status) values (?,?)", (description, 'Doing'))
        con.commit()

    return jsonify(item)


@app.route('/api/update', methods=['GET'])
def updateAPI():
    itemID = request.args.get('id', default=1, type=int)
    # Update
    with sql.connect("todoList.db") as con:
        cur = con.cursor()
        sqlQuery = "SELECT status FROM todo where id = " + str(itemID)
        cur.execute(sqlQuery)
        rows = cur.fetchall()
        status = ""

        if len(rows) == 1:
            if rows[0][0] == "Done":
                status = "Doing"
            else:
                status = "Done"

        if status != "":
            sqlQueryUpdate = "UPDATE todo SET status = '" + status + "' WHERE id = " + str(itemID)
            cur.execute(sqlQueryUpdate)
        con.commit()

    return jsonify({'id': 'id'})


@app.route('/api/delete')
def deleteAPI():
    itemID = request.args.get('id', default=1, type=int)
    # Delete
    with sql.connect("todoList.db") as con:
        cur = con.cursor()
        sqlQuery = "DELETE FROM todo WHERE id = " + str(itemID)
        cur.execute(sqlQuery)
        con.commit()

    return jsonify({'id': 'id'})


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
