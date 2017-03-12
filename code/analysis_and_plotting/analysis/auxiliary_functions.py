import SeriesRVO
import pandas as pd
import numpy as np
import matplotlib.pylab as plt



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
    dependent = SeriesRVO.Series(dependent_f)

    independent = SeriesRVO.Series(independent_f)

    min_dep = min(dependent._table.index)
    min_ind = min(independent._table.index)
    max_dep = max(dependent._table.index)
    max_ind = max(independent._table.index)

    dependent = dependent._table[dependent._table.index > max(min_ind, min_dep)]

    dependent = dependent[dependent.index < min(max_ind, max_dep)]

    independent = independent._table[independent._table.index > max(min_ind, min_dep)]
    independent = independent[independent.index < min(max_ind, max_dep)]

    independent.drop(independent.head(5).index, inplace=True)
    dependent.drop(dependent.head(5).index, inplace=True)

    independent.drop(independent.tail(5).index, inplace=True)
    dependent.drop(dependent.tail(5).index, inplace=True)

    return dependent, independent


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