import matplotlib.pyplot as plt

def build_plot(df):
    '''
    Builds a plot from a dataframe of dates, actual prices, & predicted prices.

    Inputs:
        df (pandas dataframe): A dataframe with three columns:  dates, actual
                               prices, and predicted prices.
    Outputs:
        fig (matplotlib figure): A plot of the actual and predicted prices over
                                 the time range in dates.

    Returns:
        None.
    '''
    date, actual, pred = df.columns[0], df.columns[1], df.columns[2]

    name = actual.split(',')[0]
    title = name + ': Actual and Predicted Prices'

    dates = df[date]
    actuals = df[actual]
    preds = df[pred]

    fig, ax = plt.subplots(figsize=(8,5))
    plt.subplot(111, facecolor='lightgray')
    plt.minorticks_on()
    plt.plot(dates, actuals,color='darkturquoise',lw=1.5, label='Actual')
    plt.plot(dates, preds,color='orangered',lw=1, label='Predicted')
    plt.grid(b=True, which='major', color='white', linewidth=.75)
    plt.grid(b=True, which='minor', color='white', linewidth=.25)
    plt.title(title, fontsize=15)
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend(loc=0,fontsize=11)
    plt.tight_layout()
    #plt.show()
    #plt.close()
