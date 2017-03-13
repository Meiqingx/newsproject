import reporting
import os
import pickle
from subprocess import check_output, CalledProcessError


PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pickles/')
ERROR = "Exception:  There has been a CalledProcessError, but the report has still\nbeen generated."
PICKLES = 10


if __name__ == '__main__':

    #Call the reporting module to build the reports
    header_image = '../commodity-pic.jpg'

    for i in range(PICKLES):
        name = PATH + 'df_tuple' + str(i) + '.pkl'
        df, dicto = pickle.load(open(name, "rb" ))
        try:
            reporting.build_report(df, dicto, header_image)
        except CalledProcessError:
            print(ERROR)
            continue


    for fname in os.listdir(reporting.PATH):
        if fname.endswith('.tex') or fname.endswith('.aux') or fname.endswith('log'):
            os.remove(fname)
