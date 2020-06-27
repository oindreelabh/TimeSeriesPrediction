import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
%matplotlib inline
plt.style.use('Solarize_Light2')


df = pd.read_csv(r'G:/temp/processed_data.csv').set_index('Payment Date')
#df = df[df['Client Name']=='barclays']
df[df['Client Name']=='barclays']['Paid Amount'].plot(figsize=(17,9));

df[df['Client Name']=='barclays']['z_data'] = (df[df['Client Name']=='barclays']['Paid Amount'] - df[df['Client Name']=='barclays']['Paid Amount'].rolling(window=12).mean()) / df[df['Client Name']=='barclays']['Paid Amount'].rolling(window=12).std()
df[df['Client Name']=='barclays']['zp_data'] = df[df['Client Name']=='barclays']['z_data'] - df[df['Client Name']=='barclays']['z_data'].shift(12)

def plot_rolling(df):
    fig, ax = plt.subplots(3,figsize=(17, 9))
    ax[0].plot(df.index, df['Paid Amount'], label='raw data')
    ax[0].plot(df['Paid Amount'].rolling(window=12).mean(), label="rolling mean");
    ax[0].plot(df['Paid Amount'].rolling(window=12).std(), label="rolling std (x10)");
    ax[0].legend()

    ax[1].plot(df.index, df.z_data, label="de-trended data")
    ax[1].plot(df.z_data.rolling(window=12).mean(), label="rolling mean");
    ax[1].plot(df.z_data.rolling(window=12).std(), label="rolling std (x10)");
    ax[1].legend()

    ax[2].plot(df.index, df.zp_data, label="12 lag differenced de-trended data")
    ax[2].plot(df.zp_data.rolling(window=12).mean(), label="rolling mean");
    ax[2].plot(df.zp_data.rolling(window=12).std(), label="rolling std (x10)");
    ax[2].legend()

    plt.tight_layout()
    fig.autofmt_xdate()
    plt.show()
plot_rolling(df[df['Client Name']=='barclays'])

from statsmodels.tsa.stattools import adfuller

print(" > Is the data stationary ?")
dftest = adfuller(df[df['Client Name']=='barclays']['Paid Amount'], autolag='AIC')
print("Test statistic = {:.3f}".format(dftest[0]))
print("P-value = {:.3f}".format(dftest[1]))
print("Critical values :")
for k, v in dftest[4].items():
    print("\t{}: {} - The data is {} stationary with {}% confidence".format(k, v, "not" if v<dftest[0] else "", 100-int(k[:-1])))
    
print("\n > Is the de-trended data stationary ?")
dftest = adfuller(df[df['Client Name']=='barclays'].z_data.dropna(), autolag='AIC')
print("Test statistic = {:.3f}".format(dftest[0]))
print("P-value = {:.3f}".format(dftest[1]))
print("Critical values :")
for k, v in dftest[4].items():
    print("\t{}: {} - The data is {} stationary with {}% confidence".format(k, v, "not" if v<dftest[0] else "", 100-int(k[:-1])))
    
print("\n > Is the 12-lag differenced de-trended data stationary ?")
dftest = adfuller(df[df['Client Name']=='barclays'].zp_data.dropna(), autolag='AIC')
print("Test statistic = {:.3f}".format(dftest[0]))
print("P-value = {:.3f}".format(dftest[1]))
print("Critical values :")
for k, v in dftest[4].items():
    print("\t{}: {} - The data is {} stationary with {}% confidence".format(k, v, "not" if v<dftest[0] else "", 100-int(k[:-1])))

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, ax = plt.subplots(2, figsize=(20,10))
ax[0] = plot_acf(df[df['Client Name']=='barclays'].z_data.dropna(), ax=ax[0], lags=20)
ax[1] = plot_pacf(df[df['Client Name']=='barclays'].z_data.dropna(), ax=ax[1], lags=20)

from statsmodels.tsa.holtwinters import ExponentialSmoothing
def model_call(client_name,le_name):
    df = pd.read_csv(r'G:/temp/processed_data.csv').set_index('Payment Date')
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
    sse1 = np.sqrt(np.mean(np.square(test['Paid Amount'].values - pred)))
    sse2 = np.sqrt(np.mean(np.square(test['Paid Amount'].values - pred2)))
    import pickle
    if fit.aic < fit2.aic :
        pickle.dump(fit, open('model.pkl','wb'))
    else pickle.dump(fit2, open('model.pkl','wb'))