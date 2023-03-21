from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, FloatField
from wtforms.validators import DataRequired, Email, Length

class AddUserForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField('Add User')

class AddProductForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description:', validators=[DataRequired()])
    price = FloatField('Price:', validators=[DataRequired()])
    submit = SubmitField('Add Product')

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField('Login')

class DeleteUserForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField("Delete User")