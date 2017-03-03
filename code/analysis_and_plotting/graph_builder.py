import merger as mrgr
import matplotlib.pyplot as plt



def plot_a_lot(df):
    '''
    '''

    dates = df['Date'].tolist()

    rows = len(df.columns[1:])

    fig, ax = plt.subplots(nrows=rows,ncols=1,figsize=(8,6*rows))

    for i, name in enumerate(list(df.columns)[1:]):
        label = name
        values = df[name].tolist()
        #position = int(str(rows) + str(1) + str(i + 1))
        plt.subplot(rows,1,i+1)
        build_plot(dates, values, label)


    plt.savefig('timeseries')#.pdf', format='pdf')

    plt.close('all')






def build_plot(dates, values, label):
    '''
    Generates a single plot.
    '''

    plt.plot(dates,values,color='turquoise',lw=2)
    plt.title(label, fontsize=10)
    #plt.xlabel('Date')
    #plt.ylabel(lable)
    #plt.xlim([0, 1])
    plt.tight_layout()
    #plt.show()
    #plt.close()



dataframes = mrgr.read_files()


merged_df = mrgr.merge_dfs(dataframes)

mrgr.gen_sqrs_cbcs(merged_df)


plot_a_lot(merged_df)
