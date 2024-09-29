import csv
import os
import io
from io import StringIO
import logging
import tempfile
from .post_process import ChemcellPostTabulate
from contextlib import closing
from requests import get
import pandas as pd

log = logging.getLogger('chemcell')



def response(resp):
    #if it is a functioning HTML
    content = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content is not None
            and content.find('html') > -1)


def get_response(url):
    #return html to parse, return none if it cant reach page
    with closing(get(url, stream=True)) as resp:
        if response(resp):
            return resp.content
        else:
            return None
        
def Get_Logistics(React_c, Prod_c, C_P, Pc_P):
    header_c = ['Reactant_Count', 'Product_Count']
    Chemeo_Prop = C_P
    Pubchem_Prop = Pc_P
    Props = Pubchem_Prop + Chemeo_Prop
    for i in range(React_c):
        header_c.append(f"Reactant_Name_{i+1}")
        header_c.append(f"Reactant_ID_{i+1}")
        header_c += Props
    
    for i in range(Prod_c):
        header_c.append(f"Product_Name_{i+1}")
        header_c.append(f"Product_ID_{i+1}")
        header_c += Props
    
    return(header_c)
    
def save_csv(file_location, name, headers, rows):
        if file_location == None:
            file_location = os.path.join(tempfile.gettempdir(), 'temprawdata.txt')
        else:
            file_location = os.path.join(file_location, f"Output_Data_{name}.csv")

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        csv_content = output.getvalue()

        log.debug("Saving file")
        with open(file_location, 'w', newline = '') as file:
            file.write(csv_content)

        return(file_location)

def _print_compound_data(reacts, products, data, properties):
    print("\nCompound Data:")
    
    # Calculate the number of properties per compound
    props_per_compound = len(properties)
    
    # Extract reactant and product counts
    reactant_count, product_count = data[0], data[1]
    
    # Start of compound data (after reactant and product counts)
    compound_data_start = 2
    
    def print_compound_info(compound_type, compounds, start_index):
        for i, compound in enumerate(compounds):
            print(f"\n{compound_type} {i+1}: {compound}")
            print(f"CAS: {data[start_index + i*(props_per_compound+1)]}")
            for j, prop in enumerate(properties):
                value = data[start_index + i*(props_per_compound+1) + j + 1]
                if isinstance(value, float):
                    print(f"  {prop}: {value:.2f}")
                else:
                    print(f"  {prop}: {value}")
    
    # Print reactant data
    print(f"\nReactants (Count: {reactant_count}):")
    print_compound_info("Reactant", reacts, compound_data_start)
    
    # Print product data
    print(f"\nProducts (Count: {product_count}):")
    print_compound_info("Product", products, compound_data_start + reactant_count*(props_per_compound+1))

    print("\nEnd of Compound Data")



def setup_logging(default_path='logging.conf', default_log_level=logging.INFO, env_key='LOG_CFG'):

    """
    Setup logging configuration
    
    :param default_path: path to the logging configuration file
    :param default_level: default logging level
    :param env_key: environment variable key to check for config file path
    :return: configured logger
    """

    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        try:
            logging.config.fileConfig(path)
            print(f"Loaded logging configuration from {path}")
        except Exception as e:
            print(f"Error loading logging configuration: {e}. Using basic configuration.")
            logging.basicConfig(level=default_log_level)
    else:
        print(f"Logging config file not found at {path}. Using basic configuration.")
        logging.basicConfig(level=default_log_level,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    return logging.getLogger('chemcell')


"""
This class responds to the return statement of chemcells tabulation method and has it return a string of data if printed out.

"""

class Tabulate_Store:
    def __init__(self, data = None, reactants = None, products = None, properties = None):
        self.data = data
        self.reactants = reactants
        self.products = products
        self.properties = properties
        self.Post_tabulate = ChemcellPostTabulate(self.data, self.reactants, self.products, self.properties)


    def _format_segment(self, segments):
        output = StringIO()
        total_compounds = len(segments)
        
        for compound_index in range(len(segments[0])):
            print(f"Compound {compound_index + 1}:", file=output)
            
            for segment_index, segment in enumerate(segments):
                if compound_index < len(segment):
                    row = segment.iloc[compound_index]
                    compound_type = "Reactant" if segment_index < self.reactants else "Product"
                    compound_number = segment_index + 1 if segment_index < self.reactants else segment_index - self.reactants + 1
                    
                    print(f"  {compound_type}_{compound_number}:", file=output)
                    for column, value in row.items():
                        if pd.notnull(value):
                            formatted_value = f"{value:.4f}" if isinstance(value, float) else str(value)
                            print(f"    {column}: {formatted_value}", file=output)
            
            print("-" * 40, file=output)  # Separator between compounds
        
        return output.getvalue()
    
    def __str__(self):
        try:
            data_segments = self.Post_tabulate.SplitFields()
            return self._format_segment(data_segments)
        except Exception as e:
            log.error(f"Error in Tabulate_Store __str__ method: {e}")
            return f"Error processing data: {str(e)}"
    
 
