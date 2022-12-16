from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms import IntegerField,SubmitField,StringField,EmailField,PasswordField,SelectField

class StaffRegistration(FlaskForm):
    fullname = StringField('FIRSTNAME', validators=[DataRequired(),Length(max=50)])
    email = EmailField('EMAIL', validators=[DataRequired(),Length(max=50)])
    combo = SelectField('USER_TYPE', choices=[(1,'Admin'),(2,'Staff')],coerce=int)
    password = PasswordField('PASSWORD',validators=[DataRequired(),Length(min=6,message='Please Enter minimum of 6 characters')])
    login = SubmitField('Signup')

class StudentRegistration(FlaskForm):
    fullname = StringField('FULLNAME', validators=[DataRequired(),Length(max=100)])
    reg_no = StringField('REG_NO', validators=[DataRequired(),Length(max=50)])
    email = EmailField('EMAIL', validators=[DataRequired(),Length(max=50)])
    current_level = StringField('STRING_NO', validators=[DataRequired(),Length(max=50)])
    login = SubmitField('Signup')

class Signin(FlaskForm):
    username = StringField('USERNAME',validators=[DataRequired()])
    password = PasswordField('PASSWORD',validators=[DataRequired()])

    login = SubmitField('Login')

class PaymentForm(FlaskForm):
    name = StringField('NAME', validators=[DataRequired(),Length(max=150)])
    reg_no = StringField('REG_NO', validators=[DataRequired(), Length(max=50)])
    current_level = StringField('STRING_NO', validators=[DataRequired(), Length(max=50)])
    combo = SelectField('USER_TYPE', choices=[(1, 'Paid'), (2, 'Unpaid')], coerce=int)
    submit = SubmitField('SUBMIT')

class Search(FlaskForm):
    reg_no = StringField('REG_NO', validators=[DataRequired()])
    submit = SubmitField('SUBMIT')

class Changepassword(FlaskForm):
    password = StringField('PASSWORD',validators=[DataRequired()])
    new_password = PasswordField('NEW PASSWORD',validators=[DataRequired()])

    submit = SubmitField('SUBMIT')

