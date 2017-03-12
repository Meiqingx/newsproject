import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def build_plot(df):
    '''
    '''
    date, actual, pred = df.columns[0], df.columns[1], df.columns[2]

    name = actual.split(',')[0]
    title = name + ': Actual and Predicted Prices'

    dates = df[date]
    actuals = df[actual]
    preds = df[pred]

    fig, ax = plt.subplots(figsize=(6.5,4))
    plt.subplot(111, facecolor='lightgray')
    plt.minorticks_on()
    plt.plot(dates, actuals,color='darkturquoise',lw=2, label='Actual')
    plt.plot(dates, preds,color='orangered',lw=1, label='Predicted')
    plt.grid(b=True, which='major', color='white', linewidth=.75)
    plt.grid(b=True, which='minor', color='white', linewidth=.25)
    plt.title(title, fontsize=15)
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend(loc=0,fontsize=11)
    plt.tight_layout()
    plt.show()
    #plt.close()
