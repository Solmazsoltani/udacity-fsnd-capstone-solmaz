
import os
from sqlalchemy import ForeignKey, Column, String, Integer, \
                    DateTime, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
import os
from flask_migrate import Migrate

database_name = "capstone"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
#database_path = "postgres:///{}".format(database_name)
database_path = "postgresql://{}:{}@{}/{}".format('postgres','123','localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

'''
setup_db(app)
        binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

'''
Auto
'''

class Auto(db.Model):

    __tablename__ = 'autos'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)
    buyers = relationship('Buyer', backref="auto", lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'buyers': list(map(lambda buyer: buyer.format(), self.buyers))
        }

'''
Buyer
'''

class Buyer(db.Model):

    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    auto_id = Column(Integer, ForeignKey('autos.id'), nullable=True)

    def __init__(self, name, age, gender, auto_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.auto_id = auto_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            "auto_id": self.auto_id
        }
