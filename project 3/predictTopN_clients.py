import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import date
from dateutil.relativedelta import relativedelta

def get_key(val, my_dict):

    for key, value in my_dict.items():
        if val == value:
            return key 

    return "key doesn't exist"

def predict(num):
    
    df = pd.read_csv(r'C:/Users/User/Desktop/project 3/processed_data.csv', parse_dates=['Payment Date'], index_col='Payment Date')

    model_dict = {}

    for client in df['Client Name'].unique():
        model1 = ExponentialSmoothing(np.asarray(df[df['Client Name']==client]['Paid Amount']), trend='add', seasonal='add', seasonal_periods=12, damped=True)
        hw_model1 = model1.fit()
        model2 = ExponentialSmoothing(np.asarray(df[df['Client Name']==client]['Paid Amount']), trend='add', seasonal='add', seasonal_periods=12)
        hw_model2 = model1.fit()
        model_dict[client] = hw_model1 if hw_model1.aic < hw_model2.aic else hw_model2

    predicted_amounts = {}

    for client, model in model_dict.items():
        pred = model.forecast(12)
        predicted_amounts[client] = pred.mean()

    values = list(predicted_amounts.values())
    values.sort()
    
    result = {}

    for i in range(1,num + 1):
        result[get_key(values[-1*i],predicted_amounts)] = values[-1*i]

    return result


#predict(start = date.today(), end = date.today() + relativedelta(months=+12))