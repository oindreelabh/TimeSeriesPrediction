import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
def decomposition(ts):
	ts_log = np.log(ts + 100000)
	decomposition = seasonal_decompose(ts_log) 
	trend = decomposition.trend
	seasonal = decomposition.seasonal
	residual = decomposition.resid
	ts_log_decompose = residual
	ts_log_decompose.dropna(inplace=True)
	return ts_log_decompose