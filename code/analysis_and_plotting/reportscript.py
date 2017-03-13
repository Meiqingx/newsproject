import reporting
import merger as mrgr
import pickle
from subprocess import check_output, CalledProcessError
import os

predictor_dfs, outcomes = mrgr.read_files()

predictors = mrgr.merge_dfs(predictor_dfs)

mrgr.gen_sqrs_cbcs(predictors)


df_list = [predictors, outcomes]

dicto1 = {'lag':1, 'R2': 0.9910, 'stat': 5.6678, 'num_diff': 4,\
          'independent_var': ['apple', 'banana'], 
          'dependent_var': 'orange'}

dicto2 = {'lag':2, 'R2': 0.67, 'stat': 6.2, 'num_diff': 3,\
          'independent_var':['wheatgerm and snakeoil', 'grass and cash'], 
          'dependent_var': 'gold'}

dictos = [dicto1,dicto2]

header_image = '../commodity-pic.jpg'

for i, df in enumerate(df_list):
    try:
        reporting.build_report(df, dictos[i], header_image)
    except CalledProcessError:
        print("A CalledProcessError not fixed by developer of pylatex")
        continue

    # name = 'df_tuple' + str(i) + '.p'
    # p_tuple = tuple((df, dictos[i]))
    # pickle.dump(p_tuple, open(name, 'wb'))

for fname in os.listdir(reporting.PATH):
    if fname.endswith('.tex') or fname.endswith('.aux') or fname.endswith('log'):
        os.remove(fname)