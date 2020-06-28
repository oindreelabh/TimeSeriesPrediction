
from flask import Flask, render_template, url_for, request
import pickle
import plotly.express as px
import plotly.io as pio
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
from model import model_call
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
import numpy as np
from helper_functions import give_last_date, take_fields, give_dates
import predictTopN_clients 



app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
	listofatt=take_fields()
	return render_template('index.html',listofatt=listofatt)


@app.route("/compare")
def compare():
	listofatt=take_fields()
	return render_template('compare.html', listofatt=listofatt)


@app.route('/predict',methods=['POST'])
def predict():
	cname = request.form['cname'];
	lename = request.form['lename'];
	from_d = request.form['from'];
	attribute_value = request.form['attribute_value'];
	
	df = model_call(str(cname),str(lename))
	model = pickle.load(open('model.pkl', 'rb'))
	lastdate_=give_last_date(cname, lename)
	pred=model.forecast(6)
	start = from_d
	show_predict=np.array(df[str(datetime.datetime.strptime(str(lastdate_),'%Y%m%d').date())])
	show_predict=np.append(show_predict, pred)
	

	fig = go.Figure()
	fig.add_trace(go.Scatter(x = df[start:].index, y=df[start:], mode='lines', name='Recorded'))
	fig.add_trace(go.Scatter(x=give_dates(lastdate_), y=show_predict, mode='lines', name='Predicted'))
	positive_verdict='This is the graph for predicted values of 6 months from now. It is beneficial to work with this client'
	negative_verdict='This is the graph for predicted values of 6 months from now. It is not beneficial to work with this client'
	slope = pred[-1] - pred[0]
	final_verdict=''
	if slope>0:
		final_verdict="Beneficial to work with this client"
	else :
		final_verdict="Not beneficial to work with this client"
	fig.update_layout(title_text=final_verdict)
	pio.write_html(fig, file='C:/Users/User/Desktop/project 3/templates/predict.html', auto_open=False)
	return render_template('predict.html')
	   


      
@app.route("/script", methods = ["POST"])
def script():
	client1 = request.form['client1'];
	client2 = request.form['client2'];
	legal1 = request.form['legal1'];
	legal2 = request.form['legal2'];
	from_d = request.form['from'];
	attribute_value = request.form['attribute_value'];
	start = from_d

	df1 = model_call(str(client1),str(legal1))
	model = pickle.load(open('model.pkl', 'rb'))
	lastdate_1=give_last_date(client1, legal1)
	pred1=model.forecast(6)
	show_predict1=np.array(df1[str(datetime.datetime.strptime(str(lastdate_1),'%Y%m%d').date())])
	show_predict1=np.append(show_predict1, pred1)


	df2 = model_call(str(client2),str(legal2))
	model = pickle.load(open('model.pkl', 'rb'))
	lastdate_2=give_last_date(client2, legal2)
	pred2=model.forecast(6)
	show_predict2=np.array(df2[str(datetime.datetime.strptime(str(lastdate_2),'%Y%m%d').date())])
	show_predict2=np.append(show_predict2, pred2)
	
	print('hello')
	print(start)
	fig = make_subplots(rows=1, cols=2)
	fig.add_trace(go.Scatter(x =df1[start:].index,y=df1[start:],mode='lines',name='Recorded trend 1'),row=1,col=1)
	fig.add_trace(go.Scatter(x=give_dates(lastdate_1),y=show_predict1,mode='lines',name='Predicted trend 1'),row=1,col=1)
	fig.add_trace(go.Scatter(x = df2[start:].index, y=df2[start:], mode='lines', name='Recorded Trend 2'),row=1,col=2)
	fig.add_trace(go.Scatter(x=give_dates(lastdate_2), y=show_predict2, mode='lines', name='Predicted trend 2'),row=1,col=2)
	print('hello2') 
    

	pio.write_html(fig, file='C:/Users/User/Desktop/project 3/templates/output.html', auto_open=False)
	return render_template('output.html')

@app.route("/alter.html")
def alter() :
	return render_template('alter.html')


@app.route("/predict_top", methods = ["POST", "GET"])
def predict_top():
    lis = {}
    if request.method == 'POST':
    	num = request.form['number']
    	print(num)
    	lis = predictTopN_clients.predict(int(num))
    	return render_template('predictTop.html', result = lis)
    return render_template('predictTop.html', result = lis)	

	
	

if __name__ == '__main__':
      app.run(debug=True)    