
# Chemcell - A multi-use Package To Tabulate Chemical Properties
A personal study on a curiosity + A free use package for tabulating chemical properties for your data needs!
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Basic Overview

A Software used to scrape data from [Nist](https://www.nist.gov/), [Chemeo](https://www.chemeo.com/) and [Pubchem](https://pubchem.ncbi.nlm.nih.gov/) to format chemical properties in csv form originally as a study for organic compounds and its partition coefficient, to see if we could use a deepforest algorithm to predict other following reactions.

## About Chemcell
N/A

## Implementation

```
pip install chemcell
```

## Usage
Getting a bulk dataset including a specific element while modifying what is tabulated from Sites Pubchem, Chemeo and referencing Nist's handy reaction list.
```
from chemcell import Chc
example = Chc("Hcl", Outlier=False, "file_source").range(5,20)
data = example.tabulate()
```
For self study and educational purposes, general Ml predictions et al.

## Citation
Chemical and physical properties from Cheméo.

