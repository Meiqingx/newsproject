
from Series import * 
from Predict import * 

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

com_file = "/Users/ruy/Documents/UChicago/Winter_2017/cs/Project/newsproject/code/scrapers/commodities_data/commodities_prices.csv" 

database = Series.create_series(com_file)

series = database["WLDALUMINUM"]

independent_vars = database[["WLDBEEF", "WLDSILVER"]]

model = Predict.model(series, 2, independent_vars = None)

pred = Predict.predictions(model, series, independent_vars)

residual = Predict.residuals(model, series, independent_vars = None)

dw = Predict.durbin_watson(model, series, independent_vars)

print(dw)


# results_ARIMA = model.fit(disp=-1) 

# # Back to the original scale

# # The prediction is in diff logs
# predictions = pd.Series(results_ARIMA.fittedvalues, copy=True)

# # Create a dataframe for the prediction in logs
# predictions_logs = pd.Series(np.log(series.ix[0]), index=series.index)

# # Auxiliry series to predict values (sum of the differences)
# predictions_cumsum = predictions.cumsum()

# # Prediction in logs (without differences)
# predictions_logs = predictions_logs.add(predictions_cumsum,fill_value=0)

# # Exponentiate the results to get original units
# prediction_original_units = np.exp(predictions_logs)

# return prediction_original_units
