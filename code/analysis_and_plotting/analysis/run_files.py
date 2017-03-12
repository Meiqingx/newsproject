
# from Series import * 
from Series import *
from Predict import * 
from AR_model import * 

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

import statsmodels.api as sm


# Load the databases of dependent and independent variables

## CHANGE THIS ####
dependent_f = '/Users/ruy/Documents/UChicago/Winter_2017/cs/Project/newsproject/code/analysis_and_plotting/outcomes.csv'
independent_f = '/Users/ruy/Documents/UChicago/Winter_2017/cs/Project/newsproject/code/analysis_and_plotting/predictors.csv'

def load_data(dependent_f, independent_f):
    '''
    Load the necessary data in two databases: dependent and independent
    
    Inputs:
        dependent_f = name of the csv file with dependent variables
        independent_f = names of the csv file with independent variables

    Outputs:
        (dependent, independent) where
        dependent = dataframe of dependent variables
        independent = dataframe of independent variables

    '''
    # Create individual dataframes
    dependent = Series.create_pandas(dependent_f)
    #dependent.create_pandas(dependent_f)
    independent = Series.create_pandas(independent_f)
    # dependent = Series.create_pandas(dependent_f)
    # independent = Series.create_pandas(independent_f)

    min_dep = min(dependent.index)
    min_ind = min(independent.index)
    max_dep = max(dependent.index)
    max_ind = max(independent.index)

    dependent = dependent[dependent.index > max(min_ind, min_dep)]
    dependent = dependent[dependent.index < min(max_ind, max_dep)]

    independent = independent[independent.index > max(min_ind, min_dep)]
    independent = independent[independent.index < min(max_ind, max_dep)]

    independent.drop(independent.head(5).index, inplace=True)
    dependent.drop(dependent.head(5).index, inplace=True)

    independent.drop(independent.tail(5).index, inplace=True)
    dependent.drop(dependent.tail(5).index, inplace=True)

    return dependent, independent

dependent, independent = load_data(dependent_f, independent_f)

# Get the best model for each of the dependent variables
# dic_models = {}
# for name_var in  dependent.columns:
#     model = Predict.best_model(name_var, dependent, independent)
#     dic_models[name_var] = model


def gen_graph(series, pred):
    '''
    '''
    plt.title("Data vs Prediction")
    plt.plot(pred, color = "red", label = "Prediction", linewidth = 1)
    plt.plot(series, color = "blue", label = "Original Data", linewidth = 1.5)
    plt.legend(loc="upper left")
    plt.show()
    # plt.savefig("plot_result.png")
    plt.close()

# (best_model, variables, order, independent_vars, series)
# model, variables, order, independent_vars, series = dic_models["Aluminum, $/mt, nominal$_sa"]
# pred = Predict.predictions(model, series, independent_vars)

model, variables, order, independent_vars, series = Predict.best_model('Gold, $/toz, nominal$_sa', dependent, independent)
# pred = Predict.predictions(model, series, independent_vars)







