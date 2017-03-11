from ggplot import *

def build_graphic(df):

    date, actual, pred = df.columns[0], df.columns[1], df.columns[2]

    name = actual.split(',')[0]
    title = name + ': Actual and Predicted Prices'

    plotme = ggplot(aes(x=date, y=actual), data=df) +\
                    geom_line(aes(color='darkturquoise', size=2)) +\
                    geom_line(aes(x=date,y=pred, color='orangered', size=1)) +\
                    labs(title = title,#subtitle = subtitle,
                    x = "Date",y = "Price (USD)")

    return plotme



    '''+\
                    theme(plot.title = element_text(hjust = 0.5),
                    plot.subtitle = element_text(hjust = 0.5),
                    panel.border = element_rect(linetype = "solid",
                    color = "grey70", fill=NA, size=1.1))
    '''
