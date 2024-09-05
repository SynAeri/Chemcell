from requests import get
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.request import urlretrieve
from contextlib import closing
import pubchempy as pcp
#import lxml
#from requests_html import AsyncHTMLSession

# elements = [
#     "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
#     "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
#     "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
#     "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
#     "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
#     "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
#     "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
#     "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
#     "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
#     "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
#     "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
#     "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
# ]
elements = ["H", "C", "O", "F", "Cl", "Br", "I"]
count = 0

def get_html_tables(Name):
    #the plan
    #to make it iterate the sites including the element
    #then when the webpage is shown where it outputs the links of different reactions
    #we will then list them in a table in numpy df format and then we iterate those links
    #those links we get the different names and stats of them
    #external table 
    #we will also be using this site https://www.chemeo.com/cid/69-954-7/Difluorohydroxyborane
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
    

    #\\\First Site\\\
    url = str.format('https://webbook.nist.gov/cgi/cbook.cgi?React={0}&React2=&Prod=&Prod2=&Rev=on&AllowOtherReact=on&AllowOtherProd=on&Type=Any&Units=SI', Name)

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

    #This is just a temporary tabular data maker
    rows = []


    for mixture in all_mixtures:
        data = []
        print("\n","///new sources///")
        link_for_reaction = mixture.a['href']
        print(link_for_reaction)
        #we will reset the reactants results and products and set the next timer to false
        reacts = []
        products = []
        products_next = False
        for j in mixture.a:
            if j.has_attr('title'):
                if products_next == False:
                        #print(j)
                        if j.text.strip():
                            #We grab reactants and products dataset
                            reacts.append(j.text.strip().replace(' ', '-'))
                            data.append(reacts)
                            #print("has text so we get text ", j.text)
                        else:
                            reacts.append(j['title'].strip().replace(' ', '-'))
                            data.append(products)
                else:
                        if j.text.strip():
                            products.append(j.text.strip().replace(' ', '-'))
                            data.append(products)
                            #print("has text so we get text ", j.text)
                        else:
                            products.append(j['title'].strip().replace(' ', '-'))
                            data.append(reacts)
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
        print("reactants ", reacts)
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
        for k in source_iter:
            if k.has_attr('class'):
                if(k.text == ' = '):
                    products_next = True

            if products_next == True:
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
                                    
                                    for results in Getdatasource_parse:
                                        if results.find('td'):
                                            result_index = results.find('td')
                                            if result_index.find('span').has_attr('title'):
                                                #print("found one with a title")
                                                result = results.find('td', {'class': "r"}).text
                                                data.append(result)
                                                print(result_index.find('span')['title'], "/", result_index.find('span').text, ":", result)
                                        
                                    #Getdatasource_parse =  Getdatasource.find('div' ,{"class": "props details"})
                                    #Getdatasource_parse =  Getdatasource_parse.find_all('tr')
                                except AttributeError:
                                    print("N/A - Elements not found: ", AttributeError)
                                
                                #We will also check the data from the pubchem archives to find molecular structure 
                                try:
                                    print("//PubChem-Dataset//")
                                    #compound = pcp.get_compounds(CAS, 'name')[0]
                                    properties = ['MolecularWeight', 'RotatableBondCount', 'DefinedBondStereoCount', 'Complexity', 'HBondDonorCount', 'HBondAcceptorCount', 'Complexity']
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
    return(data)



                                
                    #print(Sourceurl_CAS.text)
                    #print("CAS ", Sourceurl_CAS)
                
            #print(k)
        #print(source_iter)



    
    #we now loop for the number of links that exist till each link has been appended to the table we are making
    #The table we are now making is now hence checked thoroughly if they contain an organic SMILES image, if not then it is not an organic reaction and we remove it from the table
    
    #return(len(all_mixtures))
    
print(get_html_tables("C"))