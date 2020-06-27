import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import date
from dateutil.relativedelta import relativedelta

def get_key():
	for key, value in my_dict.items():
		if val == value:
			return key 
  
    return "key doesn't exist"

def predict():
	df = pd.read_csv(r'G:/temp/processed_data.csv', parse_dates=['Payment Date'], index_col='Payment Date')
	model_dict = {}
	for client in df['Client Name'].unique():
		model = ExponentialSmoothing(df[df['Client Name']==client]['Paid Amount'], trend='add', seasonal='add', seasonal_periods=12, damped=True)
        hw_model = model.fit(optimized=True, use_boxcox=False, remove_bias=False)
        model_dict[client] = hw_model
    predicted_amounts = {}
    for client, model in model_dict.items():
    	pred = model.predict( start = date.today(), end=date.today() + relativedelta(months=+12))
    	predicted_amounts[client] = pred.mean()
    values = list(predicted_amounts.values())
    values.sort()
    result = { get_key(values[-1]) : values[-1], get_key(values[-2]) : values[-2] }
    return result
    