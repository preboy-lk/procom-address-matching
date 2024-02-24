# src/Matching.py
import py_stringmatching as sm

class Matching:
    def __init__(self, D):
        """
        Calculate similarity cores based on the Levensthein distance. 
        We calculate on columns which may have more complex sources of errors, such as typos, abbreviations, etc... --> matching technique
            - CommuneImmeuble
            - NomVoieImmeuble

        If the similarity score is greater than 70% for the municipality and 80% for the street name, the addresses are considered similar.
        """
        self.D = D
        self.D['SimilarityScoreRue'] = self.D.apply(lambda x : self.levenshtein_similarity_score(x['l_NomVoieImmeuble'],x['r_NomVoieImmeuble']), axis=1)
        self.D['SimilarityScoreCommune'] = self.D.apply(lambda x : self.levenshtein_similarity_score(x['l_CommuneImmeuble'],x['r_CommuneImmeuble']), axis=1)
        
    def jaccard_similarity_score(self, string1, string2):
        """
        Computes the Jaccard similarity score between two strings.

        Args:
            - string1: The first string for comparison.
            - string2: The second string for comparison.

        Return: 
            - The Jaccard similarity score between the two strings.
        """ 
        alphabet_tok = sm.AlphabeticTokenizer()
        token1 = alphabet_tok.tokenize(string1)
        token2 = alphabet_tok.tokenize(string2)
        jaccard = sm.Jaccard()  # Example Jaccard similarity
        return jaccard.get_sim_score(token1, token2)

    def levenshtein_similarity_score(self, string1, string2):
        """
        Computes the Levenshtein similarity score between two strings.

        Args:
            - string1: The first string for comparison.
            - string2: The second string for comparison.

        Return: 
            - The Levenshtein similarity score between the two strings
        """ 
        distance = sm.Levenshtein()
        return distance.get_sim_score(string1.lower().replace('-',' '), string2.lower().replace('-',' '))
    
    def match(self):
        """
        Matches records based on similarity scores.
        This method filters records based on similarity scores for commune and road name.
        It first filters records with a similarity score for commune greater than or equal to 0.70.
        Then, it further filters these records based on a similarity score for street name greater than or equal to 0.80.

        Return:
            - DataFrame containing matched records.
        """
        #first, we filter the commune similiarity
        E = self.D[self.D['SimilarityScoreCommune'] >= 0.70]
        #then, we filter the street name similiarity
        E = E[E['SimilarityScoreRue'] >= 0.80]

        return E