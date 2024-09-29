import requests
import logging
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from .utlity import get_response

log = logging.getLogger('chemcell')

class abstractData_S(ABC):
    @abstractmethod
    def fetch_data(self, identifier: str, properties):
        raise NotImplementedError
        pass

class PubChemDataSource(abstractData_S):
    def fetch_data(self, identifier, properties):
        data = []
        try:
            # Use the locally defined get_properties function
            compound_p = get_properties(properties, identifier, namespace='name')
            
            if compound_p:
                for prop in properties:
                    pubchem_prop = PROPERTY_MAP.get(prop, prop)
                    value = compound_p[0].get(pubchem_prop)
                    if value is not None:
                        data.append(value)
                    else:
                        data.append("N/A")
            else:
                data = ["N/A"] * len(properties)
        except Exception as e:
            print(f"Error fetching PubChem data for {identifier}: {e}")
            data = ["N/A"] * len(properties)
        
        return data

class ChemeoDataSource(abstractData_S):

    def fetch_data(self, identifier, properties, outliers = False):
        try:
            url = f"https://www.chemeo.com/search?q={identifier}"
            response = get_response(url)

            html = BeautifulSoup(response, 'html.parser')
            data = self._extract_property(html, properties, outliers)

            return data
        except Exception as e:
            print(f"Error has occured in Chemeo_Parsing: {e}")
            return ['N/A'] * len(properties)

    def _extract_property(self, soup, property_name, outliers):
        prop_element = soup.find('div', {"class": "container"}).find('div', id="details-content")
        prop_element = prop_element.find('table', {"class": "props details"})
        prop_element = prop_element.find_all('tr')
        data = []
        count = 0
        prev_title = ""
        not_found_property_check = True
        sum = 0

        #Iterates the number of properties there are
        for i in property_name:
            not_found_property_check = True
            for results in prop_element:
                if results.find('td'):
                    result_index = results.find('td')
                    if result_index.find('span')['title']:
                        title = result_index.find('span')['title']
                        if(title == i):
                            result = results.find('td', {'class': "r"}).text
                            if(prev_title != title):
                                if(count == 0):
                                    if("[" in result):
                                        result = result.replace("[", "").replace("]", "")
                                        result_split = result.split(";")
                                        result = (float(result_split[0]) + float(result_split[1]))/2  

                                    data.append(result)
                                    not_found_property_check = False
                                else:
                                    #since count is not 0, it means that a new element is found and no more alternatives are found hence we make the average here now.
                                    if(sum > 0):
                                        data[-1] = sum/count
                                        sum = 0
                                    if("[" in result):
                                        result = result.replace("[", "").replace("]", "")
                                        result_split = result.split(";")
                                        result = (float(result_split[0]) + float(result_split[1]))/2
                                    
                                    data.append(result)
                                    not_found_property_check = False
                                    count == 0
                            else:
                                #Both titles are equal meaning we are seeing alternatives

                                    #To add: if it sees alternmatives then add the sum, if the outlier class is declared false and an outlier exists then we discount the outlier.
                                #Count to account for average values recorded
                                if "±" in result:
                                    if "Outlier " in result:
                                        results = result.replace("Outlier ", "")
                                        if(outliers == True):
                                            result_split = result.split("±")
                                            sum += float(result_split[0]) + float(result_split[-1])
                                            sum += float(result_split[0]) - float(result_split[-1])


                                    else:
                                        result_split = result.split("±")
                                        sum += float(result_split[0]) + float(result_split[-1])
                                        sum += float(result_split[0]) - float(result_split[-1])
                                else:
                                    if "Outlier " in result:
                                        results = result.replace("Outlier ", "")
                                        if(outliers == True):
                                            sum += float(results)

                                    else:
                                        sum += float(result)
                                count += 1
                            prev_title = title
            if(not_found_property_check == True):                                                       
                data.append("N/A")
        return(data)

################################################################################
# The following code is adapted from the PubChemPy library, which is
# covered under the MIT License, Copyright (c) 2014 Matt Swain.
#
# Original source: https://github.com/mcs07/PubChemPy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################

import json
from urllib.request import urlopen
from urllib.parse import quote, urlencode
from urllib.error import HTTPError

API_BASE = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'

def request(identifier, namespace='cid', domain='compound', operation=None, output='JSON', searchtype=None, **kwargs):
    """
    Construct API request from parameters and return the response.
    Full specification at http://pubchem.ncbi.nlm.nih.gov/pug_rest/PUG_REST.html
    """
    if not identifier:
        raise ValueError('identifier cannot be None')
    # If identifier is a list, join with commas into string
    if isinstance(identifier, int):
        identifier = str(identifier)
    if not isinstance(identifier, str):
        identifier = ','.join(str(x) for x in identifier)
    
    kwargs = dict((k, v) for k, v in kwargs.items() if v is not None)
    
    urlid, postdata = None, None
    if namespace in ['listkey', 'formula', 'sourceid'] \
            or searchtype == 'xref' \
            or (searchtype and namespace == 'cid') or domain == 'sources':
        urlid = quote(identifier.encode('utf8'))
    else:
        postdata = urlencode([(namespace, identifier)]).encode('utf8')
    
    comps = filter(None, [API_BASE, domain, searchtype, namespace, urlid, operation, output])
    apiurl = '/'.join(comps)
    if kwargs:
        apiurl += '?%s' % urlencode(kwargs)
    
    try:
        response = urlopen(apiurl, postdata)
        return response
    except HTTPError as e:
        raise PubChemHTTPError(e)

def get(identifier, namespace='cid', domain='compound', operation=None, output='JSON', searchtype=None, **kwargs):
    """Request wrapper that automatically handles async requests."""
    response = request(identifier, namespace, domain, operation, output, searchtype, **kwargs).read()
    if isinstance(response, bytes):
        response = response.decode()
    return response

def get_json(identifier, namespace='cid', domain='compound', operation=None, searchtype=None, **kwargs):
    """Request wrapper that automatically parses JSON response."""
    return json.loads(get(identifier, namespace, domain, operation, 'JSON', searchtype, **kwargs))

PROPERTY_MAP = {
    'molecular_formula': 'MolecularFormula',
    'molecular_weight': 'MolecularWeight',
    'canonical_smiles': 'CanonicalSMILES',
    'isomeric_smiles': 'IsomericSMILES',
    'inchi': 'InChI',
    'inchikey': 'InChIKey',
    'iupac_name': 'IUPACName',
    'xlogp': 'XLogP',
    'exact_mass': 'ExactMass',
    'monoisotopic_mass': 'MonoisotopicMass',
    'tpsa': 'TPSA',
    'complexity': 'Complexity',
    'charge': 'Charge',
    'h_bond_donor_count': 'HBondDonorCount',
    'h_bond_acceptor_count': 'HBondAcceptorCount',
    'rotatable_bond_count': 'RotatableBondCount',
    'heavy_atom_count': 'HeavyAtomCount',
    'isotope_atom_count': 'IsotopeAtomCount',
    'atom_stereo_count': 'AtomStereoCount',
    'defined_atom_stereo_count': 'DefinedAtomStereoCount',
    'undefined_atom_stereo_count': 'UndefinedAtomStereoCount',
    'bond_stereo_count': 'BondStereoCount',
    'defined_bond_stereo_count': 'DefinedBondStereoCount',
    'undefined_bond_stereo_count': 'UndefinedBondStereoCount',
    'covalent_unit_count': 'CovalentUnitCount',
    'volume_3d': 'Volume3D',
    'conformer_rmsd_3d': 'ConformerModelRMSD3D',
    'conformer_model_rmsd_3d': 'ConformerModelRMSD3D',
    'x_steric_quadrupole_3d': 'XStericQuadrupole3D',
    'y_steric_quadrupole_3d': 'YStericQuadrupole3D',
    'z_steric_quadrupole_3d': 'ZStericQuadrupole3D',
    'feature_count_3d': 'FeatureCount3D',
    'feature_acceptor_count_3d': 'FeatureAcceptorCount3D',
    'feature_donor_count_3d': 'FeatureDonorCount3D',
    'feature_anion_count_3d': 'FeatureAnionCount3D',
    'feature_cation_count_3d': 'FeatureCationCount3D',
    'feature_ring_count_3d': 'FeatureRingCount3D',
    'feature_hydrophobe_count_3d': 'FeatureHydrophobeCount3D',
    'effective_rotor_count_3d': 'EffectiveRotorCount3D',
    'conformer_count_3d': 'ConformerCount3D',
}

def get_properties(properties, identifier, namespace='cid', searchtype=None, as_dataframe=False, **kwargs):
    """Retrieve the specified properties from PubChem.

    :param identifier: The compound, substance or assay identifier to use as a search query.
    :param namespace: (optional) The identifier type.
    :param searchtype: (optional) The advanced search type, one of substructure, superstructure or similarity.
    :param as_dataframe: (optional) Automatically extract the properties into a pandas :class:`~pandas.DataFrame`.
    """
    if isinstance(properties, str):
        properties = properties.split(',')
    properties = ','.join([PROPERTY_MAP.get(p, p) for p in properties])
    properties = 'property/%s' % properties
    results = get_json(identifier, namespace, 'compound', properties, searchtype=searchtype, **kwargs)
    results = results['PropertyTable']['Properties'] if results else []
    if as_dataframe:
        import pandas as pd
        return pd.DataFrame.from_records(results, index='CID')
    return results

class PubChemHTTPError(Exception):
    """Generic error class to handle all HTTP error codes."""
    def __init__(self, e):
        self.code = e.code
        self.msg = e.reason
        try:
            self.msg += ': %s' % json.loads(e.read().decode())['Fault']['Details'][0]
        except (ValueError, IndexError, KeyError):
            pass

    def __str__(self):
        return repr(self.msg)

################################################################################
# End of code adapted from PubChemPy
################################################################################
