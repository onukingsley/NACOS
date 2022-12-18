from Nacos import db
from datetime import datetime
from flask_login import UserMixin
from Nacos import login_manager
from Nacos import forms
from Nacos.forms import Signin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    # if Signin().combo.data == 1:
    #     return Student.query.get(user_id)
    # elif Signin().combo.data == 2:
    #     return Staff.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(length=100), unique=True)
    password = db.Column(db.String(length=50), nullable=False)
    reg_no = db.Column(db.String(length=100), unique=True)
    name = db.Column(db.String(length=255), nullable=False)
    role = db.Column(db.String(length=20), nullable=False, default="staff")
    student = db.relationship('Student', backref='studentid', lazy=True)
    staff = db.relationship('Staff', backref='staffid', lazy=True)



class Student(db.Model ,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    reg_no = db.Column(db.String(length=100), unique=True, nullable=False)
    name = db.Column(db.String(length=255), nullable=False)
    current_level = db.Column(db.Integer(), nullable=False)
    payment = db.relationship('Payment',backref='studentid',lazy=True)
    def __repr__(self)->str:
        return self.name

class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    email = db.Column(db.String(length=100), unique=True, nullable=False)
    name = db.Column(db.String(length=255), nullable=False)
    password = db.Column(db.String(length=50), nullable=False)
    role = db.Column(db.String(length=20),nullable=False,default="staff")

    def __repr__(self)->str:
        return self.name


class Payment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Date = db.Column(db.DateTime(), default=datetime.utcnow().strftime("%d %B Y - %H:%M:%S"))
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))
    status = db.Column(db.Boolean(),default=False)
    level = db.Column(db.String(length=20),nullable=False)
    reg_no = db.Column(db.String(length=20),nullable=False)

    def __repr__(self):
        return self.student_id




db.create_all()
