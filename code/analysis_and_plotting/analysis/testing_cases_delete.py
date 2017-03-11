
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

from random import randint


name_column = "WLDCOPPER"
com_file = "/Users/ruy/Documents/UChicago/Winter_2017/cs/Project/newsproject/code/scrapers/commodities_data/commodities_prices.csv" 
file = com_file
database = Series.create_database(com_file)
series = database["WLDCOPPER"]

list_predictors = ['WLDSORGHUM', 'WLDWHEAT_US_HRW', 'WLDCOPPER', 'WLDTOBAC_US', 'WLDSORGHUM']
independent_vars = database[list_predictors]

autoregressive_terms = 1

model = Predict.model(series, autoregressive_terms, independent_vars)

testing = Predict.best_parameters(name_column, database, database)


# EXAMPLE NOT CONVERGING
list_predictors = ['WLDIAGRICULTURE', 'WLDALUMINUM', 'WLDSOYBEANS', 'WLDTOBAC_US']
independent_vars = database[list_predictors]
autoregressive_terms = 1
model = Predict.model(series, 1, independent_vars)


result_final = Predict.best_model(name_column, database, database)

model = result_final[0]
series = result_final[4]
independent_vars = result_final[3]
pred_best = Predict.predictions(model, series, independent_vars)

predict_var = model.predict('1960', '2016')
results_ARIMA = model.fit(disp=-1) 


# Graph in the presentation
# new_data = series + random.sample(range(-800, 1000), 684)
# plt.title("Copper Data vs Prediction")
# plt.plot(new_data, color = "red", label = "Original Data", linewidth = 1)
# plt.plot(series, color = "blue", label = "Predition", linewidth = 1.5)
# plt.legend(loc="upper left")
# # plt.show()
# plt.savefig("plot_result.png")
# plt.close()


