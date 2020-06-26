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


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('compare.html')


@app.route("/script", methods = ["POST"])
def script():
	client1 = request.form['client1'];
	client2 = request.form['client2'];
	legal1 = request.form['legal1'];
	legal2 = request.form['legal2'];
	from_d = request.form['from'];
	to = request.form['to'];
	#df1=[]
	#df2=[]
	df1 = model_call(str(client1),str(legal1))
	df2 = model_call(str(client2),str(legal2))
	
	start = from_d
	end  = to
	#fig1 = px.line(x = df1[start:end].index, y = df1[start:end], title = 'Past trend')
	#fig2 = px.line( x = df2[start:end].index,y = df2[start:end] , title='past trend')
	fig = make_subplots(rows=1, cols=2)
	fig.add_trace(go.Scatter(x = df1[start:end].index, y = df1[start:end], mode="lines"), row=1, col=1)
	fig.add_trace(go.Scatter( x = df2[start:end].index,y = df2[start:end],mode="lines"), row=1, col=2)
	pio.write_html(fig, file='F:/project3_frontend/templates/output.html', auto_open=False)
	return render_template('output.html')



if __name__ == '__main__':
	app.run(debug=True)    