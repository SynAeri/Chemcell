from setuptools import setup, find_packages
long_desc="""
Chemcell is a byproduct of a bit of a study I have done with a peer at another University, to both learn new skills and improve efficiency for data processing and analysation,
This serves to benefit scraping bulk amounts of reaction data from Nist and then using data from pubchem and chemeo (where I personally average the data), I realised (and my peer),
I could make this a tool to use later while also adding onto it (having the option to allow outliers).

In essence this is a tool to help with the process of tabulating data for data analysis and personal research purposes - for fun

"""
setup(
    name="chemcell",
    version="0.01",
    description="highly modifiable tabulation for chemical reactions",
    long_description= long_desc,
    author="Jordan Maquiran, Cooper Donnely",
    author_email="jordan.maquiran@outlook.com",
    url="https://github.com/SynAeri/Chemcell",
    install_requires=[
        "beautifulsoup4",
        "pandas",
        "html.parser",
        "lxml",
        "requests",
        "urllib3",
        "pubchempy",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Topic :: Documentation",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
    ],
    packages=find_packages(),
)
