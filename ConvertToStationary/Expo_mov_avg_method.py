import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss


#taking input from user
client = str(input("Enter Client Name : "))
legal = str(input("Enter Legal Entity (eg. CitiBank Pune) : "))

df = pd.read_csv(r'dataset.csv', parse_dates = ['Date'], index_col = 'Date')
ts = df[(df['Client Name'] == client) & (df['Legal Entity'] == legal)]['Net Amount']

print(len(ts))

plt.title('Net Amount from {} to {}'.format(client,legal))
plt.plot(ts)
plt.show()


#tests for stationarity

#testing stationarity using graphs
def test_stationarity(ts):
        rolmean = ts.rolling(window = 12).mean()
        rolstd = ts.rolling(window = 12).std()
       
        #graphical analysis of rollmean and rollstd
        orig = plt.plot(ts, color='blue',label='Original')
        mean = plt.plot(rolmean, color='red', label='Rolling Mean')
        std = plt.plot(rolstd, color='black', label = 'Rolling Std')
        plt.legend(loc='best')
        plt.title('Rolling Mean & Standard Deviation')
        plt.show(block=False)

test_stationarity(ts)


#Dickey-Fuller Test
def dickey_f_test(ts):
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(ts, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    pval = dfoutput['p-value']
    print(f'Result: The series is {"not " if pval > 0.05 else ""}stationary')
    
dickey_f_test(ts)


#KPSS Test
def kpss_test(series, **kw):    
    statistic, p_value, n_lags, critical_values = kpss(series, **kw)
    # Format Output
    print(f'KPSS Statistic: {statistic}')
    print(f'p-value: {p_value}')
    print(f'num lags: {n_lags}')
    print('Critial Values:')
    for key, value in critical_values.items():
        print(f'   {key} : {value}')
    print(f'Result: The series is {"not " if p_value < 0.05 else ""}stationary')
    
kpss_test(ts)    



#Applying log transform
ts_log = np.log(ts)
#ts_log.dropna(inplace= True)
plt.plot(ts_log)

#Moving Avg Method for making series stationary
moving_avg = ts_log.rolling(12).mean()
plt.plot(ts_log)
plt.plot(moving_avg, color='red')

ts_log_moving_avg_diff = ts_log - moving_avg
ts_log_moving_avg_diff.head(12)
ts_log_moving_avg_diff.dropna(inplace=True)

#testing results of moving avg method
test_stationarity(ts_log_moving_avg_diff)
dickey_f_test(ts_log_moving_avg_diff)



#exponential moving Avg Method for making series stationary
expwighted_avg = pd.Series.ewm(ts_log,halflife=12).mean()
plt.plot(ts_log)
plt.plot(expwighted_avg, color='red')
expwighted_avg

ts_log_ewma_diff = ts_log - expwighted_avg

#testing results of exponential moving avg method
ts_log_ewma_diff.dropna(inplace=True)
test_stationarity(ts_log_ewma_diff)
dickey_f_test(ts_log_ewma_diff)
