import requests
import pubchempy as pcp
from bs4 import BeautifulSoup
from .utlity import save_csv, get_response

class Chemcelltabulate:

    #The purpose of this method? The purpose was mainly to make a 2d array to be made into a csv
    def process_data(self, name, r_Min, r_Max, Pc_P, C_P, R_count, P_Count, outliers):
        #\\\First Site\\\
        url = str.format('https://webbook.nist.gov/cgi/cbook.cgi?React={0}&React2=&Prod=&Prod2=&Rev=on&AllowOtherReact=on&AllowOtherProd=on&Type=Any&Units=SI', name)

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

        #Data which is modified and can be as well
        max = len(all_mixtures)
        min = 0
        if r_Max is not None:
            max = r_Max
        if r_Min is not None:
            min = r_Min

        #This is just a temporary tabular data maker
        rows = []
        #print(r_Max)
        #print(r_Min)
        #print("\n")
        #print("Chemcell attr")
        
        #Misc Variables
        Products_p = []
        Reactants_p = []
        R_c = R_count
        P_c = P_Count
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
                                                                        #print("count is 0")
                                                                        print(title, "/", result_index.find('span').text, ":", result)
                                                                        data.append(result)
                                                                        not_found_property_check = False
                                                                    else:
                                                                        #print("count is not 0")
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
                                                                            print("outlier found")
                                                                            results = result.replace("Outlier ", "")
                                                                            if(outliers == True):
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
                                            properties = Pc_P
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
        return(rows,R_c, P_c)