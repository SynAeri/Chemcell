"""
Chemcell - 2024
Main File for declaring and initialising self variables

"""
from.utlity import save_csv, get_response
from .scrape import Chemcelltabulate
from .process import Chemcellprocess
from .defval import DEFAULT_PUBCHEM_DATA, DEFAULT_CHEMEO_DATA


class Chemcell:

    def __init__(self, name, outliers = False, file_location=None):
        #Defaults
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
        self.Chemcellprocess = Chemcellprocess()

    #Options
    def range(self, r_Min=None, r_Max=None):
        self.r_Min = r_Min
        self.r_Max = r_Max
        return self
    #Pubchem_properties
    def Pc_Prop(self, Pc_P = None):
        if Pc_P == None:
            Pc_P = DEFAULT_PUBCHEM_DATA
        self.Pc_P = Pc_P
        return self
    #Chemeo_properties
    def C_Prop(self, C_P = None):
        if C_P == None:
            C_P = DEFAULT_CHEMEO_DATA
        self.C_P = C_P
        return self
    
    def RP_Count(self, R_count = None, P_Count = None):
        self.R_count = R_count
        self.P_Count = P_Count
        return self

    def tabulate(self):
        raw_data, React_Count, Prod_Count = self.Chemcelltabulate.process_data(self.name, self.r_Min, self.r_Max, self.Pc_P, self.C_P, self.R_count, self.P_Count, self.outliers)
        #Next Var in the chopping block: Process data to take headers + rows
        headers = Chemcellprocess.Get_Logistics(React_Count, Prod_Count, self.C_P, self.Pc_P)
        save_csv(self.file_location, self.name, headers, raw_data)




        

