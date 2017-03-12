import SeriesRVO
from auxiliary_functions import load_data
from Predict import *
from AR_model import *

import pandas as pd
import numpy as np
from matplotlib.pylab import rcParams
import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

import statsmodels.api as sm


# Load the databases of dependent and independent variables
dependent_f = '../outcomes.csv'
independent_f = '../predictors.csv'

dependent, independent = load_data(dependent_f, independent_f)

# Get the best model for each of the dependent variables
# dic_models = {}
# for name_var in  dependent.columns:
#     model = Predict.best_model(name_var, dependent, independent)
#     dic_models[name_var] = model

series = dependent['Gold, $/toz, nominal$_sa']


# # (best_model, variables, order, independent_vars, series)
# # model, variables, order, independent_vars, series = dic_models["Aluminum, $/mt, nominal$_sa"]
# # pred = Predict.predictions(model, series, independent_vars)

# model, variables, order, independent_vars, series = Predict.best_model('Gold, $/toz, nominal$_sa', dependent, independent)

# # pred = Predict.predictions(model, series, independent_vars)

# pred = Predict.predictions(model, series, 1, independent_vars)

# dw = Predict.durbin_watson(model, series, independent_vars)

# resi = Predict.residuals(model, series, independent_vars)[:len(series)]

# r2 = Predict.r_square(model, series, independent_vars)


# # a dictionary with these keys: 'lag', 'R2', 'stat', 'num_diff', 'independent_var', 'dependent_var'





