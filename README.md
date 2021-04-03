# Forecasting of Time Series
Our current project is based on margin calls, trades, disputes etc. Future prediction using statistical models to analyze past 1-2 years of data and predict the future like whether the exposure amount is going to increase or decrease in future etc.

## TECHNOLOGY USED :

Model - Python 3 - pandas, matplotlib, numpy, statsmodels, datetime

UI - Python Flask, HTML CSS, JavaScript, flask_wtf, plotly python

## DATASET GENERATION

 Dataset Generator - Creates a csv file containing a column for amount for different clients with datetime object as index

## TESTING STATIONARITY

 Stationarity Test - Checks whether the given time series is stationary or not by using Dickey-Fuller test, KPSS test and plotting graphs.

## CONVERTING TO STATIONARY SERIES
1) Log Transform Differencing - Converts non stationary data to stationary data by taking log transform and applying differencing.
2) Seasonal Decomposition - It takes into account the seasonality of the time series. It is decomposed into trend, seasonality, and residuals out of which residual is tested and that comes out to be closest to stationary.
3) Weighted Moving Average - This method involves taking rolling average of past values in which more recent values are given higher weight. There are many methods of assigning weights , here we have used exponential weighted moving average method where weights are assigned to all values with a decay factor

## CREATING MODEL
1) Holt-Winter’s Exponential Smoothing - It is an algorithm that predicts future data based on previous data when the same data is indexed based on date (or time). We decided to go with this model because it handles trend and seasonality in data, if any.

2) Auto Regression - Autoregression is a time series model that uses observations from previous time steps as input to a regression equation to predict the value at the next time step.It is a very simple idea that can result in accurate forecasts on a range of time series problems.

## MODEL INTEGRATION TO UI

"updated" folder contains all the required files. The flaskfile.py should be run in order to view this application.
All the modules present in TECHNOLOGY USED section should be pre-installed.

<p align="center">
  For details on the models tried and tested, UI features and better understanding of system workflow, please refer to <a href="https://docs.google.com/document/d/1zDoQaWnT0mUfGLrbunjLIUqtAPevApgmvw2dFgixFj8/edit#heading=h.z6ne0og04bp5">this document</a>.
</p>
