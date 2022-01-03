from  flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


# Define flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///db2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Map flask app to database
db = SQLAlchemy(app)

migrate = Migrate(app,db)

#Create db table 
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#db.create_all()

class TodoList(db.Model):
    __tablename__='todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    todos = db.relationship('Todo', backref='list', lazy =True)




@app.route('/todo/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo =Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route ('/todo/<todo_id>/set-completed', methods=['POST'])
def check_completed(todo_id):
    try:
        completed = request.get_json()['completed']
        print(completed)
        todo =Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))



@app.route ('/todo/<todo_id>/delete', methods=['DELETE'])
def delete(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify({'success': True })

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    lists = TodoList.query.all()
    #active_list = TodoList.query.get(list_id)
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
    return render_template('index.html', lists=lists, todos=todos)

   

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))



if __name__=="__main__":
   app.run(debug=True, host="0.0.0.0")