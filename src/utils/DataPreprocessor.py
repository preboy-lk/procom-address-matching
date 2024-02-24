# src/utils/DataPreprocessor.py
import pandas as pd
from unidecode import unidecode
from tqdm import tqdm


from utils.AddressParsing import AddressParsing

class DataPreprocessor:
    def __init__(self):
        # We take ban-adresses-12 as it is the department 12, which is contained in ipe AXTD region
        self.ipe = pd.read_csv('dataset/IPE-AXTD.csv', delimiter=";")
        self.ban = pd.read_csv('dataset/BAN-address-12.csv', delimiter=";")
        self.address_parser = AddressParsing()
        self.run()
    
    def run(self):
        """
        Run the road name parser for addresses on the entire BAN dataset.
        Then delete unnecessary columns in both BAN and IPE datasets to make sure 
        both datasets have the same number of columns and column names. 
        Save these 2 datasets under name: ipe_reduced.csv and ban_reduced.csv
        """
        
        typevoie_values = []
        nomvoie_values = []
        try:
            for index in tqdm(self.ban['nom_voie'], total=len(self.ban)):
                parsed_address = self.address_parser.parsing_address(index)
                typevoie_values.append(parsed_address[0])
                nomvoie_values.append(parsed_address[1])
            self.ban['TypeVoie'] = typevoie_values
            self.ban['NomVoieReste'] = nomvoie_values
            self.ban.rename(columns={'typeVoie': 'TypeVoie'}, inplace=True)
            self.ban.rename(columns={'nomVoie': 'NomVoieReste'}, inplace=True)

            ban_reduced = self.ban[['id','numero','rep','TypeVoie','NomVoieReste','code_postal','nom_commune','x','y']]
            ipe_reduced = self.ipe[['IdentifiantImmeuble','NumeroVoieImmeuble','ComplementNumeroVoieImmeuble','TypeVoieImmeuble','NomVoieImmeuble','CodePostalImmeuble','CommuneImmeuble','CoordonneeImmeubleX','CoordonneeImmeubleY']]
            ipe_reduced['TypeVoieImmeuble'] = ipe_reduced['TypeVoieImmeuble'].apply(lambda x : unidecode(x).lower() if pd.isna(x) is False else '')

            nom_colonnes = {'id': 'IdentifiantImmeuble','numero' : 'NumeroVoieImmeuble','rep' : 'ComplementNumeroVoieImmeuble','TypeVoie' : 'TypeVoieImmeuble','NomVoieReste' : 'NomVoieImmeuble','code_postal' : 'CodePostalImmeuble','nom_commune' : 'CommuneImmeuble','x' : 'CoordonneeImmeubleX','y' : 'CoordonneeImmeubleY'}
            ban_reduced = ban_reduced.rename(columns=nom_colonnes)
            ipe_reduced.to_csv('dataset/ipe_reduced.csv')
            ban_reduced.to_csv('dataset/ban_reduced.csv')
            print("Dataset saved successfully")
        except Exception as e:
            print(f"Fail to save dataset: {e}")