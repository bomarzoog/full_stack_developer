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

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#db.create_all()



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

@app.route ('/todo/<todo_id>/delete', methods=['POST'])
def delete(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index')) 
    print ('redirect happen!!!!!')      

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all() ) 

if __name__=="__main__":
   app.run(debug=True, host="0.0.0.0")