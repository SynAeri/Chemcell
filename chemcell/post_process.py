"""
Where data once collected is preprocessed after tabulation
Most tabular manipulation is handled here

"""
import csv
import os
import io
import logging
import tempfile
from math import ceil
from contextlib import closing
from requests import get
import pandas as pd
from .config import DEFAULT_CHEMEO_DATA, DEFAULT_PUBCHEM_DATA

log = logging.getLogger('chemcell')

class ChemcellPostTabulate:

    def __init__(self, Data, reactants, products, properties):
        self.Data = Data
        self.reactants = reactants
        self.products = products
        self.properties = properties

    def SplitFields(self, data= None, reactants = None, products = None, properties = None):
        #If data here is none then we use self_data which is provided
        print("PASSED")
        if data == None:
            print(f"DATA IS NONE SO CHANGING TO SELF DATA: {self.Data}")
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
        



