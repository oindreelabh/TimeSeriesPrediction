from flask import Flask, render_template, url_for, request
import pickle
import plotly.express as px
import plotly.io as pio
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
from model import model_call
import myfile



app = Flask(__name__)

@app.route("/")
@app.route("/home")
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
	df1 = model_call(str(client1),str(legal1))
	df2 = model_call(str(client2),str(legal2))
	#return myfile.getAns(from_d)
	start = from_d
	end  = to
	fig = px.line(x = df2[start:end].index, y = df2[start:end], title = 'Past trend')
	pio.write_html(fig, file='C:/Users/User/Desktop/project 3/templates/output.html', auto_open=False)
	return render_template('output.html')

if __name__ == '__main__':
	app.run(debug=True)    