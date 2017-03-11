
from Series import * 
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima_model import ARIMA
from queue import PriorityQueue


class Predict:

    def model(series, autoregressive_terms, independent_vars = None):
        '''
        Creates the ARIMA model

        Inputs:
            series = finantial series in original units
            autoregressive_terms = number of autoregressive terms for the ARIMA model,
                those are the number of variables to consider from the past
        '''
        # Given the finantial data, and the easy intepretation,
        # I will use log
        series = np.log(series)
        differences = 1
        moving_avg_terms = 1

        params = (autoregressive_terms, differences, moving_avg_terms)

        if independent_vars is not None:
            independent_vars = np.log(independent_vars)

        model = ARIMA(series, params, exog = independent_vars, freq = 'M')

        return model

    def predictions(model, series, independent_vars = None):
        '''
        Given an ARIMA model, predicts the values of the series

        Inputs:
            model = ARIMA model
            series = series to predict of the class Predict
            independent_vars = array of controls

        Outputs:
            array with the predictions
        '''
        results_ARIMA = model.fit(disp=-1) 

        # Back to the original scale

        # The prediction is in diff logs
        predictions = pd.Series(results_ARIMA.fittedvalues, copy=True)

        # Create a dataframe for the prediction in logs
        predictions_logs = pd.Series(np.log(series.ix[0]), index=series.index)

        # Auxiliry series to predict values (sum of the differences)
        predictions_cumsum = predictions.cumsum()

        # Prediction in logs (without differences)
        predictions_logs = predictions_logs.add(predictions_cumsum,fill_value=0)

        # Exponentiate the results to get original units
        prediction_original_units = np.exp(predictions_logs)

        return prediction_original_units

    def residuals(model, series, independent_vars = None):
        '''
        Generates a series of residuals
        '''
        y_hat = Predict.predictions(model, series, independent_vars)
        residuals = series - y_hat

        return residuals

    def durbin_watson(model, series, independent_vars = None):
        '''
        Computes the Durbin - Watson statistic
        Parts of the code from: http://statsmodels.sourceforge.net/devel/_modules/statsmodels/stats/stattools.html
        '''
        resids = np.asarray(Predict.residuals(model, series, independent_vars))
        diff_resids = np.diff(resids) # First difference
        dw = np.sum(diff_resids**2) / np.sum(resids**2)
        return dw

    def measures_of_fit(model, series, independent_vars = None):
        '''
        Creates measures to decide between models

        Inputs:
            model = ARIMA model of class Predict
            series = series of class Series
            independent_vars = array of independent vars

        Outputs:

        '''
        return None

    def r_square(model, series, independent_vars = None):
        '''
        Generates the R square measure

        Inputs:
            model = timne series model of class Predict
            series = series of an asset
            independent_vars = array of independent variables
        Outputs:
            r_square [0,1]
        '''
        y_hat = Predict.predictions(model, series, independent_vars)
        y_mean = np.mean(series)
        var_org = np.sum((series - y_mean) ** 2)
        var_hat = np.sum((series - y_hat) ** 2)
        r_square = 1 - (var_hat/var_org)
        print("var_hat is", var_hat)
        print("var_org is", var_org)
        return r_square

    def mse(model, series, independent_vars = None):
        '''
        Generates MSE

        Inputs:
            model = time series model of class Predict
            series = series of an asset
            independent_vars = array of independent variables
        Outputs:
            mse (positive number)
        '''
        y_hat = Predict.predictions(model, series, independent_vars)
        mse = np.sum((y_hat - series) ** 2) / len(series)
        return mse

    def best_order(series, independent_vars = None):
        '''
        Creates the parameter for the best model
        '''
        # First, select the number of lags
        measures_of_fit_acumulator = PriorityQueue()
        for i in [1,2,3]:
            model = Predict.model(series, i, independent_vars)
            r_square = Predict.r_square(model, series, independent_vars)
            print(r_square)
            measures_of_fit_acumulator.put((-Predict.r_square(model, series, independent_vars), i))

        winner = measures_of_fit_acumulator.get()[1]
        return winner

    def best_parameters(name_column, database_dependent, database_independent):
        '''
        Selects the best model with 5 variables

        Input:
            name_column = name of the column of the dependent variable
            database_dependent
            database_independent

        Outputs:
            list of [list_independent_vars, autoregressive_terms], where
            list_independent_vars = list of the names of the independetn variables
            autoregressive_terms = number of the best number of autoregressive terms


        '''
        database_dependent = database_dependent.dropna(axis=1)
        database_independent = database_independent.dropna(axis=1)

        ### MODIFY THIS
        database_independent = database_independent.drop(['WLDCRUDE_BRENT'], axis=1)
        ### MODIFY THIS

        list_predictors = list(database_independent.columns)
        print(list_predictors)

        series = database_dependent[name_column]
        autoregressive_terms = Predict.best_order(series)

        list_independent_vars = []

        for j in range(5):
            queue_for_predictors = PriorityQueue()
            
            for element in list_predictors:

                list_independent_vars.append(element)                
                independent_vars = database_independent[list_independent_vars]
                print("before model", element)
                model = Predict.model(series, autoregressive_terms, independent_vars)
                print("before r_square", element)
                r_square = Predict.r_square(model, series, independent_vars)
                print("before queue", element)
                queue_for_predictors.put((-r_square, element))
                del list_independent_vars[-1]
                
            best_one_variable = queue_for_predictors.get()[1]
            list_independent_vars.append(best_one_variable)


        return list_independent_vars, autoregressive_terms

    def best_model(name_column, database_dependent, database_independent):
        '''
        Selects the best model and generates some parameters to test the model

        Inputs:
            name_column = name of the dependent variable
            database_dependent = database of dependent variables
            database_independent = database of independent variables

        Outputs:
            list = [best_model, variables, order, independent_vars, series]
            best_model = ARIMA model of class Predict
            variables = list of names of indepenedent variables
            order = order of the autoregression process
            independent_vars = dataframe with independent variables
        '''

        variables, order = Predict.best_parameters(name_column, database_dependent, database_independent)

        series = database_dependent[name_column]
        independent_vars = database_independent[variables]

        best_model = Predict.model(series, order, independent_vars)

        return best_model, variables, order, independent_vars, series


























