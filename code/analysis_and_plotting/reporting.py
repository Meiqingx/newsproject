import numpy as np

from pylatex import Document, MiniPage, PageStyle, Section, Subsection, Tabular, \
                    Head, Foot, Axis, Plot, Figure, Matrix, LargeText, \
                    MediumText, LineBreak, simple_page_number
from pylatex.utils import italic, bold, NoEscape

import os
import time


class Report:
    """docstring for ClassName"""
    
    def __init__(self, margin='1.0in', default_filepath='./reports/report'):
        

        geometry_options = {'margin': margin, 'paperheight': '11in', \
                            'paperwidth':'8.5in'}
        
        self.doc = Document(default_filepath= default_filepath, \
                            geometry_options=geometry_options, font_size='large')
        

    def add_headfoot(self, header_image):
        '''
        '''
        header = PageStyle('header')
        
        today = time.strftime('%B %d %Y')
        company = 'Ochoa Valdés-Ortiz Zhang Ltd.'

        #add header
        with header.create(Head('L')) as lheader:
            with lheader.create(Figure(position='t!')) as graph:
                graph.add_image(header_image, width='400px')

        
        #left footer
        with header.create(Foot('L')):
            header.append(today)
            header.append(LineBreak())
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
            self.doc.append(LineBreak())
            self.doc.append(MediumText(italic(bold(subtitle))))

    def add_executive_summary(self):
        '''
        '''
        pass

    def insert_graph(self, sec_name, graph_fname, caption):
        '''
        '''
        with self.doc.create(Section(sec_name)):
            #doc.append('add section text')
            with self.doc.create(Figure(position='t!')) as graph:
                graph.add_image(graph_fname, width='200px')
                graph.add_caption(caption)

    def insert_table(self, results):
        '''
        '''
        indie_var = ' '.join(results['independent_var'])

        section = Section('The Model')

        table = Tabular('l p{10cm}')
        table.add_hline()
        table.add_row((bold('Model'), 'AR'))
        table.add_row((bold('Lag variables'), results['lag']), color='lightgray')
        table.add_row((bold('Independent variables'), indie_var))
        table.add_row((bold('Number of differences'), results['num_diff']), color='lightgray')
        table.add_row((NoEscape('\symbf{$R^2$}'), results['R2']))
        table.add_row((bold('Durbin Watson Statistic'), results['stat']), color='lightgray')
        table.add_hline()
        
        section.append(LineBreak())
        section.append(table)

        self.doc.append(section)

    def generate_pdf(self, filepath=None):
        '''
        '''
        self.doc.generate_pdf(filepath, clean_tex=False)


if __name__ == '__main__':

    # order matters, 1. add title first

    header_image = os.path.join(os.path.dirname(__file__), 'commodities_2.jpg')

    results = {'lag':1, 'R2': 0.99, 'stat': 5.66, 'num_diff': 4,\
               'independent_var': ['apple', 'banana', 'pear', 'peach']}
    
    r = Report()

    r.set_title('Forecast', 'Wheat')
    r.add_headfoot(header_image)
    r.insert_table(results)
    r.generate_pdf()
