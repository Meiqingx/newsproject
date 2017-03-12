# AR SIMPLE
from Series import * 
from Predict import * 

from pandas import Series
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
import dateutil


def create_index(year, month, num_years_to_predict):
    '''
    Auxiliary function to create the index for the expanded part
    of the dataframe (future)

    Input:
        year = integer
        month = integer
        num_years_to_predict = integer

    Output:
        new_index = list of dates
    '''
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1

    list_months = list(range(1,13))* (num_years_to_predict + 1)
    list_years = []
    for i in range(0, num_years_to_predict + 1):
        partial_years = [year + i] * 12
        list_years += partial_years

    number_cycles = 12 * num_years_to_predict
    index = list_months.index(month)

    new_index = []
    for i in range(index, index + number_cycles):
        month = str(list_months[i])
        year =str(list_years[i])
        if len(month) == 1:
            month = "0" + month
        new_index.append(year + "-" + month + "-01")

    return new_index


def create_data_for_ar(series, num_years_to_predict):
    '''
    Create series suitable to predict the future (out of the sample)
    of independent variables

    Input:
        series = pandas array
        num_years_to_predict = integer

    Outpus:
        result = pandas series with empty rows for the number of years to predict
    '''

    initial_date = str(max(series.index))[:10]
    year = int(initial_date[:4])
    month = int(initial_date[5:7])

    new_index = create_index(year, month, num_years_to_predict)
    list_nas = np.empty(num_years_to_predict * 12)
    list_nas[:] = np.NAN

    data_expanded = pd.DataFrame({'Date':new_index, 'values':list_nas})
    data_expanded['Date'] = [dateutil.parser.parse(x) for x in data_expanded['Date']]

    data_expanded.index = data_expanded['Date']
    data_expanded.drop(['Date'], axis = 1, inplace = True)
    result = series.append(data_expanded)
    result.drop(['values'], axis = 1, inplace = True)
    result = result[0]

    return result


def AR_independent_vars(series, num_years_to_predict):
    '''
    Creates predictions for the independent variables

    Inputs:
        series = pandas series
        num_years_to_predict = integer

    Output:
        (original_data, predictions), where
        original_data = series of original data
        predictions = predictions for the specified number of years
    '''
    X = create_data_for_ar(series, num_years_to_predict)
    train, future = X[:len(X)-num_years_to_predict*12], X[len(X)-num_years_to_predict*12:]
    # train autoregression
    model = AR(train)
    model_fit = model.fit()
    num_lags = model_fit.k_ar
    predictions = model_fit.predict(start=num_lags, end=len(train)+len(future)-1, dynamic=False)
    integrated = train.append(predictions[len(predictions)-num_years_to_predict*12:])

    return X, predictions, integrated
