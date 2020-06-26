# Forecasting of Time Series
Our current project is based on margin calls, trades, disputes etc. Future prediction using artificial intelligence to analyze past 1-2 years of data and predict the future like whether the exposure amount is going to increase or decrease in future etc.

Files created so far : 
1) Dataset Generator - Creates a csv file containing a column for amount for different clients with datetime object as index
2) Stationarity Test - Checks whether the given time series is stationary or not by using Dickey-Fuller test, KPSS test and plotting graphs.
3) Log Transform Differencing - Converts non stationary data to stationary data by taking log transform and applying differencing.
4) Seasonal Decomposition - It takes into account the seasonality of the time series. It is decomposed into trend, seasonality, and residuals out of which residual is tested and that comes out to be closest to stationary.
5) Weighted Moving Average - This method involves taking rolling average of past values in which more recent values are given higher weight. There are many methods of assigning weights , here we have used exponential weighted moving average method where weights are assigned to all values with a decay factor
6) "project3" folder contains the flask app files to run this application.
