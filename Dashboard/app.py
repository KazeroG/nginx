from flask import Flask, request, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import requests
import pandas as pd
import os

# Load environment variables
load_dotenv()

# Define API endpoint
API_ENDPOINT = os.getenv("API_ENDPOINT")  # get the API endpoint from .env file

app = Flask(__name__)

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add User')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UserForm()

    if form.validate_on_submit():
        response = requests.post(f'{API_ENDPOINT}/register', json={
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data
        })
        if response.status_code == 201:
            flash('User added successfully!', 'success')
        else:
            flash('Failed to add user!', 'error')

    response = requests.get(f'{API_ENDPOINT}/users')
    users = []
    if response.status_code == 200:
        users = response.json()

    return render_template('index.html', form=form, users=users)

if __name__ == '__main__':
    app.run(debug=True)
