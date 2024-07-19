from requests import get
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.request import urlretrieve
from contextlib import closing

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
            
    url = str.format('https://webbook.nist.gov/cgi/cbook.cgi?React={0}&React2=&Prod=&Prod2=&Rev=on&AllowOtherReact=on&AllowOtherProd=on&Type=Any&Units=SI', Name)
    #(He+ • helium) + helium = (He+ • 2helium)

    #gets the html
    actualHtml = get_response(url)

    #beautifulsoup to parse
    html = BeautifulSoup(actualHtml, 'html.parser')

    #we locate the segment where links are located
    link_iter = html.find(id="main")
    element_lists = link_iter.find('ol')
    all_mixtures = element_lists.find_all("li", {"class": "mixture"})
    one_mixture = element_lists.find("li", {"class": "mixture"})
    for mixture in all_mixtures:
        a_tags = mixture.find_all('a')
        for a_tag in a_tags:
            span = a_tag.get_attribute_list
            if span:
                print(span, "\n")


    
    #we now loop for the number of links that exist till each link has been appended to the table we are making
    #The table we are now making is now hence checked thoroughly if they contain an organic SMILES image, if not then it is not an organic reaction and we remove it from the table
    
    #return(len(all_mixtures))
    
print(get_html_tables("Hcl"))