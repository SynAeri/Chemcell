import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
from bs4 import BeautifulSoup, NavigableString, Tag
from .utlity import save_csv, get_response, _print_compound_data
from .data_sources import PubChemDataSource, ChemeoDataSource
from .config import *

#Initialising Log
log = logging.getLogger('chemcell')
class Chemcelltabulate:
    def __init__(self, max_workers: int = 5):
        self.pubchem_source = PubChemDataSource()
        self.chemeo_source = ChemeoDataSource()
        self.max_workers = max_workers

    #The purpose of this method? The purpose was mainly to make a 2d array to be made into a csv
    def process_data(self, name, r_Min, r_Max, Pc_P, C_P, R_count: int, P_count, outliers: bool):
        name_p = name + [None] * (R_count + P_count - len(name))
        url = self._construct_nist_url(name_p)
        html = self._get_parsed_url(url)

        all_mixtures = self._get_all_mixtures(html)
        if not all_mixtures:
            return [], R_count, P_count
        
        rows = self._process_mixtures(all_mixtures, r_Min, r_Max, Pc_P, C_P, R_count, P_count, outliers)
        return rows, R_count, P_count

    def _construct_nist_url(self, name_p):
        return(str.format(
            'https://webbook.nist.gov/cgi/cbook.cgi?React={0}&React2={1}&Prod={2}&Prod2={3}&Rev=on&AllowOtherReact=on&AllowOtherProd=on&Type=Any&Units=SI',
            # Use '' if None
            name_p[0], 
            name_p[1] if name_p[1] else '', 
            name_p[2] if name_p[2] else '', 
            name_p[3] if name_p[3] else ''   
        ))
    
    def _get_parsed_url(self, name_p):
        #gets the html
        actualHtml = get_response(name_p)
        #beautifulsoup to parse
        return(BeautifulSoup(actualHtml, 'html.parser'))
    
    def _get_all_mixtures(self, html):
        #we locate the segment where links are located
        link_iter = html.find(id="main")
        element_lists = link_iter.find('ol')
        if element_lists:
            return element_lists.find_all("li", {"class": "mixture"})
        log.debug("Yielded nil result next method")
        
        element_lists_2 = link_iter.ul.li.find(string=lambda text: "Reaction by formula:" in text if text else False)
        if element_lists_2:
            element_lists_2 = element_lists_2.find_parent('li')
            return [element_lists_2]

        if element_lists is None:
            raise ValueError("Nothing found for this combination. Please choose another combination.")
        return element_lists.find_all("li", {"class": "mixture"})

    def _process_mixtures(self, all_mixtures, r_Min, r_Max, Pc_P, C_P, R_count, P_count, outliers):
        rows = []
        total_mix = len(all_mixtures)
        log.info(f"r_min: {r_Min}, r_max: {r_Max}, total_mixture: {total_mix}")

        if r_Max is None or r_Max > total_mix:
            log.warning(f"r_Max was either none or larger than total, assumed and defaulted to max value")
            r_Max = total_mix
        if r_Min is None or r_Min == r_Max:
            r_Min = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_mixture = {
                executor.submit(
                    self._process_single_mixture, 
                    mixture, 
                    Pc_P, 
                    C_P, 
                    R_count, 
                    P_count, 
                    outliers
                ): mixture
                for mixture in all_mixtures[r_Min:r_Max]
            }
            total_mix = len(future_to_mixture)
            processed_mix = 0
            for future in as_completed(future_to_mixture):
                mixture = future_to_mixture[future]
                try:
                    result = future.result()
                    if result:
                        rows.append(result)
                        log.info(f"Successfully processed mixture: {processed_mix + 1}/{total_mix}")
                    else:
                        log.warning(f"Mixture {processed_mix + 1}/{total_mix} did not yield results")
                except Exception as exc:
                    log.error(f'Error processing mixture {processed_mix + 1}/{total_mix}:')
                    log.error(f'Exception: {exc}')
                finally:
                    processed_mix += 1
                    self._print_progress(processed_mix, total_mix)

        log.info(f"\nProcessed {len(rows)} mixtures successfully out of {total_mix} attempted.")
        return rows
    
    def _process_single_mixture(self, mixture, Pc_p, C_P, R_count, P_count, outliers):
        data = []
        link_for_react = mixture.a['href']
        reacts, products, method2 = self._get_reactants_and_products(mixture)
        property_Aggregate = Pc_p + C_P
        if len(reacts) <= R_count and len(products) <= P_count:
            data.extend([len(reacts), len(products)])

            #Pad if fewer than expected
            reacts = reacts + ["N/A"] * (R_count - len(reacts))
            products = products + ["N/A"] * (P_count - len(products))

            data.extend(self._process_compounds(reacts + products, Pc_p, C_P, outliers, method2))
            _print_compound_data(reacts, products, data, property_Aggregate)
        else:
            log.warning(f"BEGINNING PROCESS SINGLE MIXTURE: FAILED\nData shown is not fullilling criteria {reacts + products} Could be due to passing the R_count, P_count")
            pass
        
        return data if data else None
    
    def _get_reactants_and_products(self, mixture):

        reacts, products = [], []
        products_next = False
        #fallback link if first method does not work
        link = mixture.a['href']
        #If the reactants + products are the same then we skip them until it is different
        for j in mixture.a:
            if(isinstance(j, NavigableString)):
                for i in mixture:
                    if(str(i.text) == " = "):
                        products_next = True
                    if(i.a):
                        compound = i.a.parent['title']
                        (products if products_next else reacts).append(compound)

                break
            if j.has_attr('title'):
                compound = j.text.strip().replace(' ', '-') if j.text.strip() else j['title'].strip().replace(' ', '-')
                (products if products_next else reacts).append(compound)
            elif j.has_attr('class') and j.text == ' = ':
                products_next = True
        return reacts, products, link
                
    def _process_compounds(self, compounds, Pc_P, C_P, outliers, method2):
        data = []
        #they passed the number or react + products specified, it gets iterated and table extended according to 
        for compound in compounds:
            if(compound == "N/A"):
                data.extend(["N/A"] * (2 + len(Pc_P) + len(C_P)))
            else:
                cas = self._get_cas_num(compound, method2)
                if cas:
                    data.append(compound)
                    data.append(cas)
                    data.extend(self._get_compound_data(cas, C_P, Pc_P, outliers))

        return data
    
    def _get_cas_num(self, compound, method2):

        def method1(compound, alternative = None):
            if alternative == None:
                url = str.format("https://webbook.nist.gov/cgi/cbook.cgi?Name={0}&Units=SI", compound)
            else:
                url = str.format(f"{NIST_}{alternative}")
            html = self._get_parsed_url(url)
            cas_element = html.find(id="main")
            cas_element = cas_element.ul.find(string=lambda text: "CAS Registry Number:" in text if text else False)
            if cas_element:
                #Parent parent <strong> -> <li>           
                cas_number = cas_element.parent.parent
                cas_number = cas_number.text.replace('CAS Registry Number:', '').strip()
                return cas_number
            
            return None
        
        def method2_(method2, compound):
            url = str.format(f"{NIST_}{method2}")
            html = self._get_parsed_url(url)
            html = html.find(id="main")
            # Look for the span with the title containing the compound formula
            find_list = html.ul.li.find(string=lambda text: "Reaction by formula:" in text if text else False)
            if find_list:
                find_list = find_list.find_parent('li')
                for i in find_list:
                    #every i.a has atleast a link so it means it must be a compound.
                    if(i.a is not None):
                        if i.a.text == compound:
                            return(i.a['href'])
            return None
        
        try:
            cas_number= method1(compound)
            if cas_number:
                return cas_number
            log.warning(f"Method 1 has failed going for Method 2")
            
            reaction_site = method2_(method2, compound)
            if reaction_site:
                method_2_ = method1(None, reaction_site)
                if method_2_:
                    log.info(f"Method 2 fully passed for {compound}: {method_2_}")
                    return(method_2_)
            
            log.error(f"Both methods failed to find CAS for {compound}")
            return None
        except Exception as e:
            log.exception(f"Error occurred while fetching CAS number for {compound}: {str(e)}")
            return None
    
    def _get_compound_data(self, cas, C_P, Pc_P, outliers):
        pubchem_data = self.pubchem_source.fetch_data(cas,Pc_P)
        chemeo_data = self.chemeo_source.fetch_data(cas, C_P, outliers = outliers)

        compound_data = chemeo_data + pubchem_data
        #processed_data = self.data_processor.process_compound_data(compound_data, {**C_P, **Pc_P})
        return pubchem_data + chemeo_data
    
    def _print_progress(self, processed, total):
        progress = processed / total * 100
        log.info(f"Processing mixture: {processed}/{total} ({progress: .2f}%)")
        #sys.stdout.flush()
