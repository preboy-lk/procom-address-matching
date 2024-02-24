# src/main.py
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import os
from utils.DataPreprocessor import DataPreprocessor
from Blocking import Blocking
from Filtering import Filtering
from Matching import Matching

def main():
    #obj1 = AddressParsing()
    #obj2 = DataPreprocessor()
    dataset_path = ['dataset/ipe_reduced.csv', 'dataset/ban_reduced.csv']
    if not (os.path.exists(dataset_path[0]) and os.path.exists(dataset_path[1])):
        DataPreprocessor()

    A = pd.read_csv('dataset/ipe_reduced.csv')
    B = pd.read_csv('dataset/ban_reduced.csv')

    step_1 = Blocking(A,B)
    C = step_1.block()

    step_2 = Filtering(C, 3000) #Default 2000
    D = step_2.filter()

    step_3 = Matching(D)
    E = step_3.match()
    print('From IPE Dataset with : ' , A.shape[0] , '    rows and BAN Dataset with : ', B.shape[0], '   rows we found ', len(E) , ' matching adresses')
    E.to_csv('results/matched_address_BAN_IPE_UsingRulesBase.csv')
    print('Done')

    
if __name__ == "__main__":
    main()