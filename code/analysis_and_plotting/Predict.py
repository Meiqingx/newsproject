
import SeriesRVO
from AR_model import * 

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima_model import ARIMA
from queue import PriorityQueue
import time

import statsmodels.api as sm


class Predict:


    def model(series, autoregressive_terms, num_years_to_predict = 1, independent_vars = None):
        '''
        Creates the ARIMA model

        Inputs:
            series = finantial series in original units
            autoregressive_terms = number of autoregressive terms for the ARIMA model,
                those are the number of variables to consider from the past
        '''
        # Params
        differences = 1
        moving_avg_terms = 0
        params = (autoregressive_terms, differences, moving_avg_terms)

        # Log to finantial interpretation 
        series = np.log(series)
        dependent_future = create_data_for_ar(series, num_years_to_predict)

        if independent_vars is not None:
            independent_vars = np.log(independent_vars)
            independent_future = SeriesRVO.series_for_prediction(
                independent_vars, num_years_to_predict)

            model = sm.tsa.ARIMA(dependent_future[:len(dependent_future)-(
                12*num_years_to_predict)], (1,1,0), 
                exog = independent_future[:len(dependent_future)-(
                    12*num_years_to_predict)])
        else:
            model = sm.tsa.ARIMA(dependent_future[:len(dependent_future)-(
                12*num_years_to_predict)], (1,1,0))

        return model, differences


    def predictions(model, series, num_years_to_predict = 1, independent_vars = None):
        '''
        Given an ARIMA model, predicts the values of the series

        Inputs:
            model = ARIMA model
            series = series to predict of the class Predict
            independent_vars = array of controls

        Outputs:
            array with the predictions
        '''
        if not isinstance(num_years_to_predict, int):
            num_years_to_predict = int(num_years_to_predict // 1)
            print("Please use integers in number of years to predict. This time,")
            print("we will predict", num_years_to_predict, "years")

        original_expanded = create_data_for_ar(series, num_years_to_predict)

        # TO LOGS
        series = np.log(series)
        independent_future = None
        if independent_vars is not None:
            independent_vars = np.log(independent_vars)
            independent_future = SeriesRVO.series_for_prediction(independent_vars, num_years_to_predict)

        dependent_future = create_data_for_ar(series, num_years_to_predict)
        
        results_ARIMA = model.fit(disp=-1) 

        if independent_future is not None:
            predictions = results_ARIMA.predict(start=1,  end = len(independent_future), exog = independent_future)[:-1]
        else:
            predictions = results_ARIMA.predict(start=1,  end = len(dependent_future))[:-1]

        # Back to the original scale because the prediction is in diff logs
        # Create a dataframe for the prediction in logs (initial value)
        predictions_logs = pd.Series(series.ix[0], index=dependent_future.index)

        # Auxiliry series to predict values (sum of the differences)
        predictions_cumsum = predictions.cumsum()

        # Prediction in logs (without differences)
        predictions_logs = predictions_logs.add(predictions_cumsum,fill_value=0)

        # Exponentiate the results to get original units
        prediction_original_units = np.exp(predictions_logs)

        return prediction_original_units, original_expanded


    def residuals(model, series, independent_vars = None):
        '''
        Generates a series of residuals
        
        Inputs:
            model = arima model
            series = series of dependend variable
            independent_vars = array of independent variables
        Outputs:
            residual = series of residuals
        '''
        y_hat = Predict.predictions(model, series, independent_vars = independent_vars)[0]
        residuals = series - y_hat
        residuals = residuals[:len(series)]

        return residuals


    def durbin_watson(model, series, independent_vars = None):
        '''
        Computes the Durbin - Watson statistic
        Parts of the code from: http://statsmodels.sourceforge.net/devel/_modules/statsmodels/stats/stattools.html

        Inputs:
            model = arima model
            series = series of dependend variable
            independent_vars = array of independent variables
        Outputs:
            dw = statistic durbin-watson
        '''
        resids = np.asarray(Predict.residuals(model, series, independent_vars))
        diff_resids = np.diff(resids) # First difference
        dw = np.sum(diff_resids**2) / np.sum(resids**2)
        return dw


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
        y_hat = Predict.predictions(model, series, independent_vars = independent_vars)[0]
        y_mean = np.mean(series)
        var_org = np.sum((series - y_mean) ** 2)
        var_hat = np.sum((series - y_hat) ** 2)
        r_square = 1 - (var_hat/var_org)

        return r_square


    def adjusted_r_square(model, series, autoregressive_terms, independent_vars = None):
        '''
        Computes the adjusted R2 

        Inputs:
            model = model class Predict
            series = array
            autoregressive_terms = number of autoregressive terms
            independent_vars = array of independent variables
        Outputs:
            adjusted R2 [0,1]
        '''
        sample_size = len(series)
        number_predictors = autoregressive_terms

        if independent_vars is not None:
            number_predictors += len(independent_vars.columns)

        r2 = Predict.r_square(model, series, independent_vars)

        rv = 1 - ((1 - r2) * ((sample_size - 1)/(sample_size - number_predictors -1)))

        return rv


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
        y_hat = Predict.predictions(model, series, independent_vars = independent_vars)[0]
        mse = np.sum((y_hat - series) ** 2) / len(series)
        return mse


    def best_order(series, independent_vars = None, stop_num_lags = 1):
        '''
        Selects the number of lags

        Inputs:
            series = series of dependent vars
            independent_vars = dataframe of independent variables
            stop_num_lags = maximum number of lags to explore
        Outputs:
            winner = best number of lags 
        '''
        # First, select the number of lags
        measures_of_fit_acumulator = PriorityQueue()

        for i in list(range(1, stop_num_lags + 1)):
            model = Predict.model(series, i, independent_vars = independent_vars)[0]
            adjusted_r_square = Predict.adjusted_r_square(model, series, i, independent_vars)
            measures_of_fit_acumulator.put((-Predict.adjusted_r_square(model, series, i, independent_vars), i))


        winner = measures_of_fit_acumulator.get()[1]
        return winner

    def best_parameters(name_column, database_dependent, database_independent, num_ind_var = 2):
        '''
        Selects the best model with X (num_ind_var) variables

        Input:
            name_column = name of the column of the dependent variable
            database_dependent
            database_independent
            num_ind_var = number of independent vars to select

        Outputs:
            list of [list_independent_vars, autoregressive_terms], where
            list_independent_vars = list of the names of the independetn variables
            autoregressive_terms = number of the best number of autoregressive terms


        '''
        database_dependent = database_dependent.dropna(axis=1)
        database_independent = database_independent.dropna(axis=1)

        list_predictors = list(database_independent.columns)

        series = database_dependent[name_column]
        autoregressive_terms = Predict.best_order(series)

        list_independent_vars = []

        for j in range(num_ind_var):
            queue_for_predictors = PriorityQueue()
            
            for element in list_predictors:
                if element not in list_independent_vars:
                    list_independent_vars.append(element)
                    print("The dependent var is", name_column)
                    print("The independent vars are", list_independent_vars, ".Number regressive terms", autoregressive_terms)
                    independent_vars = database_independent[list_independent_vars]
                    model = Predict.model(series, autoregressive_terms, independent_vars = independent_vars)[0]
                    adjusted_r_square = Predict.adjusted_r_square(model, series, autoregressive_terms, independent_vars)
                    queue_for_predictors.put((-adjusted_r_square, element))
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

        best_model, differences = Predict.model(series, order, independent_vars = independent_vars)

        r2 = Predict.adjusted_r_square(best_model, series, order, independent_vars = independent_vars)

        dw = Predict.durbin_watson(best_model, series, independent_vars)

        return name_column, best_model, series, independent_vars, variables, order, r2, dw, differences


























