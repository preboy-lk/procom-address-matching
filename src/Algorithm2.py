# src/Algorithm2.py
import pandas as pd
import os
from utils.DataPreprocessor import DataPreprocessor
from Blocking import Blocking
from Model import Model

class Algorithm2:
    def run(self):
        dataset_path = ['../dataset/ipe_reduced.csv', '../dataset/ban_reduced.csv']
        if not (os.path.exists(dataset_path[0]) and os.path.exists(dataset_path[1])):
            DataPreprocessor()

        A = pd.read_csv('../dataset/ipe_reduced.csv')
        B = pd.read_csv('../dataset/ban_reduced.csv')

        block = Blocking(A,B)
        C = block.block()

        step_2 = Model()
        D = step_2.predict(C)

        match_table = D[D['predicted_labels'] == 1]
        # Sort the DataFrame by column 'B' in ascending order
        df_sorted = match_table.sort_values(by='real_distance')

        # Keep only the first occurrence of each value in column 'A' (which has the minimum value in column 'B')
        match_table1 = df_sorted.drop_duplicates(subset='l_IdentifiantImmeuble', keep='first')
        E = match_table1.drop_duplicates(subset='r_IdentifiantImmeuble', keep='first')

        print('From IPE Dataset with : ' , A.shape[0] , '    rows and BAN Dataset with : ', B.shape[0], '   rows we found ', len(E) , ' matching adresses')
        E.to_csv('../results/matched_address_BAN_IPE_UsingML.csv')
        print('Done')

