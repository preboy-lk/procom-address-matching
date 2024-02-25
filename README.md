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
![alt text](https://github.com/preboy-lk/procom-address-matching/tree/main/diagrams/Algo1.png?raw=true)
![alt text](https://github.com/preboy-lk/procom-address-matching/tree/main/diagrams/Algo2.png?raw=true)
## Requirements
- Python 3.x
- Other dependencies as specified in requirements.txt
