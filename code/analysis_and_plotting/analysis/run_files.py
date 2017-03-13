import SeriesRVO
from auxiliary_functions import load_data
from Predict import *
from AR_model import *
# import reportingEMO #change this name once the module is finalized

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


def create_one_output(name_var, dependent, independent, num_years_to_predict = 1):
    '''
    Generates the outputs of the model for only one dependent variable

    Inputs:
        name_var = name of the variable as in the dependent dataframe
        dependent = pandas data frame with dependent vars
        independent = pandas data frame with independent vars
        num_years_to_predict = integer of number of months to predict
    Output:
        () 
    '''

    # Dictionary for report
    output_dictionary = {  'lag': None,
                            'R2': None,
                            'stat': None,
                            'num_diff': None,
                            'independent_var': None,
                            'dependent_var': None}

    name_column, model, series, independent_vars, variables, order, r2, dw, differences = Predict.best_model(name_var, dependent, independent)

    output_dictionary['lag'] = order
    output_dictionary['R2'] = r2
    output_dictionary['stat'] = dw
    output_dictionary['num_diff'] = differences
    output_dictionary['independent_var'] = variables
    output_dictionary['dependent_var'] = name_column

    # Databaase for report
    pred, original = Predict.predictions(model, series, num_years_to_predict, independent_vars)
    date = pred.index
    data_for_graphs = pd.DataFrame({'date': date, 'original':original, 'prediction':pred})
    data_for_graphs.date = pd.to_datetime(data_for_graphs.date).dt.to_period('m')

    return output_dictionary, data_for_graphs

def generate_outputs(dependent, independent, num_years_to_predict = 1):
    '''
    Generates a list of dictionaries (key information of the model for the report) 
    and a list of dataframes with the original series and the predictions

    Inputs:
        dependent = dataframe with dependent variables
        independent = dataframe with independetn variables
        num_years_to_predict = integer with the number of years to predict

    Outputs:
        (list_dictionaries, list_dataframes)
    '''
    
    list_dictionaries = []
    list_dataframes = []

    for commodity in dependent.columns:
        one_result = create_one_output(commodity, dependent, independent, num_years_to_predict)
        list_dictionaries.append(one_result[0])
        list_dataframes.append(one_result[1])

    return list_dictionaries, list_dataframes


list_dictionaries, list_dataframes = generate_outputs(dependent, independent, 1)


# list_dictionaries, list_dataframes = generate_outputs(dependent[["Agr: Food: Grains, 2010=100, nominal$_sa", "Agriculture, 2010=100, nominal$_sa"]], independent, 1)

#Call the reporting module to build the reports
'''
# Assume dfs are in a list called df_list & dictionaries in a list called dictos
# THEY MUST BE IN THE SAME ORDER

for i, df in enumerate(df_list):
    #reportingEMO.build_report(df, dictos[i])
    name = 'df_tuple' + str(i) + '.p'
    p_tuple = tuple((df, dictos[i]))
    pickle.dump(p_tuple, open(name, 'wb'))

'''
