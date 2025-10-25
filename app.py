from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

uri = 'mongodb+srv://wikiIngWebMolones:ultraMegaMolones@cluster0.78jhrsp.mongodb.net/todos'

client = MongoClient(uri)

db = client.get_default_database()
todos_collection = db['task']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        new_task = {
            'content': content,
            'completed': 0,
            'date_created': datetime.utcnow()
        }
        try:
            todos_collection.insert_one(new_task)
        except:
            return 'There was an issue adding your task'
    
    tasks = list(todos_collection.find())
    return render_template('tabla.html', tasks=tasks)


@app.route('/delete/<id>')
def delete(id):
    try:
        todos_collection.delete_one({'_id': ObjectId(id)})
        tasks = list(todos_collection.find())
        return render_template('tabla.html', tasks=tasks)
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    try:
        task = todos_collection.find_one({'_id': ObjectId(id)})
        if not task:
            return 'Task not found'
            
        if request.method == 'POST':
            new_content = request.form['content']
            todos_collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': {'content': new_content}}
            )
            tasks = list(todos_collection.find())
            return render_template('tabla.html', tasks=tasks)
        else:
            return render_template('update.html', task=task)
    except:
        return 'There was an issue updating your task'


if __name__ == '__main__':
    app.run(debug=True)
