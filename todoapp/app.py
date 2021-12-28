from  flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys


# Define flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///db2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'postgresql:///db2'


#Map flask app to database
db = SQLAlchemy(app)

#Create db table 
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#db.create_all()



@app.route('/todo/create', methods=['POST'])
def create_todo():
    error = False
    try:
        description = request.get_json()['description']
        todo =Todo(description=description)
        db.session.add(todo)
        db.session.commit()
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if not error:
        return jsonify({
        'description':todo.description
        })

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

if __name__=="__main__":
   app.run(host="0.0.0.0")