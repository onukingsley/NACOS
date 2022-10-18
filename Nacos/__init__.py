from flask import Flask,render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Secrete_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'signin'




from Nacos import  models
from Nacos import  forms
from Nacos import  routes
from Nacos import  function

