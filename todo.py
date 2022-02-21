from flask import Flask,jsonify,request,redirect,url_for
from flask_pymongo import PyMongo
from matplotlib.pyplot import title


app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://meryem2:Mb12345.@cluster0.x7wyu.mongodb.net/todolist?retryWrites=true&w=majority'
mongo = PyMongo(app)


@app.route('/get_todo', methods=['GET'])
def get_all_todo():
    todolist=list() 
    todo =mongo.db.todos
    for i in todo.find():
        todolist.append({'title':i['title'],'description':i['description'],'created_at':i['created_at'],'updated_at':i['updated_at'],'is_completed':i['is_completed']})
    return jsonify(todolist)


@app.route('/get_one_todo/<title>', methods=['GET'])
def get_one_todo(title):
    todo = mongo.db.todos
    data = todo.find_one({'title':title})
    return jsonify({'title':data['title'],'description':data['description'],'created_at':data['created_at'],'updated_at':data['updated_at'],'is_completed':data['is_completed']})

@app.route('/add_todo', methods=['POST'])
def add_todo():
    todo = mongo.db.todos
    title = request.json['title']
    description = request.json['description']
    is_completed= request.json['is_completed']
    created_at = request.json['created_at']
    updated_at = request.json['updated_at']
    todo.insert({'title':title,'description':description,'is_completed':is_completed,'created_at':created_at,'updated_at':updated_at})
    return jsonify({'title':title,'description':description,'is_completed':is_completed,'created_at':created_at,'updated_at':updated_at})


@app.route('/update/<title>', methods=['PUT'])
def update_todo(title):
    todo = mongo.db.todos
    updatetitle =request.json['title']
    todo.update_one({'title':title},{"$set" :{'title':updatetitle}})
    return redirect(url_for('get_all_todo'))


@app.route('/delete/<title>', methods=['DELETE'])
def delete_todo(title):   
    todo=mongo.db.todos
    todo.delete_one({'title': title })
    return redirect(url_for('get_all_todo'))
    

if __name__ == '__main__':
    app.run(debug = True)