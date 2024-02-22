# src/AddressParsing.py
from fuzzywuzzy import fuzz
from unidecode import unidecode

class AddressParsing:
    def __init__(self):
        # Alt + Z to fit code on the viewport
        self.abbreviations_list = ['ABE', 'ACH', 'AER', 'AIRE', 'ALL', 'ANSE', 'AR', 'ARC', 'ART', 'AUT', 'AV', 'BAL', 'BAS', 'BASE', 'BAT', 'BCH', 'BCLE', 'BD', 'BER', 'BOIS', 'BRC', 'BRE', 'BRG', 'BRTL', 'BSTD', 'BUT', 'CALE', 'CAMP', 'CAN', 'CAR', 'CARE', 'CARR', 'CASR', 'CAU', 'CC', 'CCAL', 'CD', 'CEIN', 'CGNE', 'CHE', 'CHEM', 'CHEZ', 'CHI', 'CHL', 'CHP', 'CHS', 'CHT', 'CITE', 'CLOS', 'COL', 'COLI', 'COR', 'CORO', 'COT', 'COTE', 'COTT', 'COUR', 'CPG', 'CR', 'CRS', 'CST', 'CTR', 'CTRE', 'CVE', 'CHV', 'D', 'DIG', 'DOM', 'DSC', 'ECA', 'ECL', 'EGL', 'EN', 'ENC', 'ENV', 'ESC', 'ESP', 'ESPA', 'FG', 'FON', 'FORM', 'FORT', 'FOS', 'FRM', 'GAL', 'GARE', 'GBD', 'GPE', 'GPL', 'GPT', 'GR', 'GRI', 'HAM', 'HCH', 'HIP', 'HLE', 'HLG', 'HLM', 'ILE', 'ILOT', 'IMM', 'IMP', 'JARD', 'JTE', 'LD', 'LEVE', 'LOT', 'MAIL', 'MAIS', 'MAR', 'MAS', 'MLN', 'MTE', 'MUS', 'NTE', 'PAE', 'PAL', 'PARC', 'PAS', 'PASS', 'PAT', 'PAV', 'PCH', 'PERI', 'PIM', 'PISTE', 'PKG', 'PL', 'PLAN', 'PLCI', 'PLE', 'PLN', 'PLT', 'PN', 'PNT', 'PONT', 'PORT', 'POT', 'PR', 'PRE', 'PROM', 'PRQ', 'PRT', 'PRV', 'PTA', 'PTE', 'PTTE', 'QU', 'QUA', 'R', 'RAC', 'RAID', 'RDE', 'REM', 'RES', 'RLE', 'RN', 'RNG', 'ROC', 'RPE', 'RPT', 'RTD', 'RTE', 'RUELLETTE', 'RUETTE', 'SEN', 'SENTE', 'SQ', 'STA', 'STDE', 'TOUR', 'TPL', 'TRA', 'TRN', 'TRT', 'TSSE', 'VAL', 'VC', 'VCHE', 'VEN', 'VIA', 'VLA', 'VLGE', 'VOI', 'VR', 'VTE', 'ZA', 'ZAC', 'ZAD', 'ZI', 'ZONE', 'ZUP']

        self.fullname_list = ['Abbaye', 'Ancien chemin', 'Aéroport', 'Aire', 'Allée', 'Anse', 'Ancienne Rue', 'Arcade', 'Ancienne route', 'Autoroute', 'Avenue', 'Balcon', 'Bastion', 'Base', 'Bâtiment', 'Bas Chemin', 'Boucle', 'Boulevard', 'Berge','Bois', 'Brèche', 'Barrière', 'Bourg', 'Bretelle', 'Bastide', 'Butte', 'Cale', 'Camp', 'Canal', 'Carrefour', 'Carrière', 'Carrè', 'Caserne', 'Carreau', 'Chemin communal', 'Centre Commercial', 'Chemin départemental', 'Ceinture', 'Campagne', 'Chemin', 'Cheminement', 'Chez', 'Charmille', 'Chalet', 'Chapelle','Chaussée', 'Château', 'Cité', 'Clos', 'Col', 'Colline', 'Corniche', 'Coron', 'Côte','Coteau', 'Cottage', 'Cour', 'Camping', 'Chemin rural', 'Cours', 'Castel','Contour', 'Centre', 'Coursive', 'Chemin Vicinal', 'Départementale', 'Digue','Domaine', 'Descente', 'Écart', 'Écluse', 'Église', 'Enceinte', 'Enclos','Enclave', 'Escalier', 'Esplanade', 'Espace', 'Faubourg', 'Fontaine', 'Forum','Fort', 'Fosse', 'Ferme', 'Galerie', 'Gare', 'Grand boulevard', 'Groupe','Grande Place', 'Groupement', 'Grande rue', 'Grille', 'Hameau', 'Haut Chemin','Hippodrome', 'Halle', 'Halage', 'HLM', 'Île', 'Îlot', 'Immeuble', 'Impasse','Jardin', 'Jetée', 'Lieu dit', 'Levée', 'Lotissement', 'Mail', 'Maison', 'Marché','Mas', 'Moulin', 'Montée', 'Musée', 'Nouvelle Route', 'Petite Avenue', 'Palais','Parc', 'Passage', 'Passe', 'Patio', 'Pavillon', 'Petit Chemin', 'Périphérique','Petite Impasse', 'Piste', 'Parking', 'Place', 'Plan', 'Placis', 'Passerelle','Plaine', 'Plateau', 'Passage à Niveau', 'Pointe', 'Pont', 'Port', 'Poterne','Petite Rue', 'Pré', 'Promenade', "Presqu'île", 'Petite Route', 'Parvis', 'Petite Allée', 'Porte', 'Placette', 'Quai', 'Quartier', 'Rue', 'Raccourci', 'Raidillon', 'Ronde', 'Rempart', 'Résidence', 'Ruelle', 'Route Nationale','Rangée', 'Rocade', 'Rampe', 'Rond Point', 'Rotonde', 'Route', 'Ruellette','Ruette', 'Sentier', 'Sente', 'Square', 'Station', 'Stade', 'Tour', 'Terre Plein','Traverse', 'Terrain', 'Tertre', 'Terrasse', 'Vallée', 'Voie Communale','Vieux Chemin', 'Venelle', 'Via', 'Villa', 'Village', 'Voie', 'Vieille Rue','Vieille Route', 'Zone Artisanale', 'Zone Aménagement Concerté','Zone Aménagement Différé', 'Zone Industrielle', 'Zone', 'Zone à Urbaniser en Priorité']

        self.abbreviation_to_type_mapping = dict(zip(self.abbreviations_list, self.fullname_list))

        self.find_string_contains_2_words = self.find_string_contains_multi_words(self.fullname_list, 2)
        self.find_string_contains_3_words = self.find_string_contains_multi_words(self.fullname_list, 3)

    def find_string_contains_multi_words(self, string_list, nb_words):
        """
        Filter the full name of road type that have more than 1 word

        Args:
        - string_list (list): List full name of road type.
        - nb_words (int): The number of words of the full road type name for filtering.

        Returns:
        - List of strings containing the specified number of words of the original strings.
        """
        result_list = []
        for string in string_list:
            words = string.split()
            if len(words) == nb_words:
                result_list.append(string)
        return result_list

    def compare_2_strings(self, string_list, words, threshold=75):
        """
        Calculate the similarity score using Fuzzy Logic of the selected words with each string of the list
        We just take into account the score that is higher than threshold
        The highest score corresponds to the word considered to be the best match in the list
        If no scores exceed the threshold, return None

        Args:
        - string_list (list): List of strings to compare, fullname_list or abbreviations_list.
        - words (str): String to compare against each elements in list.
        - threshold (int, optional): Minimum similarity threshold. Defaults to 75.

        Returns:
        - The string in string_list that has highest score of similarity with the words.
        - The highest score of similarity.
        """
        best_match = None
        best_score = 0
        for item in string_list:
                similarity_score = fuzz.ratio(words, item)
                if similarity_score >= threshold and similarity_score > best_score:
                    best_match = item
                    best_score = similarity_score
        return best_match, best_score

    def parsing_address(self, input_string, words_to_compare=3):
        """
        Parse an address string by comparing it to a list of predefined words.
        The goal is to separate road names from road types

        Args:
        - input_string (str): Input address string.
        - words_to_compare (int, optional): Number of words to compare in the input string. Defaults to 3.

        Returns:
        - List with road name and road type separated.
        """
        # This is the recursive function
        words = input_string.split() #Split the address into list of string

        if len(words) > 1:
            nb_words = min(words_to_compare, len(words) - 1)  #Take into account the number of words to compare
        else:
            return '',input_string
        compared_words =' '.join(words[:nb_words])

        if words[0] == "le" or words[0] == "la": # Address start with le/la easily confuse with ile, villa
            return '', input_string                # So we assign these addresses to Nom de voie

        if nb_words == 1:
        #Create the stop condition for recursive function (the base case)
        # In case we need to compare first 1 word of the address, we will compare it with string in abbreviation list and fullname_list
        # After having compared that word with 2 lists, we will see that the word is more similar to which string in which list (to Return it correctly)
            match_abbre, match_score_abbre = self.compare_2_strings(self.abbreviations_list, compared_words.upper()) # Uppercase the word when compare with abbreviation list because the string in this list is uppercased
            match_full , match_score_full = self.compare_2_strings(self.fullname_list, unidecode(compared_words.lower())) # Lowercase the word and then remove the accents
            if match_abbre != None or match_full != None:
                if match_score_abbre > match_score_full:
                    return self.abbreviation_to_type_mapping[match_abbre], ' '.join(words[1:])
                else:
                    return match_full,  ' '.join(words[1:])
            else:
                return '', input_string # If no string in both lists matches that word then Invalid Address or there 's no type of the road in this address

        else:
            # If type of the roads contain 2 or 3 words then
            # we need to compare the first 2,3 words of the input string with the string in fullname_list
            # If Match, stop the function immediately
            # If not, decrease the nb of words for comparison from 3 to 2 or 2 to 1.
            reference_list = self.find_string_contains_2_words if nb_words == 2 else self.find_string_contains_3_words
            match_word, match_score = self.compare_2_strings(reference_list, unidecode(compared_words.lower()))
            if match_word == None :
                return self.parsing_address(input_string, nb_words - 1)
            else:
                return match_word,  input_string.replace(compared_words,"")
