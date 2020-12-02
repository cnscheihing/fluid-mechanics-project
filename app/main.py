import random
import requests
import os
from flask import Flask, render_template, request
# from math import ceil
# from datetime import datetime
# from faker import Faker
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import jsonify

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# url = 'https://api.chucknorris.io/jokes/random'
# fake = Faker()


class CustomForm(FlaskForm):
    text_message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


@app.route("/", methods=['GET', 'POST'])
# def home(messages_list=messages, page_count=ceil(len(messages)/5)):
def home():
    form = CustomForm()
    if form.validate_on_submit():
        # messages.insert(0, {'username': fake.name(), 'text': form.text_message.data, 'timestamp': datetime.now()})
        # LOGICA GRAFICO
        print(form.text_message.data)
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
