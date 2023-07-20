import os
from datetime import datetime
from flask import current_app
from initapp import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))

    name = db.Column(db.String(20))

    checkins = db.relationship('Checkin', back_populates='user', cascade='all')
    inspections = db.relationship('Inspection', back_populates='user', cascade='all')
    repairs = db.relationship('Repair', back_populates='user', cascade='all')

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        self.set_password()
        self.account = 'admin'
        self.name='David'

    def set_password(self, password='123456'):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    illumination = db.Column(db.Integer)
    windvelocity = db.Column(db.Integer)
    pm2p5 = db.Column(db.Integer)
    noise = db.Column(db.Integer)


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ths = db.Column(db.Boolean)
    ils = db.Column(db.Boolean)
    wss = db.Column(db.Boolean)
    pms = db.Column(db.Boolean)
    nos = db.Column(db.Boolean)
    ltm = db.Column(db.Boolean)

class Light(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    state=db.Column(db.Boolean)



class Checkin(db.Model): #巡检记录
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(), index=True)
    datestring = db.Column(db.String(40), index=True)
    userid = db.Column(db.Integer, db.ForeignKey('admin.id'))
    user = db.relationship('Admin', back_populates='checkins')


class Inspection(db.Model):  #异常报修记录
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(), index=True)
    datestring = db.Column(db.String(40), index=True)
    ths = db.Column(db.Boolean)
    ils = db.Column(db.Boolean)
    wss = db.Column(db.Boolean)
    pms = db.Column(db.Boolean)
    nos = db.Column(db.Boolean)
    ltm = db.Column(db.Boolean)
    userid = db.Column(db.Integer, db.ForeignKey('admin.id'))
    user = db.relationship('Admin', back_populates='inspections')



class Repair(db.Model):#维修记录
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(), index=True)
    datestring = db.Column(db.String(40), index=True)
    ths = db.Column(db.Boolean)
    ils = db.Column(db.Boolean)
    wss = db.Column(db.Boolean)
    pms = db.Column(db.Boolean)
    nos = db.Column(db.Boolean)
    ltm = db.Column(db.Boolean)
    userid = db.Column(db.Integer, db.ForeignKey('admin.id'))
    user = db.relationship('Admin', back_populates='repairs')

