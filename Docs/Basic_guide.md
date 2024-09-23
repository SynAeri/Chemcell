# Initialisation
## Basic Setup
When setting up Chemcell install it by doing the following:
```
pip install chemcell
```
Once downloading always make sure its initialised in every ```.py```
```
from chemcell import Chemcell
```
The typical basic format of Chemcell is shown here
```
from chemcell import Chemcell
example = Chemcell(["Compound"], Outlier = False, "File_Location")
example.tabulate()

```
Note: the tabulate method will be reconfigured later to define as converting the raw data into csv form, search will be made its own method.

# Searching
When searching for reactions including A,B,C,D compounds, you typically send them in a 1d array ```["A","B","C","D"]```, The search method at best looks for 2 products and 2 reactants, adding data for all elements and the arrangement is not important, nor does it change the outcome of results. If there exists results for these and it is not shown, please let me know!

Note: Leaving the search in String form does not cause any errors, however it is highly reccomended for multi-filtered search!

Extra Note: search is not case sensitive.

```
Chemcell(["HCl", "O"], False, "/workspaces/Chemcell/Example_Data").tabulate()
```

## Including Outliers
When including outliers, it is either a true or false choice. The change in including the outlier or not decides on how the average for some datasets are calculated. This is shown through ```True``` or ```False```

## Specifying file location
Provide the file location where the output (e.g., CSV) will be saved. Ensure the file path is correct and accessible.
```
example = Chemcell(["HCl"], False, "/path/to/file")
```

## Advanced Usage
### Range
Range takes in two parameters: minimum_search and max_search.

Range is defaulted to ```(0, max_results)```, hence this parameter can be very important if you need to reduce the dataset scrape time. This is done through the ```range()``` function.
```
example = Chemcell(["HCl", "O"], False "File_location")
#sets the range from 2nd up to 4th element
example.range(2,4).tabulate()
```
### RP_Count
RP_Count takes in two parameters: Reaction_Count, Product_Count.

RP_Count is defaulted into 2 Reactions and 2 Products. This has not been tested as much and can cause issues, let me know if this occurs. The purpose is to exactly find reaction counts with these exact numbers

Note: This can hence cause little data to be produced.

```
example = Chemcell(["HCl", "O"], False "File_location")
#finds Reactions with 2 and Products producing 4.
example.RP_Count(2,4).tabulate()
```

### Pc_Prop
Pc_Prop takes [x_1,...,x_n] properties

Pc_Prop takes from [PubChemPy's](https://github.com/mcs07/PubChemPy/tree/master) api due  to my inability to scrape its products, which I will reattempt at a later day.

The following properties available to be searched are as follows: ```MolecularFormula, MolecularWeight, CanonicalSMILES, IsomericSMILES, InChI, InChIKey, IUPACName, XLogP, ExactMass, MonoisotopicMass, TPSA, Complexity, Charge, HBondDonorCount, HBondAcceptorCount, RotatableBondCount, HeavyAtomCount, IsotopeAtomCount, AtomStereoCount, DefinedAtomStereoCount, UndefinedAtomStereoCount, BondStereoCount, DefinedBondStereoCount, UndefinedBondStereoCount, CovalentUnitCount, Volume3D, XStericQuadrupole3D, YStericQuadrupole3D, ZStericQuadrupole3D, FeatureCount3D, FeatureAcceptorCount3D, FeatureDonorCount3D, FeatureAnionCount3D, FeatureCationCount3D, FeatureRingCount3D, FeatureHydrophobeCount3D, ConformerModelRMSD3D, EffectiveRotorCount3D, ConformerCount3D.```

Collected from : [Pubchempy Docs: Properties](https://pubchempy.readthedocs.io/en/latest/guide/properties.html)

```
example = Chemcell(["HCl", "O"], False "File_location")
#Finds data with "HBondAcceptorCount", if nothing found input N/A
example.Pc_Prop(["HBondAcceptorCount"]).tabulate()
```

### C_Prop
Due to Chemeo's terms of service C_Prop isn't made and the static properties available are as follows:
- Electron affinity 
- Ionization energy
- Critical Pressure
- Dipole Moment
- Critical Temperature
- Octanol/Water partition coefficient
