# src/main.py
import warnings
warnings.filterwarnings('ignore')

from AddressParsing import AddressParsing
from DataPreprocessor import DataPreprocessor

def main():
    obj1 = AddressParsing()
    obj2 = DataPreprocessor()
    
if __name__ == "__main__":
    main()