from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="chemcell",
    version="0.2.4",
    description="highly modifiable tabulation for chemical reactions",
    long_description= description,
    long_description_content_type="text/markdown",
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
