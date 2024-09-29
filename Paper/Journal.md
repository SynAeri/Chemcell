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

While the singular python libraries `beautifulsoup4` and `pandas` do provide the building blocks for processing, data manipulation and web scraping. There lacks a readily available and modular solution which is tailored to taking bulk data reactions, splitting them into singular columns and pre-process data into the needed format in a short time span. A researcher would need to build a system with considerations for different cases and components.

The need for a tool like `chemcell` is especially critical for researchers working with large datasets, students just beginning their journey in chemical informatics, and even hobbyists looking for a quick and effective way to preprocess and analyze chemical property data. By reducing the amount of time spent on data wrangling, chemcell allows users to focus on higher-level research tasks such as modeling and prediction, thereby accelerating the pace of research in both academic and industrial contexts.



# Implementation

`chemcell` takes reaction data from [Nist](https://www.nist.gov/), and parses this into [Chemeo](https://www.chemeo.com/) and [Pubchem](https://pubchem.ncbi.nlm.nih.gov/) databases, and parses this into a process 

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References