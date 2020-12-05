import random
import requests
import os
from flask import Flask, render_template, request, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
from flask import jsonify

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


class CustomForm(FlaskForm):
    text_message = DecimalField(
        'Valor de coeficiente de arrastre', validators=[DataRequired()])
    submit = SubmitField('Cargar')


@app.route("/", methods=['GET', 'POST'])
def home():
    form = CustomForm()
    if form.validate_on_submit():
        return render_template('index.html', form=form, coef=form.text_message.data)
    return render_template('index.html', form=form, coef=0)


@app.route('/plot-<coef>.png')
def plot_png(coef):
    fig = create_figure(float(coef))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# AQUI RELLENAR CON FUNCION QUE GENERA GRAFICO


def create_figure(coef):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) * coef for x in xs]
    axis.plot(xs, ys)
    return fig


if __name__ == "__main__":
    app.run(debug=True)
