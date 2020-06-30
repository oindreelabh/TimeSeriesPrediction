import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pickle
import numpy as np

def success(df):
	model_dict = {}
	for client in df['Client Name'].unique():
		model1 = ExponentialSmoothing(np.asarray(df[df['Client Name']==client]['Resolved']), trend='add', seasonal='add', seasonal_periods=12, damped=True)
        hw_model1 = model1.fit()
        model2 = ExponentialSmoothing(np.asarray(df[df['Client Name']==client]['Resolved']), trend='add', seasonal='add', seasonal_periods=12)
        hw_model2 = model2.fit()
        model_dict[client] = hw_model1 if hw_model1.aic < hw_model2.aic else hw_model2

    predicted_successes = {}

    for client, model in model_dict.items():
        pred = model.forecast(12)
        predicted_successes[client] = (pred, int(pred.mean()))

    return predicted_successes

'''from datetime import date, timedelta
import calendar
start_date = date(2018,12,1)
num_months = (date.today().year - 2019)*12 + date.today().month 
data = []
for i in range(num_months):
    for client in df['Client Name'].unique():
        days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
        date_ = start_date + timedelta(days=days_in_month)
        df1 = df[str(date_)[:-3]]
        count = len(df1[(df1['Client Name']==client)&(df1['Payment Status']=='RESOLVED')])
        row = [date_, client, count]
        data.append(row)        
df2 = pd.DataFrame(data).set_index(0)'''