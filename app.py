from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with
from random import randrange
import click
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwer1234@localhost/ssm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
CORS(app)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<x: %d, y: %d>' % (self.x, self.y)

resource_fields = {
    'x': fields.Integer,
    'y': fields.Integer,
}

class Hello(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        datas = Sale.query.all()
        return datas

@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    for i in range(1,500):
        s = Sale(x=i, y=randrange(90,110))
        db.session.add(s)
    db.session.commit()
    click.echo('Initialized database')

api.add_resource(Hello, '/')

