# src/Predict.py
import pickle
import pandas as pd
import py_entitymatching as em
from Model import Model
from Blocking import Blocking
from Model import Model

class Predict:
    def __init__(self):
        with open('../model/cfg.pkl', 'rb') as f:
            self.feature_table = pickle.load(f)
        self.feature_method = Model()
        em.add_blackbox_feature(self.feature_table,'real_distance',self.feature_method.real_distance)

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