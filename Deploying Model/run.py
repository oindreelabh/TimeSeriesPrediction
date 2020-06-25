from flask import Flask, request, render_template
import pickle
import plotly.express as px
import plotly.io as pio
#import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from model import model_call
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/output',methods=['POST'])
def output():
    value_list = request.form.values()
    df = model_call(str(value_list[0]),str(value_list[1]))
    start = datetime.date(value_list[2])
    end = datetime.date(value_list[3])
    fig = px.line(x = df[start:end].index, y=df[start:end], title='Past trend')
    pio.write_html(fig, file='G:/Deploying Model/templates/output.html', auto_open=False)

    return render_template('output.html', output_text = 'This is the graph for predicted values of given time interval : ')

@app.route('/predict',methods=['POST'])
def predict():

    model = pickle.load(open('model.pkl', 'rb'))
    pred = model.predict(start=date.today(), end=date.today() + relativedelta(months=+6))

    fig = px.line(pred, title='Future Prediction')

    pio.write_html(fig, file='G:/Deploying Model/templates/predict.html', auto_open=False)
    slope = pred[-1] - pred[0]
    output = "" if slope > 0 else "not "

    return render_template('predict.html', prediction_text = 'This is the graph for predicted values of 6 months from now. It is {}beneficial to work with this client'.format(output))	

if __name__ == "__main__":
    app.run(debug=True)