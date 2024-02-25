# src/Model.py
import pandas as pd
import numpy as np
import py_entitymatching as em
from unidecode import unidecode
import pickle

from Blocking import Blocking

class Model:
    def __init__(self):
        self.labeled = pd.read_csv('../dataset/dataset_annote_V3.csv')
        self.block = Blocking()
        self.run()

    def get_table_feature(self):
        return self.match_f
    def run(self):
        self.training_set_preprocessing()
        self.split_dataset_BAN_IPE()
        self.create_record_table()
        G = self.sampling()
        self.match_f = self.get_feature_for_matching()
        H = self.extracting_feature_vectors(G)
        self.training(H)
        print('Model saved successfully')

    def training_set_preprocessing(self):
        self.labeled = self.labeled[~self.labeled['id'].duplicated()]
        self.labeled = self.labeled[~self.labeled['IdentifiantImmeuble'].duplicated()]
        self.labeled = self.labeled.fillna('')

        self.labeled = self.labeled.astype(
            {
                "id": "string",
                "numero": "float32",
                "rep": "string",
                "TypeVoie": "string",
                "NomVoieReste": "string",
                "code_postal": "int32",
                "nom_commune": "string",
                "x": "float32",
                "y": "float32",
                "IdentifiantImmeuble": "string",
                "NumeroVoieImmeuble": "float32",
                "ComplementNumeroVoieImmeuble": "string",
                "TypeVoieImmeuble": "string",
                "NomVoieImmeuble": "string",
                "CodePostalImmeuble": "int32",
                "CommuneImmeuble": "string",
                "CoordonneeImmeubleX": "float32",
                "CoordonneeImmeubleY": "float32",
                "Label": "int32",
            }
        )
    def split_dataset_BAN_IPE(self):
        self.A = self.labeled.iloc[:, :len(self.labeled.columns)//2]
        self.B = self.labeled.iloc[:, len(self.labeled.columns)//2:-1]

        self.B['TypeVoieImmeuble'] = self.B['TypeVoieImmeuble'].apply(lambda x : unidecode(x).lower() if pd.isna(x) is False else '')

        self.A['rep'] = self.A['rep'].apply(self.block.complement_numero_voie)
        self.B['ComplementNumeroVoieImmeuble'] = self.B['ComplementNumeroVoieImmeuble'].apply(self.block.complement_numero_voie)

    def create_record_table(self):
        ban = self.A.copy()
        ipe = self.B.copy()
        self.labeled = pd.concat([ban,ipe,self.labeled.iloc[:,-1]],axis=1)
        nom_colonnes = {
            "id": "l_id",
            "numero": "l_NumeroVoieImmeuble",
            "rep": "l_ComplementNumeroVoieImmeuble",
            "TypeVoie": "l_TypeVoieImmeuble",
            "NomVoieReste": "l_NomVoieImmeuble",
            "code_postal": "l_CodePostalImmeuble",
            "nom_commune": "l_CommuneImmeuble",
            "x": "l_CoordonneeImmeubleX",
            "y": "l_CoordonneeImmeubleY",
            "IdentifiantImmeuble": "r_id",
            "NumeroVoieImmeuble": "r_NumeroVoieImmeuble",
            "ComplementNumeroVoieImmeuble": "r_ComplementNumeroVoieImmeuble",
            "TypeVoieImmeuble": "r_TypeVoieImmeuble",
            "NomVoieImmeuble": "r_NomVoieImmeuble",
            "CodePostalImmeuble": "r_CodePostalImmeuble",
            "CommuneImmeuble": "r_CommuneImmeuble",
            "CoordonneeImmeubleX": "r_CoordonneeImmeubleX",
            "CoordonneImmeubleY": "r_CoordonneeImmeubleY",
            "Label": "label",
        }
        self.labeled = self.labeled.rename(columns=nom_colonnes)
        self.labeled['l_TypeVoieImmeuble'] = self.labeled['l_TypeVoieImmeuble'].apply(lambda x : unidecode(x).lower() if pd.isna(x) is False else '')
        nom_colonnes = {
            "id": "IdentifiantImmeuble",
            "numero": "NumeroVoieImmeuble",
            "rep": "ComplementNumeroVoieImmeuble",
            "TypeVoie": "TypeVoieImmeuble",
            "NomVoieReste": "NomVoieImmeuble",
            "code_postal": "CodePostalImmeuble",
            "nom_commune": "CommuneImmeuble",
            "x": "CoordonneeImmeubleX",
            "y": "CoordonneeImmeubleY",
        }
        self.A = self.A.rename(columns=nom_colonnes)

        self.labeled['_id'] = range(len(self.labeled))

        # We need to set key for each table to create metadata so that we can continue the next step
        em.set_key(self.labeled,'_id')
        em.set_fk_ltable(self.labeled, 'l_id')
        em.set_fk_rtable(self.labeled, 'r_id')
        em.set_key(self.A, 'IdentifiantImmeuble')
        em.set_key(self.B, 'IdentifiantImmeuble')
        em.set_ltable(self.labeled, self.A)
        em.set_rtable(self.labeled, self.B)
        return self.A, self.B
    
    def sampling(self):
        return em.sample_table(self.labeled, self.labeled.shape[0])
    
    def get_feature_for_matching(self):
        match_f = em.get_features_for_matching(self.A,self.B, validate_inferred_attr_types = False)
        em.add_blackbox_feature(match_f,'real_distance',self.real_distance)
        feature_to_remain = [6,13,23,26,38,54]
        match_f.drop([i for i in range(match_f.shape[0]) if i not in feature_to_remain],inplace=True)
        #match_f.to_csv('../model/cfg.csv', index = False)
        return match_f
    
    def extracting_feature_vectors(self, G):
        H = em.extract_feature_vecs(G, feature_table=self.match_f , attrs_after=['label'])
        return H
    
    def training(self, dataset):
        self.dt = em.RFMatcher(n_estimators=300, max_depth = 15)
        train_test = em.split_train_test(dataset, train_proportion=0.7)
        devel_set = train_test['train']
        eval_set = train_test['test']
        self.dt.fit(table=devel_set, exclude_attrs=['_id', 'l_id', 'r_id'], target_attr='label')
        pred_table = self.dt.predict(table=eval_set, exclude_attrs=['_id', 'l_id', 'r_id','label'], target_attr='predicted_labels', append=True, inplace=True)
        eval_summary = em.eval_matches(pred_table, 'label', 'predicted_labels')

        print(eval_summary)
        with open('../model/matching_model.pkl', 'wb') as f:
            pickle.dump(self.dt, f)

    def real_distance(self,ltuple,rtuple):
        return np.sqrt((ltuple['CoordonneeImmeubleX']-rtuple['CoordonneeImmeubleX'])**2+(ltuple['CoordonneeImmeubleY']-rtuple['CoordonneeImmeubleY'])**2)

    def predict(self, C):
        H = em.extract_feature_vecs(C, feature_table=self.match_f)
        print(H.columns)
        pred_table = self.dt.predict(table=H, exclude_attrs=['_id', 'l_IdentifiantImmeuble', 'r_IdentifiantImmeuble'], target_attr='predicted_labels', append=True, inplace=True)
        return pred_table