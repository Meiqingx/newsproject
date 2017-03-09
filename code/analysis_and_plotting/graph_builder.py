import merger as mrgr
import matplotlib.pyplot as plt



def plot_a_lot(df, filename):
    '''
    '''

    dates = df['Date'].tolist()

    rows = len(df.columns[1:])

    fig, ax = plt.subplots(nrows=rows,ncols=1,figsize=(8,6*rows))

    for i, name in enumerate(list(df.columns)[1:]):
        label = name
        values = df[name].tolist()
        plt.subplot(rows,1,i+1)
        build_plot(dates, values, label)


    plt.savefig(filename)#.pdf', format='pdf')

    plt.close('all')






def build_plot(dates, values, label):
    '''
    Generates a single plot.
    '''

    plt.plot(dates,values,color='turquoise',lw=2)
    plt.title(label, fontsize=10)
    plt.xlabel('Date')
    #plt.ylabel(label)
    #plt.xlim([0, 1])
    plt.tight_layout()
    #plt.show()
    #plt.close()



def plot_plots(predictors):
    '''
    Because of the size limitation for figures, breaks predictors dataframe into
    chunks of many columns and generates one plot for each chunk.
    '''

    cols = len(predictors.columns) - 1
    date = predictors.iloc[:,0]

    m = 1
    n = 50
    x = 1

    while m < cols:
        zero = [0]
        sel = [x for x in range(m,n)]
        for i in range(len(sel)):
            val = sel[i]
            if val > cols:
                sel.remove(val)
        selected = zero + sel
        preds = predictors.iloc[:, selected]
        plot_a_lot(preds,'predictors' + str(x))
        m = n
        n += 50
        x += 1



predictor_dfs, outcomes = mrgr.read_files()


predictors = mrgr.merge_dfs(predictor_dfs)
mrgr.gen_sqrs_cbcs(predictors)

plot_plots(predictors)

#plot_a_lot(outcomes,'outcomes')
