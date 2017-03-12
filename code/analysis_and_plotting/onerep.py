import pickle
import reportingEMO
import sys





if __name__=="__main__":
    pckl = str(sys.argv[1])
    print(pckl)

    df, dicto = pickle.load( open( pckl, "rb" ) )

    reportingEMO.build_report(df, dicto)
