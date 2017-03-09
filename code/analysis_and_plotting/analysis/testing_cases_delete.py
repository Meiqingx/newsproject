
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



# WLDBEEF
# WLDSILVER

# independent_vars = database[["WLDBEEF"]]

# model = Predict.model(series, 1, independent_vars)

# pred = Predict.predictions(model, series, independent_vars)

# residual = Predict.residuals(model, series, independent_vars)

# dw = Predict.durbin_watson(model, series, independent_vars)

# r_square = Predict.r_square(model, series, independent_vars)

# print(dw)

# print(r_square)

# list_predictors = ['WLDSORGHUM', 'WLDWHEAT_US_HRW', 'WLDCOPPER', 'WLDTOBAC_US', 'WLDSORGHUM']

# independent_vars = database[list_predictors]

# everything_ok = Predict.model(series, 1, independent_vars)

# residual = Predict.residuals(everything_ok, series, independent_vars)

# dw_2 = Predict.durbin_watson(everything_ok, series, independent_vars)

# r_square_2 = Predict.r_square(everything_ok, series, independent_vars)

# print(dw_2)

# print(r_square_2)


# prediction_ok = Predict.predictions(everything_ok, series, independent_vars)

# parameters_testing = Predict.best_parameters("WLDBEEF", database, database)


# order = parameters_testing[1]

# variables = parameters_testing[0]

# series = database[name_column]
# independent_vars = database[variables]

# best_model = Predict.model(series, order, independent_vars)

# best_test_model = Predict.best_model("WLDBEEF", 1, database)


best_model, variables, order, independent_vars, series    


name_column = "WLDBEEF"
com_file = "/Users/ruy/Documents/UChicago/Winter_2017/cs/Project/newsproject/code/scrapers/commodities_data/commodities_prices.csv" 
database = Series.create_series(com_file)
series = database["WLDBEEF"]


result_final = Predict.best_model(name_column, database, database)

model = result_final[0]
series = result_final[4]
independent_vars = result_final[3]


pred_best = Predict.predictions(model, series, independent_vars)


# predict_var = model.predict('1960', '2016')

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
