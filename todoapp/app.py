from  flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


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
        return f'<Todo {self.id} {self.description}'

db.create_all()
    
data1 = Todo.query.all()

print (data1)


#@app.route('/')
#def index():
#    return render_template('index.html', data=Todo.query.all())


#if __name__=="__main__":
#   app.run(host="0.0.0.0")