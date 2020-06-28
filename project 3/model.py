import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pickle
import numpy as np 

def model_call(client_name, le_name):
    df = pd.read_csv(r'C:/Users/User/Desktop/project 3/processed_data.csv').set_index('Payment Date')
    df = df[df['Client Name']==client_name]
    train = df.iloc[:-10, :]
    test = df.iloc[-10:, :]
    pred = test.copy()
    model = ExponentialSmoothing(np.asarray(train['Paid Amount']), trend="add", seasonal="add", seasonal_periods=12)
    model2 = ExponentialSmoothing(np.asarray(train['Paid Amount']), trend="add", seasonal="add", seasonal_periods=12, damped=True)
    fit = model.fit()
    pred = fit.forecast(len(test))
    fit2 = model2.fit()
    pred2 = fit2.forecast(len(test))
    if fit.aic < fit2.aic :
    	pickle.dump(fit, open('model.pkl','wb'))
    else :
    	pickle.dump(fit2, open('model.pkl','wb'))
    return df['Paid Amount']


