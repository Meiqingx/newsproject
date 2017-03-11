import numpy as np

from pylatex import Document, MiniPage, PageStyle, Section, Subsection, Tabular, \
                    Math, TikZ, Axis, Plot, Figure, Matrix, LargeText, \
                    MediumText, LineBreak
from pylatex.utils import italic, bold, NoEscape
import os



# order matters, 1. add title first
# add main
# insert a default pic

class Report(object):
    """docstring for ClassName"""
    
    def __init__(self, header_image, margin='1.0in', default_filepath='./reports/report'):
        

        geometry_options = {"margin": margin}
        self.doc = Document(default_filepath= default_filepath, \
                            geometry_options=geometry_options)
        
        graph_filename = os.path.join(os.path.dirname(__file__), 'commodities.jpg')

        with self.doc.create(Figure(position='t!')) as graph:
            graph.add_image(header_image, width='200px')

        

    def set_title(self, title, subtitle):
        '''
        '''
        with self.doc.create(MiniPage(align='c')):
            self.doc.append(LargeText(bold(title)))
            self.doc.append(LineBreak())
            self.doc.append(MediumText(italic(bold(subtitle))))

    def insert_graph(self, sec_name, graph_fname, caption):
        '''
        '''
        with self.doc.create(Section(sec_name)):
            #doc.append('add section text')
            with self.doc.create(Figure(position='h!')) as graph:
                graph.add_image(graph_fname, width='180px')
                graph.add_caption(caption)

    def insert_table(self, lag, independent_var, num_diff, R2, stat):
        '''
        '''
        #Rodrigo can give me this info as a dictionary

        lag_var = ('Lag variables', lag)
        indie_var = ('Independent variables', ' '.join(independent_var))

        section = Section('The model')

        table = Tabular('c p{5cm}')
        table.add_hline()
        table.add_row(('Model', 'AR'))
        table.add_row(lag_var, color='lightgray')
        table.add_row(indie_var)
        table.add_row(('Number of differences', num_diff), color='lightgray')
        table.add_row((NoEscape('$R^2$'), R2))
        table.add_row(('Durbin Watson Statistic', stat), color='lightgray')
        table.add_hline()
        
        section.append(LineBreak())
        section.append(table)

        self.doc.append(section)

    def generate_pdf(self, filepath=None):
        '''
        '''
        self.doc.generate_pdf(filepath, clean_tex=False)


if __name__ == '__main__':

    header_image = os.path.join(os.path.dirname(__file__), 'commodities.jpg')

    r = Report(header_image)
    r.set_title('Forecast', 'Wheat')
    r.insert_table(1, ['apple', 'banana', 'pear', 'peach'], 4, 0.99, 5.66)
    r.generate_pdf()
