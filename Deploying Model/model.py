import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pickle

def model_call(client_name, le_name):
    df = pd.read_csv(r"dataset.csv", parse_dates=['Date'], index_col='Date')
    ts = df[(df['Client Name']==client_name)&(df['Legal Entity']==le_name)]['Net Amount']
    model = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=12, damped=True)
    hw_model = model.fit(optimized=True, use_boxcox=False, remove_bias=False)
    pickle.dump(hw_model, open('model.pkl','wb'))
    return ts


