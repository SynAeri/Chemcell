from setuptools import setup, find_packages
long_desc=""
setup(
    name="chemcell",
    version="0.01"
    description="highly modifiable tabulation for chemical reactions"
    long_description= long_desc,
    author="Jordan Maquiran, Cooper Donnaly",
    author_email="jordan.maquiran@outlook.com",
    url="https://github.com/SynAeri/Chemcell",
    install_requires=[
        "reqests",
        "beautifulsoup4",
        "pandas",
        "pubchempy",
        "html.parser",
        "lxml",
        "urllib3",
        "numpy"

    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Topic :: Documentation",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
    ]
    packages=find_packages()
)