# src/Blocking.py
import py_entitymatching as em

class Blocking:
    def __init__(self, A,B):
        """
        We compare certain columns strictly --> blocking technique
        Íf there is no strict correspondence on each of these columns between the 2 addresses compared, we consider that they are not the same addresses.
        The blocked columns are as follows:
            - NumeroVoieImmeuble
            - ComplementNumeroVoieImmeuble
            - TypeVoieImmeuble
            - CodePostalImmeuble

        Args:
            - A,B (Dataframe): 2 Dataframes that need to make the comparison
        """
        self.A = A
        self.B = B
        em.set_key(self.A, 'IdentifiantImmeuble')
        em.set_key(self.B, 'IdentifiantImmeuble')

        self.A['ComplementNumeroVoieImmeuble'] = self.A['ComplementNumeroVoieImmeuble'].apply(self.complement_numero_voie)
        self.B['ComplementNumeroVoieImmeuble'] = self.B['ComplementNumeroVoieImmeuble'].apply(self.complement_numero_voie)
        self.create_column_for_blocking()

    def complement_numero_voie(self, string):
        """
        Convert complement road name address to one form, for example bis, ter, quater to b,t,q

        Args:
            - string (string): The complement address of BAN and IPE
        
        Return:
            - Normalized string
        """
        try:
            string = string.lower()
        except:
            pass
        if string == 'bis':
            string = 'b'
        if string == 'ter':
            string = 't'
        if string == 'quater':
            string = 'q'
        return string

    def create_column_for_blocking(self):
        """
        Define the blocker attributes to check and put in 1 column (because AttrEquivalenceBlocker can only handle 1 column comparison)
        For the unknown NumeroVoieImmeuble, we impute with the value 0

        Return:
            - 2 new dataframes that are imputed and have new column 'blocking_data'
        """

        self.A['NumeroVoieImmeuble'] = self.A['NumeroVoieImmeuble'].fillna(value = 0).astype(int)
        print('We imputed', len(self.A[self.A['NumeroVoieImmeuble'] == 0]), 'unknown NumeroVoieImmeuble in the IPE dataset')

        self.B['NumeroVoieImmeuble'] = self.B['NumeroVoieImmeuble'].fillna(value = 0).astype(int)
        print('We imputed', len(self.B[self.B['NumeroVoieImmeuble'] == 0]), 'unknown NumeroVoieImmeuble in the BAN dataset')

        self.A['CodePostalImmeuble'] = self.A['CodePostalImmeuble'].fillna(value = 00000).astype(int)
        print('We imputed', len(self.A[self.A['CodePostalImmeuble'] == 0]), 'unknown CodePostalImmeuble in the IPE dataset')

        self.B['CodePostalImmeuble'] = self.B['CodePostalImmeuble'].fillna(value = 00000).astype(int)
        print('We imputed', len(self.B[self.B['CodePostalImmeuble'] == 0]), 'unknown CodePostalImmeuble in the BAN dataset')

        self.A["blocking_data"] = (
            self.A["NumeroVoieImmeuble"].fillna("").astype(str)
            + " "
            + self.A["ComplementNumeroVoieImmeuble"].fillna("").astype(str)
            + " "
            + self.A["TypeVoieImmeuble"].fillna("").astype(str)
            + " "
            + self.A["CodePostalImmeuble"].fillna("").astype(str)
        )
        self.B["blocking_data"] = (
            self.B["NumeroVoieImmeuble"].fillna("").astype(str)
            + " "
            + self.B["ComplementNumeroVoieImmeuble"].fillna("").astype(str)
            + " "
            + self.B["TypeVoieImmeuble"].fillna("").astype(str)
            + " "
            + self.B["CodePostalImmeuble"].fillna("").astype(str)
        )

    def block(self):
        """
        Make candidate record pairs that agree on one or more variables.
        Blocking is an effective way to make a subset of the record space (A * B).

        Returns: 
            - All record pairs that agree on the given variable, in this case is the column "blocking_data". 
        """
        attributes = [
            "IdentifiantImmeuble",
            "NumeroVoieImmeuble",
            "ComplementNumeroVoieImmeuble",
            "TypeVoieImmeuble",
            "NomVoieImmeuble",
            "CodePostalImmeuble",
            "CommuneImmeuble",
            "CoordonneeImmeubleX",
            "CoordonneeImmeubleY",
        ]
        ab = em.AttrEquivalenceBlocker()

        # Use block_tables to apply blocking over two input tables.
        C = ab.block_tables(self.A, self.B,
                            l_block_attr='blocking_data', r_block_attr='blocking_data',
                            l_output_attrs=attributes,
                            r_output_attrs=attributes,
                            l_output_prefix='l_', r_output_prefix='r_')
        return C