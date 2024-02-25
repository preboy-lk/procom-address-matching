# Postal Address Databases Matching
In France, as in numerous other countries, postal addresses are gathered across various systems managed by multiple organizations. Prominent among these are La Poste, along with entities such as IGN, DGFIP, municipalities, telephone, internet, electricity, gas, or water operators. Additionally, the State has recently introduced the National Address Base (BAN) to establish an authoritative and comprehensive address repository.
These addresses originate from diverse origins, including land surveys, postal envelope scans, or declarations from property owners. Despite standardized address formats in France, there exist multiple representations for the same address in certain cases. </br>
The objective of this research project is to devise an effective Machine Learning-based approach for comparing and matching addresses efficiently.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Requirements](#requirements)

## Installation

```bash
# Clone the repository
git clone https://github.com/preboy-lk/procom-address-matching.git

# Navigate to the 'src' directory of the project:
cd procom-address-matching/src

# Install the required packages using pip:
pip install -r requirements.txt
```

## Usage
To run the project, execute the following command from the 'src' directory:
```bash
python -u main.py algo1
```
Replace algo1 with algo2 if you want to run the second algorithm. </br>
For detailed usage and demonstration, refer to the Jupyter notebooks provided in the notebooks directory.
## Workflow
# Rules - Based Method
The simplest kind of record linkage, called deterministic or rules-based record linkage, generates links based on the number of individual identifiers that match among the available data sets. Two records are said to match via a deterministic record linkage procedure if all or some identifiers (above a certain threshold) are identical. Deterministic record linkage is a good option when the entities in the data sets are identified by a common identifier, or when there are several representative identifiers whose quality of data is relatively high.
![alt text](https://github.com/preboy-lk/procom-address-matching/blob/main/diagrams/Algo1.png)
- Data Pre-processing: In this step, we clean the data before entering the model by dealing with the missing values or reducing the columns,… With BAN, we created an algorithm to separate the road type and road name into 2 separate columns (because in the original data of BAN, they are not separated).
- Indexing, blocking: is a technique used in record linkage to improve the efficiency of the matching process by reducing the number of record comparisons. The idea is to group records into smaller subsets or blocks based on certain key attributes. This way, comparisons are only made within the same block, significantly reducing the overall number of potential comparisons.
- Record pair comparison: involves systematically comparing pairs of records to determine their similarity or dissimilarity.  To do this, we use string comparison methods such as Jaccard similarity, cosine similarity, Levenshtein distance,…
- Classification: Based on professional knowledge, select important comparison pairs to decide whether the two addresses match or not.
- Evaluation: Calculating the accuracy, precision, recall, especially false positives to assess the performance of model.
- Tuning rules: Selecting other comparison pairs or tuning the threshold of Fuzzy Logic.
- Tuning block (optional): In case the above adjustments do not improve the performance of the model, we can re-tune the block.

# Machine Learning
In recent years, a variety of machine learning techniques have been used in record linkage. Higher accuracy can often be achieved by using various other machine learning techniques, including a single-layer perceptron, random forest, and SVM. In conjunction with distributed technologies, accuracy and scale for record linkage can be improved further. 
![alt text](https://github.com/preboy-lk/procom-address-matching/blob/main/diagrams/Algo2.png) </br> 
In this method, we add some new steps to take:
- Data Labelling: After preprocessing the two datasets, we will join them together and label them to create the dataset for training ML model. This step will be done manually or using a rules-based method.
- Train/test splitting: To split the dataset into 2 sets, one for training and one for evaluation.
- Classification: this is the supervised learning, whose input is the record pair comparison of all columns and output is the label 1 for match, and 0 for non-match. 
- Using different classification algorithms: we can use SVM, Random Forest, Gradient Boosting or Deep Learning. 

## Requirements
- Python 3.x
- Other dependencies as specified in requirements.txt
