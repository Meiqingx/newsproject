import merger as mrgr
import matplotlib.pyplot as plt



def plot_a_lot(df, filename):
    '''
    Plots a lot of plots in one single figure.

    Inputs:
        df (pandas dataframe): A dataframe of the variables to be plotted.
        filename (str): The name of the filename to output.

    Returns:
        None

    Outputs:
        [filename].png (png image): A png file with the name [filename].
    '''

    dates = df['Date'].tolist()

    rows = len(df.columns[1:])

    fig, ax = plt.subplots(nrows=rows,ncols=1,figsize=(8,6*rows))

    for i, name in enumerate(list(df.columns)[1:]):
        label = name
        values = df[name].tolist()
        plt.subplot(rows,1,i+1)
        build_plot(dates, values, label)

    plt.savefig(filename)

    plt.close('all')



def build_plot(dates, values, label):
    '''
    Generates a single plot.

    Inputs:
        dates (list of date-time objects): A list of the dates to be plotted on
                                           the x-axis.
        values (list of numbers): A list of the values to be plotted on the
                                  y-axis.
        label (str): A string to use as the title for the plot.

    Returns:
        None

    Outputs:
        The plot generated.
    '''

    plt.plot(dates,values,color='turquoise',lw=2)
    plt.title(label, fontsize=10)
    plt.xlabel('Date')
    plt.tight_layout()
    #plt.show()
    #plt.close()



def plot_plots(predictors):
    '''
    Because of the size limitation for figures, breaks predictors dataframe into
    chunks of many columns and generates one plot for each chunk.

    Inputs:
        predictors (pandas df): A dataframe of the independent variables,
                                including their second- and third-order terms.

    Returns:
        None

    Outputs:
        A series of png files, each containing up to 50 plots.
    '''

    cols = len(predictors.columns) - 1
    date = predictors.iloc[:,0]

    m = 1
    n = 51
    x = 1

    bad = []

    while m < cols:
        zero = [0]
        sel = [x for x in range(m,n)]
        for i in range(len(sel)):
            val = sel[i]
            if val > cols:
                bad.append(val)
        for val in bad:
                sel.remove(val)
        selected = zero + sel
        preds = predictors.iloc[:, selected]
        plot_a_lot(preds,'predictors' + str(x))
        m = n
        n += 50
        x += 1


# Tiny bit of duplication here, but I think it's better than copying a function
# to serve as the date converter.

predictor_dfs, outcomes = mrgr.read_files()
predictors = mrgr.merge_dfs(predictor_dfs)
mrgr.gen_sqrs_cbcs(predictors)

plot_plots(predictors)
plot_a_lot(outcomes,'outcomes')
