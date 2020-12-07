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
        'Valor de coeficiente de arrastre', validators=[DataRequired()])
    submit = SubmitField('Cargar')


@app.route("/", methods=['GET', 'POST'])
def home():
    form = CustomForm()
    if form.validate_on_submit():
        return render_template('index.html', form=form, coef=form.drag_coef.data)
    return render_template('index.html', form=form, coef=0)


@app.route('/plot-<drag_coef>.png')
def plot_png(drag_coef):
    fig = create_figure(float(drag_coef))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# AQUI RELLENAR CON FUNCION QUE GENERA GRAFICO


def create_figure(coef):
    ca = coef
    rho = 1.2
    A = 0.1
    velocidades = np.linspace(0, 35*3.6, 36*3.6)
    cte = 0.5*rho*A*ca
    arrastre = []

    for vel in velocidades:
        arrastre.append(vel*vel*cte)

    # plt.xlabel("Velocidad (m/s)")
    # plt.ylabel("Fuerza de Arrastre (N)")
    # plt.title("Fuerza de Arrastre vs Velocidad")
    fig = Figure()
    # plt
    axis = fig.add_subplot(1, 1, 1)
    # xs = range(100)
    # ys = [random.randint(1, 50) * coef for x in xs]
    axis.set_ylim([0, 1500])
    axis.plot(velocidades, arrastre)
    # plt.plot(velocidades, arrastre)
    # plt.xlabel('xlabel', fontsize=18)
    # plt.ylabel('ylabel', fontsize=16)
    # plt.savefig('/static/img/tablas/test.png')
    fig.text(0.5, 0.04, 'Velocidad (km/h)', ha='center')
    fig.text(0, 0.5, 'Fuerza de Arrastre (N)',
             va='center', rotation='vertical')
    axis.title.set_text('Fuerza de Arrastre vs Velocidad')
    return fig


if __name__ == "__main__":
    app.run(debug=True)
