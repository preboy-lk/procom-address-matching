# src/Matching.py
import math

class Filtering:
    def __init__(self, C, distance = 2000):
        """
        Using coordinates to calculate the distance between 2 addresses. 
        If the distance is greater than 2000m (we can increase/lower this threshold), 
        we consider that they are not the same addresses because they are too far away.

        Args:
            - C (Dataframe): A subset of the record space (A * B) after blocking.
        """
        self.C = C
        self.distance = distance

    def distance_calculator(self, row):
        """
        Calculate the distance (in meter) between 2 coordinates.

        Args:
            - row.

        Return:
            - New column that contains the distance.
        """
        # left, right will be of type pandas series
        # get coordinates X Y
        left_x = row['l_CoordonneeImmeubleX']
        left_y = row['l_CoordonneeImmeubleY']
        right_x = row['r_CoordonneeImmeubleX']
        right_y = row['r_CoordonneeImmeubleY']

        distance = math.sqrt((right_x - left_x)**2 + (right_y - left_y)**2)

        return distance
    def filter(self):
        self.C['distanceXY'] = self.C[['l_CoordonneeImmeubleX','l_CoordonneeImmeubleY','r_CoordonneeImmeubleX','r_CoordonneeImmeubleY']].apply(lambda row : self.distance_calculator(row)  ,axis = 1)
        # Only take rows where distance <= 2000 (default)
        self.D = self.C[self.C['distanceXY'] <= self.distance]

        print(f" The record space filtered successfully with distance between 2 addresses <=  {self.distance}")
        return self.D