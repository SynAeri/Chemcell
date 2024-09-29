---
title: 'Chemcell: A python package for chemical property data analysis'
tags:
  - Python
  - Chemistry
  - Documentation
  - Formatting
  - Data analysis
authors:
  - name: Jordan Maquiran
    orcid: 0009-0001-7830-9417
    equal-contrib: false
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Cooper Donnely
    orcid: 0009-0004-8905-7691
    equal-contrib: false # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
affiliations:
 - name: University Of Technology Sydney, Australia
   index: 1
   ror: 00hx57361
 - name: Macquarie University, Australia
   index: 2
date: 29 September 2024
bibliography: paper.bib
---

# Summary

Finding data for chemical properties, especially reactions can be a truly arduous and tedious process. And past this, the process of making this data into tabular a format made for data preprocessing and formatting to both analyse and research.

Our software package, Chemcell, addresses this challenge by providing highly modular and flexible tools to automate the extraction and tabulation of chemical property data from multiple well-known chemistry databases. Designed with both computer scientists and researchers in mind, Chemcell streamlines the process of converting raw chemical data into clean, structured formats ready for analysis along with tools that auto process the data preprocessing stage.

By combining disciplines from both computer science and chemistry, this package provides flexibility in organising and formatting data to meet specific research needs. This makes Chemcell a valuable asset for data-driven chemical research, enabling users to focus more on analysis and less on manual data preparation.

# Statement of need

`chemcell` is a data analysis python package for research and data analysis purposes. Python enables the use of reputable software such as pandas and bs4 to take reaction data from a facet of databases and parse them in readable and research built output. `chemcell` API is built to be designed to be simple, robust and efficient in it's purpose of modulating and manipulating data. `chemcell` was purposed to be used by both researchers, students and hobbyists for use of bulk data preprocessing and tabulation at a quick and easy rate for uses on prediction, data referral and analysis.

While python libraries `beautifulsoup4` and `pandas` do provide the building blocks for processing, data manipulation and web scraping. There lacks a out-of-the-box and modular solution which is tailored to taking bulk data reactions, splitting them into singular columns and pre-process data into the needed format in a short time span. A researcher would need to build a system with considerations for different cases and components.

The need for a tool like `chemcell` is especially critical for researchers working with large datasets, students just beginning their journey in chemical informatics, and even hobbyists looking for a quick and effective way to preprocess and analyze chemical property data. By reducing the amount of time spent on data wrangling, chemcell allows users to focus on higher-level research tasks such as modeling and prediction, thereby accelerating the pace of research in both academic and industrial contexts.



# Implementation

`chemcell` takes reaction data from [Nist](https://www.nist.gov/), and parses this into [Chemeo](https://www.chemeo.com/) and [Pubchem](https://pubchem.ncbi.nlm.nih.gov/) databases. This data is parsed into an easily read csv format which can be automatically pre-processed to remove duplications and similar forms, split into reaction and product data formats and labelled according to it's correlation.

The core workflow of chemcell involves three main steps:

Data Extraction: chemcell connects to the APIs or HTML endpoints of the databases to retrieve reaction data in raw format. For [NIST](https://www.nist.gov/), the tool scrapes reaction details such as reactants, products, and conditions. Data from [Chemeo](https://www.chemeo.com/) and [PubChem](https://pubchem.ncbi.nlm.nih.gov/), which focus on chemical properties and molecular structures, is collected to enrich the reaction dataset.

Data Parsing: The raw data is parsed into structured formats. The parsing process organizes data into reaction-specific rows and product-specific rows, ensuring that each entry is properly labeled with key identifiers (e.g., CAS numbers, reaction types), accounting for multiple versions of provided data, they are averaged, not including or including the outlier (according to the user). This step also involves checking for missing values and duplicates, ensuring data quality.

Data Preprocessing: To prepare the data for analysis, chemcell provides built-in preprocessing functionalities. These include:

Deduplication: Automated removal of redundant entries and duplicate reactions across the sources.
Data Cleaning: Standardizing units, chemical names, and molecular formulas.
Labeling: Each reaction and product is labeled according to its correlation, which helps researchers easily distinguish between reactants and products when conducting further analysis.

Output: The cleaned and preprocessed data is then exported to CSV format for easy integration with other tools. The CSV format allows for compatibility with a wide variety of data analysis pipelines, from machine learning models to statistical analysis.

| Reactant_Count | Product Count| Reactant_Name_1 | Reactant_ID_1 | Molecular Weight |
|----------|:---------------:|:-----------------:|------------|---------|
| 2  | 1  | 1,3-Butadiene               | 106-99-0 | 54.09    |
| 2      | 1 | 	1-Butene               | 106-98-9   | 56.11    |
| 2        | 1 | 1-Propene,-2-methyl-     | 115-11-7   | 56.11    |

