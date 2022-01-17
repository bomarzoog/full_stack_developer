from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///db1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Person(db.Model):
    __tablename__= "persons"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

#db.create_all()


@app.route('/')
def index():
  person= Person.query.first()
  return "hello " + person.name

if __name__=="__main__":
   app.run(host="0.0.0.0")

# test git
#test 2