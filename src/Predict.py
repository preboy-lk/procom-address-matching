# src/Predict.py
import pickle
import pandas as pd
import py_entitymatching as em
from Model import Model
from Blocking import Blocking

class Predict:
    def __init__(self):
        self.feature_table = pd.read_csv('../model/cfg.csv')

        model_file = '../model/matching_model.pkl'
        try:
            # Try to load the saved matcher
            with open(model_file, 'rb') as f:
                self.model = pickle.load(f)
                
            print("Model loaded successfully.")
        except FileNotFoundError:
            # Handle the case where the model file does not exist
            print(f"Error: Matching Model at '{model_file}' not found. Exiting.")
            exit(1)
        

    def predict(self,C):
        H = em.extract_feature_vecs(C, feature_table=self.feature_table)
        #H = em.impute_table(H, exclude_attrs=['_id', 'ltable_IdentifiantImmeuble', 'rtable_IdentifiantImmeuble'], strategy='mean')
        pred_table = self.dt.predict(table=H, exclude_attrs=['_id', 'ltable_IdentifiantImmeuble', 'rtable_IdentifiantImmeuble'], target_attr='predicted_labels', append=True, inplace=True)
        return pred_table