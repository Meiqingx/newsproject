import numpy as np
from plot_pred import build_plot
from pylatex import Document, MiniPage, PageStyle, Section, Subsection, Tabular, \
                    MultiColumn, Head, Foot, Figure, LargeText, figure,\
                    MediumText, LineBreak, simple_page_number
from pylatex.utils import italic, bold, NoEscape
import os
import time


PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')

###########################################################
# This module produces individual reports for commodities #
# prices prediction. It provides methods to set titles,   #
# executive summaries, headers and footers, graphs, and   #
# tables for individual reports.                          #
###########################################################

class Report:
    """
    A class for customized report producing for commodities prices
    prediction models.

    """

    def __init__(self, margin='1.0in', default_filepath=PATH):

        if not os.path.exists(default_filepath):
            os.makedirs(default_filepath)

        geometry_options = {'margin': margin, 'paperheight': '11in', \
                            'paperwidth':'8.5in'}

        self.doc = Document(default_filepath= default_filepath, \
                            geometry_options=geometry_options, font_size='large')


    def add_headfoot(self, header_image):
        '''
        Take a path of a header image, and insert it in the report. Also
        set default footers.
        '''
        header = PageStyle('header')

        today = time.strftime('%Y %B %d')
        company = 'Ochoa Valdés-Ortiz Zhang, Ltd.'

        #add header
        with header.create(Head('C')) as cheader:
            with cheader.create(Figure(position='t!')) as graph:
                graph.add_image(header_image, width='6.5in')


        #left footer
        with header.create(Foot('L')):
            header.append(today)

        #right footer
        with header.create(Foot('R')):
            header.append(company)


        self.doc.preamble.append(header)

        self.doc.change_document_style('header')

    def set_title(self, title, subtitle):
        '''
        Take two strings, and set report title and subtitle.
        '''
        with self.doc.create(MiniPage(align='c')):
            self.doc.append(LargeText(bold(title)))
            #self.doc.append(LineBreak())
            self.doc.append(MediumText(italic(bold(subtitle))))

    def add_executive_summary(self, text):
        '''
        Take a text string, and insert executive summary.
        '''
        with self.doc.create(Section('Executive Summary')) as summary:
            with summary.create(Tabular('p{15.4cm}')) as sumtable:
                sumtable.add_hline()
                sumtable.add_row([italic(text)])
                sumtable.add_empty_row()
                sumtable.add_empty_row()

    def gen_summary_text(self, results):
        '''
        Takes a dictionary of analysis results, and generate a summary text string. 
        '''
        text0 = 'Summary: {} and {} have {} explanation power for {} price trend.' 

        var1, var2 = results['independent_var']

        dependent_var = results['dependent_var']

        R2 = results['R2']

        if R2 >= 0.9:
            interpretation = 'high'

        elif R2 < 0.9 and R2 > 0.5:
            interpretation = 'adequate'

        else:
            interpretation = 'low'

        text = text0.format(var1, var2, interpretation, dependent_var)

        return text

    def insert_graph(self, df):
        '''
        Take a dataframe of prices prediction data, draw a plot
        and insert it in the report.
        '''

        with self.doc.create(Figure(position='ht!')) as plot:
            build_plot(df)
            plot.add_plot(width="6.5in")


    def insert_table(self, results):
        '''
        Take a dictionary of statistical results of the model, and
        insert a summary table in the report.
        '''
        indie_var = ', '.join(results['independent_var'])
        R2 = round(results['R2'], 2)
        dstat = round(results['stat'], 2)

        section = Section('Statistical Results')

        table = Tabular('l p{10cm}')
        table.add_hline()
        table.add_row((MultiColumn(2, align='c', data=bold('Characteristics of Model')),))
        table.add_hline(cmidruleoption='r')
        table.add_row((bold('Model'), 'ARIMA'), color='lightgray')
        table.add_row((bold('Lag variables'), results['lag']))
        table.add_row((bold('Independent variables'), indie_var), color='lightgray')
        table.add_row((bold('Number of differences'), results['num_diff']))
        table.add_row((NoEscape('\symbf{$R^2$}'), results['R2']), color='lightgray')
        table.add_row((bold('Durbin-Watson Statistic'), results['stat']))
        table.add_hline()

        section.append(LineBreak())
        section.append(table)

        self.doc.append(section)


    def gen_pdf(self, filepath=None):
        '''
        Generate pdf report. Take a filepath as optional.
        '''
        self.doc.generate_pdf(filepath, clean=True, clean_tex=True,\
                              compiler='pdflatex',silent=True)


def build_report(df, results, header_image):
    '''
    Take a dataframe of prediction data and a dictionary of
    analysis results, and build a report for an individual model.
    '''

    name = df.columns[1].split(',')[0]

    r = Report()

    r.set_title('Forecast:  ', name)
    r.add_headfoot(header_image)

    summary = r.gen_summary_text(results)

    r.add_executive_summary(summary)
    r.insert_graph(df)
    r.insert_table(results)

    output_path = os.path.join(PATH, name)

    r.gen_pdf(output_path)
