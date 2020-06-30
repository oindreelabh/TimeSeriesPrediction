
from flask import Flask, render_template, url_for, request, jsonify
import pickle
import plotly.express as px
import plotly.io as pio
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
from model import model_call , predict_top_clients
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
import numpy as np
from helper_functions import give_last_date, take_fields, give_dates, give_clients_and_entities
from forms import OutputForm
import csv
from successfulTransactionCompare import comparareClientsTransaction



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

allClients=[]
allLegalEntities=[]
allData=give_clients_and_entities()
allClients=allData[0]
allLegalEntities=allData[1]
listofatt=take_fields()
final_result = predict_top_clients(len(allClients))

df = pd.read_csv(r'F:/try/processed_data.csv')
d = {}
for i in range(len(df)):
	key = df.iloc[i,1]
	val = df.iloc[i,2]
	if key in d.keys():
		if val not in d[key]:
			d[key].append(val)
	else:	
	    d[key] = []
	    d[key].append(df.iloc[i,2])


print(final_result)
print('..................')
print(allLegalEntities)
print(',..............................................start......................................................')


@app.route('/get_food/<cl>')
def get_food(cl):                                                                                    
    return jsonify(d[cl])


@app.route('/')
@app.route('/home')
def home():
	form = OutputForm()
	return render_template('index.html', listofatt=listofatt, allClients=allClients, allLegalEntities=allLegalEntities, form = form)


@app.route("/compare")
def compare():
	return render_template('compare.html', listofatt=listofatt,allClients=allClients, allLegalEntities=allLegalEntities)


@app.route('/predict',methods=['POST'])
def predict():
	form = OutputForm()
	from_d = request.form['from'];
	cname = form.clientName.data
	lename = form.Legal.data;
	#attribute_value = request.form['attribute_value'];
	
	df = model_call(str(cname),str(lename))
	model = pickle.load(open('model.pkl', 'rb'))
	lastdate_=give_last_date(cname, lename)
	pred=model.forecast(6)
	start = from_d
	show_predict=np.array(df[str(datetime.datetime.strptime(str(lastdate_),'%Y%m%d').date())])
	show_predict=np.append(show_predict, pred)
	


	fig = go.Figure()
	fig.add_trace(go.Scatter(x = df[start:].index, y=df[start:], mode='lines', name='Recorded'))
	fig.add_trace(go.Scatter(x=give_dates(lastdate_), y=show_predict, mode='lines', name='Predicted',line=dict(width=4, dash='dot')))
	slope = pred[-1] - df[-1]
	final_verdict=''
	if slope>0:
		final_verdict="Beneficial to work with this client"
	else :
		final_verdict="Not beneficial to work with this client"
	fig.update_layout(title_text=final_verdict)
	fig.update_yaxes(title_text="Paid Amount")
	fig.update_xaxes(title_text='Dates')
	pio.write_html(fig, file='F:/try/templates/predict.html', auto_open=False)
	return render_template('predict.html')
	   


      
@app.route("/script", methods = ["POST"])
def script():
	client1 = request.form['client1'];
	client2 = request.form['client2'];
	legal1 = request.form['legal1'];
	legal2 = request.form['legal2'];
	from_d = request.form['from'];
	#attribute_value = request.form['attribute_value'];
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
	print(lastdate_2)
	print('.............................................................')
	show_predict2=np.array(df2[str(datetime.datetime.strptime(str(lastdate_2),'%Y%m%d').date())])
	show_predict2=np.append(show_predict2, pred2)
	
	print(type(show_predict2))
	#fig = make_subplots(rows=1, cols=2)
	fig = go.Figure()
	fig.add_trace(go.Scatter(x =df1[start:].index,y=df1[start:],mode='lines',name='Recorded trend 1'))
	fig.add_trace(go.Scatter(x=give_dates(lastdate_1),y=show_predict1,mode='lines',name='Predicted trend 1',line=dict(width=4, dash='dot')))
	fig.add_trace(go.Scatter(x = df2[start:].index, y=df2[start:], mode='lines', name='Recorded Trend 2'))
	fig.add_trace(go.Scatter(x=give_dates(lastdate_2), y=show_predict2, mode='lines', name='Predicted trend 2', line=dict(width=4, dash='dot')))
	fig.update_yaxes(title_text="Paid Amount")
	fig.update_xaxes(title_text='Dates')

	pio.write_html(fig, file='F:/try/templates/output.html', auto_open=False)
	return render_template('output.html')


@app.route("/topNClients.html",  methods = ["POST", "GET"])
def topNClients() :
	
	if request.method == 'POST' :
		number = request.form['number']
		criteria= request.form['criteria']

		if criteria == 'Mean' :
			x_bar = list()
			name_scatter =[]
			now_date=str(date.today())
			new_now_date=""
			for w in now_date :
				if(w!='-') :
					new_now_date+=w
			x_scatter_temp = give_dates(new_now_date, 6)
			x_scatter=x_scatter_temp[1:]
			y_bar = list()
			y_scatter = list()
			table_col = list()
			table_col.append('Clients')
			for var in x_scatter :
				table_col.append(str(var))
			table_col.append('Predicted Paid Amt Mean(USD)')
			table_row = list()
			
			i=0
			for key in final_result.keys():
				x_bar.append(key)
				y_bar.append(int(final_result[key][0]))
				table_row_temp=list()
				table_row_temp.append(key)
				y_scatter_temp = list()
				j=1
				while j < len(final_result[key]):
					y_scatter_temp.append(final_result[key][j])
					table_row_temp.append(final_result[key][j])
					j=j+1
				table_row_temp.append(final_result[key][0])
				y_scatter.append(y_scatter_temp)
				table_row.append(table_row_temp)
				i=i+1
				if i ==int(number) :
					break

			new_table_row = []
			for i in range(len(table_row[0])):
				table_row_temp_new = []
				for elem in table_row :
					table_row_temp_new.append(elem[i])
				new_table_row.append(table_row_temp_new)

			for word in x_bar:
				if len(word) < 12:
					name_scatter.append(word)
				else :
					small_word=""
					for i in range(12) :
						small_word+=word[i]
					name_scatter.append(small_word+"...")
			
			fig = make_subplots(rows=3, cols=1,  vertical_spacing=0.09,specs=[ [{"type": "table"}],[{"type": "bar"}],[{"type": "scatter"}] ] )
			fig.add_trace(go.Table(header=dict(values=table_col,font=dict(size=10),align="left"), cells=dict(values=new_table_row,  height=40,align="left")), row=1, col=1)
			fig.add_trace(go.Bar(x=name_scatter, y=y_bar, text=x_bar,textposition='outside'), row=2, col=1)
			fig.update_yaxes(title_text="Mean Prdicted Amt(USD)", row=2, col=1)
			fig.update_yaxes(title_text="Predicted Paid Amt ", row=3, col=1)
			fig.update_xaxes(title_text="Dates", row=3, col=1)
			
			i=0
			for element_y in y_scatter:
				fig.add_trace(go.Scatter(x=x_scatter, y=element_y, name=name_scatter[i]), row=3, col=1)
				i=i+1
			pio.write_html(fig, file='F:/try/templates/topNClientsGraph.html')

		else :
			comparareClientsTransaction(number, allClients)

	
		return render_template('topNClientsGraph.html')
    

	return render_template('topNClients.html', allClientsNumber=len(allClients))


@app.route("/alter.html")
def alter() :
	return render_template('alter.html')



if __name__ == '__main__':
      app.run(debug=True)    