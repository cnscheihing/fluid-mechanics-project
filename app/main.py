import random
import requests
import os
from flask import Flask, render_template, request, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
from flask import jsonify
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


class CustomForm(FlaskForm):
    drag_coef = DecimalField(
        'Valor de coeficiente de arrastre (Cd)', validators=[DataRequired()])
    sust_coef = DecimalField(
        'Valor de coeficiente de sustentación (Cl)', validators=[DataRequired()])
    submit = SubmitField('Cargar')


@app.route("/", methods=['GET', 'POST'])
def home():
    form = CustomForm()
    if form.validate_on_submit():
        return render_template('index.html', form=form, drag_coef=form.drag_coef.data, sust_coef=form.sust_coef.data)
    return render_template('index.html', form=form, drag_coef=0, sust_coef=0)


@app.route('/plot/<drag_coef>/<sust_coef>.png')
def plot_png(drag_coef, sust_coef):
    fig = create_figure(float(drag_coef), float(sust_coef))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure(drag_coef, sust_coef):
    ca = drag_coef
    rho = 1.2
    A = 0.1
    velocidades = np.linspace(0, 3.6*35, 3.6*36)
    cte = 0.5*rho*A*ca
    cs = sust_coef
    cte_sus = 0.5*rho*cs

    sustentacion = []
    arrastre = []

    for vel in velocidades:
        arrastre.append(vel*vel*cte)
        sustentacion.append(vel*vel*cte_sus)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(velocidades, arrastre, color="blue", label="Fuerza de Arrastre")
    axis.plot(velocidades, sustentacion, color="red",
              label="Fuerza de Sustenación")
    fig.text(0.5, 0.04, 'Velocidad (km/h)', ha='center')
    fig.text(0, 0.5, 'Fuerza (N)', va='center', rotation='vertical')
    axis.title.set_text('Fuerza de Arrastre y Sustentación vs Velocidad')
    axis.legend(loc='upper left', frameon=True)
    return fig


if __name__ == "__main__":
    app.run(debug=True)
