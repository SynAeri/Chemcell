import csv
import os
import io
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

def save_csv(file_location, name, headers, rows):
        if file_location == None:
            file_location = os.path.join(tempfile.gettempdir(), 'temprawdata.txt')
        else:
            file_location = os.path.join(file_location, f"Ouput_Data_{name}.csv")

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        csv_content = output.getvalue()

        print("\n Saving file")
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
    
    def __str__(self):
        try:
            data_segments = self.Post_tabulate.SplitFields()
            output = []
            
            for segment in data_segments:
                output.append(self._format_segment(segment))
            
            return "\n\n".join(output)
        except Exception as e:
            log.error(f"Error in Tabulate_Store __str__ method: {e}")
            return f"Error processing data: {str(e)}"

    def _format_segment(self, segment):
        formatted_output = []
        for _, row in segment.iterrows():
            formatted_output.append("Compound Data:")
            for column, value in row.items():
                if pd.notnull(value):  # Only include non-null values
                    if isinstance(value, float):
                        formatted_output.append(f"{column}: {value:.4f}")
                    else:
                        formatted_output.append(f"{column}: {value}")
            formatted_output.append("-" * 40)  # Separator between compounds
        return "\n".join(formatted_output)
    
 
