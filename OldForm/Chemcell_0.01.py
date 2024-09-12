from typing import Any
from requests import get
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.request import urlretrieve
from contextlib import closing
import pandas as pd
import pubchempy as pcp
import os
import tempfile
import csv


elements = ["H", "C", "O", "F", "Cl", "Br", "I"]
count = 0

class Chemcell:
    #the plan
    #to make it iterate the sites including the element
    #then when the webpage is shown where it outputs the links of different reactions
    #we will then list them in a table in numpy df format and then we iterate those links
    #those links we get the different names and stats of them
    #external table 
    #we will also be using this site https://www.chemeo.com/cid/69-954-7/Difluorohydroxyborane

    def_Pc_P = ['MolecularWeight', 
                'RotatableBondCount', 
                'DefinedBondStereoCount', 
                'Complexity', 
                'HBondDonorCount', 
                'HBondAcceptorCount', 
                'Complexity',
                'CovalentUnitCount',
                'Charge',
                'HeavyAtomCount',
                'IsotopeAtomCount'
                ]
    
    def_C_P = ['Electron affinity', 
                'Ionization energy', 
                'Critical Pressure', 
                'Dipole Moment',
                'Critical Temperature',
                'Octanol/Water partition coefficient'
                ]
    
    def __init__(self, name, outliers = False, file_location=None):
        #Defaults
        self.name = name
        self.outliers = outliers
        self.file_location = file_location
        self.r_Min = None
        self.r_Max = None
        self.Pc_P = self.def_Pc_P
        self.C_P = self.def_C_P
        self.R_count = 2
        self.P_Count = 2

    
    #Options
    def range(self, r_Min=None, r_Max=None):
        self.r_Min = r_Min
        self.r_Max = r_Max
        return self
    #Pubchem_properties
    def Pc_Prop(self, Pc_P = None):
        if Pc_P == None:
            Pc_P = self.def_Pc_P
        self.Pc_P = Pc_P
        return self
    #Chemeo_properties
    def C_Prop(self, C_P = None):
        if C_P == None:
            C_P = self.def_C_P
        self.C_P = C_P
        return self
    
    def RP_Count(self, R_count = None, P_Count = None):
        self.R_count = R_count
        self.P_Count = P_Count

    
    
    def tabulate(self):
        if self.file_location == None:
            file_location_t = os.path.join(tempfile.gettempdir(), 'temprawdata.txt')
        else:
            file_location_t = os.path.join(self.file_location, f"Ouput_Data_{self.name}.csv")

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
        
        def headerformat(React_c, Prod_c):
            header_c = ['Reactant_Count', 'Product_Count']
            Chemeo_Prop = self.C_P
            Pubchem_Prop = self.Pc_P
            Props = Chemeo_Prop + Pubchem_Prop
            for i in range(React_c):
                header_c.append(f"Reactant_Name_{i+1}")
                header_c.append(f"Reactant_ID_{i+1}")
                header_c += Props
            
            for i in range(Prod_c):
                header_c.append(f"Product_Name_{i+1}")
                header_c.append(f"Product_ID_{i+1}")
                header_c += Props
            
            return(header_c)



        #\\\First Site\\\
        url = str.format('https://webbook.nist.gov/cgi/cbook.cgi?React={0}&React2=&Prod=&Prod2=&Rev=on&AllowOtherReact=on&AllowOtherProd=on&Type=Any&Units=SI', self.name)

        #gets the html
        actualHtml = get_response(url)

        #beautifulsoup to parse
        html = BeautifulSoup(actualHtml, 'html.parser')
        #\\\First Site\\\

        #\\\Second Site\\\
        url_2 = str.format('')

        #we locate the segment where links are located
        link_iter = html.find(id="main")
        element_lists = link_iter.find('ol')
        all_mixtures = element_lists.find_all("li", {"class": "mixture"})
        one_mixture = element_lists.find("li", {"class": "mixture"})

        print("Welcome to Jordans Organicle-- Beginning process...")
        #Data which is modified and can be as well
        max = len(all_mixtures)
        min = 0
        if self.r_Max is not None:
            max = self.r_Max
        if self.r_Min is not None:
            min = self.r_Min

        #This is just a temporary tabular data maker
        rows = []
        
        #Misc Variables
        Products_p = []
        Reactants_p = []
        R_c = self.R_count
        P_c = self.P_Count
        print(max)
        #Find the reaction lists
        for i in range(min, max):
            data = []
            print("\n","///new sources///")
            link_for_reaction = all_mixtures[i].a['href']
            print(link_for_reaction)
            #we will reset the reactants results and products and set the next timer to false
            reacts = []
            products = []
            products_next = False
            #If the reactants + products are the same then we skip them until it is different
            repeated = False
            for j in all_mixtures[i].a:
                if j.has_attr('title'):
                    if products_next == False:
                            #print(j)
                            if j.text.strip():
                                #We grab reactants and products dataset
                                reacts.append(j.text.strip().replace(' ', '-'))
                                #print("has text so we get text ", j.text)
                            else:
                                reacts.append(j['title'].strip().replace(' ', '-'))
                    else:
                            if j.text.strip():
                                products.append(j.text.strip().replace(' ', '-'))
                                #print("has text so we get text ", j.text)
                            else:
                                products.append(j['title'].strip().replace(' ', '-'))
                elif j.has_attr('class'):
                    #reacts.append(j.text)
                    if(j.text == ' = '):
                        products_next = True
                    #print(j.text)
                else:
                    print(j, "bug")
                    
                
                # if j.find("span")["title"]:
                #     print(j.find(("span"))["title"])
                # else:
                #     print(j.contents)       
            #If the reaction + products not same then we continue
            if(Reactants_p == reacts and Products_p == products):
                repeated = True

            #If there is no repetiation and the reactants and products are equal to the required then pass and read on
            if(reacts != products):
                if(repeated == False and R_c == len(reacts) and P_c == len(products)):
                    Products_p = products
                    Reactants_p = reacts
                    print("reactants ", reacts)
                    data.append(len(reacts))
                    data.append(len(products))
                    print("products ", products)
                    print("///Data///")
                    products_next = False
                    #We now get the data for the products 
                    data_url  = str.format("https://webbook.nist.gov{0}", link_for_reaction)
                    data_url = get_response(data_url)
                    data_url = BeautifulSoup(data_url, 'html.parser')
                    #print(html)
                    #parse the source site
                    source_iter = data_url.find(id="main").ul.li
                    #Finds the compounds in the reactions
                    for k in source_iter:
                        #if k.has_attr('class'):
                            #This is to make sure the data only captures reactants
                            #if(k.text == ' = '):
                                #products_next = True

                        #if products_next == True:
                        if k.has_attr('title'):
                            data_link = k.a['href']
                            print("sources for ", k['title'], " ", data_link)
                            #We now append the title data
                            data.append(k['title'])
                            #we now search the site listed in the source
                            source_url = str.format("https://webbook.nist.gov{0}", data_link)
                            source_url = get_response(source_url)
                            source_url = BeautifulSoup(source_url, 'html.parser')
                            Sourceurl_CAS = source_url.find(id="main")
                            Sourceurl_CAS = Sourceurl_CAS.ul.find_all("li")
                            #Sourceurl_CAS = Sourceurl_CAS.find_all('li')

                            for l in Sourceurl_CAS:
                                #print(Sourceurl_CAS.find_all("CAS Registry Number:"))
                                #print(l['strong'] or "no strong")
                                if l.find('strong'):
                                    if(l.strong.text == "CAS Registry Number:"):
                                        CAS = l.text.replace("CAS Registry Number:", '').strip()
                                        print(l.text)
                                        data.append(CAS)
                                        #We check if the chemeo exists
                                        Getdatasource = str.format("https://www.chemeo.com/search?q={0}", CAS)
                                        Getdatasource = get_response(Getdatasource)
                                        Getdatasource = BeautifulSoup(Getdatasource, 'html.parser')
                                        #In the off chance that there doesnt exist class container/table we will return an N/A
                                        try:
                                            print("//Chemeo-Dataset//")
                                            Getdatasource_parse = Getdatasource.find('div', {"class": "container"}).find('div', id="details-content")
                                            Getdatasource_parse = Getdatasource_parse.find('table', {"class": "props details"})
                                            Getdatasource_parse = Getdatasource_parse.find_all('tr')
                                            #print(Getdatasource_parse)
                                            #What i realised is that there is no tbody but there is thead which I can reference which I found silly
                                            #Process of getting average without considering the outlier we grab the ('span')['title' ] before every iteration and check if they are equal to the previous
                                            #If so we do a count, if not but count is more than 0 then we do the equation.
                                            count = 0
                                            prev_title = ""
                                            properties = self.C_P
                                            not_found_property_check = True
                                            largest = 0
                                            smallest = 0
                                            not_found_prop = ""
                                            sum = 0
                                            #Available_Properties
                                            for i in properties:
                                                not_found_property_check = True
                                                for results in Getdatasource_parse:
                                                    if results.find('td'):
                                                        result_index = results.find('td')
                                                        if result_index.find('span').has_attr('title'):
                                                            #print("found one with a title")
                                                            title = result_index.find('span')['title']
                                                            if(title == i):
                                                                result = results.find('td', {'class': "r"}).text
                                                                if(prev_title != title):
                                                                    if(count == 0):
                                                                        if("[" in result):
                                                                            result = result.replace("[", "").replace("]", "")
                                                                            result_split = result.split(";")
                                                                            result = (float(result_split[0]) + float(result_split[1]))/2  
                                                                        print("count is 0")
                                                                        print(title, "/", result_index.find('span').text, ":", result)
                                                                        data.append(result)
                                                                        not_found_property_check = False
                                                                    else:
                                                                        print("count is not 0")
                                                                        #since count is not 0, it means that a new element is found and no more alternatives are found hence we make the average here now.
                                                                        if(sum > 0):
                                                                            data[-1] = sum/count
                                                                            sum = 0
                                                                        if("[" in result):
                                                                            result = result.replace("[", "").replace("]", "")
                                                                            result_split = result.split(";")
                                                                            result = (float(result_split[0]) + float(result_split[1]))/2
                                                                        
                                                                        print(title, "/", result_index.find('span').text, ":", result)
                                                                        data.append(result)
                                                                        not_found_property_check = False
                                                                        count == 0
                                                                else:
                                                                    #Both titles are equal meaning we are seeing alternatives
                                                                    #print(prev_title, " is equal to ", title)

                                                                        #To add: if it sees alternmatives then add the sum, if the outlier class is declared false and an outlier exists then we discount the outlier.
                                                                    #Count to account for average values recorded
                                                                    if "±" in result:
                                                                        #print("found")
                                                                        if "Outlier " in result:
                                                                            results = result.replace("Outlier ", "")
                                                                            if(self.outliers == True):
                                                                                result_split = result.split("±")
                                                                                sum += float(result_split[0]) + float(result_split[-1])
                                                                                sum += float(result_split[0]) - float(result_split[-1])


                                                                        else:
                                                                            result_split = result.split("±")
                                                                            sum += float(result_split[0]) + float(result_split[-1])
                                                                            sum += float(result_split[0]) - float(result_split[-1])
                                                                    else:
                                                                        if "Outlier " in result:
                                                                            print("outlier found")
                                                                            results = result.replace("Outlier ", "")
                                                                            if(self.outliers == True):
                                                                                sum += float(results)

                                                                        else:
                                                                            sum += float(result)
                                                                    count += 1
                                                                prev_title = title
                                                if(not_found_property_check == True):                                                       
                                                    print(i, ": ", "N/A")
                                                    data.append("N/A")
                                                
                                            #Getdatasource_parse =  Getdatasource.find('div' ,{"class": "props details"})
                                            #Getdatasource_parse =  Getdatasource_parse.find_all('tr')
                                        except AttributeError:
                                            print("N/A - Elements not found: ", AttributeError)
                                        
                                        #We will also check the data from the pubchem archives to find molecular structure 
                                        try:
                                            print("//PubChem-Dataset//")
                                            #compound = pcp.get_compounds(CAS, 'name')[0]
                                            properties = self.Pc_P
                                            compound_p = pcp.get_properties(properties, CAS, 'name')
                                            print(compound_p)
                                            for i in properties:
                                                try:
                                                    value = compound_p[0].get(i)
                                                    if value is not None:
                                                        print(f"{i}:", compound_p[0].get(i))
                                                        data.append(compound_p[0].get(i))
                                                    else:
                                                        print(f"{i} not found.")
                                                except KeyError:
                                                    print(f"{i}: ", KeyError)
                                        except (KeyError, ValueError, IndexError):
                                            print("Doesnt exist")


                                        print("\n")
                            print(data)
                            rows.append(data)
                else:
                    print("Skipped because identitcal reaction. or not right amount of Prod,Reacts or same products + reacts")
        print(rows)
        headers = headerformat(R_c, P_c)
        print(headers)
        #df = pd.DataFrame(rows, columns=headers)
        print("\n Saving file")
        with open(file_location_t, 'w', newline = '') as file:
            write_csv = csv.writer(file)
            write_csv.writerow(headers)
            write_csv.writerows(rows)
        return(rows)



                                
                    #print(Sourceurl_CAS.text)
                    #print("CAS ", Sourceurl_CAS)
                
            #print(k)
        #print(source_iter)



    
    #we now loop for the number of links that exist till each link has been appended to the table we are making
    #The table we are now making is now hence checked thoroughly if they contain an organic SMILES image, if not then it is not an organic reaction and we remove it from the table
    
    #return(len(all_mixtures))
test = Chemcell("HCl", False, "/workspaces/Organicle/Example_Data").range(0, 6).tabulate()
