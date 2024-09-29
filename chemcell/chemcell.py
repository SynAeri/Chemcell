"""
Chemcell - A Python Package for Chemical Data Analysis and Tabulation
This module contains the main Chemcell class, which orchestrates the process of
fetching, analyzing, and tabulating chemical data from various sources.

License: MIT
"""


import logging
import os
import logging.config
from typing import List, Dict, Optional
from.utlity import save_csv, setup_logging, Get_Logistics, Tabulate_Store
from .scrape import Chemcelltabulate
from .config import DEFAULT_PUBCHEM_DATA, DEFAULT_CHEMEO_DATA

log = setup_logging(default_path=os.path.join(os.path.dirname(__file__), 'logging.conf'))

class Chemcell:

    def __init__(self, name: List[str], outliers: bool = False, file_location: Optional[str]=None):
        #Defaults
        log.info(f"Initialising Chemcell with {name}, Keep outliers: {outliers}, file_location: {file_location}")

        if isinstance(name, str):
            self.name = [name]
        else:
            self.name = name

        self.outliers = outliers
        self.file_location = file_location
        self.r_Min = None
        self.r_Max = None
        self.Pc_P = DEFAULT_PUBCHEM_DATA
        self.C_P = DEFAULT_CHEMEO_DATA
        self.R_count = 2
        self.P_Count = 2

        # Initialize Chemcelltabulate with all parameters
        self.Chemcelltabulate = Chemcelltabulate()
        self.Tabulate_data = Tabulate_Store()

    #Options
    def range(self, r_Min: Optional[int] = None, r_Max: Optional[int] = None):
        self.r_Min = r_Min
        self.r_Max = r_Max
        return self
    
    #Pubchem_properties
    def Pc_Prop(self, Pc_P: Optional[List[str]] = None):
        if Pc_P == None:
            Pc_P = DEFAULT_PUBCHEM_DATA
        self.Pc_P = Pc_P
        return self
    
    #Chemeo_properties
    def C_Prop(self):
        self.C_P = DEFAULT_CHEMEO_DATA
        return self
    
    def RP_Count(self, R_count: Optional[int] = None, P_Count: Optional[int] = None):
        self.R_count = R_count
        self.P_Count = P_Count
        return self

    def tabulate(self):
        """
        Process and tabulate the chemical data.

        This method orchestrates the entire data processing pipeline, including
        data retrieval, processing, and tabulation.

        Returns:
            Tabulate_Store: An object containing the processed and tabulated data.
        """
        log.info("Starting Bulk data buildup")
        raw_data, React_Count, Prod_Count = self.Chemcelltabulate.process_data(
            self.name, self.r_Min, self.r_Max, self.Pc_P, self.C_P, 
            self.R_count, self.P_Count, self.outliers
        )

        headers = Get_Logistics(React_Count, Prod_Count, self.C_P, self.Pc_P)
        data = save_csv(self.file_location, self.name, headers, raw_data)
        print(f"Chemcell class data: {data}")
        self.Tabulate_data = Tabulate_Store(data, React_Count, Prod_Count, self.Pc_P + self.C_P)

        return self.Tabulate_data






        

