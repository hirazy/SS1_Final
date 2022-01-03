from flask import Flask, render_template, request, jsonify
from werkzeug.utils import redirect

app = Flask(__name__, template_folder='templates')

# Data Test
todoList = [
    {'id': 1, 'description': 'SS1 Assignment 1', 'status': 'Done'},
    {'id': 2, 'description': 'SS1 Assignment 2', 'status': 'Doing'},
    {'id': 3, 'description': 'SS1 Final', 'status': 'Doing'},
]


@app.route('/')
def index():
    list = todoList
    return render_template('index.html', todoList=list)


# Get All Item of TODOList
@app.route('/api/list')
def allItems():
    return jsonify(todoList)

# Add Item to TODOList
@app.route('/add', methods=['POST'])
def add():
    description = request.form.get("itemDescription")
    idItem = 1
    if len(todoList) != 0:
        set = []
        for i in range(0, len(todoList)):
            itemTODO = todoList[i]
            set.append(itemTODO['id'])

        for i in range(1, len(todoList) + 2):
            if set.count(i) == 0:
                idItem = i
                break

    item = {'id': idItem,
            'description': description,
            'status': 'Doing'}
    todoList.append(item)
    return redirect('/')


# Update Item of TODOList
@app.route('/edit', methods=['POST'])
def update():
    itemID = request.form.get("itemID")

    if request.form["clickBtn"] == 'update':

        print(itemID)

        description = request.form["itemDescription"]
        status = "Doing"

        if request.form.get('itemStatus'):
            status = "Done"

        for i in range(0, len(todoList)):
            if todoList[i]['id'] == int(itemID):
                todoList[i]['description'] = description
                todoList[i]['status'] = status
                break

    elif request.form["clickBtn"] == 'delete':
        for i in range(0, len(todoList)):
            if todoList[i]['id'] == int(itemID):
                todoList.pop(i)
                break

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
