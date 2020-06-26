
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
import csv

#import cufflinks as cf
#cf.go_offline()


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')



@app.route("/compare")
def compare():
      return render_template('compare.html')



@app.route('/predict',methods=['POST'])
def predict():
	fig = go.Figure()
	cname = request.form['cname'];
	lename = request.form['lename'];
	from_d = request.form['from'];
	df = model_call(str(cname),str(lename))
	start = from_d
	fig.add_trace(go.Scatter(x = df[start:].index, y=df[start:], mode='lines', name='Recorded Trend'))

	model = pickle.load(open('model.pkl', 'rb'))
	with open("F:/project3_frontend/dataset.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields=next(csvreader)
		last_date =""
		for row in csvreader:
			if row[1]==cname and row[2]==lename :
				last_date=row[0]
	lastdate_=""
	for w in last_date:
		if w!='-':
			lastdate_+=w
	pred = model.predict(start=datetime.datetime.strptime(str(lastdate_), '%Y%m%d').date(), end=date.today() + relativedelta(months=+6))
	#pred = model.predict(start=date.today(), end=date.today() + relativedelta(months=+6))
	start=date.today()
	fig.add_trace(go.Scatter(x=pred[start:].index, y=pred[start:], mode='lines', name='Predicted trend'))
	pio.write_html(fig, file='F:/project3_frontend/templates/predict.html', auto_open=False)
	slope = pred[-1] - pred[0]
	return render_template('predict.html')
	output = "" if slope > 0 else "not "
	return render_template('predict.html', prediction_text = 'This is the graph for predicted values of 6 months from now. It is {}beneficial to work with this client'.format(output))   

      

@app.route("/script", methods = ["POST"])
def script():
      client1 = request.form['client1'];
      client2 = request.form['client2'];
      legal1 = request.form['legal1'];
      legal2 = request.form['legal2'];
      from_d = request.form['from'];
      #to = request.form['to'];
      #df1=[]
      #df2=[]
      df1 = model_call(str(client1),str(legal1))
      df2 = model_call(str(client2),str(legal2))
      #dataframe1= pd.DataFrame(df1)
      #dataframe2 = pd.DataFrame(df2)
      #temp_df={'A':df1 , 'B':df2}
      #combined_df = pd.DataFrame(temp_df) 
      #return render_template('test.html', df1=dataframe1, df2=dataframe2)
      #return myfile.getAns(from_d)
      start = from_d
      #end  = to
      #fig1 = px.line(x = df1[start:end].index, y = df1[start:end], title = 'Past trend')
      #fig2 = px.line( x = df2[start:end].index,y = df2[start:end] , title='past trend')
      fig = make_subplots(rows=1, cols=2)
      fig.add_trace(go.Scatter(x = df1[start:].index, y = df1[start:], mode="lines"), row=1, col=1)
      fig.add_trace(go.Scatter( x = df2[start:].index,y = df2[start:],mode="lines"), row=1, col=2)
      pio.write_html(fig, file='F:/project3_frontend/templates/output.html', auto_open=False)
      return render_template('output.html')



if __name__ == '__main__':
      app.run(debug=True)    