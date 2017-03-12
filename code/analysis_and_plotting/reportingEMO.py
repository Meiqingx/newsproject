import numpy as np
from plot_pred import build_plot
from pylatex import Document, MiniPage, PageStyle, Section, Subsection, Tabular, \
                    MultiColumn, Head, Foot, Figure, LargeText, figure,\
                    MediumText, LineBreak, simple_page_number
from pylatex.utils import italic, bold, NoEscape
import os
import time


HEADER_IMAGE = '../commodity-pic.jpg'
PATH = './reports'


# subprocess error with gen_pdf
# filepath with the picture
# challenge, their package not stable
# newly added simple page number is not returning correct value

class Report:
    """docstring for ClassName"""

    def __init__(self, df, dicto, margin='1.0in', default_filepath=PATH):

        #parentdir= os.path.dirname(default_filepath)

        #if not os.path.exists(parentdir):
            #os.makedirs(parentdir)

        geometry_options = {'margin': margin, 'paperheight': '11in', \
                            'paperwidth':'8.5in'}

        self.doc = Document(default_filepath= default_filepath, \
                            geometry_options=geometry_options, font_size='large')
        self._df = df
        self._dicto = dicto


    def add_headfoot(self, header_image):
        '''
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
            #header.append(LineBreak())
            #header.append(company)

        #center footer
        with header.create(Foot('C')):
            header.append(company)

        #right footer
        with header.create(Foot('R')):
            header.append(simple_page_number())





        self.doc.preamble.append(header)

        self.doc.change_document_style('header')

    def set_title(self, title, subtitle):
        '''
        '''
        with self.doc.create(MiniPage(align='c')):
            self.doc.append(LargeText(bold(title)))
            #self.doc.append(LineBreak())
            self.doc.append(MediumText(italic(bold(subtitle))))

    def add_executive_summary(self, text):
        '''
        '''
        with self.doc.create(Section('Executive Summary')) as summary:
            with summary.create(Tabular('p{15.4cm}')) as sumtable:
                sumtable.add_hline()
                sumtable.add_row([italic(text)])
                sumtable.add_empty_row()
                sumtable.add_empty_row()


    def insert_graph(self):#, graph_fname):
        '''
        '''

        with self.doc.create(Figure(position='ht!')) as plot:
            build_plot(self._df)
            plot.add_plot(width="6.5in")




    def insert_table(self, results):
        '''
        '''
        indie_var = ', '.join(results['independent_var'])

        section = Section('Statistical Results')

        table = Tabular('l p{10cm}')
        table.add_hline()
        table.add_row((MultiColumn(2, align='c', data=bold('Characteristics of Model')),))
        table.add_hline(cmidruleoption='r')
        table.add_row((bold('Model'), 'AR'), color='lightgray')
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
        '''
        self.doc.generate_pdf(filepath, clean=True, clean_tex=False,#True,  \
                              compiler='pdflatex',silent=False)#, compiler_args = ["-synctex=1"])#True)


def create_output_dir():
    '''
    Creates directory if precipitation_maps directory does not already exist.

    Inputs:
        None.

    Outputs:
        The output directory at current_path/OUTPUT_DIR.

    Returns:
        None.
    '''

    cur_path = os.path.split(os.path.abspath(__file__))[0]
    output_path = os.path.join(cur_path, PATH)
    if not os.access(output_path, os.F_OK):
        os.makedirs(output_path)



def build_report(df, dicto):
    '''
    '''
    name = df.columns[1].split(',')[0]

    r = Report(df,dicto)

    r.set_title('Forecast:  ', name)
    r.add_headfoot(HEADER_IMAGE)
    r.add_executive_summary('Summary')
    r.insert_graph()
    r.insert_table(dicto)
    output_path = os.path.join(PATH, name)
    r.gen_pdf(output_path)

    #return r



create_output_dir()

#if __name__ == '__main__':

    #for i, df in enumerate(dfs_list):
    #    build_report(df, dicto[i])
