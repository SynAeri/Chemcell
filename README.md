
# Chemcell - A multi-use Package To Tabulate Chemical Properties
[Link to pypi](https://pypi.org/project/chemcell/0.1/)
A personal study on a curiosity + A free use package for tabulating chemical properties for your data needs!
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Basic Overview

A Software used to scrape data from [Nist](https://www.nist.gov/), [Chemeo](https://www.chemeo.com/) and [Pubchem](https://pubchem.ncbi.nlm.nih.gov/) to format chemical properties in csv form originally as a study for organic compounds and its partition coefficient, to see if we could use a deepforest algorithm to predict other following reactions.

## About Chemcell
Chemcell is a byproduct of a bit of a study I have done with a peer at another University, to both learn new skills and improve efficiency for data processing and analysation,
This serves to benefit scraping bulk amounts of reaction data from Nist and then using data from pubchem and chemeo (where I personally average the data), I realised (and my peer),
I could make this a tool to use later while also adding onto it (having the option to allow outliers).

In essence this is a tool to help with the process of tabulating data for data analysis and personal research purposes - for fun

## Implementation

```
pip install chemcell
```

## Usage
Getting a bulk dataset including a specific element while modifying what is tabulated from Sites Pubchem, Chemeo and referencing Nist's handy reaction list.
```
from chemcell import Chemcell as Chc
example = Chc(["HCl"], False, "file_source").range(5,20)
data = example.tabulate()
```
For self study and educational purposes, general Ml predictions et al.

## Citation
Chemical and physical properties from Cheméo.

