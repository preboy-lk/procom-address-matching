# src/main.py
import warnings
warnings.filterwarnings('ignore')
import sys

from Algorithm1 import Algorithm1
from Algorithm2 import Algorithm2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -u main.py [algo1/algo2]")
        sys.exit(1)

    algorithm_choice = sys.argv[1]

    if algorithm_choice == "algo1":
        algorithm = Algorithm1()
    elif algorithm_choice == "algo2":
        algorithm = Algorithm2()
    else:
        print("Invalid algorithm choice. Please choose 'algo1' or 'algo2'.")
        sys.exit(1)

    algorithm.run()