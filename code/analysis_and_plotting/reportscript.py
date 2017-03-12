import reportingEMO
import merger as mrgr
import pickle

predictor_dfs, outcomes = mrgr.read_files()

predictors = mrgr.merge_dfs(predictor_dfs)

mrgr.gen_sqrs_cbcs(predictors)


df_list = [predictors, outcomes]

dicto1 = {'lag':1, 'R2': 0.9910, 'stat': 5.6678, 'num_diff': 4,\
          'independent_var': ['apple', 'banana', 'pear', 'peach']}

dicto2 = {'lag':2, 'R2': 0.67, 'stat': 6.2, 'num_diff': 3,\
          'independent_var':['wheatgerm and snakeoil','oil','global mean precipitation','grass and cash']}

dictos = [dicto1,dicto2]

for i, df in enumerate(df_list):
    "r = reportingEMO.build_report(df, dictos[i])"
    name = 'df_tuple' + str(i) + '.p'
    p_tuple = tuple((df, dictos[i]))
    pickle.dump(p_tuple, open(name, 'wb'))
