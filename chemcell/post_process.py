"""
Where data once collected is preprocessed after tabulation
Most tabular manipulation is handled here

"""
import logging
from math import ceil
from requests import get
import pandas as pd
from .config import DEFAULT_CHEMEO_DATA, DEFAULT_PUBCHEM_DATA

log = logging.getLogger('chemcell')

class ChemcellPostTabulate:

    def __init__(self, Data, reactants, products, properties, file_loc = ""):
        self.Data = Data
        self.reactants = reactants
        self.products = products
        self.properties = properties
        self.file_loc = file_loc

    def SplitFields(self, data= None, reactants = None, products = None, properties = None, Download: bool = False):
        #If data here is none then we use self_data which is provided
        if data == None:
            print(f"No data given, changing to: {self.Data}")
            try:
                data = pd.read_csv(self.Data)
            except Exception as e:
                return log.error(f"Exception found through data splitting: {e}")
                
        if reactants == None:
            reactants = self.reactants
        
        if products == None:
            products = self.products

        if properties == None:
            properties = self.properties
            
        try:
            total_R_P = (reactants + products)
            columns_dropped = data.drop(columns=["Reactant_Count","Product_Count"], axis=1)
            columns = len(columns_dropped.columns)
            columns_per_segment = ceil(columns/total_R_P)

            output = []
            for i in range(0, columns, columns_per_segment):
                            segment = columns_dropped.iloc[:, i:i+columns_per_segment]
                            #output.append(f"Segment {i//columns_per_segment + 1}, lenght [{len(segment.columns)}]:\n{segment.to_string(index=False)}\n")
                            output.append(segment)
            #return "\n".join(output)
            return(output)
        except Exception as e:
            return f"Error converting data to string: {str(e)}"
        



